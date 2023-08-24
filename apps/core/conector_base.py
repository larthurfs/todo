import pandas as pd
from datetime import datetime


def semana(data_inicio):
    dict = {'Date': [datetime.today(), data_inicio]}
    df = pd.DataFrame.from_dict(dict)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df.astype('int64').dtypes

    weekNumber = df['Date'].dt.week
    if weekNumber[1] - weekNumber[0] + (int(str(data_inicio)[:4]) - int(str(datetime.today())[:4])) * 52 < 0:
        semana = "Passado"
    elif weekNumber[1] - weekNumber[0] + (int(str(data_inicio)[:4]) - int(str(datetime.today())[:4])) * 52 > 6:
        semana = "Mais do que 6 semanas"

    else:
        semana = weekNumber[1] - weekNumber[0] + (int(str(data_inicio)[:4]) - int(str(datetime.today())[:4])) * 52

    return str(semana)


def conector_base(tasks):
    df_tasks = pd.DataFrame(columns=['semana', 'status', 'Atividade', 'quantidade'])

    for task in tasks:
        df_tasks.loc[len(df_tasks)] = [semana(task.data_inicio), task.status, task.task_name, 1]

    return df_tasks
