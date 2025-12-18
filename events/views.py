from django.views.generic import TemplateView, DetailView, ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import logging
from .models import Event, Category, NewsletterSubscriber, TicketType, Order, OrderItem
from django.utils import timezone
from django.db import models
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .services.cobalt_payment import CobaltPaymentGateway, CobaltPaymentError

logger = logging.getLogger(__name__)

def _get_client_ip(request):
    """
    Best-effort client IP extraction (supports reverse proxies).
    """
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        # XFF can be a comma-separated list. First is original client.
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

def _parse_bool(value, default=None):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    v = str(value).strip().lower()
    if v in ("1", "true", "yes", "y", "on"):
        return True
    if v in ("0", "false", "no", "n", "off"):
        return False
    return default

class EventListView(TemplateView):
    template_name = "events/event_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get hero events (events marked for hero section)
        context['hero_events'] = Event.objects.filter(
            status='published',
            show_in_hero=True,
            end_date__gte=timezone.now().date()
        ).order_by('start_date')[:3]  # Show up to 3 hero events
        
        # Get featured events
        context['featured_events'] = Event.objects.filter(
            status='published',
            is_featured=True,
            end_date__gte=timezone.now().date()
        ).order_by('start_date')[:4]
        
        # Get all categories
        context['categories'] = Category.objects.filter(is_active=True).order_by('order', 'name')
        
        # Get popular cities
        cities = (
            Event.objects.filter(status='published', start_date__gte=timezone.now().date())
            .values('city', 'state_province', 'country')
            .annotate(event_count=models.Count('id'))
            .order_by('-event_count')
        )[:6]  # Top 6 cities
        context['popular_cities'] = cities
        
        # Get most popular events (for now, just get recent events)
        context['popular_events'] = Event.objects.filter(
            status='published',
            end_date__gte=timezone.now().date()
        ).order_by('-created_at')[:4]
        
        # Get stats
        context['stats'] = {
            'total_events': Event.objects.filter(status='published').count(),
            'total_cities': Event.objects.filter(status='published').values('city').distinct().count(),
            'total_players': '100k+',  # Mock data for now
            'average_rating': 4.8,  # Mock data for now
        }
        
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    
    def get_queryset(self):
        # Only show published events
        return Event.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get related events (same category, excluding current event)
        event = self.get_object()
        context['related_events'] = Event.objects.filter(
            status='published',
            category=event.category,
            end_date__gte=timezone.now().date()
        ).exclude(id=event.id).order_by('start_date')[:3]
        
        # Get available ticket types for this event
        context['ticket_types'] = event.ticket_types.filter(is_active=True).order_by('order', 'price')
        
        # Get event stats for display
        context['event_stats'] = {
            'days_until_event': (event.start_date - timezone.now().date()).days,
            'is_upcoming': event.is_upcoming,
            'is_ongoing': event.is_ongoing,
        }
        
        return context

