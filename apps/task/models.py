from django.contrib.auth.models import User
from django.db import models
from django.conf import settings



class Task(models.Model):
    STATUS = (
        ('A Fazer', 'A Fazer'),
        ('Fazendo', 'Fazendo'),
        ('Feito', 'Feito'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name= models.CharField(max_length=100)
    descricao= models.TextField()
    data_inicio= models.DateField()
    data_fim= models.DateField()
    data_fim_real= models.DateField(blank=True, null=True)
    status= models.CharField(max_length=20, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'db_task'
        verbose_name = 'BD Task'
        verbose_name_plural = 'BD Task'


    def __str__(self):
        return self.task_name
