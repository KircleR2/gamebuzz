#!/usr/bin/env python
import os
import sys
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_platform.settings')
django.setup()

from events.models import Category, Event

def create_categories():
    """Create gaming categories with appropriate icons"""
    categories = [
        {"name": "Esports", "icon": "bi-trophy", "description": "Competitive gaming tournaments and events"},
        {"name": "Conventions", "icon": "bi-people", "description": "Gaming conventions and expos"},
        {"name": "Tournaments", "icon": "bi-joystick", "description": "Local and regional gaming tournaments"},
        {"name": "Streaming", "icon": "bi-display", "description": "Live streaming events and meetups"},
        {"name": "Board Games", "icon": "bi-puzzle", "description": "Board game nights and competitions"},
        {"name": "VR Events", "icon": "bi-headset-vr", "description": "Virtual reality gaming experiences"},
        {"name": "Cosplay", "icon": "bi-magic", "description": "Gaming cosplay contests and showcases"},
        {"name": "Retro", "icon": "bi-clock-history", "description": "Retro gaming events and arcades"}
    ]
    
    created_categories = []
    for i, cat_data in enumerate(categories):
        category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={
                "icon": cat_data["icon"],
                "description": cat_data["description"],
                "order": i,
                "is_active": True
            }
        )
        created_categories.append(category)
        print(f"{'Created' if created else 'Found'} category: {category.name}")
    
    return created_categories

def create_events(categories):
    """Create sample events across different categories and cities"""
    
    # Sample cities with venue data
    cities = [
        {"city": "New York", "state": "NY", "venues": ["Tech Convention Center", "Esports Arena NYC", "Retro Arcade Bar"]},
        {"city": "Los Angeles", "state": "CA", "venues": ["LA Gaming Center", "Esports Stadium", "Pixel Lounge"]},
        {"city": "Chicago", "state": "IL", "venues": ["Chicago Convention Center", "Game Vault", "Arcade Legacy"]},
        {"city": "San Francisco", "state": "CA", "venues": ["Moscone Center", "VR World SF", "Game Parlor"]},
        {"city": "Seattle", "state": "WA", "venues": ["Seattle Center", "Gaming Hub", "Retro Game Paradise"]},
        {"city": "Boston", "state": "MA", "venues": ["Boston Exhibition Center", "Game On", "Bit Bar"]},
    ]
    
    # Sample event titles and descriptions
    event_templates = [
        {
            "title_template": "{game} {event_type}",
            "games": ["Fortnite", "League of Legends", "Valorant", "Counter-Strike", "Dota 2", "Overwatch"],
            "event_types": ["Tournament", "Championship", "World Cup Qualifier", "Pro League", "Amateur Night"],
            "description": "Join us for an exciting {game} competition where players will battle for prizes and glory!"
        },
        {
            "title_template": "{prefix} Gaming Convention {year}",
            "prefix": ["GameCon", "GamerX", "GameFest", "PixelCon", "GameWorld", "GameBuzz"],
            "description": "The ultimate gaming convention featuring the latest games, panels with industry experts, and networking opportunities."
        },
        {
            "title_template": "Retro Gaming Night: {era} Classics",
            "era": ["80s", "90s", "2000s", "Arcade", "Console", "PC"],
            "description": "Relive the golden age of gaming with classic titles from the {era}. Bring friends and enjoy nostalgic gaming moments!"
        },
        {
            "title_template": "{type} Experience: {theme}",
            "type": ["VR", "AR", "Mixed Reality"],
            "theme": ["New Worlds", "Future Gaming", "Immersive Adventures", "Beyond Reality"],
            "description": "Step into a new dimension with our {type} gaming experience. Explore virtual worlds and cutting-edge technology."
        }
    ]
    
    # Create events
    current_date = timezone.now().date()
    
    for i in range(20):  # Create 20 events
        # Select random data
        category = random.choice(categories)
        location = random.choice(cities)
        template = random.choice(event_templates)
        
        # Generate event title
        if "games" in template and "event_types" in template:
            game = random.choice(template["games"])
            event_type = random.choice(template["event_types"])
            title = template["title_template"].format(game=game, event_type=event_type)
            description = template["description"].format(game=game)
        elif "prefix" in template:
            prefix = random.choice(template["prefix"])
            title = template["title_template"].format(prefix=prefix, year=current_date.year + 1)
            description = template["description"]
        elif "era" in template:
            era = random.choice(template["era"])
            title = template["title_template"].format(era=era)
            description = template["description"].format(era=era)
        elif "type" in template and "theme" in template:
            type_value = random.choice(template["type"])
            theme = random.choice(template["theme"])
            title = template["title_template"].format(type=type_value, theme=theme)
            description = template["description"].format(type=type_value)
        else:
            title = f"Gaming Event {i+1}"
            description = "A fantastic gaming event you won't want to miss!"
        
        # Generate dates
        start_date = current_date + timedelta(days=random.randint(7, 120))
        end_date = start_date + timedelta(days=random.randint(0, 3))
        start_time = f"{random.randint(9, 18):02d}:00:00"
        end_time = f"{random.randint(19, 23):02d}:00:00"
        
        # Select venue
        venue = random.choice(location["venues"])
        
        # Determine if featured (make ~25% of events featured)
        is_featured = random.random() < 0.25
        
        # Create the event
        event, created = Event.objects.get_or_create(
            title=title,
            defaults={
                "description": description,
                "short_description": description[:100] + "..." if len(description) > 100 else description,
                "organizer_name": "GameBuzz Events",
                "start_date": start_date,
                "start_time": start_time,
                "end_date": end_date,
                "end_time": end_time,
                "location_name": venue,
                "address": f"{random.randint(100, 999)} Main Street",
                "city": location["city"],
                "state_province": location["state"],
                "country": "United States",
                "category": category,
                "is_featured": is_featured,
                "is_published": True,
                "is_free": random.random() < 0.3,  # 30% chance of being free
                "price_display": f"{random.randint(10, 100)}.99" if random.random() > 0.3 else "Free",
                "tags": ",".join(random.sample(["gaming", "esports", "tournament", "convention", "vr", "retro", "cosplay", "streaming"], k=random.randint(2, 4)))
            }
        )
        
        print(f"{'Created' if created else 'Found'} event: {event.title} ({'Featured' if event.is_featured else 'Regular'})")

def run():
    """Run the seed script"""
    print("Starting seed script...")
    print("Creating categories...")
    categories = create_categories()
    
    print("\nCreating events...")
    create_events(categories)
    
    print("\nSeed script completed!")

if __name__ == "__main__":
    run()