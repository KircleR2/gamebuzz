from django.core.management.base import BaseCommand
from events.models import NewsletterSubscriber
import csv
from django.utils import timezone


class Command(BaseCommand):
    help = 'Export newsletter subscribers to CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default=f'subscribers_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv',
            help='Output CSV filename'
        )
        parser.add_argument(
            '--active-only',
            action='store_true',
            help='Export only active subscribers'
        )

    def handle(self, *args, **options):
        filename = options['output']
        active_only = options['active_only']
        
        # Get subscribers
        if active_only:
            subscribers = NewsletterSubscriber.objects.filter(is_active=True)
            self.stdout.write(f"Exporting {subscribers.count()} active subscribers...")
        else:
            subscribers = NewsletterSubscriber.objects.all()
            self.stdout.write(f"Exporting {subscribers.count()} subscribers...")
        
        # Write to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['email', 'subscribed_at', 'is_active', 'unsubscribed_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for subscriber in subscribers:
                writer.writerow({
                    'email': subscriber.email,
                    'subscribed_at': subscriber.subscribed_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_active': subscriber.is_active,
                    'unsubscribed_at': subscriber.unsubscribed_at.strftime('%Y-%m-%d %H:%M:%S') if subscriber.unsubscribed_at else ''
                })
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully exported subscribers to {filename}')
        ) 