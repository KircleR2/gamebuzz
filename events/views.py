from django.views.generic import TemplateView, DetailView, ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Event, Category, NewsletterSubscriber
from django.utils import timezone
from django.db import models
from django.shortcuts import get_object_or_404

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
    
    def get_queryset(self):
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
