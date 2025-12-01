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
from django.shortcuts import get_object_or_404
from .services.cobalt_payment import CobaltPaymentGateway, CobaltPaymentError

logger = logging.getLogger(__name__)

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
            
            # Process payment through Cobalt
            try:
                gateway = CobaltPaymentGateway()
                payment_result = gateway.process_sale(
                    amount=amount_in_cents,
                    pan=card_number,
                    exp_date=card_exp,
                    cvv2=card_cvv,
                    card_holder=card_holder
                )
                
                logger.info(f"Cobalt payment result: {payment_result.get('status')} for amount ${total_amount}")
                
                if not payment_result.get('success'):
                    # Payment was denied or failed
                    status = payment_result.get('status', 'error')
                    
                    if status == 'denied':
                        message = 'El pago fue rechazado por el banco. Por favor verifica los datos de tu tarjeta o intenta con otra.'
                    elif status == 'refused':
                        message = 'La transacción fue rechazada. Por favor contacta a tu banco.'
                    else:
                        message = payment_result.get('message', 'Error procesando el pago. Por favor intenta de nuevo.')
                    
                    return JsonResponse({
                        'success': False,
                        'message': message
                    }, status=400)
                
                # Payment successful - create order
                order = Order.objects.create(
                    event=event,
                    customer_name=customer_name,
                    customer_email=customer_email,
                    customer_phone=customer_phone,
                    total_amount=total_amount,
                    status='completed',
                    payment_method='cobalt',
                    payment_reference=f"TX:{payment_result.get('id')} AUTH:{payment_result.get('authorization_number')}"
                )
                
                # Create order items and update ticket quantities
                for item in ticket_items:
                    OrderItem.objects.create(
                        order=order,
                        ticket_type=item['ticket_type'],
                        quantity=item['quantity'],
                        unit_price=item['unit_price'],
                        subtotal=item['subtotal']
                    )
                    # Update sold count
                    item['ticket_type'].quantity_sold += item['quantity']
                    item['ticket_type'].save()
                
                logger.info(f"Order {order.order_number} created successfully with Cobalt TX:{payment_result.get('id')}")
                
                return JsonResponse({
                    'success': True,
                    'message': '¡Compra completada! Te hemos enviado un correo con los detalles.',
                    'order_number': order.order_number
                })
                
            except CobaltPaymentError as e:
                logger.error(f"Cobalt payment error: {e.message}")
                return JsonResponse({
                    'success': False,
                    'message': e.message
                }, status=500)
            
        except Exception as e:
            logger.exception(f"Checkout error: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error al procesar la compra: {str(e)}'
            }, status=500)
