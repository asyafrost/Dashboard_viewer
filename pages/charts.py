from libraries import dbc, html

chart_content = [
    dbc.Row([
        dbc.Col(html.Div(id='chicks_age_chart'), width=6),
        dbc.Col(html.Div(id='chicks_density_chart'), width=6)
    ], style={'margin-bottom': 20}),
    
    dbc.Row([
        dbc.Col(html.Div(id='chickSize_age_chart'), width=6),
        dbc.Col(html.Div(id='chickSize_density_chart'), width=6)
    ], style={'margin-bottom': 20}),
    
    dbc.Row([
        dbc.Col(html.Div(id='sui_age_chart'), width=6),
        dbc.Col(html.Div(id='sui_density_chart'), width=6)
    ], style={'margin-bottom': 20}),
    
    dbc.Row([
        dbc.Col(html.Div(id='od_age_chart'), width=6),
        dbc.Col(html.Div(id='od_density_chart'), width=6)
    ], style={'margin-bottom': 20}),
    
    dbc.Row([
        dbc.Col(html.Div(id='activityIndex_age_chart'), width=6),
        dbc.Col(html.Div(id='activityIndex_density_chart'), width=6)
    ], style={'margin-bottom': 20}),
    
    dbc.Row([
        dbc.Col(html.Div(id='avgActivityIndex_age_chart'), width=6),
        dbc.Col(html.Div(id='avgActivityIndex_density_chart'), width=6)
    ], style={'margin-bottom': 20}),
    
    dbc.Row([
        dbc.Col(html.Div(id='actLevels_age_chart'), width=8),
        dbc.Col(html.Div(id='actLevels_age_pie'), width=4)
    ], style={'margin-bottom': 20}),
    
    dbc.Row([
        dbc.Col(html.Div(id='illumination_age_chart'), width=6),
        dbc.Col(html.Div(id='illumination_density_chart'), width=6)
    ], style={'margin-bottom': 20}),
    
    dbc.Row([
        dbc.Col(html.Div(id='huddlingIndex_chart'), width=6),
        dbc.Col(html.Div(id='huddlingTime_bar'), width=6)
    ], style={'margin-bottom': 20}),
    
    dbc.Row([
        dbc.Col(html.Div(id='feeders_height_age_chart'), width=6),
        dbc.Col(html.Div(id='feeders_height_density_chart'), width=6)
    ], style={'margin-bottom': 20})
]
