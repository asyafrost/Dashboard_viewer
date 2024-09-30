from libraries import dbc, dcc, html


def create_layout(camera_type_selector, client_selector, cycle_selector, cycleId_selector, deviceId_selector, age_selector, trend_switcher, pipe_switcher, chart_content, cycle_chart_content, table_content, metrics_content):
    layout = html.Div([ 
    #header
    dbc.Row(
        dbc.Col(
            html.H1(
                'Dashboard'
            , style={'text-align': 'center'}),
            width=12
        ),
        style={'margin-bottom': 20, 'margin-top': 20}
    ),

    #filters
    dbc.Row([
              dbc.Col([
                     dbc.Row([
                            html.Div('Camera type', style={'text-align': 'center'}),
                            html.Div(camera_type_selector),
                            ]),
                     dbc.Row([
                            html.Div('Client selector', style={'text-align': 'center'}),
                            html.Div(client_selector)
                     ]),
              ],
              width={'size': 2}),
              dbc.Col([
                     dbc.Row([
                            html.Div('Trend', style={'text-align': 'center'}),
                            html.Div(trend_switcher),
                     ]),
                     dbc.Row([ 
                            html.Div('Pipe', style={'text-align': 'center'}),
                            html.Div(pipe_switcher),
                     ]),
              ],
              width={'size': 1}),
              dbc.Col([
                     dbc.Row([
                            html.Div('Cycle selector', style={'text-align': 'center'}),
                            html.Div(cycle_selector),
                     ]),
                     dbc.Row([
                            html.Div('House selector', style={'text-align': 'center'}),
                            html.Div(cycleId_selector)
                     ]),
              ],
              width={'size': 4}),
              dbc.Col([
                     dbc.Row([
                            html.Div('Device selector', style={'text-align': 'center'}),
                            html.Div(deviceId_selector),
                     ]),
                     dbc.Row([
                            html.Div('Age selector', style={'text-align': 'center'}),
                            html.Div(age_selector),
                     ]),     
              ],
              width={'size': 5})
    ],
        style={'margin-bottom': 20}),

    #tabs
        dbc.Tabs([
            dbc.Tab(metrics_content, label = 'Metrics'),
            dbc.Tab(chart_content, label='Charts'),
            dbc.Tab(cycle_chart_content, label='Charts by cycle'),
            dbc.Tab(table_content, label = 'Table')
        ])
    ],
        style={'margin-left': '80px',
               'margin-right': '80px'})
    
    return layout