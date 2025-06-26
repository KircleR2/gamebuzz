from django.core.management.base import BaseCommand
from events.models import Event, Category
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Set up test hero events for demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing hero events first'
        )

    def handle(self, *args, **options):
        if options['clear']:
            Event.objects.filter(show_in_hero=True).update(show_in_hero=False)
            self.stdout.write('Cleared existing hero events')
        
        # Get or create a category
        category, created = Category.objects.get_or_create(
            name='Tournaments',
            defaults={
                'slug': 'tournaments',
                'description': 'Competitive gaming tournaments',
                'icon': 'bi-trophy'
            }
        )
        
        if created:
            self.stdout.write(f'Created category: {category.name}')
        
        # Create hero events
        hero_events_data = [
            {
                'title': 'Epic Gaming Championship 2025',
                'short_description': 'The biggest gaming tournament of the year with massive prizes',
                'description': 'Join us for the most epic gaming championship featuring top players from around the world. Compete in multiple game categories and win amazing prizes.',
                'start_date': timezone.now().date() + timedelta(days=30),
                'end_date': timezone.now().date() + timedelta(days=30),
                'start_time': '09:00:00',
                'end_time': '18:00:00',
                'location_name': 'Gaming Arena Center',
                'address': '123 Gaming Street',
                'city': 'Los Angeles',
                'state_province': 'CA',
                'country': 'United States',
                'organizer_name': 'Epic Gaming Events',
                'is_free': False,
                'price_display': '$25',
                'show_in_hero': True,
                'is_featured': True,
                'status': 'published'
            },
            {
                'title': 'Indie Game Showcase',
                'short_description': 'Discover the next big indie games before anyone else',
                'description': 'Experience the future of gaming at our indie game showcase. Meet developers, play exclusive demos, and discover hidden gems.',
                'start_date': timezone.now().date() + timedelta(days=45),
                'end_date': timezone.now().date() + timedelta(days=45),
                'start_time': '10:00:00',
                'end_time': '20:00:00',
                'location_name': 'Innovation Hub',
                'address': '456 Tech Boulevard',
                'city': 'San Francisco',
                'state_province': 'CA',
                'country': 'United States',
                'organizer_name': 'Indie Game Collective',
                'is_free': True,
                'price_display': 'Free',
                'show_in_hero': True,
                'is_featured': True,
                'status': 'published'
            },
            {
                'title': 'Retro Gaming Convention',
                'short_description': 'Celebrate classic games and nostalgic memories',
                'description': 'Step back in time at our retro gaming convention. Play classic arcade games, meet fellow retro enthusiasts, and relive gaming history.',
                'start_date': timezone.now().date() + timedelta(days=60),
                'end_date': timezone.now().date() + timedelta(days=60),
                'start_time': '11:00:00',
                'end_time': '22:00:00',
                'location_name': 'Retro Arcade Museum',
                'address': '789 Nostalgia Lane',
                'city': 'Austin',
                'state_province': 'TX',
                'country': 'United States',
                'organizer_name': 'Retro Gaming Society',
                'is_free': False,
                'price_display': '$15',
                'show_in_hero': True,
                'is_featured': True,
                'status': 'published'
            }
        ]
        
        created_count = 0
        for event_data in hero_events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults={
                    **event_data,
                    'category': category
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'Created hero event: {event.title}')
            else:
                # Update existing event to be a hero event
                event.show_in_hero = True
                event.is_featured = True
                event.status = 'published'
                event.save()
                self.stdout.write(f'Updated event to hero: {event.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully set up {created_count} hero events')
        )
        
        # Show current hero events
        hero_events = Event.objects.filter(show_in_hero=True, status='published')
        self.stdout.write(f'\nCurrent hero events ({hero_events.count()}):')
        for event in hero_events:
            self.stdout.write(f'- {event.title} ({event.start_date})') 