class CategoryEventsView(ListView):
    template_name = "events/category_events.html"
    context_object_name = "events"
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Event.objects.filter(
            status='published',
            category=self.category,
            end_date__gte=timezone.now().date()
        ).order_by('start_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.filter(is_active=True).order_by('order', 'name')
        return context

class FeaturedEventsView(ListView):
    template_name = "events/featured_events.html"
    context_object_name = "events"
    paginate_by = 12
    
    def get_queryset(self):
        return Event.objects.filter(
            status='published',
            is_featured=True,
            end_date__gte=timezone.now().date()
        ).order_by('start_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).order_by('order', 'name')
        return context

class PopularEventsView(ListView):
    template_name = "events/popular_events.html"
    context_object_name = "events"
    paginate_by = 12
    
    def get_queryset(self):
        return Event.objects.filter(
            status='published',
            end_date__gte=timezone.now().date()
        ).order_by('-created_at')  # Using created_at as a proxy for popularity for now
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).order_by('order', 'name')
        return context

@method_decorator(csrf_exempt, name='dispatch')
class NewsletterSubscriptionView(View):
    """Handle newsletter subscription from frontend forms"""
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            
            if not email:
                return JsonResponse({
                    'success': False,
                    'message': 'Email is required.'
                }, status=400)
            
            # Check if already subscribed
            if NewsletterSubscriber.objects.filter(email=email).exists():
                subscriber = NewsletterSubscriber.objects.get(email=email)
                if subscriber.is_active:
                    return JsonResponse({
                        'success': False,
                        'message': 'This email is already subscribed to our newsletter.'
                    }, status=400)
                else:
                    # Reactivate
                    subscriber.resubscribe()
                    return JsonResponse({
                        'success': True,
                        'message': 'Welcome back! Your subscription has been reactivated.'
                    })
            
            # Create new subscriber
            subscriber = NewsletterSubscriber.objects.create(email=email)
            return JsonResponse({
                'success': True,
                'message': 'Successfully subscribed to our newsletter!'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Something went wrong. Please try again.'
            }, status=500)


class OrderSummaryView(TemplateView):
    """Display order summary after successful purchase"""
    template_name = "events/order_summary.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the order by order_number
        order_number = self.kwargs.get('order_number')
        order = get_object_or_404(Order, order_number=order_number)
        
        context['order'] = order
        context['event'] = order.event
        context['order_items'] = order.items.select_related('ticket_type').all()
        
        return context


class EventCheckoutView(TemplateView):
    """Handle ticket checkout for an event"""
    template_name = "events/checkout.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the event
        event = get_object_or_404(Event, slug=self.kwargs['slug'], status='published')
        context['event'] = event
        
        # Get available ticket types
        context['ticket_types'] = event.ticket_types.filter(is_active=True).order_by('order', 'price')
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle checkout form submission with Cobalt payment processing"""
        try:
            event = get_object_or_404(Event, slug=self.kwargs['slug'], status='published')
            
            # Get customer info
            customer_name = request.POST.get('customer_name', '').strip()
            customer_email = request.POST.get('customer_email', '').strip()
            customer_phone = request.POST.get('customer_phone', '').strip()
            
            if not customer_name or not customer_email:
                return JsonResponse({
                    'success': False,
                    'message': 'Nombre y correo electrónico son requeridos.'
                }, status=400)
            
            # Get payment info
            card_number = request.POST.get('card_number', '').replace(' ', '').strip()
            card_exp = request.POST.get('card_exp', '').strip()
            card_cvv = request.POST.get('card_cvv', '').strip()
            card_holder = request.POST.get('card_holder', '').strip()
            
            if not card_number or not card_exp or not card_cvv or not card_holder:
                return JsonResponse({
                    'success': False,
                    'message': 'Todos los datos de la tarjeta son requeridos.'
                }, status=400)
            
            # Validate card number length
            if len(card_number) < 13 or len(card_number) > 19:
                return JsonResponse({
                    'success': False,
                    'message': 'Número de tarjeta inválido.'
                }, status=400)
            
            # Get ticket selections
            ticket_items = []
            total_amount = 0
            
            for ticket_type in event.ticket_types.filter(is_active=True):
                quantity = int(request.POST.get(f'ticket_{ticket_type.id}', 0))
                if quantity > 0:
                    # Validate quantity
                    if quantity > ticket_type.quantity_remaining:
                        return JsonResponse({
                            'success': False,
                            'message': f'No hay suficientes entradas de tipo "{ticket_type.name}" disponibles.'
                        }, status=400)
                    if quantity > ticket_type.max_per_order:
                        return JsonResponse({
                            'success': False,
                            'message': f'Máximo {ticket_type.max_per_order} entradas de tipo "{ticket_type.name}" por orden.'
                        }, status=400)
                    
                    ticket_items.append({
                        'ticket_type': ticket_type,
                        'quantity': quantity,
                        'unit_price': ticket_type.price,
                        'subtotal': ticket_type.price * quantity
                    })
                    total_amount += ticket_type.price * quantity
            
            if not ticket_items:
                return JsonResponse({
                    'success': False,
                    'message': 'Por favor selecciona al menos una entrada.'
                }, status=400)
            
            # Convert total to cents for Cobalt API (amount is in dollars, API expects cents)
            amount_in_cents = int(total_amount * 100)

            # Prepare 3DS browser params (deviceChannel=browser)
            # Values come from JS + server IP (browserIP).
            three_ds_params = {
                "deviceChannel": "browser",
                "browserIP": _get_client_ip(request) or "",
                "browserJavaEnabled": _parse_bool(request.POST.get("browserJavaEnabled"), default=False),
                "browserJavascriptEnabled": _parse_bool(request.POST.get("browserJavascriptEnabled"), default=True),
                "browserLanguage": (request.POST.get("browserLanguage") or "").strip()[:8],
                "browserColorDepth": int(request.POST.get("browserColorDepth") or 0) or 24,
                "browserScreenHeight": int(request.POST.get("browserScreenHeight") or 0) or 1080,
                "browserScreenWidth": int(request.POST.get("browserScreenWidth") or 0) or 1920,
                "browserTZ": str(request.POST.get("browserTZ") or "0").strip(),
                "browserUserAgent": (request.POST.get("browserUserAgent") or request.META.get("HTTP_USER_AGENT") or "").strip()[:2048],
                "challengeWindowSize": int(request.POST.get("challengeWindowSize") or 0) or int(request.POST.get("browserScreenWidth") or 0) or 1920,
                "email": customer_email,
            }

            # Create a pending order first (needed for return_url and to correlate webhook).
            # Also reserve tickets immediately to avoid overselling while 3DS challenge happens.
            with transaction.atomic():
                order = Order.objects.create(
                    event=event,
                    customer_name=customer_name,
                    customer_email=customer_email,
                    customer_phone=customer_phone,
                    total_amount=total_amount,
                    status='pending',
                    payment_method='cobalt',
                )

                # Lock ticket rows and reserve quantities
                for item in ticket_items:
                    tt = TicketType.objects.select_for_update().get(id=item["ticket_type"].id)
                    if item["quantity"] > tt.quantity_remaining:
                        raise ValueError(f'No hay suficientes entradas de tipo "{tt.name}" disponibles.')
                    OrderItem.objects.create(
                        order=order,
                        ticket_type=tt,
                        quantity=item['quantity'],
                        unit_price=item['unit_price'],
                        subtotal=item['subtotal']
                    )
                    tt.quantity_sold += item['quantity']
                    tt.save(update_fields=["quantity_sold"])

            # Build webhook + return URLs (absolute)
            return_url = request.build_absolute_uri(reverse("order_summary", kwargs={"order_number": order.order_number}))
            webhook_url = request.build_absolute_uri(reverse("cobalt_webhook"))
            # Add shared secret token (required)
            from django.conf import settings
            webhook_token = getattr(settings, "COBALT_WEBHOOK_TOKEN", "")
            if not webhook_token:
                raise CobaltPaymentError(
                    message="Configuración incompleta: COBALT_WEBHOOK_TOKEN no está configurado",
                    error_code="missing_webhook_token",
                )
            webhook_url = f"{webhook_url}?token={webhook_token}"

            # Process payment through Cobalt (with 3DS)
            try:
                gateway = CobaltPaymentGateway()
                payment_result = gateway.process_sale(
                    amount=amount_in_cents,
                    pan=card_number,
                    exp_date=card_exp,
                    cvv2=card_cvv,
                    card_holder=card_holder,
                    metas={
                        "order_number": order.order_number,
                        "order_id": str(order.id),
                        "customer_email": customer_email,
                        "event_id": str(event.id),
                    },
                    three_ds_params=three_ds_params,
                    webhook=webhook_url,
                    return_url=return_url,
                )

                tx_id = payment_result.get("id")
                tx_status = payment_result.get("status")
                order.payment_reference = f"TX:{tx_id}" if tx_id else ""
                order.save(update_fields=["payment_reference"])

                logger.info(f"Cobalt payment status: {tx_status} for order {order.order_number}")

                # 3DS challenge required (authenticating)
                if payment_result.get("requires_3ds"):
                    challenge_url = payment_result.get("3ds_authentication_form")
                    if not challenge_url:
                        raise CobaltPaymentError(
                            message="Error 3DS: no se recibió URL de autenticación",
                            error_code="missing_3ds_authentication_form",
                            response_data=payment_result.get("raw_response"),
                        )
                    return JsonResponse({
                        "success": True,
                        "requires_3ds": True,
                        "challenge_url": challenge_url,
                        "order_number": order.order_number,
                        "return_url": return_url,
                    })

                # Immediate authorization (no challenge)
                if payment_result.get('success'):
                    order.status = "completed"
                    auth = payment_result.get("authorization_number")
                    if auth:
                        order.payment_reference = f"TX:{tx_id} AUTH:{auth}"
                    order.save(update_fields=["status", "payment_reference"])

                    logger.info(f"Order {order.order_number} completed with Cobalt TX:{tx_id}")

                    return JsonResponse({
                        'success': True,
                        'message': '¡Compra completada! Te hemos enviado un correo con los detalles.',
                        'order_number': order.order_number
                    })

                # Denied/refused/error (release reservation and cancel order)
                status = tx_status or "error"
                if status == 'denied':
                    message = 'El pago fue rechazado por el banco. Por favor verifica los datos de tu tarjeta o intenta con otra.'
                elif status == 'refused':
                    message = 'La transacción fue rechazada. Por favor contacta a tu banco.'
                else:
                    message = payment_result.get('message', 'Error procesando el pago. Por favor intenta de nuevo.')

                with transaction.atomic():
                    # release reserved tickets
                    for item in order.items.select_related("ticket_type").all():
                        tt = TicketType.objects.select_for_update().get(id=item.ticket_type_id)
                        tt.quantity_sold = max(0, tt.quantity_sold - item.quantity)
                        tt.save(update_fields=["quantity_sold"])
                    order.status = "cancelled"
                    order.save(update_fields=["status"])

                return JsonResponse({'success': False, 'message': message}, status=400)

            except CobaltPaymentError as e:
                logger.error(f"Cobalt payment error: {e.message}")
                # Cancel order and release reservation
                with transaction.atomic():
                    for item in order.items.select_related("ticket_type").all():
                        tt = TicketType.objects.select_for_update().get(id=item.ticket_type_id)
                        tt.quantity_sold = max(0, tt.quantity_sold - item.quantity)
                        tt.save(update_fields=["quantity_sold"])
                    order.status = "cancelled"
                    order.save(update_fields=["status"])

                return JsonResponse({'success': False, 'message': e.message}, status=500)
            
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
        except Exception as e:
            logger.exception(f"Checkout error: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error al procesar la compra: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class CobaltWebhookView(View):
    """
    Webhook receiver for Cobalt transaction updates (used by 3DS flow).
    We secure it using a shared token query param.
    """

    def post(self, request, *args, **kwargs):
        from django.conf import settings
        token = request.GET.get("token", "")
        expected = getattr(settings, "COBALT_WEBHOOK_TOKEN", "")
        if not expected or token != expected:
            return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)

        try:
            payload = json.loads(request.body or b"{}")
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

        data = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(data, dict):
            # Some integrations may POST the transaction object directly
            data = payload if isinstance(payload, dict) else {}

        tx_id = data.get("id")
        tx_status = data.get("status")
        auth = data.get("authorization_number")

        if not tx_id:
            return JsonResponse({"success": False, "message": "Missing transaction id"}, status=400)

        # Find the order correlated with this transaction
        order = Order.objects.filter(payment_reference__startswith=f"TX:{tx_id}").first()
        if not order:
            return JsonResponse({"success": False, "message": "Order not found"}, status=404)

        # Only act on terminal-ish statuses
        if tx_status == "authorized":
            order.status = "completed"
            if auth:
                order.payment_reference = f"TX:{tx_id} AUTH:{auth}"
            order.save(update_fields=["status", "payment_reference"])
            return JsonResponse({"success": True})

        if tx_status in ("denied", "refused", "error", "cancelled"):
            with transaction.atomic():
                for item in order.items.select_related("ticket_type").all():
                    tt = TicketType.objects.select_for_update().get(id=item.ticket_type_id)
                    tt.quantity_sold = max(0, tt.quantity_sold - item.quantity)
                    tt.save(update_fields=["quantity_sold"])
                order.status = "cancelled"
                order.save(update_fields=["status"])
            return JsonResponse({"success": True})

        # For authenticating or any intermediate state, acknowledge
        return JsonResponse({"success": True})


class OrderStatusView(View):
    """Lightweight status endpoint to support 3DS return_url polling."""

    def get(self, request, order_number, *args, **kwargs):
        order = get_object_or_404(Order, order_number=order_number)

        # Safety: auto-expire very old pending orders to release inventory
        if order.status == "pending":
            age_seconds = (timezone.now() - order.created_at).total_seconds()
            if age_seconds > 30 * 60:  # 30 minutes
                with transaction.atomic():
                    for item in order.items.select_related("ticket_type").all():
                        tt = TicketType.objects.select_for_update().get(id=item.ticket_type_id)
                        tt.quantity_sold = max(0, tt.quantity_sold - item.quantity)
                        tt.save(update_fields=["quantity_sold"])
                    order.status = "cancelled"
                    order.save(update_fields=["status"])

        return JsonResponse({
            "success": True,
            "order_number": order.order_number,
            "status": order.status,
            "payment_reference": order.payment_reference,
        })
