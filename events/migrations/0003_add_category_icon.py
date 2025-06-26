from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_remove_event_timezone_remove_event_zip_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.CharField(blank=True, help_text="Bootstrap icon class e.g. 'bi-trophy'", max_length=50),
        ),
    ]
