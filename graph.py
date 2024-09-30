from libraries import np, pd, go, px, gaussian_kde, mode, daq, html, dcc

def plot_density(data, x_name):
   
    filtered_data = data.dropna()
   
    kde = gaussian_kde(filtered_data)
    x_values = np.linspace(filtered_data.min(), filtered_data.max(), 100)
    y_values = kde(x_values)

    mean = filtered_data.mean()
    std = filtered_data.std()

    mod_result = mode(filtered_data)
    mod = mod_result.mode if isinstance(mod_result.mode, np.ndarray) else mod_result.mode.item()

    lower_bound = mean - 2 * std
    upper_bound = mean + 2 * std

    fig = go.Figure()

    # Плотность
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        name='Density Estimate',
        line=dict(color='blue')
    ))

    # среднее
    fig.add_trace(go.Scatter(
        x=[mean, mean],
        y=[0, kde(mean)[0]],  # Высота линии
        mode='lines',
        name='Mean',
        line=dict(color='orange', dash='dash'),
        hovertemplate=f'Mean: {mean:.2f}'
    ))

    # мода
    if mod is not None:
        fig.add_trace(go.Scatter(
            x=[mod, mod],
            y=[0, kde(mod)[0]],  # Высота линии
            mode='lines',
            name='Mode',
            line=dict(color='green', dash='dash'),
            hovertemplate=f'Mode: {mod:.2f}'
        ))

    # границы ±2 std
    fig.add_trace(go.Scatter(
        x=[lower_bound, lower_bound],
        y=[0, kde(lower_bound)[0]],  
        mode='lines',
        name='-2 STD',
        line=dict(color='red', dash='dot'),
        hovertemplate=f'-2 STD: {lower_bound:.2f}'
    ))

    fig.add_trace(go.Scatter(
        x=[upper_bound, upper_bound],
        y=[0, kde(upper_bound)[0]],  # Высота линии
        mode='lines',
        name='+2 STD',
        line=dict(color='red', dash='dot'),
        hovertemplate=f'+2 STD: {upper_bound:.2f}'
    ))

    fig.update_layout(
        xaxis_title=x_name,
        yaxis_title='Density',
        template='plotly_white'
    )

    return fig

def plot_scatter(data, x_name, y_name, color_name, trend, pipe, color_map):
    
    if trend:
        fig = px.scatter(data, x=x_name, y=y_name, color=color_name, color_discrete_map=color_map, trendline="ols")
    else:
        fig = px.scatter(data, x=x_name, y=y_name, color=color_name, color_discrete_map=color_map)

    grouped_data = data.groupby([x_name, color_name]).agg(
        y_mean=(y_name, 'mean'),
        y_std=(y_name, 'std')
    ).reset_index()

    if pipe:
        # Добавление трубы для каждого cycleId
        for cycle_id in grouped_data[color_name].unique():
            cycle_data = grouped_data[grouped_data[color_name] == cycle_id]

            # Верхняя и нижняя границы трубы (±2 std)
            upper_bound = cycle_data['y_mean'] + 2 * cycle_data['y_std']
            lower_bound = cycle_data['y_mean'] - 2 * cycle_data['y_std']

            # Добавление закрашенной области между границами
            fig.add_traces(go.Scatter(
                x=pd.concat([cycle_data[x_name], cycle_data[x_name][::-1]]),
                y=pd.concat([upper_bound, lower_bound[::-1]]),
                fill='toself',
                fillcolor=f'rgba(0, 100, 250, 0.1)', 
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False,
                name=f'Tube for {cycle_id}'
            ))

    return fig

def plot_line(data, x_name, y_name, color_name, color_map):
    
    fig = px.line(data, x=x_name, y=y_name, color=color_name, 
                    color_discrete_map=color_map, markers=True, 
                    line_shape="linear")

    return fig
