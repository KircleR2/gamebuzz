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
        if self.parent_id:  # Use parent_id to avoid triggering a query/recursion
            return f"{self.parent.name} > {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        """Build full category path, with protection against circular references"""
        names = [self.name]
        parent = self.parent
        seen_ids = {self.id}
        while parent:
            if parent.id in seen_ids:  # Circular reference detected
                break
            seen_ids.add(parent.id)
            names.insert(0, parent.name)
            parent = parent.parent
        return " > ".join(names)

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


class TicketType(models.Model):
    """Different ticket types/tiers for an event"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types', verbose_name=_('evento'))
    name = models.CharField(_('nombre'), max_length=100, help_text=_("ej., 'Entrada General', 'VIP', 'Early Bird'"))
    description = models.TextField(_('descripción'), blank=True, help_text=_("Descripción del tipo de entrada"))
    price = models.DecimalField(_('precio'), max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(_('cantidad disponible'), help_text=_("Número total de entradas disponibles"))
    quantity_sold = models.PositiveIntegerField(_('cantidad vendida'), default=0)
    sale_start = models.DateTimeField(_('inicio de venta'), blank=True, null=True)
    sale_end = models.DateTimeField(_('fin de venta'), blank=True, null=True)
    max_per_order = models.PositiveIntegerField(_('máximo por orden'), default=10, help_text=_("Número máximo de entradas por orden"))
    is_active = models.BooleanField(_('activo'), default=True)
    order = models.PositiveIntegerField(_('orden'), default=0, help_text=_("Orden de visualización"))
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('fecha de actualización'), auto_now=True)

    class Meta:
        verbose_name = _("Tipo de Entrada")
        verbose_name_plural = _("Tipos de Entradas")
        ordering = ['order', 'price']

    def __str__(self):
        return f"{self.name} - {self.event.title} (${self.price})"

    @property
    def quantity_remaining(self):
        return self.quantity_available - self.quantity_sold

    @property
    def is_sold_out(self):
        return self.quantity_remaining <= 0

    @property
    def is_on_sale(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.sale_start and now < self.sale_start:
            return False
        if self.sale_end and now > self.sale_end:
            return False
        return not self.is_sold_out


class Order(models.Model):
    """Track ticket purchases"""
    STATUS_CHOICES = [
        ('pending', _('Pendiente')),
        ('completed', _('Completado')),
        ('cancelled', _('Cancelado')),
        ('refunded', _('Reembolsado')),
    ]
    
    order_number = models.CharField(_('número de orden'), max_length=50, unique=True)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='orders', verbose_name=_('evento'))
    customer_email = models.EmailField(_('correo del cliente'))
    customer_name = models.CharField(_('nombre del cliente'), max_length=200)
    customer_phone = models.CharField(_('teléfono del cliente'), max_length=50, blank=True)
    status = models.CharField(_('estado'), max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(_('monto total'), max_digits=10, decimal_places=2)
    payment_method = models.CharField(_('método de pago'), max_length=50, blank=True)
    payment_reference = models.CharField(_('referencia de pago'), max_length=200, blank=True)
    notes = models.TextField(_('notas'), blank=True)
    
    vault_customer_id = models.IntegerField(_('ID de cliente en Vault'), null=True, blank=True, help_text=_("ID del cliente en Vault si se usó tokenización"))
    used_saved_card = models.BooleanField(_('usó tarjeta guardada'), default=False)
    saved_card_token = models.CharField(_('token de tarjeta guardada'), max_length=255, blank=True)
    
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('fecha de actualización'), auto_now=True)

    class Meta:
        verbose_name = _("Orden")
        verbose_name_plural = _("Órdenes")
        ordering = ['-created_at']

    def __str__(self):
        return f"Orden {self.order_number} - {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Individual line items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('orden'))
    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT, verbose_name=_('tipo de entrada'))
    quantity = models.PositiveIntegerField(_('cantidad'))
    unit_price = models.DecimalField(_('precio unitario'), max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Ítem de Orden")
        verbose_name_plural = _("Ítems de Orden")

    def __str__(self):
        return f"{self.quantity}x {self.ticket_type.name}"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class CustomerVaultProfile(models.Model):
    """Customer profile in Cobalt Vault API for tokenization"""
    DOC_TYPE_CHOICES = [
        ('C', _('Cédula')),
        ('P', _('Pasaporte'))
    ]
    
    customer_email = models.EmailField(_('correo del cliente'), unique=True, db_index=True)
    vault_customer_id = models.IntegerField(_('ID de cliente en Vault'), help_text=_("ID del cliente en la API de Cobalt"))
    vault_reference = models.CharField(_('referencia de Vault'), max_length=100, unique=True)
    
    name = models.CharField(_('nombre'), max_length=50)
    first_surname = models.CharField(_('primer apellido'), max_length=120)
    second_surname = models.CharField(_('segundo apellido'), max_length=120, blank=True)
    doc_id_type = models.CharField(_('tipo de documento'), max_length=1, choices=DOC_TYPE_CHOICES)
    doc_id = models.CharField(_('número de documento'), max_length=50)
    
    is_active = models.BooleanField(_('activo'), default=True)
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('fecha de actualización'), auto_now=True)
    
    class Meta:
        verbose_name = _("Perfil de Cliente Vault")
        verbose_name_plural = _("Perfiles de Cliente Vault")
        ordering = ['-created_at']
        indexes = [models.Index(fields=['customer_email'])]
    
    def __str__(self):
        return f"{self.name} {self.first_surname} ({self.customer_email})"


class SavedPaymentMethod(models.Model):
    """Tokenized payment cards stored in Cobalt Vault"""
    customer_profile = models.ForeignKey(
        CustomerVaultProfile, 
        on_delete=models.CASCADE, 
        related_name='saved_cards',
        verbose_name=_('perfil de cliente')
    )
    
    vault_card_id = models.IntegerField(_('ID de tarjeta en Vault'), help_text=_("ID de la tarjeta en la API de Cobalt"))
    customer_token = models.CharField(_('token de cliente'), max_length=255, unique=True, db_index=True)
    
    card_brand = models.CharField(_('marca de tarjeta'), max_length=20)
    last_four = models.CharField(_('últimos 4 dígitos'), max_length=4)
    exp_month = models.CharField(_('mes de expiración'), max_length=2)
    exp_year = models.CharField(_('año de expiración'), max_length=4)
    card_holder = models.CharField(_('titular de tarjeta'), max_length=255)
    alias = models.CharField(_('alias'), max_length=50)
    
    is_default = models.BooleanField(_('predeterminada'), default=False)
    is_active = models.BooleanField(_('activa'), default=True)
    
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('fecha de actualización'), auto_now=True)
    last_used_at = models.DateTimeField(_('último uso'), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Método de Pago Guardado")
        verbose_name_plural = _("Métodos de Pago Guardados")
        ordering = ['-is_default', '-last_used_at']
        indexes = [models.Index(fields=['customer_token'])]
    
    def __str__(self):
        return f"{self.alias} - {self.customer_profile.customer_email}"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            SavedPaymentMethod.objects.filter(
                customer_profile=self.customer_profile,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
