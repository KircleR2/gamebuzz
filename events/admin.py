# /Users/aaay/dev/events/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Event, NewsletterSubscriber
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .forms import IconField

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order', 'is_active', 'display_icon', 'created_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    list_editable = ('order', 'is_active')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')
    
    def display_icon(self, obj):
        """Display the icon in the list view"""
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 1.2rem;"></i>', obj.icon)
        return "-"
    display_icon.short_description = _("Icono")
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Override form field for icon to use our custom IconField"""
        if db_field.name == 'icon':
            return IconField(required=False, help_text=db_field.help_text)
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    class Media:
        css = {
            'all': [
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css',
            ]
        }

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'event_date', 'location_display', 'is_featured', 'show_in_hero')
    list_filter = (
        'status',
        'is_featured',
        'is_free',
        'category',
        'start_date',
        'city',
        'registration_required',
        'show_in_hero',
    )
    list_editable = ('status', 'is_featured', 'show_in_hero')
    search_fields = (
        'title',
        'description',
        'short_description',
        'location_name',
        'address',
        'city',
        'organizer_name'
    )
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    
    fieldsets = (
        (_('Información Básica'), {
            'fields': (
                'title', 'slug', 'status', 'is_featured',
                'short_description', 'description'
            )
        }),
        (_('Fecha y Hora'), {
            'fields': (
                ('start_date', 'start_time'),
                ('end_date', 'end_time')
            )
        }),
        (_('Ubicación'), {
            'fields': (
                'location_name',
                'address',
                'address_2',
                ('city', 'state_province'),
                'country',
                'venue_directions'
            )
        }),
        (_('Información del Organizador'), {
            'fields': (
                'organizer_name',
                'organizer_description',
                'organizer_logo'
            )
        }),
        (_('Categorización'), {
            'fields': (
                'category',
                'tags'
            )
        }),
        (_('Multimedia'), {
            'fields': (
                'featured_image',
                'hero_image',
                'image_gallery',
                'video_url'
            )
        }),
        (_('Registro y Capacidad'), {
            'fields': (
                'registration_required',
                'registration_url',
                'max_capacity',
                'is_free',
                'price_display'
            )
        }),
        (_('Información Adicional'), {
            'fields': (
                'faq',
                'additional_info'
            ),
            'classes': ('collapse',)
        }),
        (_('Campos del Sistema'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': _('Campos gestionados automáticamente')
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')

    def event_date(self, obj):
        return obj.duration_display
    event_date.short_description = _('Fecha y Hora')

    def location_display(self, obj):
        return f"{obj.location_name}, {obj.city}"
    location_display.short_description = _('Ubicación')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.organizer_name = obj.organizer_name or request.user.get_full_name() or request.user.username
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('admin/css/event_admin.css',)
        }
        js = ('admin/js/event_admin.js',)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active', 'days_subscribed')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at', 'unsubscribed_at')
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    fieldsets = (
        (_('Información del Suscriptor'), {
            'fields': ('email', 'is_active')
        }),
        (_('Marcas de Tiempo'), {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        })
    )
    
    def days_subscribed(self, obj):
        """Calculate days since subscription"""
        if obj.subscribed_at:
            delta = timezone.now() - obj.subscribed_at
            return f"{delta.days} " + _("días")
        return _("N/A")
    days_subscribed.short_description = _("Días Suscrito")
    
    def activate_subscribers(self, request, queryset):
        """Activate selected subscribers"""
        updated = queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, _("{} suscriptores activados correctamente.").format(updated))
    activate_subscribers.short_description = _("Activar suscriptores seleccionados")
    
    def deactivate_subscribers(self, request, queryset):
        """Deactivate selected subscribers"""
        updated = queryset.update(is_active=False, unsubscribed_at=timezone.now())
        self.message_user(request, _("{} suscriptores desactivados correctamente.").format(updated))
    deactivate_subscribers.short_description = _("Desactivar suscriptores seleccionados")
