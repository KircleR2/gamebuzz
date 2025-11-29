from django.urls import path
from django.http import JsonResponse
from .views import EventListView, EventDetailView, CategoryEventsView, FeaturedEventsView, PopularEventsView
from .models import Event

# Debug view to check if event exists
def debug_event_view(request, slug):
    """Debug view to check event lookup"""
    all_events = Event.objects.all()
    event_data = {
        'requested_slug': slug,
        'total_events': all_events.count(),
        'all_slugs': list(all_events.values_list('slug', flat=True)),
        'event_found': Event.objects.filter(slug=slug).exists(),
    }
    if Event.objects.filter(slug=slug).exists():
        event = Event.objects.get(slug=slug)
        event_data['event'] = {
            'id': event.id,
            'title': event.title,
            'slug': event.slug,
            'status': event.status,
        }
    return JsonResponse(event_data)

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('event/debug/<slug:slug>/', debug_event_view, name='debug_event'),  # Debug endpoint
    path('event/<slug:slug>/', EventDetailView.as_view(), name='event_detail'),
    path('category/<slug:slug>/', CategoryEventsView.as_view(), name='category_events'),
    path('featured/', FeaturedEventsView.as_view(), name='featured_events'),
    path('popular/', PopularEventsView.as_view(), name='popular_events'),
] 