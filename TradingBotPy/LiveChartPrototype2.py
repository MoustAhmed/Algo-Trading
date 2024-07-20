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
    html.H1("Live Updating Chart", style={'text-align': 'center', 'color': 'white'}),
    dcc.Graph(
        id='live-update-graph',
        style={'height': '80vh', 'border': '2px solid white'},
        config={'scrollZoom': True}  # Enable scroll wheel zooming
    ),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Update every second
        n_intervals=0
    ),
    html.Div("Real-time data visualization using Dash", style={'text-align': 'center', 'margin-top': '20px', 'color': 'white'})
], style={'backgroundColor': '#1a1a1a', 'padding': '20px'})  # Set background color of the entire page

# Initialize data lists
x_data = []
y_data = []

# Define the callback to update the graph
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    global x_data, y_data
    
    # Generate new data
    current_time = datetime.datetime.now()
    x_data.append(current_time)
    y_data.append(random.random())
    
    # Keep only the last 10 seconds of data
    if len(x_data) > 10:
        x_data = x_data[-10:]
        y_data = y_data[-10:]
    
    # Create the graph with the updated data
    fig = go.Figure(
        data=[go.Scatter(x=list(x_data), y=list(y_data),
                         mode='lines+markers', 
                         line=dict(color='#1f77b4', width=2),  # Blue line
                         marker=dict(color='#ff7f0e', size=8))]  # Orange markers
    )
    
    # Update the layout
    fig.update_layout(
        title='Live Data Stream',
        xaxis_title='Time',
        yaxis_title='Value',
        paper_bgcolor='#1a1a1a',  # Dark background for the paper
        plot_bgcolor='#1a1a1a',  # Dark background for the plot area
        font=dict(color='white'),  # White text
        xaxis=dict(
            range=[min(x_data), max(x_data)],
            showgrid=True,
            gridwidth=1,
            gridcolor='gray',
            fixedrange=False  # Allow panning but keep the range fixed on updates
        ),
        yaxis=dict(
            range=[0, 1],
            showgrid=True,
            gridwidth=1,
            gridcolor='gray',
            fixedrange=False  # Allow panning but keep the range fixed on updates
        ),
        title_font=dict(size=24),
        margin=dict(l=40, r=40, t=40, b=40),  # Margin around the plot
        uirevision='constant',  # Prevent resetting the zoom on update
        dragmode='pan',  # Enable panning
    )
    
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
