from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.shop_view, name='blog'),
    path('<int:id>/', views.detail_view, name='detail'),
    path('contact/', views.contact, name="contact"),
    path('<int:id>/contact/', views.contact, name="contact"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
