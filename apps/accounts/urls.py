from django.urls import path, include

from apps.accounts.views import register

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),

]