from django.urls import path

from apps.usuario.views import profile_detail, profile_edit


urlpatterns = [
    path('', profile_detail, name='profile_detail'),
    path('profile_edit/<int:id>/', profile_edit, name='profile_edit'),

]
