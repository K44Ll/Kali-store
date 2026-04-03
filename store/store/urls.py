
from django.contrib import admin
from django.urls import path
from APP_SITE_LOJA.views import home, login, register, sair


urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', home, name='home'),
    path('accounts/login/', login, name='login'),
    path('accounts/register/', register, name='register'),
    path('accounts/logout', sair, name='logout'),
]