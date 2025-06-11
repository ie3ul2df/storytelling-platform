from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from stories.views import register_view

# ------------------ Project URL config: admin, auth, and story app routes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', register_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/Logout
    path('', include('stories.urls')),  # app homepage and story-related URLs
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)