from django.urls import path,include
from .views import RegisterAPI, LoginAPI, restpassapi, ChangePasswordView
from knox import views as knox_views


urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/restpassapi/', restpassapi.as_view(), name='restpassapi'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]