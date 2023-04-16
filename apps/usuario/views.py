from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from apps.usuario.forms import UserProfileEditForm
from apps.usuario.models import Profile


# Create your views here.

@csrf_exempt
@login_required
def profile_detail(request):
    id = request.user.id
    usuario = User.objects.get(id=id)
    profile = Profile.objects.get(user=usuario)
    form = UserProfileEditForm(request.POST or None, instance=profile)

    return render(request, 'profile.html', {'usuario':usuario, 'profile':profile, 'form':form})


@csrf_exempt
@login_required
def profile_edit(request, id):
    usuario = User.objects.get(id=id)
    profile = Profile.objects.get(user=usuario)
    form = UserProfileEditForm(request.POST or None, instance=profile)

    if request.method == 'POST':
        user_foto = request.FILES.get('user_foto')
        if form.is_valid():
            if user_foto != None:
                profile_user = form.save(commit=False)
                profile_user.user_foto = user_foto
                profile_user.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

