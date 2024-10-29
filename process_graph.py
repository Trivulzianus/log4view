import pandas as pd
import os
import json


def process_graph(G, file_path, secondary_key):
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)
    with open(file_path,'r') as f:
        try:
            if file_extension.lower() == '.csv':
                # Read CSV file into DataFrame
                df = pd.read_csv(f)
                output_json_data = df.to_json(orient='records', lines=True)
            elif file_extension.lower() == '.json':
                output_json_data = json.load(f)
            else:
                raise ValueError("Unsupported file type: {}".format(file_extension))
            for val, data in output_json_data.items():
                G.add_edge(val, data[secondary_key])
            return G

        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

