import io
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.task.forms import TaskFormAdd, TaskStatusChange
from apps.task.models import Task
from datetime import timedelta, date
import json
from apps.task.relatorio import criar_planilha
from apps.usuario.models import Profile
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@csrf_exempt
@login_required
def task_list(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    tasks = Task.objects.filter(user=user)
    paginator = Paginator(tasks, 4)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    try:
        tasks_page = paginator.page(page)
    except PageNotAnInteger:
        tasks_page = paginator.page(1)
    except EmptyPage:
        tasks_page = paginator.page(paginator.num_pages)



    form_task = TaskFormAdd(request.POST or None)
    form_change = TaskStatusChange(request.POST or None)

    return render(request, 'task_list.html', {'profile':profile, 'tasks_page':tasks_page,'page_obj':page_obj ,'form_task':form_task, "form_change":form_change})

@csrf_exempt
@login_required
def task_new(request):
    form_task = TaskFormAdd(request.POST or None)
    user = request.user

    if request.method == "POST":
        if form_task.is_valid():
            task = form_task.save(commit=False)
            task.user = user
            task.status = "A Fazer"
            task.save()

        else:
            user = request.user
            profile = Profile.objects.get(user=user)
            tasks = Task.objects.filter(user=user)
            messages.error(request, form_task.errors['__all__'])

            return render(request, 'task_list.html', {'profile': profile, 'tasks': tasks, 'form_task':form_task})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@csrf_exempt
@login_required
def task_edit_ajax(request, pk):
    task = Task.objects.get(id=pk)

    data = {
        'nome':task.task_name,
        'descricao':task.descricao,
        'di':task.data_inicio,
        'df':task.data_fim,
    }
    return JsonResponse(data)
@csrf_exempt
@login_required
def task_edit(request):
    user = request.user
    id = request.POST.get("task_id")
    task = Task.objects.get(id=id)

    if task.user != user:
        profile = Profile.objects.get(user=user)
        tasks = Task.objects.filter(user=user)
        messages.error(request, "Você não pode essa atividade")
        form_task = TaskFormAdd(request.POST or None)
        form_change = TaskStatusChange(request.POST or None)

        return render(request, 'task_list.html', {'profile': profile, 'tasks': tasks, 'form_task': form_task, "form_change":form_change})

    form_task = TaskFormAdd(request.POST or None, instance = task)
    if request.method == "POST":
        if form_task.is_valid():
            form_task.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@csrf_exempt
@login_required
def task_status_change_ajax(request, pk):
    task = Task.objects.get(id=pk)

    data = {
        'status':task.status,
        'dfr':task.data_fim_real,

    }
    return JsonResponse(data)
@csrf_exempt
@login_required
def task_status_change(request):
    id = request.POST.get("task_id_change")
    task = Task.objects.get(id=id)
    user = request.user

    if task.user != user:
        profile = Profile.objects.get(user=user)
        tasks = Task.objects.filter(user=user)
        messages.error(request, "Você não pode editar essa atividade")
        form_task = TaskFormAdd(request.POST or None)
        form_change = TaskStatusChange(request.POST or None)
        return render(request, 'task_list.html',
                      {'profile': profile, 'tasks': tasks, 'form_task': form_task, "form_change": form_change})
    if request.method == "POST":
        form_change = TaskStatusChange(request.POST or None, instance=task)
        if form_change.is_valid():
            form_change.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            profile = Profile.objects.get(user=user)
            tasks = Task.objects.filter(user=user)
            messages.error(request, "Formulário Invaldo")
            form_task = TaskFormAdd(request.POST or None)
            form_change = TaskStatusChange(request.POST or None)
            return render(request, 'task_list.html',
                          {'profile': profile, 'tasks': tasks, 'form_task': form_task, "form_change": form_change})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@csrf_exempt
@login_required
def task_deletar(request):
    id = request.POST.get("task_id_delet")
    task = Task.objects.get(id=id)
    task.delete()
    messages.success(request, "Atividade excluida com sucesso")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
@login_required
def relatorio_download(request):
    d_inicio = date.today() - timedelta(days=date.today().weekday())
    d_fim = date.today() + timedelta(days=6 - date.today().weekday())

    user = request.user
    profile = Profile.objects.get(user=user)
    tasks = Task.objects.filter(user=user , data_inicio__range=(d_inicio, d_fim))

    output = io.BytesIO()

    criar_planilha(output, tasks, profile, d_inicio, d_fim)

    output.seek(0)

    filename = 'atividade_semana.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


def cor(status):
    colors = {'A Fazer': '#3390FF', 'Fazendo': '#f2ab11',  'Feito': '#008000'}
    return colors[status]

def task_calendario(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    tasks = Task.objects.filter(user=user)
    form_task = TaskFormAdd(request.POST or None)

    tasks_jason =[]
    for task in tasks:
        tasks_jason.append({'title': task.task_name,
                            'start':task.data_inicio.strftime('%Y-%m-%dT%H:%M:%S'),
                            'end':task.data_fim.strftime('%Y-%m-%dT%H:%M:%S'),
                            'borderColor': cor(task.status),
                            'backgroundColor': cor(task.status),
                            'allDay': True,
                            'id': task.id,
                            })

    eventos_json = json.dumps(tasks_jason)

    return render(request, 'task_calendario.html', {'form_task':form_task, 'profile':profile,'eventos_json':eventos_json})


