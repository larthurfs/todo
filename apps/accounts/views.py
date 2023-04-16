from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.accounts.forms import UserRegistrationForms
from apps.usuario.forms import RegisterFormset

@csrf_exempt
def register(request):
    if request.method == 'POST':
        user_instance = User()
        user_form = UserRegistrationForms(request.POST or None, instance=user_instance)
        user_profile_formset = RegisterFormset(request.POST or None, instance=user_instance)

        if user_form.is_valid() and user_profile_formset.is_valid():
            new_user = user_form.save(commit=False) # salvaos dados mas não envia para o banco de dados
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.username = new_user.email
            try:
                new_user.save()
                user_profile_formset.save()
            except:
                user_form = UserRegistrationForms(request.POST or None)
                user_profile_formset = RegisterFormset(request.POST or None)

                return render(request, 'registration/register.html',
                              {'user_form': user_form, 'user_profile_formset': user_profile_formset})


            return render(request, 'registration/login.html')

        else:
            return render(request, 'registration/register.html',
                          {'user_form': user_form, 'user_profile_formset': user_profile_formset})


    else:
        user_form = UserRegistrationForms(request.POST or None)
        user_profile_formset = RegisterFormset(request.POST or None)

        return render(request, 'registration/register.html',{'user_form':user_form,'user_profile_formset':user_profile_formset})