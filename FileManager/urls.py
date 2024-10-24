from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from files.views import file_list, upload_file, download_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', file_list, name='file_list'),
    path('upload/', upload_file, name='upload_file'),
    path('download/<str:file_name>/', download_file, name='download_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)