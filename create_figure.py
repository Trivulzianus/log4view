import plotly.graph_objs as go


def create_figure(pos, output_json_data, G, secondary_key, clickData=None):
    edge_x, edge_y, node_x, node_y, node_text, node_hovertext, node_color = [], [], [], [], [], [], {}
    color_palettes = [
        ["#FF5733", "#FFBD33"],  # Palette 1 - Red
        ["#33FF57", "#33FFBD"],  # Palette 2 - Green
        ["#5733FF", "#BD33FF"],  # Palette 3 - Purple
        ["#33A1FF", "#33C3FF"],  # Palette 4 - Blue
        ["#FF33A1", "#FF33C3"],  # Palette 5 - Pink
    ]
    scale_factor = 0.7

    # If a node is clicked, show that node and its neighbors
    if clickData:
        clicked_node = clickData['points'][0]['text']

        # Add the clicked node
        if clicked_node in G.nodes:
            x, y = pos[clicked_node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(clicked_node)
            node_color[clicked_node] = '#3498db'

            # Hover text for clicked node
            if clicked_node in output_json_data:
                json_data = output_json_data[clicked_node]
                hover_text = ''
                for key, value in json_data.items():
                    hover_text = hover_text + f"<b>{key}:</b> {value} <br>"
            else:
                hover_text = f"<b>{secondary_key}:</b> {clicked_node}"
            node_hovertext.append(hover_text)

            # Add neighboring nodes
            for neighbor in G.neighbors(clicked_node):
                nx, ny = pos[neighbor]
                node_x.append(nx)
                node_y.append(ny)
                node_text.append(neighbor)
                node_color[neighbor] = '#e74c3c'

                # Hover text for neighbors
                if neighbor in output_json_data:
                    json_data = output_json_data[neighbor]
                    neighbor_hover_text = ''
                    for key, value in json_data.items():
                        neighbor_hover_text = neighbor_hover_text + f"<b>{key}:</b> {value} <br>"
                else:
                    neighbor_hover_text = f"<b>{secondary_key}:</b> {neighbor}"
                node_hovertext.append(neighbor_hover_text)

                # Calculate shortened edge positions
                mid_x, mid_y = (x + nx) / 2, (y + ny) / 2
                scaled_x0 = mid_x + (x - mid_x) * scale_factor
                scaled_y0 = mid_y + (y - mid_y) * scale_factor
                scaled_x1 = mid_x + (nx - mid_x) * scale_factor
                scaled_y1 = mid_y + (ny - mid_y) * scale_factor

                edge_x.extend([scaled_x0, scaled_x1, None])
                edge_y.extend([scaled_y0, scaled_y1, None])
    else:
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]

            # Calculate shortened edge positions
            mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
            scaled_x0 = mid_x + (x0 - mid_x) * scale_factor
            scaled_y0 = mid_y + (y0 - mid_y) * scale_factor
            scaled_x1 = mid_x + (x1 - mid_x) * scale_factor
            scaled_y1 = mid_y + (y1 - mid_y) * scale_factor

            edge_x.extend([scaled_x0, scaled_x1, None])
            edge_y.extend([scaled_y0, scaled_y1, None])

        color_palette_nodes = {}
        main_node_color_count = 0
        main_nodes = []
        for node in G.nodes():
            # Check if the node is an endpoint (no outgoing edges)
            is_main_node = G.out_degree(node) == 0
            if is_main_node:
                color_palette_nodes[node] = color_palettes[main_node_color_count]
                node_color[node] = color_palettes[main_node_color_count][0]
                main_node_color_count += 1
                main_nodes.append(node)
        for node in G.nodes():
            is_main_node = G.out_degree(node) == 0
            if is_main_node:
                node_color[node] = color_palette_nodes[node][0]
            if not is_main_node:
                for main_node in main_nodes:
                    if G.has_edge(node, main_node):
                        node_color[node] = color_palette_nodes[main_node][0]
        # Populate node information for the initial view
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)

            if node in output_json_data:
                json_data = output_json_data[node]
                hover_text = ''
                for key, value in json_data.items():
                    hover_text = hover_text + f"<b>{key}:</b> {value} <br>"
            else:
                hover_text = f"<b>Action:</b> {node}"
            node_hovertext.append(hover_text)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.8, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        hoverinfo='text',
        hovertext=node_hovertext,
        marker=dict(
            color=[node_color[node] for node in node_text],
            size=[len(str(node)) * 10 for node in node_text],
            opacity=0.2
        )
    )

    # Create the figure
    return go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
        title=f'<b>{secondary_key} network graph</b>'.upper(),
        titlefont=dict(size=24, color='#333333', family='Arial'),
        title_x=0.5,
        dragmode='pan',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=80),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='#f9f9f9',
        height=700
    ))