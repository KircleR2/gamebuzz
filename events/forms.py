from django import forms
from django.utils.html import format_html

# List of common Bootstrap icons for the dropdown
BOOTSTRAP_ICONS = [
    ('bi-trophy', 'Trophy'),
    ('bi-calendar-event', 'Calendar Event'),
    ('bi-controller', 'Game Controller'),
    ('bi-joystick', 'Joystick'),
    ('bi-people', 'People'),
    ('bi-person', 'Person'),
    ('bi-music-note', 'Music'),
    ('bi-film', 'Film'),
    ('bi-camera', 'Camera'),
    ('bi-book', 'Book'),
    ('bi-laptop', 'Laptop'),
    ('bi-phone', 'Phone'),
    ('bi-house', 'House'),
    ('bi-shop', 'Shop'),
    ('bi-cart', 'Cart'),
    ('bi-bag', 'Bag'),
    ('bi-gift', 'Gift'),
    ('bi-truck', 'Truck'),
    ('bi-cup', 'Cup'),
    ('bi-geo-alt', 'Location'),
    ('bi-map', 'Map'),
    ('bi-chat', 'Chat'),
    ('bi-envelope', 'Envelope'),
    ('bi-bell', 'Bell'),
    ('bi-heart', 'Heart'),
    ('bi-star', 'Star'),
    ('bi-flag', 'Flag'),
    ('bi-gear', 'Gear'),
    ('bi-tools', 'Tools'),
    ('bi-wrench', 'Wrench'),
    ('bi-clock', 'Clock'),
    ('bi-hourglass', 'Hourglass'),
    ('bi-wallet', 'Wallet'),
    ('bi-currency-dollar', 'Dollar'),
    ('bi-credit-card', 'Credit Card'),
    ('bi-graph-up', 'Graph Up'),
    ('bi-award', 'Award'),
    ('bi-ticket', 'Ticket'),
    ('bi-emoji-smile', 'Smile'),
    ('bi-briefcase', 'Briefcase'),
]

class IconPickerWidget(forms.Select):
    """Custom widget for selecting Bootstrap icons with visual preview"""
    
    class Media:
        css = {
            'all': [
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css',
                'css/icon-picker.css',
            ]
        }
        js = ['js/icon-picker.js']
    
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs['class'] = attrs.get('class', '') + ' icon-picker-select'
        output = super().render(name, value, attrs, renderer)
        
        # Add a preview div that will show the selected icon
        preview = format_html(
            '<div class="icon-preview"><i class="{}" style="font-size: 1.5rem;"></i></div>',
            value or 'bi-question-circle'
        )
        
        return format_html('{}<div class="icon-picker-container">{}</div>', output, preview)

class IconField(forms.ChoiceField):
    """Custom form field for icon selection"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', BOOTSTRAP_ICONS)
        kwargs.setdefault('widget', IconPickerWidget)
        super().__init__(*args, **kwargs) 