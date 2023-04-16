from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from apps.usuario.models import Profile


class UserProfileRegistrationForm(forms.ModelForm):
    nome = forms.CharField()
    data_aniversario = forms.DateField(
        label='Data de Aniversário',
        widget=forms.DateInput(format='y%-%m-%d', attrs={'type':'date', 'class':'form-control'})
    )
    whatsapp = forms.CharField()
    nome.widget.attrs.update({'class':'form-control'})
    whatsapp.widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Profile
        fields = ('nome', 'data_aniversario', 'whatsapp')





RegisterFormset = inlineformset_factory(
    User,
    Profile,
    form = UserProfileRegistrationForm,
    extra = 0,
    can_delete=False,
    min_num= 1,
    validate_min=True,

)



class UserProfileEditForm(forms.ModelForm):
    data_aniversario = forms.DateField(
        label='Data Aniversário',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    class Meta:
         model = Profile
         fields = ('user_foto', 'data_aniversario', 'whatsapp')
