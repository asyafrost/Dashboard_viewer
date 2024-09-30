from libraries import dash, dcc, html, dbc, Input, Output, dash_table, daq, pd, px, pio, go

import components
import graph
import interface
from pages.charts import chart_content
from pages.cycle_charts import create_cycle_charts
from pages.table import create_table
from pages.metrics import generate_metric_tabs
from datasets import load_and_preprocess_csv

pio.templates.default = "plotly_white"
pio.renderers.default = 'browser'


'''ENTER PATHS TO DATASETS'''

file_paths = [
    'data/Dataset.csv',
    'data/Dataset_THSXS2-9.csv',
    r'D:\загрузки\Dataset_THMHGE-6.csv'
]

df = load_and_preprocess_csv(file_paths)
df = df.round(3)

unique_cycle_ids = df['cycleId'].unique()
unique_cycle = df['cycle'].unique()
color_map = {cycle_id: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, cycle_id in enumerate(unique_cycle_ids)}
color_map_cycle = {cycle: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, cycle in enumerate(unique_cycle_ids)}

'''SELECTORS'''

def generate_options(df_column):
    return [{'label': val, 'value': val} for val in df_column.unique()]

selectors_info = {
    'camera_type_selector': df['cameraId'],
    'client': df['client'],
    'cycle': df['cycle'],
    'cycleId_selector': df['cycleId'],
    'deviceId_selector': df['deviceId']
}

selectors = {
    key: components.create_dropdown(key, generate_options(col)) for key, col in selectors_info.items()
}

age_selector = components.create_range_slider('age_slider', df['age'])
trend_switcher = components.create_boolean_switcher('trend_switcher')
pipe_switcher = components.create_boolean_switcher('pipe_switcher')



'''GRAPHS'''

app = dash.Dash(__name__, suppress_callback_exceptions=True, 
                external_stylesheets=[dbc.themes.QUARTZ])


"""LAYOUT"""
metrics_content = generate_metric_tabs(df, components.list_of_features)
cycle_chart_content = create_cycle_charts(df)
table_content = create_table(df)

app.layout = interface.create_layout(*selectors.values(), age_selector, trend_switcher, pipe_switcher, chart_content, cycle_chart_content, table_content, metrics_content)


"""CALLBACKS"""
@app.callback(
    [Output(f'{chart}_age_chart', 'children') for chart in ['chicks', 'chickSize', 'sui', 'od', 'activityIndex', 'avgActivityIndex', 'illumination']] +
    [Output(f'{chart}_density_chart', 'children') for chart in ['chicks', 'chickSize', 'sui', 'od', 'activityIndex', 'avgActivityIndex', 'illumination']] + 
    [
        Output(component_id='feeders_height_age_chart', component_property='children'),
        Output(component_id='feeders_height_density_chart', component_property='children'),
        Output(component_id='huddlingIndex_chart', component_property='children'),
        Output(component_id='huddlingTime_bar', component_property='children'),
        Output(component_id='actLevels_age_chart', component_property='children'),
        Output(component_id='actLevels_age_pie', component_property='children')
    ],
    [
        Input('age_slider', 'value'), 
        Input('camera_type_selector', 'value'), 
        Input('client', 'value'), 
        Input('cycle', 'value'), 
        Input('cycleId_selector', 'value'), 
        Input('deviceId_selector', 'value'), 
        Input('trend_switcher', 'on'), 
        Input('pipe_switcher', 'on')
    ]
)
def update_charts(age_value, camera_type, client, cycle, cycleId, deviceId, trend, pipe):
    
    chart_data = df[(df['age'] > age_value[0]) & 
                    (df['age'] < age_value[1]) & 
                    (df['cameraId'].isin(camera_type)) & 
                    (df['client'].isin(client)) & 
                    (df['cycle'].isin(cycle)) & 
                    (df['cycleId'].isin(cycleId)) & 
                    (df['deviceId'].isin(deviceId))]

    if len(chart_data) == 0:
        return [html.Div('Please select more data')] * 20 

   
    scatter_params = [
        ('chicks', 'Chicks'),
        ('chickSize', 'ChickSize'),
        ('spaceUniformityIndex', 'Space Uniformity Index'),
        ('occupationDensity', 'Occupation Density'),
        ('activityIndex', 'Activity Index'),
        ('averageActivityIndex', 'Average Activity Index'),
        ('illumination', 'Illumination')
    ]

    #Main charts
    scatter_graphs = [components.create_scatter(chart_data, param[0], param[1], trend, pipe, color_map) for param in scatter_params]
    density_graphs = [components.create_density(chart_data[param[0]], param[0]) for param in scatter_params]

    results = scatter_graphs + density_graphs


    # Feeders height charts
    filtered_data = chart_data[chart_data['feedersHeight'] > 0]
    fig9 = graph.plot_scatter(filtered_data, 'age', 'feedersHeight', 'cycleId', trend, pipe, color_map)
    html9 = [html.Div('Feeders height ~ Age', style={'text-align': 'center'}), dcc.Graph(figure=fig9)]
    
    fig10 = graph.plot_density(df['feedersHeight'].loc[df['feedersHeight'] > 0], 'feedersHeight')
    html10 = [html.Div('Feeders Height ~ Age', style={'text-align': 'center'}), dcc.Graph(figure=fig10)]

    # Huddling charts
    aggregated_data1 = chart_data.groupby(['age', 'cycleId']).agg({'huddlingIndex': 'mean'}).reset_index()
    fig11 = px.line(aggregated_data1, x='age', y='huddlingIndex', color='cycleId', color_discrete_map=color_map, markers=True)
    html11 = [html.Div('Huddling Index ~ Age', style={'text-align': 'center'}), dcc.Graph(figure=fig11)]

    aggregated_data2 = chart_data.groupby(['age', 'cycleId']).agg({'huddlingTime': 'mean'}).reset_index()
    fig12 = px.bar(aggregated_data2, x='age', y='huddlingTime', color='cycleId', color_discrete_map=color_map, labels={'huddlingTime': 'Huddling Time', 'age': 'Age'}, barmode='group')
    html12 = [html.Div('Huddling Time ~ Age', style={'text-align': 'center'}), dcc.Graph(figure=fig12)]


    # Activity levels charts
    aggregated_data_act = chart_data.groupby(['cycleId', 'age']).agg({
        'lowActivity': 'mean',
        'normalActivity': 'mean',
        'highActivity': 'mean'
    }).reset_index()

    melted_data = pd.melt(aggregated_data_act, id_vars=['cycleId', 'age'],
                          value_vars=['lowActivity', 'normalActivity', 'highActivity'],
                          var_name='Activity Level', value_name='Activity Value')

    fig1_act = px.line(melted_data, x='age', y='Activity Value', color='cycleId', symbol='Activity Level')
    html_act_1 = [html.Div('Activity Levels ~ Age', style={'text-align': 'center'}), dcc.Graph(figure=fig1_act)]

    activity_levels = {
        'Low activity': chart_data['lowActivity'].sum(),
        'Normal activity': chart_data['normalActivity'].sum(),
        'High activity': chart_data['highActivity'].sum()
    }

    activity_df = pd.DataFrame({
        'Activity Level': activity_levels.keys(),
        'Count': activity_levels.values()
    })

    fig2_act = px.pie(activity_df, names='Activity Level', values='Count')
    html_act_2 = [html.Div('Activity Levels Pie ~ Age', style={'text-align': 'center'}), dcc.Graph(figure=fig2_act)]

    return results + [html9, html10, html11, html12, html_act_1, html_act_2]

