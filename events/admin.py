# /Users/aaay/dev/events/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import Category, Event, NewsletterSubscriber, TicketType, Order, OrderItem, CustomerVaultProfile, SavedPaymentMethod
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .forms import IconField
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display


# =============================================================================
# Dashboard Callback - Stats widgets for the admin home page
# =============================================================================

def dashboard_callback(request, context):
    """Add custom stats to the admin dashboard"""
    from datetime import timedelta
    
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # Event stats
    total_events = Event.objects.count()
    published_events = Event.objects.filter(status='published').count()
    upcoming_events = Event.objects.filter(status='published', start_date__gte=today).count()
    
    # Order stats
    total_orders = Order.objects.filter(status='completed').count()
    recent_orders = Order.objects.filter(status='completed', created_at__date__gte=thirty_days_ago).count()
    revenue_30d = Order.objects.filter(
        status='completed', 
        created_at__date__gte=thirty_days_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Subscriber stats
    total_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()
    new_subscribers = NewsletterSubscriber.objects.filter(
        is_active=True, 
        subscribed_at__date__gte=thirty_days_ago
    ).count()
    
    context.update({
        "stats": [
            {
                "title": _("Eventos Publicados"),
                "value": published_events,
                "subtitle": _("{} próximos").format(upcoming_events),
                "icon": "event",
            },
            {
                "title": _("Órdenes Completadas"),
                "value": total_orders,
                "subtitle": _("{} últimos 30 días").format(recent_orders),
                "icon": "receipt_long",
            },
            {
                "title": _("Ingresos (30 días)"),
                "value": f"${revenue_30d:,.2f}",
                "subtitle": _("{} órdenes").format(recent_orders),
                "icon": "payments",
            },
            {
                "title": _("Suscriptores"),
                "value": total_subscribers,
                "subtitle": _("{} nuevos (30 días)").format(new_subscribers),
                "icon": "mail",
            },
        ],
    })
    return context


# =============================================================================
# Inlines
# =============================================================================

class TicketTypeInline(TabularInline):
    model = TicketType
    extra = 1
    fields = ('name', 'price', 'quantity_available', 'quantity_sold', 'max_per_order', 'is_active', 'order')
    readonly_fields = ('quantity_sold',)
    tab = True


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('ticket_type', 'quantity', 'unit_price', 'subtotal')
    can_delete = False


class SavedPaymentMethodInline(TabularInline):
    model = SavedPaymentMethod
    extra = 0
    readonly_fields = ('card_brand', 'last_four', 'exp_month', 'exp_year', 'card_holder', 'created_at', 'last_used_at')
    can_delete = True
    fields = ('alias', 'card_brand', 'last_four', 'exp_month', 'exp_year', 'is_default', 'is_active', 'last_used_at')


# =============================================================================
# Category Admin
# =============================================================================

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'parent', 'display_icon', 'order', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    list_editable = ('order', 'is_active')
    list_per_page = 25
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')
    
    @display(description=_("Icono"))
    def display_icon(self, obj):
        """Display the icon in the list view"""
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 1.2rem;"></i>', obj.icon)
        return "-"
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Override form field for icon to use our custom IconField"""
        if db_field.name == 'icon':
            return IconField(required=False, help_text=db_field.help_text)
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    class Media:
        css = {
            'all': (
                'admin/css/admin_custom.css',
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css',
            )
        }


# =============================================================================
# Event Admin - With tabs for better organization
# =============================================================================

@admin.register(Event)
class EventAdmin(ModelAdmin):
    # Simplified list view - only essential columns
    list_display = ('title', 'display_status', 'category', 'event_date', 'display_featured')
    list_display_links = ('title',)
    inlines = [TicketTypeInline]
    list_filter = (
        'status',
        'is_featured',
        'category',
        'city',
    )
    list_editable = ('category',)
    search_fields = ('title', 'location_name', 'city', 'organizer_name')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    list_per_page = 20
    
    # Organize fields into tabs using Unfold
    fieldsets = (
        (_('Información Básica'), {
            'fields': (
                'title', 'slug', 'status', 
                ('is_featured', 'show_in_hero'),
                'short_description', 'description'
            ),
            'classes': ('tab',),
        }),
        (_('Fecha y Lugar'), {
            'fields': (
                ('start_date', 'start_time'),
                ('end_date', 'end_time'),
                'location_name',
                'address',
                'address_2',
                ('city', 'state_province'),
                'country',
                'venue_directions'
            ),
            'classes': ('tab',),
        }),
        (_('Multimedia'), {
            'fields': (
                'featured_image',
                'hero_image',
                'image_gallery',
                'video_url'
            ),
            'classes': ('tab',),
        }),
        (_('Entradas'), {
            'fields': (
                'registration_required',
                'registration_url',
                'max_capacity',
                'is_free',
                'price_display'
            ),
            'description': _('Configura los tipos de entrada en la sección inferior'),
            'classes': ('tab',),
        }),
        (_('Organizador'), {
            'fields': (
                'organizer_name',
                'organizer_description',
                'organizer_logo',
                'category',
                'tags'
            ),
            'classes': ('tab',),
        }),
        (_('Avanzado'), {
            'fields': (
                'faq',
                'additional_info',
                'created_at', 
                'updated_at'
            ),
            'classes': ('tab',),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

    @display(description=_('Estado'), label={
        'draft': 'warning',
        'published': 'success', 
        'cancelled': 'danger',
        'ended': 'info'
    })
    def display_status(self, obj):
        return obj.status

    @display(description=_('Fecha'))
    def event_date(self, obj):
        if obj.start_date == obj.end_date:
            return obj.start_date.strftime('%d %b %Y')
        return f"{obj.start_date.strftime('%d %b')} - {obj.end_date.strftime('%d %b %Y')}"

    @display(description=_('Destacado'), boolean=True)
    def display_featured(self, obj):
        return obj.is_featured

    def save_model(self, request, obj, form, change):
        if not change:
            obj.organizer_name = obj.organizer_name or request.user.get_full_name() or request.user.username
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }


# =============================================================================
# Newsletter Subscriber Admin
# =============================================================================

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(ModelAdmin):
    list_display = ('email', 'subscribed_at', 'display_status', 'days_subscribed')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at', 'unsubscribed_at')
    actions = ['activate_subscribers', 'deactivate_subscribers']
    list_per_page = 50
    
    fieldsets = (
        (_('Información del Suscriptor'), {
            'fields': ('email', 'is_active')
        }),
        (_('Marcas de Tiempo'), {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        })
    )
    
    @display(description=_("Estado"), label={'True': 'success', 'False': 'danger'})
    def display_status(self, obj):
        return str(obj.is_active)
    
    @display(description=_("Días Suscrito"))
    def days_subscribed(self, obj):
        if obj.subscribed_at:
            delta = timezone.now() - obj.subscribed_at
            return f"{delta.days} días"
        return "N/A"
    
    @admin.action(description=_("Activar suscriptores seleccionados"))
    def activate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, _("{} suscriptores activados correctamente.").format(updated))
    
    @admin.action(description=_("Desactivar suscriptores seleccionados"))
    def deactivate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=False, unsubscribed_at=timezone.now())
        self.message_user(request, _("{} suscriptores desactivados correctamente.").format(updated))

    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }


# =============================================================================
# Order Admin - Simplified view
# =============================================================================

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    # Reduced columns - removed customer_email and created_at from main view
    list_display = ('order_number', 'event', 'customer_name', 'display_total', 'display_status')
    list_filter = ('status', 'event')
    search_fields = ('order_number', 'customer_name', 'customer_email')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    list_per_page = 30
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Orden'), {
            'fields': ('order_number', 'event', 'status')
        }),
        (_('Cliente'), {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        (_('Pago'), {
            'fields': ('total_amount', 'payment_method', 'payment_reference')
        }),
        (_('Detalles Técnicos'), {
            'fields': ('used_saved_card', 'saved_card_token', 'vault_customer_id'),
            'classes': ('collapse',),
            'description': _('Información técnica del procesamiento de pago')
        }),
        (_('Notas'), {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        (_('Fechas'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    @display(description=_('Total'))
    def display_total(self, obj):
        return f"${obj.total_amount:,.2f}"
    
    @display(description=_('Estado'), label={
        'pending': 'warning',
        'completed': 'success',
        'cancelled': 'danger', 
        'refunded': 'info'
    })
    def display_status(self, obj):
        return obj.status
    
    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }


# =============================================================================
# Customer Vault Profile Admin - Simplified, technical fields hidden
# =============================================================================

@admin.register(CustomerVaultProfile)
class CustomerVaultProfileAdmin(ModelAdmin):
    # Simplified list - removed vault_customer_id
    list_display = ('customer_email', 'full_name', 'display_status', 'card_count')
    list_filter = ('is_active',)
    search_fields = ('customer_email', 'name', 'first_surname')
    readonly_fields = ('vault_customer_id', 'vault_reference', 'created_at', 'updated_at')
    inlines = [SavedPaymentMethodInline]
    list_per_page = 30
    
    fieldsets = (
        (_('Cliente'), {
            'fields': ('customer_email', ('name', 'first_surname', 'second_surname'), 'is_active')
        }),
        (_('Documento'), {
            'fields': (('doc_id_type', 'doc_id'),),
            'classes': ('collapse',)
        }),
        (_('Datos Técnicos de Vault'), {
            'fields': ('vault_customer_id', 'vault_reference'),
            'classes': ('collapse',),
            'description': _('IDs internos del sistema de tokenización')
        }),
        (_('Fechas'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    @display(description=_('Nombre'))
    def full_name(self, obj):
        return f"{obj.name} {obj.first_surname}"
    
    @display(description=_('Estado'), label={'True': 'success', 'False': 'danger'})
    def display_status(self, obj):
        return str(obj.is_active)
    
    @display(description=_('Tarjetas'))
    def card_count(self, obj):
        count = obj.saved_cards.filter(is_active=True).count()
        return f"{count}"
    
    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }


# =============================================================================
# NOTE: TicketType and SavedPaymentMethod are managed through inlines only
# They don't need standalone admin pages - access via Event and CustomerVaultProfile
# =============================================================================
