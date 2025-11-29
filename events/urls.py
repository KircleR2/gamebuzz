from django.urls import path
from .views import EventListView, EventDetailView, CategoryEventsView, FeaturedEventsView, PopularEventsView, EventCheckoutView

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('e/<slug:slug>/', EventDetailView.as_view(), name='event_detail'),  # Use /e/ to avoid DigitalOcean ingress conflict
    path('e/<slug:slug>/checkout/', EventCheckoutView.as_view(), name='event_checkout'),  # Checkout page
    path('category/<slug:slug>/', CategoryEventsView.as_view(), name='category_events'),
    path('featured/', FeaturedEventsView.as_view(), name='featured_events'),
    path('popular/', PopularEventsView.as_view(), name='popular_events'),
] 