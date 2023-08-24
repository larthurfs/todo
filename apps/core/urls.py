from django.urls import path, include

from apps.core.views import home

urlpatterns = [
    path('', home, name='home'),
    path('dash/', include('django_plotly_dash.urls')),
]
