from django.views.generic import TemplateView, DetailView, ListView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import os
from .models import Event, Category, NewsletterSubscriber
from django.utils import timezone
from django.db import models
from django.shortcuts import get_object_or_404
from django.conf import settings

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


def debug_static_files(request):
    """Debug endpoint to check static file configuration"""
    import os
    from django.conf import settings
    
    result = {
        'BASE_DIR': str(settings.BASE_DIR),
        'STATIC_URL': settings.STATIC_URL,
        'STATIC_ROOT': str(settings.STATIC_ROOT),
        'STATICFILES_DIRS': [str(d) for d in settings.STATICFILES_DIRS],
        'DEBUG': settings.DEBUG,
    }
    
    # Check if STATIC_ROOT exists
    static_root = str(settings.STATIC_ROOT)
    result['STATIC_ROOT_exists'] = os.path.exists(static_root)
    result['STATIC_ROOT_is_dir'] = os.path.isdir(static_root)
    
    if result['STATIC_ROOT_exists']:
        # List contents of STATIC_ROOT
        try:
            contents = []
            for root, dirs, files in os.walk(static_root):
                rel_root = os.path.relpath(root, static_root)
                for f in files[:10]:  # Limit to 10 files per directory
                    path = os.path.join(rel_root, f) if rel_root != '.' else f
                    contents.append(path)
                if len(contents) > 50:  # Limit total files
                    break
            result['STATIC_ROOT_contents'] = contents[:50]
        except Exception as e:
            result['STATIC_ROOT_contents_error'] = str(e)
    
    # Check if specific CSS file exists
    css_path = os.path.join(static_root, 'css', 'gamebuzz.css')
    result['gamebuzz_css_exists'] = os.path.exists(css_path)
    result['gamebuzz_css_path'] = css_path
    result['gamebuzz_css_is_file'] = os.path.isfile(css_path)
    
    # Try to read first 100 chars of the CSS file
    if result['gamebuzz_css_exists']:
        try:
            with open(css_path, 'r') as f:
                result['gamebuzz_css_content_preview'] = f.read(100)
        except Exception as e:
            result['gamebuzz_css_read_error'] = str(e)
    
    # Check working directory
    result['cwd'] = os.getcwd()
    
    # Check URL patterns
    from django.urls import get_resolver
    resolver = get_resolver()
    result['url_patterns'] = [str(p.pattern) for p in resolver.url_patterns[:10]]
    
    return JsonResponse(result, json_dumps_params={'indent': 2})


def serve_css(request):
    """Directly serve the gamebuzz.css file"""
    import os
    from django.conf import settings
    
    css_path = os.path.join(str(settings.STATIC_ROOT), 'css', 'gamebuzz.css')
    
    try:
        with open(css_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/css')
    except FileNotFoundError:
        return HttpResponse(f"File not found: {css_path}", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


def test_serve(request, path="css/gamebuzz.css"):
    """Test the serve view logic"""
    import os
    from django.conf import settings
    from django.views.static import serve
    from django.http import Http404
    
    result = {
        'path': path,
        'document_root': str(settings.STATIC_ROOT),
        'full_path': os.path.join(str(settings.STATIC_ROOT), path),
    }
    
    # Check if file exists
    full_path = os.path.join(str(settings.STATIC_ROOT), path)
    result['file_exists'] = os.path.exists(full_path)
    result['is_file'] = os.path.isfile(full_path)
    
    # Try to call serve directly
    try:
        from django.http import HttpRequest
        # This will raise Http404 if file not found
        response = serve(request, path, document_root=str(settings.STATIC_ROOT))
        result['serve_status'] = response.status_code
        result['serve_content_type'] = response.get('Content-Type', 'unknown')
    except Http404 as e:
        result['serve_error'] = f"Http404: {str(e)}"
    except Exception as e:
        result['serve_error'] = f"Exception: {type(e).__name__}: {str(e)}"
    
    return JsonResponse(result, json_dumps_params={'indent': 2})
