import json
import dash
from dash.dependencies import Input, Output, State
import networkx as nx
from app_layout import create_layout
from create_figure import create_figure
from process_graph import initialize_graph

# Initialize Dash app
app = dash.Dash(__name__)
G = nx.DiGraph()

# Handle user input once
user_input = input('Enter data in the form [file_path, secondary_key] (or leave empty for example): ')
output_json_data, secondary_key, G, total_pages = initialize_graph(user_input=user_input, G=G)

# Generate positions for nodes with spring layout for improved visual spacing
pos = nx.spring_layout(G, k=0.4, seed=42)

# Create figure
figure = create_figure(pos=pos, output_json_data=output_json_data, G=G, secondary_key=secondary_key, clickData=None)

# Store component for toggling views
app.layout = create_layout(figure=figure)

# Unified callback to handle node clicks and update the graph
@app.callback(
    Output('network-graph', 'figure'),
    Output('store-data', 'data'),
    Output('graph-index', 'children'),
    Input('next-btn', 'n_clicks'),
    Input('prev-btn', 'n_clicks'),
    State('store-data', 'data'),
    prevent_initial_call=True
)
def update_graph(n_clicks_next, n_clicks_prev, store_data):
    # Get the current clicked node and graph index from the store data
    clicked_node = store_data.get('clicked_node')
    graph_index = store_data.get('graph_index', 1)  # Default to 1 if not set
    internal_output_json_data_file, internal_secondary_key, updated_G, total_pages = initialize_graph(user_input=user_input, G=G,
                                                                              index=graph_index)

    graph_index = graph_index % total_pages
    # Generate positions for nodes with spring layout for improved visual spacing
    updated_pos = nx.spring_layout(updated_G, k=0.4, seed=42)

    # Handle next/previous button clicks
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'next-btn':
        if graph_index < total_pages:# - 1:
            graph_index += 1
        else:
            graph_index = 0
        internal_output_json_data_file, internal_secondary_key, updated_G, total_pages = initialize_graph(user_input=user_input, G=G,
                                                                                             index=graph_index)
        updated_pos = nx.spring_layout(updated_G, k=0.4, seed=42)
    elif triggered_id == 'prev-btn':
        # Move to the previous page; if at the first page, stay on it
        if graph_index > 0:
            graph_index -= 1
        else:
            graph_index = total_pages - 1
        graph_index = (graph_index - 1) % total_pages  # Cycle through total_pages
        internal_output_json_data_file, internal_secondary_key, updated_G, total_pages = initialize_graph(user_input=user_input, G=G,
                                                                                             index=graph_index)
        updated_pos = nx.spring_layout(updated_G, k=0.4, seed=42)

    # Update the store data with the new graph index while keeping the clicked node
    updated_store_data = {'clicked_node': clicked_node, 'graph_index': graph_index}


    # Format the graph index display text
    graph_index_text = f"Graph {graph_index} of {total_pages}"

    # Return the updated figure for the new graph index and the store data
    return (
        create_figure(G=updated_G, pos=updated_pos, output_json_data=internal_output_json_data_file,
                      secondary_key=secondary_key),
        updated_store_data,
        graph_index_text
    )


if __name__ == '__main__':
    app.run_server(debug=True)
