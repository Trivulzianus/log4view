import json
import dash
from dash.dependencies import Input, Output, State
import networkx as nx
from app_layout import create_layout
from create_figure import create_figure
from process_graph import process_graph

# Initialize Dash app
app = dash.Dash(__name__)
G = nx.DiGraph()

def initialize_graph(user_input=None):
    secondary_key = 'actions'
    if not user_input:
        process_graph(G=G, file_path='output_json_data.json', secondary_key=secondary_key)
        return 'output_json_data.json', secondary_key
    else:
        file_path, secondary_key = user_input.split(',')
        file_path = file_path.strip()
        secondary_key = secondary_key.strip()
        process_graph(G=G, file_path=file_path, secondary_key=secondary_key)
        return file_path, secondary_key

# Handle user input once
user_input = input('Enter data in the form [file_path, secondary_key] (or leave empty for default): ')
output_json_data_file, secondary_key = initialize_graph(user_input)

with open(output_json_data_file, 'r') as f:
    output_json_data = json.load(f)

# Generate positions for nodes with spring layout for improved visual spacing
pos = nx.spring_layout(G, k=0.45, seed=42)

# Create figure
figure = create_figure(pos=pos, output_json_data=output_json_data, G=G, secondary_key=secondary_key, clickData=None)

# Store component for toggling views
app.layout = create_layout(figure=figure)

# Unified callback to handle node clicks and update the graph
@app.callback(
    Output('network-graph', 'figure'),
    Output('store-clicked-node', 'data'),
    Input('network-graph', 'clickData'),
    State('store-clicked-node', 'data'),
    prevent_initial_call=True
)
def update_graph(clickData, store_data):
    if clickData:
        clicked_node = clickData['points'][0]['text']
        relevant_nodes = []

        # Iterate through all edges in the graph
        for source, target in G.edges():
            if clicked_node in target:
                relevant_nodes.append(source)  # Add target to the list if condition is met

        print(f"Nodes containing {clicked_node}:", relevant_nodes)
        new_edges = []
        for node in relevant_nodes:
            G.add_edge(clicked_node, node)
            # Keep track of new edges to remove after resetting
            new_edges.append((clicked_node, node))

        # If clicked node matches the stored node, reset to original view
        if store_data['node'] == clicked_node:
            G.remove_edges_from(new_edges)
            return create_figure(G=G, pos=pos, output_json_data=output_json_data), {
                'node': None}  # Reset to original view

        # Store the clicked node
        new_store_data = {'node': clicked_node}
        return create_figure(G=G, pos=pos, output_json_data=output_json_data, clickData=clickData), new_store_data

    return create_figure(G=G, pos=pos, output_json_data=output_json_data,
                         clickData=clickData), store_data  # Return original view if no click data

if __name__ == '__main__':
    app.run_server(debug=True)
