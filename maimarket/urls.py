from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from maimarket import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('users/', include('users.urls', namespace="users")),
    path('goods/', include('goods.urls', namespace="goods")),
    path('favorites/', include('favorites.urls', namespace="favorites"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)