from libraries import dbc, html, dcc
import components

def create_cycle_charts(data):
    # Создание нового столбца 'cycle'

    cycle_chart_content = [
        dbc.Row([
            dbc.Col(html.Div(id='chicks_cycle_age_chart'), width=6),
            dbc.Col([html.Div('Chicks by Cycle', style={'text-align': 'center'}), dcc.Graph(figure=components.create_static_box_plot(data, 'chicks'))], width=6)
        ], style={'margin-bottom': 20}),
        
        dbc.Row([
            dbc.Col(html.Div(id='chickSize_cycle_age_chart'), width=6),
            dbc.Col([html.Div('Chick Size by Cycle', style={'text-align': 'center'}), dcc.Graph(figure=components.create_static_box_plot(data, 'chickSize'))], width=6)
        ], style={'margin-bottom': 20}),
        
        dbc.Row([
            dbc.Col(html.Div(id='sui_cycle_age_chart'), width=6),
            dbc.Col([html.Div('Space Uniformity Index by Cycle', style={'text-align': 'center'}), dcc.Graph(figure=components.create_static_box_plot(data, 'spaceUniformityIndex'))], width=6) 
        ], style={'margin-bottom': 20}),
        
        dbc.Row([
            dbc.Col(html.Div(id='od_cycle_age_chart'), width=6),
            dbc.Col([html.Div('Occupation Density by Cycle', style={'text-align': 'center'}), dcc.Graph(figure=components.create_static_box_plot(data, 'occupationDensity'))], width=6)
        ], style={'margin-bottom': 20}),
        
        dbc.Row([
            dbc.Col(html.Div(id='activityIndex_cycle_age_chart'), width=6),
            dbc.Col([html.Div('Activity Index by Cycle', style={'text-align': 'center'}), dcc.Graph(figure=components.create_static_box_plot(data, 'activityIndex'))], width=6)
        ], style={'margin-bottom': 20}),
        
        dbc.Row([
            dbc.Col(html.Div(id='avgActivityIndex_cycle_age_chart'), width=6),
            dbc.Col([html.Div('Average Activity Index by Cycle', style={'text-align': 'center'}), dcc.Graph(figure=components.create_static_box_plot(data, 'averageActivityIndex'))], width=6) 
        ], style={'margin-bottom': 20}),
        
        dbc.Row([
            dbc.Col(html.Div(id='actLevels_cycle_age_chart'), width=8),
            dbc.Col(html.Div(id='actLevels_cycle_age_pie'), width=4)
        ], style={'margin-bottom': 20}),
        
        dbc.Row([
            dbc.Col(html.Div(id='illumination_cycle_age_chart'), width=6),
            dbc.Col([html.Div('Illumination by Cycle', style={'text-align': 'center'}), dcc.Graph(figure=components.create_static_box_plot(data, 'illumination'))], width=6)  
        ], style={'margin-bottom': 20}),
    ]

    return cycle_chart_content
