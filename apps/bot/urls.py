
from django.urls import path
from apps.bot.views import bot_whatsapp

urlpatterns = [
    path('bot_whatsapp/', bot_whatsapp, name="bot_whatsapp"),



]