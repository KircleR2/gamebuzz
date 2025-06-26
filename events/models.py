from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap icon class e.g. 'bi-trophy'")
    order = models.IntegerField(default=0, help_text="Order in which the category should be displayed")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
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
    STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published'), ('cancelled', 'Cancelled'), ('ended', 'Ended')]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200, help_text="A brief description for listings", blank=True)
    organizer_name = models.CharField(max_length=100)
    organizer_description = models.TextField(blank=True)
    organizer_logo = models.ImageField(upload_to='organizer_logos/', blank=True, null=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    location_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="United States")
    venue_directions = models.TextField(blank=True, help_text="Directions to the venue, parking info, etc.")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    featured_image = models.ImageField(upload_to='events_images/', blank=True, null=True)
    image_gallery = models.JSONField(default=list, blank=True, help_text="List of additional image URLs")
    video_url = models.URLField(blank=True, help_text="Link to video (YouTube, Vimeo, etc.)")
    max_capacity = models.PositiveIntegerField(null=True, blank=True)
    registration_required = models.BooleanField(default=False)
    registration_url = models.URLField(blank=True, help_text="External registration/ticketing URL")
    is_free = models.BooleanField(default=True)
    price_display = models.CharField(max_length=100, blank=True, help_text="e.g., 'Free', '-', 'Starting at .99'")
    faq = models.JSONField(default=list, blank=True, help_text="List of FAQ items")
    additional_info = models.TextField(blank=True, help_text="Any additional information about the event")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False, help_text="Featured events will be displayed on the homepage")
    show_in_hero = models.BooleanField(default=False, help_text="Show this event in the homepage hero section")
    hero_image = models.ImageField(upload_to='events_hero_images/', blank=True, null=True, help_text="Special image for the homepage hero section (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', '-start_time']
        verbose_name = "Event"
        verbose_name_plural = "Events"
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
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Whether the subscriber is active")
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
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