@app.callback(
    [Output(f'{chart}_cycle_age_chart', 'children') for chart in ['chicks', 'chickSize', 'sui', 'od', 'activityIndex', 'avgActivityIndex', 'illumination']],
    [
        Input('age_slider', 'value'), 
        Input('camera_type_selector', 'value'), 
        Input('client', 'value'), 
        Input('cycle', 'value'), 
        Input('cycleId_selector', 'value'), 
        Input('deviceId_selector', 'value'), 
        Input('trend_switcher', 'on')
    ]
)
def update_charts_cycle(age_value, camera_type, client, cycle, cycleId, deviceId, trend):
    
    chart_data = df[(df['age'] > age_value[0]) & 
                    (df['age'] < age_value[1]) & 
                    (df['cameraId'].isin(camera_type)) &
                    (df['client'].isin(client)) & 
                    (df['cycle'].isin(cycle)) &  
                    (df['cycleId'].isin(cycleId)) & 
                    (df['deviceId'].isin(deviceId))]

    if len(chart_data) == 0:
        return [html.Div('Please select more data')] * 20 
    
    scatter_params = [
        ('chicks', 'Chicks'),
        ('chickSize', 'ChickSize'),
        ('spaceUniformityIndex', 'Space Uniformity Index'),
        ('occupationDensity', 'Occupation Density'),
        ('activityIndex', 'Activity Index'),
        ('averageActivityIndex', 'Average Activity Index'),
        ('illumination', 'Illumination')
    ]

    mean_columns = [param[0] for param in scatter_params]

    aggregated_data_cycle = chart_data.groupby(['cycle', 'age'])[mean_columns].mean().reset_index()

    line_graphs = [components.create_line(aggregated_data_cycle, param[0], param[1], trend, color_map_cycle) for param in scatter_params]
    
    return line_graphs


@app.callback(
    Output('tbl_out', 'children'),
    [Input('tbl', 'active_cell')]
)
def update_output(active_cell):
    if active_cell:
        cell_info = f"Вы выбрали строку {active_cell['row'] + 1}, колонку {df.columns[active_cell['column']]}"
        return cell_info
    return "Нажмите на ячейку таблицы."


if __name__ == '__main__':
    app.run_server(debug=True)

