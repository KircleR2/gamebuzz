from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    EventViewSet, 
    CategoryViewSet, 
    FeaturedEventsView, 
    PopularCitiesView,
    HomepageStatsView,
    NewsletterSubscriptionView,
    HeroEventsView
)

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('homepage/featured-events/', FeaturedEventsView.as_view(), name='featured-events'),
    path('homepage/hero-events/', HeroEventsView.as_view(), name='hero-events'),
    path('homepage/popular-cities/', PopularCitiesView.as_view(), name='popular-cities'),
    path('homepage/stats/', HomepageStatsView.as_view(), name='homepage-stats'),
    path('newsletter/subscribe/', NewsletterSubscriptionView.as_view(), name='newsletter-subscribe'),
]
