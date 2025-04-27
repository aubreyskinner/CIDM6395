from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CNAViewSet, ClientProfileViewSet
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'cnas', CNAViewSet)
router.register(r'clients', ClientProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cna-list/', views.cna_list, name='cna_list'),
    path('contact-cna/<int:cna_id>/', views.contact_cna, name='contact_cna'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
