from django.urls import path

from apps.task.views import task_list, task_new,task_edit_ajax, task_edit, task_status_change_ajax,task_status_change, task_deletar, relatorio_download, task_calendario

urlpatterns = [
    path('', task_list, name='task_list'),
    path('atividade_nova/', task_new, name='task_new'),
    path('task_edit/', task_edit, name='task_edit'),
    path('task_edit_ajax/<int:pk>', task_edit_ajax, name='task_edit_ajax'),
    path('task_status_change_ajax/<int:pk>', task_status_change_ajax, name='task_status_change_ajax'),
    path('task_status_change/', task_status_change, name='task_status_change'),
    path('task_deletar/', task_deletar, name='task_deletar'),
    path('relatorio_download/', relatorio_download, name='relatorio_download'),
    path('task_calendario/', task_calendario, name='task_calendario'),

]
