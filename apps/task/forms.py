from django import forms
from django.core.exceptions import ValidationError

from apps.task.models import Task



class TaskFormAdd(forms.ModelForm):
    task_name = forms.CharField(label='Nome da Atividade', widget=forms.TextInput(attrs={"placeholder":"Atividade"}))
    data_inicio = forms.DateField(
        label='Data Início',
        widget=forms.DateInput(format='y%-%m-%d', attrs={'type':'date', 'class':'form-control'})
    )
    data_fim = forms.DateField(
        label='Data Fim',
        widget=forms.DateInput(format='y%-%m-%d', attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ('task_name', 'descricao', 'data_inicio', 'data_fim')

    def clean(self):
        self.cleaned_data = super().clean()

        if self.cleaned_data.get("data_inicio") > self.cleaned_data.get("data_fim"):
            raise ValidationError("A data início não pode ser maior do que a data fim ")
        return self.cleaned_data


class TaskStatusChange(forms.ModelForm):
    data_fim_real = forms.DateField(
        label='Data Fim Real',
        required=False,
        widget=forms.DateInput(format='y%-%m-%d', attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ('status', 'data_fim_real')
