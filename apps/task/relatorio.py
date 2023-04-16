import xlsxwriter as xls
import xlsxwriter.utility as xl_util


def criar_planilha(output, tasks, profile, d_inicio, d_fim):
    wb = xls.Workbook(output)

    relatorio = wb.add_worksheet("Relatório")
    tabelas = wb.add_worksheet("Tabelas")

    planilha_relatorio(relatorio, wb, tasks, profile, d_inicio, d_fim)
    planilha_tabelas(tabelas, wb)

    wb.close()


def planilha_relatorio(relatorio, wb, tasks, profile, d_inicio, d_fim):

    relatorio.set_column('A:A', 0.83)
    relatorio.set_column('B:B', 0.67)
    relatorio.set_column('C:C', 10.00)
    relatorio.set_column('D:D', 25.00)
    relatorio.set_column('E:E', 38.14)
    relatorio.set_column('F:F', 9.86)
    relatorio.set_column('G:G', 9.86)
    relatorio.set_column('H:H', 9.86)
    relatorio.set_column('I:I', 9.86)
    relatorio.set_column('J:J', 11.71)

    relatorio.set_row(5, 18.0)
    relatorio.set_row(6, 18.0)
    relatorio.hide_gridlines(2)

    relatorio.add_table(xl_util.xl_range_abs(10, 3, 10, 5),
                        {'name': 'tarefas', 'style': None, 'columns': [{'header': 'Nome'},
                                                                       {'header': 'Descrição'},
                                                                       {'header': 'Data Início'},
                                                                       {'header': 'Data Fim'},
                                                                       {'header': 'Status'},
                                                                       ]})

    relatorio.write_row(8, 3, ['Nome', 'Descrição', 'Data Início', 'Data Fim', 'Status'],
                        wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '11'}))

    row_num = 10

    for task in tasks:
        if row_num % 2 == 0:
            relatorio.write(row_num, 3, task.task_name)
            relatorio.write(row_num, 4, task.descricao)
            relatorio.write(row_num, 5, task.data_inicio, wb.add_format({'num_format': 'dd/mmm/yy'}))
            relatorio.write(row_num, 6, task.data_fim, wb.add_format({'num_format': 'dd/mmm/yy'}))
            relatorio.write(row_num, 7, task.status)
        else:
            relatorio.write(row_num, 3, task.task_name, wb.add_format({'bg_color': '#bfbfbf'}))
            relatorio.write(row_num, 4, task.descricao, wb.add_format({'bg_color': '#bfbfbf'}))
            relatorio.write(row_num, 5, task.data_inicio,
                            wb.add_format({'bg_color': '#bfbfbf', 'num_format': 'dd/mmm/yy'}))
            relatorio.write(row_num, 6, task.data_fim,
                            wb.add_format({'bg_color': '#bfbfbf', 'num_format': 'dd/mmm/yy'}))
            relatorio.write(row_num, 7, task.status, wb.add_format({'bg_color': '#bfbfbf'}))

        row_num += 1

    # Formatação
    condicional_Feito = wb.add_format({'bold': True, 'font_color': 'green'})
    condicional_Fazendo = wb.add_format({'bold': True, 'font_color': 'orange'})
    condicional_Afazer = wb.add_format({'bold': True, 'font_color': 'gray'})

    # Regras da Formatação condicional
    relatorio.conditional_format('H1:H1048576', {'type': 'text', 'criteria': 'containing', 'value': "Feito",
                                                 'format': condicional_Feito})
    relatorio.conditional_format('H1:H1048576',
                                 {'type': 'text', 'criteria': 'containing', 'value': "Fazendo",
                                  'format': condicional_Fazendo})
    relatorio.conditional_format('H1:H1048576', {'type': 'text', 'criteria': 'containing', 'value': "A Fazer",
                                                 'format': condicional_Afazer})



    relatorio.merge_range(1, 1, 1, 10, "MODELO RELATÓRIO",wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '22'}))

    relatorio.merge_range(2, 1, 2, 10, 'Atividades da Semana', wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '16'}))



    relatorio.write(5, 2, "Nome:",
                    wb.add_format(
                        {'bold': True, 'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 2,
                         'top': 2, 'bottom': 1, 'right': 1, 'bottom_color': 'gray', 'right_color': 'white',
                         'top_color': 'gray', 'left_color': 'gray'}))

    relatorio.merge_range(5, 3, 5, 4, profile.nome,
                          wb.add_format(
                              {'bold': True, 'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11',
                               'left': 1,
                               'top': 2, 'bottom': 1, 'right': 1, 'bottom_color': 'gray', 'right_color': 'white',
                               'top_color': 'gray', 'left_color': 'white'}))

    relatorio.write(5, 5, "Data Início:", wb.add_format(
        {'bold': True, 'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
         'top': 2, 'bottom': 1, 'right': 1, 'bottom_color': 'gray', 'right_color': 'white',
         'top_color': 'gray', 'left_color': 'white'}))

    relatorio.write(5, 6, d_inicio
                    , wb.add_format(
            {'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
             'top': 2, 'bottom': 1, 'right': 1, 'bottom_color': 'gray', 'right_color': 'white',
             'top_color': 'gray', 'left_color': 'white', 'align': 'center', 'valign': 'vcenter',
             'num_format': 'dd/mmm/yy'}))

    relatorio.write(5, 7, "Data Fim:",
                    wb.add_format(
                        {'bold': True, 'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
                         'top': 2, 'bottom': 1, 'right': 1, 'bottom_color': 'gray', 'right_color': 'white',
                         'top_color': 'gray', 'left_color': 'white'}))

    relatorio.merge_range(5, 8, 5, 9,
                          d_fim,
                          wb.add_format(
                              {'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
                               'top': 2, 'bottom': 1, 'right': 2, 'bottom_color': 'gray', 'right_color': 'gray',
                               'top_color': 'gray', 'left_color': 'white', 'align': 'center', 'valign': 'vcenter',
                               'num_format': 'dd/mmm/yy'}))

    graf_colunas = wb.add_chart({'type': 'column'})
    graf_colunas.set_legend({'position': 'bottom'})
    graf_colunas.set_x_axis({'text_axis': True, 'date_axis': False})

    graf_colunas.set_chartarea({
        'border': {'none': True},
        'fill': {'none': True}
    })

    graf_colunas.add_series({
        'categories': 'Quantidade total de atividades',
        'values': '=Tabelas!$B$3',
        'fill': {'color': 'green', 'border': {'color': 'white'}},
        'name': 'Quantidade total de atividades'
    })

    graf_colunas.add_series({
        'categories': 'Atividades Concluídas',
        'values': '=Tabelas!$C$3',

        'fill': {'color': 'orange', 'border': {'color': 'white'}},
        'name': 'Atividades Concluídas'
    })

    relatorio.insert_chart('$M$8', graf_colunas, {'x_scale': 0.80, 'y_scale': 1, 'x_offset': 40})






def planilha_tabelas(tabelas, wb):
    tabelas.hide_gridlines(2)

    tabelas.write_row(1, 1, ['Quantidade total de atividades', 'Atividades Concluídas', 'Avanço'],
                      wb.add_format({'bg_color': '#d9d9d9', 'font_color': 'white', 'bold': True, 'align': 'center',
                                     'valign': 'vcenter', 'font_size': '11'}))
    tabelas.write_row(2, 1, ['=COUNTA(Relatório!H:H)-2', '=COUNTIFS(Relatório!H:H,"Feito")', '=C3/B3'],
                      wb.add_format({'bg_color': '#d9d9d9', 'font_color': 'white', 'bold': True, 'align': 'center',
                                     'valign': 'vcenter', 'font_size': '11'}))

    tabelas.set_column('A:A', 3.14)
    tabelas.set_column('B:B', 28.14)
    tabelas.set_column('C:C', 19.86)
    tabelas.set_column('D:D', 8.43)
    tabelas.hide()


