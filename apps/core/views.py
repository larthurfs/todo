from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.core.conector_base import conector_base
from apps.task.models import Task
from apps.usuario.models import Profile

import plotly.express as px
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

from dash import html, dcc
from django_plotly_dash import DjangoDash



@login_required
@csrf_exempt
def home(request):
    user= request.user
    profile = Profile.objects.get(user=user)
    qtd_task= Task.objects.filter(user=user).count()
    qtd_task_afazer= Task.objects.filter(user=user, status="A Fazer").count()
    qtd_task_fazendo= Task.objects.filter(user=user, status="Fazendo").count()
    qtd_task_feito= Task.objects.filter(user=user, status="Feito").count()

    tasks = Task.objects.filter(user=user)
    df_tasks = conector_base(tasks)
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    load_figure_template('minty')
    app = DjangoDash('graf_barras', external_stylesheets=external_stylesheets)

    fig = px.bar(df_tasks, y="quantidade", x="semana", color="status", custom_data=['Atividade'], color_discrete_map={
        'Fazendo': '#ffa500',
        'A Fazer': '#3390FF',
        'Feito': 'green'
    }, category_orders={"semana": ["Passado", "0", "1", "2", "3", "4", "5", "6", "Mais do que 6 semanas"]},
                 barmode="group")

    fig.update_layout(template="minty")
    fig.update_traces(hovertemplate="%{customdata[0]}")

    app.layout = html.Div(children=[
        dcc.Graph(
            id='task-graph',
            figure=fig,
            style={"backgroundColor": "#1a2d46", "color": "#ffffff"}
        )

    ])

    context = {'profile':profile,'qtd_task':qtd_task,'qtd_task_afazer':qtd_task_afazer, 'qtd_task_fazendo':qtd_task_fazendo,'qtd_task_feito':qtd_task_feito}

    return render(request, 'index.html', context)