from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CNAViewSet, ClientProfileViewSet
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'cnas', CNAViewSet)
router.register(r'clients', ClientProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cna-list/', views.cna_list, name='cna_list'),
    path('contact-cna/<int:cna_id>/', views.contact_cna, name='contact_cna'),
    path('success/', views.success, name='success'),
    path('notifications/', views.notification_page, name='notifications'),
    path('api/unread-notifications/', views.unread_notification_count, name='unread_notification_count'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
