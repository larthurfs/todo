from django import forms
from django.contrib.auth.models import User


class UserRegistrationForms(forms.ModelForm): #ModelForm cria um formulário por uma tabela
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password.widget.attrs.update({'class':'form-control'})
    password2.widget.attrs.update({'class':'form-control'})
    email = forms.EmailField()
    email.widget.attrs.update({'class':'form-control'})

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('O Password salvo estão diferentes')
        return cd['password2']
    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email já cadastrado no sistema')
        return email