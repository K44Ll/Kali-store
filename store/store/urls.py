
from django.contrib import admin
from django.urls import path
from APP_SITE_LOJA.views import home, login_view, register, sair, confirmar_email


urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', home, name='home'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/register/', register, name='register'),
    path('accounts/logout', sair, name='logout'),
    path('confirmar/<uidb64>/<token>/', confirmar_email, name='confirmar_email'),
]