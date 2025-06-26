from rest_framework import serializers
from events.models import Event, Category, NewsletterSubscriber


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "parent", "order", "is_active"]


class EventSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        required=False
    )
    image_gallery = serializers.JSONField(required=False)

    class Meta:
        model = Event
        fields = [
            "id", "title", "slug", "description", "short_description",
            "organizer_name", "organizer_description", "organizer_logo",
            "start_date", "start_time", "end_date", "end_time",
            "location_name", "address", "address_2", "city",
            "state_province", "country", "venue_directions",
            "category", "category_id", "tags", "featured_image",
            "hero_image", "image_gallery", "video_url", "max_capacity"
        ]
        read_only_fields = ["slug"]

    def validate(self, data):
        if data.get("start_date") and data.get("end_date"):
            if data["start_date"] > data["end_date"]:
                raise serializers.ValidationError("End date must be after start date")
            elif data["start_date"] == data["end_date"]:
                if data.get("start_time") and data.get("end_time"):
                    if data["start_time"] >= data["end_time"]:
                        raise serializers.ValidationError("End time must be after start time")
        return data


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'subscribed_at', 'is_active']
        read_only_fields = ['subscribed_at', 'is_active']
    
    def validate_email(self, value):
        """Check if email is already subscribed"""
        if NewsletterSubscriber.objects.filter(email=value).exists():
            subscriber = NewsletterSubscriber.objects.get(email=value)
            if subscriber.is_active:
                raise serializers.ValidationError("This email is already subscribed to our newsletter.")
            else:
                # Reactivate the subscriber
                subscriber.resubscribe()
                raise serializers.ValidationError("Welcome back! Your subscription has been reactivated.")
        return value
