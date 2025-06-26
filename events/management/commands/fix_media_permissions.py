import os
import stat
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Fix permissions for media files and directories'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        self.stdout.write(f"Checking media directory at: {media_root}")
        
        # Create media directory if it doesn't exist
        if not os.path.exists(media_root):
            os.makedirs(media_root, exist_ok=True)
            self.stdout.write(self.style.SUCCESS(f"Created media directory at {media_root}"))
        
        # Create subdirectories for uploads if they don't exist
        subdirs = ['events_images', 'events_hero_images', 'organizer_logos']
        for subdir in subdirs:
            subdir_path = os.path.join(media_root, subdir)
            if not os.path.exists(subdir_path):
                os.makedirs(subdir_path, exist_ok=True)
                self.stdout.write(self.style.SUCCESS(f"Created subdirectory {subdir}"))
        
        # Set permissions for media directory and all subdirectories/files
        for root, dirs, files in os.walk(media_root):
            # Set directory permissions (755)
            os.chmod(root, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            self.stdout.write(f"Fixed permissions for directory: {root}")
            
            # Set file permissions (644)
            for file in files:
                file_path = os.path.join(root, file)
                os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
                self.stdout.write(f"Fixed permissions for file: {file_path}")
        
        self.stdout.write(self.style.SUCCESS('Successfully fixed media permissions')) 