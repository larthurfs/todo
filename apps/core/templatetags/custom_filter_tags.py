from django import template
import pandas as pd
from datetime import datetime

register = template.Library()

@register.filter
def semana_atividade(data_inicio):
    dict = {'Date': [datetime.today(), data_inicio]}
    df = pd.DataFrame.from_dict(dict)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df.astype('int64').dtypes

    weekNumber = df['Date'].dt.week

    return weekNumber[1] - weekNumber[0] + (int(str(data_inicio)[:4]) - int(str(datetime.today())[:4])) * 52