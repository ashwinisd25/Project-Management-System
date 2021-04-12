from django.contrib import admin
from django.urls import path, include
from projectapp.views import home,client
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('client/', client, name='client'),
    path('project/', include('projectapp.urls')),

    path('api/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
