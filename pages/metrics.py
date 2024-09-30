from libraries import dash_table, pd, html
import functions

'''CALCULATING METRICKS'''

def create_metrics_table(data, metric, camera_id=None):
    
    
    group_data = data.groupby('cycleId')

    metrics = group_data[metric].agg(
        min='min',
        max='max',
        mean='mean',
        std='std'
    ).reset_index()

    metrics['kde'] = group_data[metric].apply(functions.calculate_kde)
    metrics['mae'] = group_data[metric].apply(functions.calculate_mae)

    metrics['kde'] = metrics['kde'].fillna(0)
    metrics['mae'] = metrics['mae'].fillna(0)


    metrics = metrics.round(3)

    table = dash_table.DataTable(
        columns=[{'name': col, 'id': col} for col in metrics.columns],
        data=metrics.to_dict('records'),
        style_table={'overflowX': 'auto', 'color': 'black'},
        style_cell={'textAlign': 'center'},
        
        style_header={
            'fontWeight': 'bold', 
            'backgroundColor': '#FFA500', 
            'color': '#333',  
        },
        style_data_conditional=[
            {
                'if': {'column_id': col},
                'fontWeight': 'light', 
                'backgroundColor': '#f9f9f9',  
                'color': '#000', 
            } for col in metrics.columns
        ],
        
        style_data={
            'textAlign': 'center',
            'padding': '4px',  
        },
    )

    header = f"Metrics for {metric}" + (f" (Camera ID: {camera_id})" if camera_id else "")
    
    return html.Div(
        [
            html.H2(header, style={'text-align': 'center', 'margin-top': '20px', 'margin-bottom': '10px'}),  # Отступы перед и после заголовка
            table
        ],
        style={'margin-bottom': '30px'}  
    )


def generate_metric_tabs(data, metrics_list):
    metrics_tab = []

    for metric in metrics_list:
        if metric in data.columns:
            unique_camera_ids = data['cameraId'].unique()

            if len(unique_camera_ids) > 1:
                for camera_id in unique_camera_ids:
                    camera_data = data[data['cameraId'] == camera_id]
                    table = create_metrics_table(camera_data, metric, camera_id)
                    metrics_tab.append(table)
            else:
                table = create_metrics_table(data, metric)
                metrics_tab.append(table)

    return metrics_tab
