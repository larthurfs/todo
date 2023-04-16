from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    data_aniversario = models.DateField()
    user_foto = models.ImageField(blank=True, null=True)
    whatsapp = models.CharField(max_length=11)

    class Meta:
        db_table = 'db_profile'
        verbose_name = 'BD Profile'
        verbose_name_plural = 'BD Profile'


    def __str__(self):
        return self.nome
