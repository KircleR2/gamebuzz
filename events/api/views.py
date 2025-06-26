from rest_framework import viewsets, filters, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from events.models import Event, Category, NewsletterSubscriber
from .serializers import EventSerializer, CategorySerializer, NewsletterSubscriberSerializer
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "order"]
    ordering = ["order", "name"]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(status='published')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "start_date", "city", "state_province", "country"]
    search_fields = [
        "title",
        "description",
        "short_description",
        "organizer_name",
        "location_name",
    ]
    ordering_fields = ["start_date", "title", "created_at"]
    ordering = ["-start_date"]

    def get_queryset(self):
        """
        Optionally restricts the returned events to a given date range,
        by filtering against `start_date` and `end_date` query parameters.
        """
        queryset = Event.objects.filter(status='published')
        start_after = self.request.query_params.get("start_after", None)
        end_before = self.request.query_params.get("end_before", None)

        if start_after is not None:
            queryset = queryset.filter(start_date__gte=start_after)
        if end_before is not None:
            queryset = queryset.filter(end_date__lte=end_before)

        return queryset


class FeaturedEventsView(generics.ListAPIView):
    """
    Returns a list of featured events.
    """
    queryset = Event.objects.filter(status='published', is_featured=True).order_by('start_date')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None # Disable pagination for this view


class PopularCitiesView(generics.GenericAPIView):
    """
    Returns a list of cities with the highest number of upcoming events.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        upcoming_events = Event.objects.filter(status='published', start_date__gte=timezone.now().date())
        cities = (
            upcoming_events
            .values('city', 'state_province')
            .annotate(event_count=Count('id'))
            .order_by('-event_count')
        )[:6] # Top 6 cities
        return Response(cities)


class HomepageStatsView(generics.GenericAPIView):
    """
    Returns key statistics for the homepage.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        total_events = Event.objects.filter(status='published').count()
        total_cities = Event.objects.filter(status='published').values('city').distinct().count()
        # These would be more complex in a real app, mocking for now
        total_players = "100k+" 
        avg_rating = 4.8

        stats = {
            'total_events': total_events,
            'total_cities': total_cities,
            'total_players': total_players,
            'average_rating': avg_rating,
        }
        return Response(stats)


class NewsletterSubscriptionView(generics.CreateAPIView):
    """
    Handle newsletter subscription requests.
    """
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = []  # Allow anonymous access
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            subscriber = serializer.save()
            return Response({
                'message': 'Successfully subscribed to our newsletter!',
                'email': subscriber.email,
                'subscribed_at': subscriber.subscribed_at
            }, status=status.HTTP_201_CREATED)
        
        # Handle validation errors
        if 'email' in serializer.errors:
            error_message = serializer.errors['email'][0]
            if 'reactivated' in error_message:
                return Response({
                    'message': error_message,
                    'status': 'reactivated'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': error_message,
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': 'Invalid request data.',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)


class HeroEventsView(generics.ListAPIView):
    """
    Returns a list of events marked for hero section display.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None  # Disable pagination for hero events
    
    def get_queryset(self):
        """
        Returns events marked for hero section that are published and upcoming.
        """
        return Event.objects.filter(
            status='published', 
            show_in_hero=True,
            end_date__gte=timezone.now().date()
        ).order_by('start_date')
