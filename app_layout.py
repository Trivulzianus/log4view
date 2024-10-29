from dash import dcc, html
from create_figure import create_figure


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
        dcc.Store(id='store-clicked-node', data={'node': None}),  # Store for tracking clicked node
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
        )
    ], style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'justify-content': 'center',
        'background-color': '#f4f6f9',
        'padding': '20px',
        'width': '100vw'
    })
