from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_('nombre'), max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name=_('categoría padre'))
    description = models.TextField(_('descripción'), blank=True, null=True)
    icon = models.CharField(_('icono'), max_length=50, blank=True, help_text=_("Clase de icono Bootstrap, ej. 'bi-trophy'"))
    order = models.IntegerField(_('orden'), default=0, help_text=_("Orden en el que se debe mostrar la categoría"))
    is_active = models.BooleanField(_('activa'), default=True)
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('fecha de actualización'), auto_now=True)

    class Meta:
        verbose_name = _("Categoría")
        verbose_name_plural = _("Categorías")
        ordering = ['order', 'name']
        unique_together = ['name', 'parent']

    def __str__(self):
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        if self.parent:
            return f"{self.parent.full_name} > {self.name}"
        return self.name

class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', _('Borrador')), 
        ('published', _('Publicado')), 
        ('cancelled', _('Cancelado')), 
        ('ended', _('Finalizado'))
    ]
    
    title = models.CharField(_('título'), max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(_('descripción'))
    short_description = models.CharField(_('descripción corta'), max_length=200, help_text=_("Una breve descripción para los listados"), blank=True)
    organizer_name = models.CharField(_('nombre del organizador'), max_length=100)
    organizer_description = models.TextField(_('descripción del organizador'), blank=True)
    organizer_logo = models.ImageField(_('logo del organizador'), upload_to='organizer_logos/', blank=True, null=True)
    start_date = models.DateField(_('fecha de inicio'))
    start_time = models.TimeField(_('hora de inicio'))
    end_date = models.DateField(_('fecha de finalización'))
    end_time = models.TimeField(_('hora de finalización'))
    location_name = models.CharField(_('nombre del lugar'), max_length=255)
    address = models.CharField(_('dirección'), max_length=255)
    address_2 = models.CharField(_('dirección (línea 2)'), max_length=255, blank=True)
    city = models.CharField(_('ciudad'), max_length=100)
    state_province = models.CharField(_('estado/provincia'), max_length=100)
    country = models.CharField(_('país'), max_length=100, default="España")
    venue_directions = models.TextField(_('indicaciones del lugar'), blank=True, help_text=_("Indicaciones para llegar al lugar, información de estacionamiento, etc."))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='events', verbose_name=_('categoría'))
    tags = models.CharField(_('etiquetas'), max_length=500, blank=True, help_text=_("Etiquetas separadas por comas"))
    featured_image = models.ImageField(_('imagen destacada'), upload_to='events_images/', blank=True, null=True)
    image_gallery = models.JSONField(_('galería de imágenes'), default=list, blank=True, help_text=_("Lista de URLs de imágenes adicionales"))
    video_url = models.URLField(_('URL del video'), blank=True, help_text=_("Enlace al video (YouTube, Vimeo, etc.)"))
    max_capacity = models.PositiveIntegerField(_('capacidad máxima'), null=True, blank=True)
    registration_required = models.BooleanField(_('requiere registro'), default=False)
    registration_url = models.URLField(_('URL de registro'), blank=True, help_text=_("URL externa de registro/venta de entradas"))
    is_free = models.BooleanField(_('es gratuito'), default=True)
    price_display = models.CharField(_('mostrar precio'), max_length=100, blank=True, help_text=_("ej., 'Gratis', '-', 'Desde .99'"))
    faq = models.JSONField(_('preguntas frecuentes'), default=list, blank=True, help_text=_("Lista de elementos de preguntas frecuentes"))
    additional_info = models.TextField(_('información adicional'), blank=True, help_text=_("Cualquier información adicional sobre el evento"))
    status = models.CharField(_('estado'), max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(_('destacado'), default=False, help_text=_("Los eventos destacados se mostrarán en la página principal"))
    show_in_hero = models.BooleanField(_('mostrar en hero'), default=False, help_text=_("Mostrar este evento en la sección hero de la página principal"))
    hero_image = models.ImageField(_('imagen hero'), upload_to='events_hero_images/', blank=True, null=True, help_text=_("Imagen especial para la sección hero de la página principal (opcional)"))
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('fecha de actualización'), auto_now=True)

    class Meta:
        ordering = ['-start_date', '-start_time']
        verbose_name = _("Evento")
        verbose_name_plural = _("Eventos")
        indexes = [models.Index(fields=['start_date', 'status']), models.Index(fields=['is_featured'])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        today = timezone.now().date()
        return self.end_date >= today

    @property
    def is_ongoing(self):
        now = timezone.now()
        event_start = timezone.make_aware(timezone.datetime.combine(self.start_date, self.start_time))
        event_end = timezone.make_aware(timezone.datetime.combine(self.end_date, self.end_time))
        return event_start <= now <= event_end

    @property
    def duration_display(self):
        if self.start_date == self.end_date:
            return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"
        return f"{self.start_date.strftime('%B %d')} {self.start_time.strftime('%I:%M %p')} - {self.end_date.strftime('%B %d')} {self.end_time.strftime('%I:%M %p')}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(_('correo electrónico'), unique=True)
    subscribed_at = models.DateTimeField(_('fecha de suscripción'), auto_now_add=True)
    is_active = models.BooleanField(_('activo'), default=True, help_text=_("Si el suscriptor está activo"))
    unsubscribed_at = models.DateTimeField(_('fecha de cancelación'), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Suscriptor del Boletín")
        verbose_name_plural = _("Suscriptores del Boletín")
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
    
    def unsubscribe(self):
        """Mark subscriber as unsubscribed"""
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save()
    
    def resubscribe(self):
        """Reactivate subscriber"""
        self.is_active = True
        self.unsubscribed_at = None
        self.save()
