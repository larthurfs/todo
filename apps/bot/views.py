import time
import re
from django.shortcuts import render
from django.http import HttpResponse
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from apps.task.models import Task
from apps.usuario.models import Profile
from datetime import timedelta, date, datetime

# Your Account SID from twilio.com/console
account_sid = "AC9d1cd5a1a166c27d2aada06ba0ee817b"
# Your Auth Token from twilio.com/console
auth_token  = "2354bb7bdba9425989d98d05972ac4f6"

client = Client(account_sid, auth_token)

@csrf_exempt
def bot_whatsapp(request):
    message = request.POST["Body"]
    SENDER_NUMBER = request.POST["From"]
    whatsapp_number = SENDER_NUMBER[12:14] + "9" + SENDER_NUMBER[14:]
    TWILIO_NUMBER = "whatsapp:+14155238886"


    try:
        profile = Profile.objects.get(whatsapp=whatsapp_number)
    except:
        client.messages.create(
            from_=TWILIO_NUMBER,
            body="Não encontramos o seu número cadastrado no sistema! Certifique-se de que você salvou o número certo, ou crie uma conta em www.neurondat.com",
            to=SENDER_NUMBER,
        )

        return HttpResponse("olá")

    d_inicio = date.today() - timedelta(days=date.today().weekday())
    d_fim = date.today() + timedelta(days=6 - date.today().weekday())
    user = profile.user

    tasks = Task.objects.filter(user=user, data_inicio__range=(d_inicio, d_fim))



    if message == "1":
        if tasks.count() == 0:
            body = render_to_string("bot_sematividades.txt")
            client.messages.create(
                from_=TWILIO_NUMBER,
                body=body,
                to=SENDER_NUMBER,
            )
        else:

            body = render_to_string("bot_saudacoes.txt", {'profile':profile})
            client.messages.create(
                from_=TWILIO_NUMBER,
                body=body,
                to=SENDER_NUMBER,
            )

            for atividade in tasks:
                task = {'task_name': atividade.task_name, 'descricao': atividade.descricao,
                        'data_inicio': atividade.data_inicio, 'data_fim': atividade.data_fim,
                        'status': atividade.status}
                context = {'task':task}

                body = render_to_string("bot_atividades.txt", context)
                client.messages.create(
                    from_=TWILIO_NUMBER,
                    body=body,
                    to=SENDER_NUMBER,
                )

        body = render_to_string("bot_loop.txt")
        client.messages.create(
            from_=TWILIO_NUMBER,
            body=body,
            to=SENDER_NUMBER,
        )



    elif message == "2":
        body = render_to_string("bot_create_instrucao.txt")
        client.messages.create(
            from_=TWILIO_NUMBER,
            body=body,
            to=SENDER_NUMBER,
        )

        time.sleep(1)

        body = render_to_string("bot_create.txt")
        client.messages.create(
            from_=TWILIO_NUMBER,
            body=body,
            to=SENDER_NUMBER,
        )

        time.sleep(1)

        body = render_to_string("bot_loop.txt")
        client.messages.create(
            from_=TWILIO_NUMBER,
            body=body,
            to=SENDER_NUMBER,
        )

    elif message == "3":
        body = render_to_string("bot_despedida.txt", {'profile':profile})
        client.messages.create(
            from_=TWILIO_NUMBER,
            body=body,
            to=SENDER_NUMBER,
        )

    elif "Criar atividade" in message:
        try:
            bot_cria_tarefa(message, user)
        except:
            body = render_to_string("bot_erro_atividade.txt")
            client.messages.create(
                from_=TWILIO_NUMBER,
                body=body,
                to=SENDER_NUMBER,
            )

            time.sleep(1)

            body = render_to_string("bot_loop.txt")
            client.messages.create(
                from_=TWILIO_NUMBER,
                body=body,
                to=SENDER_NUMBER,
            )

        else:
            body = render_to_string("bot_sucesso_atividade.txt")
            client.messages.create(
                from_=TWILIO_NUMBER,
                body=body,
                to=SENDER_NUMBER,
            )
            time.sleep(1)

            body = render_to_string("bot_loop.txt")
            client.messages.create(
                from_=TWILIO_NUMBER,
                body=body,
                to=SENDER_NUMBER,
            )


    else:
        body = render_to_string("bot_comandos.txt", {'profile':profile})
        client.messages.create(
            from_=TWILIO_NUMBER,
            body=body,
            to=SENDER_NUMBER,
        )

    return HttpResponse("olá")



def bot_cria_tarefa(message, user):

    nome = re.search(r'Nome:(.*?)\n', message)
    nome = nome.group(0).replace('Nome:', '').replace('\n', '').strip()

    descricao = re.search(r'Descrição:(.*?)\n', message)
    descricao = descricao.group(0).replace('Descrição:', '').replace('\n', '').strip()

    format_str = '%d/%m/%Y'
    d_inicio = re.search(r'Data Início:(.*?)\n', message)
    d_inicio= datetime.strptime(d_inicio.group(0).replace('Data Início:', '').replace('\n', '').strip(),format_str)

    d_fim = re.search(r'Data Fim:(.*)', message)
    d_fim = datetime.strptime(d_fim.group(0).replace('Data Fim:', '').strip(), format_str)


    atividade = Task.objects.create(
        user=user,
        task_name=nome,
        descricao=descricao,
        data_inicio=d_inicio,
        data_fim=d_fim,
        status="A Fazer",
    )