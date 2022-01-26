# -*- coding: utf-8 -*-
from django.urls import path, include
from ai_club import views
from django.conf.urls.static import static
from django.conf import settings
from ai_club.views import (
    MyChunkedUploadView, 
    MyChunkedUploadCompleteView,
    homeView,
    mousCreateView,
    mousUpdate,
    mouView,
)

urlpatterns = [
    path('home/', homeView.as_view(), name = 'home'),
    path('mous/<int:mou_id>', mouView.as_view(), name = 'mou'),
    path('upload/mous/<int:mou_id>/', mousCreateView.as_view(), name='upload_file_page'),
    path('api/chunked_upload_complete/', MyChunkedUploadCompleteView.as_view(), name='api_chunked_upload_complete'),
    path('api/chunked_upload/', MyChunkedUploadView.as_view(), name='api_chunked_upload'),
    path('api/mous/<int:mou_id>/update/', mousUpdate.as_view(), name='api_mou_update'),
    path('api/stream_video/<path:video_path>', views.stream_video, name = 'api_stream_video'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)