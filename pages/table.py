from libraries import dbc, dash_table

column_colors = ['#FFDDC1', '#FFABAB', '#FFC3A0', '#FF677D', '#D4A5A5', '#39FA5A', '#31A2AC']

def create_table(df):
    table_content = [dbc.Container([
        dbc.Label('Click a cell in the table:'),

        # Таблица данных
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            id='tbl',
            style_table={'overflowX': 'auto', 'color': 'black'},
            
            
            style_data_conditional=[
                {
                    'if': {'column_id': df.columns[i]},
                    'backgroundColor': column_colors[i % len(column_colors)],
                    'color': 'black'
                } for i in range(len(df.columns))
            ] + [
                # Выделение активной ячейки
                {
                    'if': {'state': 'active'},
                    'backgroundColor': '#FFD700', 
                    'border': '3px solid #FF4500' 
                }
            ],
            
            style_cell={
                'textAlign': 'left',
                'padding': '4px',
            },
        ),
        
        dbc.Alert(id='tbl_out', color='info')
    ])]
    return table_content