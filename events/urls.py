from django.urls import path
from .views import EventListView, EventDetailView, CategoryEventsView, FeaturedEventsView, PopularEventsView

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('event/<slug:slug>/', EventDetailView.as_view(), name='event_detail'),
    path('category/<slug:slug>/', CategoryEventsView.as_view(), name='category_events'),
    path('featured/', FeaturedEventsView.as_view(), name='featured_events'),
    path('popular/', PopularEventsView.as_view(), name='popular_events'),
] 