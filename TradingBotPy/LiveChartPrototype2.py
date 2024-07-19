import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import random
import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Live Updating Chart", style={'text-align': 'center'}),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Update every second
        n_intervals=0
    ),
    html.Div("Real-time data visualization using Dash", style={'text-align': 'center', 'margin-top': '20px'})
])

# Initialize data lists
x_data = []
y_data = []

# Define the callback to update the graph
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    global x_data, y_data
    
    # Generate new data
    x_data.append(datetime.datetime.now())
    y_data.append(random.random())
    
    # Keep only the last 10 seconds of data
    if len(x_data) > 10:
        x_data = x_data[-10:]
        y_data = y_data[-10:]
    
    # Create the graph with the updated data
    fig = go.Figure(
        data=[go.Scatter(x=list(x_data), y=list(y_data),
                         mode='lines+markers', 
                         line=dict(color='royalblue', width=2),
                         marker=dict(color='red', size=8))]
    )
    
    # Update the layout
    fig.update_layout(
        title='Live Data Stream',
        xaxis_title='Time',
        yaxis_title='Value',
        xaxis=dict(
            range=[min(x_data), max(x_data)],
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey'
        ),
        yaxis=dict(
            range=[0, 1],
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey'
        ),
        plot_bgcolor='white',
        uirevision='constant'  # Prevent resetting the zoom on update
    )
    
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
