from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

admin.site.site_header = 'Storefront Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    re_path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('summernote/', include('django_summernote.urls')),
    path('quizapp/', include('Quizapp2.urls')),
    path('', include('Activate.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)