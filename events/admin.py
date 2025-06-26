# /Users/aaay/dev/events/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Event, NewsletterSubscriber
from django.utils import timezone

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order', 'is_active', 'icon', 'created_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    list_editable = ('order', 'is_active', 'icon')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')

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
        ('Basic Information', {
            'fields': (
                'title', 'slug', 'status', 'is_featured',
                'short_description', 'description'
            )
        }),
        ('Date and Time', {
            'fields': (
                ('start_date', 'start_time'),
                ('end_date', 'end_time')
            )
        }),
        ('Location', {
            'fields': (
                'location_name',
                'address',
                'address_2',
                ('city', 'state_province'),
                'country',
                'venue_directions'
            )
        }),
        ('Organizer Information', {
            'fields': (
                'organizer_name',
                'organizer_description',
                'organizer_logo'
            )
        }),
        ('Categorization', {
            'fields': (
                'category',
                'tags'
            )
        }),
        ('Media', {
            'fields': (
                'featured_image',
                'hero_image',
                'image_gallery',
                'video_url'
            )
        }),
        ('Registration & Capacity', {
            'fields': (
                'registration_required',
                'registration_url',
                'max_capacity',
                'is_free',
                'price_display'
            )
        }),
        ('Additional Information', {
            'fields': (
                'faq',
                'additional_info'
            ),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Automatically managed fields'
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')

    def event_date(self, obj):
        return obj.duration_display
    event_date.short_description = 'Date & Time'

    def location_display(self, obj):
        return f"{obj.location_name}, {obj.city}"
    location_display.short_description = 'Location'

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
        ('Subscriber Information', {
            'fields': ('email', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        })
    )
    
    def days_subscribed(self, obj):
        """Calculate days since subscription"""
        if obj.subscribed_at:
            delta = timezone.now() - obj.subscribed_at
            return f"{delta.days} days"
        return "N/A"
    days_subscribed.short_description = "Days Subscribed"
    
    def activate_subscribers(self, request, queryset):
        """Activate selected subscribers"""
        updated = queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, f"{updated} subscribers activated successfully.")
    activate_subscribers.short_description = "Activate selected subscribers"
    
    def deactivate_subscribers(self, request, queryset):
        """Deactivate selected subscribers"""
        updated = queryset.update(is_active=False, unsubscribed_at=timezone.now())
        self.message_user(request, f"{updated} subscribers deactivated successfully.")
    deactivate_subscribers.short_description = "Deactivate selected subscribers"
