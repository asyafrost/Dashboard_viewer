from libraries import dcc, html, dbc, daq, px
import graph

list_of_features = ['activityIndex','averageActivityIndex','lowActivity','normalActivity','highActivity','chicks','chickSize','spaceUniformityIndex','occupationDensity','illumination','feedersHeight','huddlingIndex','huddlingTime', 'people']

def create_dropdown(id_name, options, multi=True):
    return dcc.Dropdown(
        id=id_name,
        options=options,
        value=[opt['value'] for opt in options],
        multi=multi,
        style={
            'backgroundColor': '#f8f9fa',  
            'color': '#495057', 
            'border': '1px solid #ced4da', 
        }
    )

def create_range_slider(id_name, df_column):
    return dcc.RangeSlider(
        id=id_name,
        min=df_column.min(),
        max=df_column.max(),
        marks={i: {'label': str(i), 'style': {'color': 'white'}} for i in range(int(df_column.min()), int(df_column.max()) + 1, 5)},
        step=1,
        value=[df_column.min(), df_column.max()]
    )

def create_boolean_switcher(id_name):
     return daq.BooleanSwitch(
            id=id_name,
            on=False,
            labelPosition="top"
        )

def create_scatter(chart_data, column, title, trend, pipe, color_map):
        fig = graph.plot_scatter(chart_data, 'age', column, 'cycleId', trend, pipe, color_map)
        return [html.Div(f'{title} ~ Age', style={'text-align': 'center'}),
                dcc.Graph(figure=fig)]

def create_line(chart_data, column, title, trend, color_map):
        fig = graph.plot_line(chart_data, 'age', column, 'cycle', color_map)
        return [html.Div(f'{title} ~ Age', style={'text-align': 'center'}),
                dcc.Graph(figure=fig)]

def create_density(chart_data, column):
        fig = graph.plot_density(chart_data, column)
        return [html.Div(f'{column} ~ Age', style={'text-align': 'center'}),
                dcc.Graph(figure=fig)]


def create_tab_content(df_columns, chart_ids):
    rows = []
    for i in range(0, len(df_columns), 2):
        row = dbc.Row([
            dbc.Col(html.Div(id=chart_ids[i]), width=6),
            dbc.Col(html.Div(id=chart_ids[i+1]), width=6)
        ], style={'margin-bottom': 20})
        rows.append(row)
    return rows

def create_static_box_plot(data, column_name):
    fig = px.box(data, x='cycle', y=column_name)
    return fig
