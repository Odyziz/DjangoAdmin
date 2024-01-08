from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.glowna, name='glowna'),
    path('logowanie/', views.logowanie, name='logowanie'),
    path('wylogowanie/', views.wylogowanie, name='wylogowanie'),
    path('klienci/', include('klienci.urls')),
    path('zarzadzanie/', include('zarzadzanie.urls')),
    path('montaze/', include('montaze.urls')),
    path('finanse/', include('finanse.urls')),
    path('helpdesk/', include('helpdesk.urls')),
] 


if settings.DEBUG:
    urlpatterns= urlpatterns + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    urlpatterns= urlpatterns + static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
