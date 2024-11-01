from dash import dcc, html
from typing import List
import plotly.graph_objs as go


def create_layout(figure):
    return html.Div([
        html.H1(
            "Log4View - Interactive Graph View of Logs",
            style={
                'text-align': 'center',
                'color': '#2C3E50',
                'font-family': 'Arial, sans-serif',
                'font-size': '2.5em',
                'margin-bottom': '20px'
            }
        ),
        # Store to keep track of the clicked node and graph index
        dcc.Store(id='store-data', data={'clicked_node': None, 'graph_index': 1}),

        # Graph display area
        html.Div(
            dcc.Graph(id='network-graph', figure=figure, style={
                'width': '100%',
                'border-radius': '10px',
                'box-shadow': '0 4px 12px rgba(0, 0, 0, 0.1)',
                'padding': '10px',
                'background-color': '#ffffff'
            }),
            style={
                'width': '90%',
                'max-width': '1500px',
                'display': 'flex',
                'justify-content': 'center'
            }
        ),

        # Navigation buttons for switching graphs
        html.Div([
            html.Button('<', id='prev-btn', n_clicks=0),
            html.Button('>', id='next-btn', n_clicks=0)
        ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '200px', 'margin': '20px auto'})

    ], style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'justify-content': 'center',
        'background-color': '#f4f6f9',
        'padding': '20px',
        'width': '100vw'
    })