# GameBuzz Deployment Guide

This guide provides step-by-step instructions for deploying the GameBuzz event platform to Render.

## Prerequisites

1. A [Render account](https://render.com/)
2. A Git repository with your GameBuzz code
3. Basic familiarity with the command line

## Deployment Files

The following files have been set up for deployment:

- `requirements.txt`: Lists all Python dependencies
- `build.sh`: Script that runs during the build process
- `render.yaml`: Configuration for Render Blueprint deployment
- `Procfile`: Specifies the command to run the application
- `runtime.txt`: Specifies the Python version

## Deployment Options

### Option 1: Render Blueprint (Recommended)

1. Push your code to a Git repository (GitHub, GitLab, etc.)
2. In your Render dashboard, click "New" and select "Blueprint"
3. Connect your Git repository
4. Render will automatically detect the `render.yaml` configuration
5. Click "Apply" to create the services defined in the configuration
6. Wait for the build and deployment to complete

### Option 2: Manual Deployment

#### Step 1: Create a PostgreSQL Database

1. In your Render dashboard, click "New" and select "PostgreSQL"
2. Configure your database:
   - Name: `gamebuzz_db`
   - Database: `gamebuzz`
   - User: `gamebuzz`
   - Plan: Free
3. Click "Create Database"
4. Note the "Internal Database URL" for the next step

#### Step 2: Create a Web Service

1. In your Render dashboard, click "New" and select "Web Service"
2. Connect your Git repository
3. Configure your web service:
   - Name: `gamebuzz`
   - Runtime: Python
   - Build Command: `./build.sh`
   - Start Command: `gunicorn event_platform.wsgi:application`
4. Add the following environment variables:
   - `DATABASE_URL`: Your PostgreSQL connection string (from Step 1)
   - `SECRET_KEY`: A secure random string (you can generate one [here](https://djecrety.ir/))
   - `DEBUG`: false
   - `ALLOWED_HOSTS`: your-app.onrender.com
   - `DJANGO_SETTINGS_MODULE`: event_platform.settings
5. Add a disk for media files:
   - Click on "Advanced" and then "Add Disk"
   - Name: `media`
   - Mount Path: `/opt/render/project/src/media`
   - Size: 1 GB
6. Click "Create Web Service"

## Post-Deployment Steps

### 1. Create a Superuser

After deployment, you'll need to create a superuser to access the admin interface:

1. In your Render dashboard, go to your web service
2. Click on "Shell"
3. Run the following command:
   ```
   python manage.py createsuperuser
   ```
4. Follow the prompts to create a superuser

### 2. Upload Initial Data

If you need to load initial data:

1. In your Render dashboard, go to your web service
2. Click on "Shell"
3. Run the following command:
   ```
   python manage.py loaddata initial_data.json
   ```

### 3. Fix Media File Permissions

If you encounter issues with media files not displaying correctly:

1. In your Render dashboard, go to your web service
2. Click on "Shell"
3. Run the following command:
   ```
   python manage.py fix_media_permissions
   ```
   This will create necessary directories and set proper permissions.

### 4. Media File Management

The application is configured to store media files on a persistent disk on Render. This ensures that uploaded images and other media files are preserved between deployments.

If you need to manually upload media files:

1. In your Render dashboard, go to your web service
2. Click on "Shell"
3. Use the following commands to create directories and upload files:
   ```
   # Create directories if they don't exist
   mkdir -p media/events_images
   mkdir -p media/events_hero_images
   mkdir -p media/organizer_logos
   
   # Set permissions
   chmod -R 755 media
   ```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check your DATABASE_URL environment variable
   - Ensure your database is running and accessible

2. **Static Files Not Loading**
   - Check that collectstatic ran successfully during build
   - Verify WhiteNoise is properly configured

3. **Media Files Not Displaying**
   - Run the `fix_media_permissions` management command
   - Check that the media directories exist and have proper permissions
   - Verify that the persistent disk is properly mounted

4. **Application Errors**
   - Check the logs in your Render dashboard
   - Set DEBUG=true temporarily to see detailed error messages

### Viewing Logs

1. In your Render dashboard, go to your web service
2. Click on "Logs" to view application logs

## Maintenance

### Updating Your Application

1. Push changes to your Git repository
2. Render will automatically rebuild and deploy your application

### Database Backups

Render automatically backs up your PostgreSQL database daily. To create a manual backup:

1. In your Render dashboard, go to your database
2. Click on "Backups"
3. Click "Create Backup"

## Security Considerations

The deployment configuration includes several security enhancements:

- HTTPS enforcement
- Secure cookies
- HTTP Strict Transport Security (HSTS)
- Secret key management via environment variables

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/en/stable/)

## Support

If you encounter issues with your deployment, check the Render documentation or contact Render support. 