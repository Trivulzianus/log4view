import pandas as pd
import os
import json
from typing import List


class PaginationObject:
    def __init__(self, outer_key, inner_key, rest_of_json):
        self.outer_key = outer_key
        self.inner_key = inner_key
        self.rest_of_json = rest_of_json

    def get(self):
        return [self.outer_key, self.inner_key, self.rest_of_json]


def initialize_graph(G, user_input=None, index=1):
    secondary_key = 'actions'
    if not user_input:
        process_graph(G=G, file_path='output_json_data.json', secondary_key=secondary_key, index=index)
        with open(file='output_json_data.json', mode='r') as f:
            output_json_data = json.load(f)
        return output_json_data, secondary_key, G
    else:
        file_path, secondary_key = user_input.split(',')
        file_path = file_path.strip()
        with open(file=file_path, mode='r') as f:
            output_json_data = json.load(f)
        secondary_key = secondary_key.strip()
        process_graph(G=G, file_path=file_path, secondary_key=secondary_key, index=index)
        return output_json_data, secondary_key, G


def paginate_json(output_json_data, secondary_key, index) -> List[PaginationObject]:
    acceptable_number_of_nodes_in_page = 50
    paginationObject_list = create_paginationObject_list(json_data=output_json_data, secondary_key=secondary_key)

    # Ensure there's data to paginate
    if len(paginationObject_list) == 0:
        return []  # Handle empty list case

    # Create a sorted list of unique main nodes
    paginationObject_list_sorted = sorted(paginationObject_list, key=lambda x: x.get()[1][1])
    main_nodes = []

    # Collect unique main nodes
    for PagObj in paginationObject_list_sorted:
        main_node_value = PagObj.get()[1][1]
        if main_node_value not in main_nodes:
            main_nodes.append(main_node_value)

    # Create a dictionary to hold paginated results
    paginated_json_dict_of_lists = {}

    # Iterate over each unique main node to create pages
    for i, main_node in enumerate(main_nodes):
        paginated_json_list = []

        # Collect items for the current main node
        for PagObj in paginationObject_list_sorted:
            if PagObj.get()[1][1] == main_node:
                paginated_json_list.append(PagObj)

        # Store the list for the current main node, with 1-based index
        paginated_json_dict_of_lists[i + 1] = paginated_json_list[:acceptable_number_of_nodes_in_page]

    # Return the requested page, ensuring it exists
    return paginated_json_dict_of_lists.get(index, [])


def process_graph(G, file_path, secondary_key, index):
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)
    with open(file_path, 'r') as f:
        try:
            if file_extension.lower() == '.csv':
                # Read CSV file into DataFrame
                df = pd.read_csv(f)
                output_json_data = df.to_json(orient='records', lines=True)
            elif file_extension.lower() == '.json':
                output_json_data = json.load(f)
            else:
                raise ValueError("Unsupported file type: {}".format(file_extension))
            paginated_json_list = paginate_json(output_json_data=output_json_data, secondary_key=secondary_key,
                                                index=index)
            G.clear()
            for paginated_object in paginated_json_list:
                try:
                    G.add_edge(paginated_object.get()[0], paginated_object.get()[1][1])
                except KeyError:
                    print(f"{paginated_object.get()[1][1]} has no {secondary_key}")
                except Exception as e:
                    print(f"Unexpected error while processing graph: {e}")
            return G

        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None


# Create (outer_key, secondary_key, JSON) structure, for pagination purposes
def create_paginationObject_list(json_data, secondary_key):
    PaginationObjectList = []

    # Iterate through outer JSON keys
    for outer_key, inner_json in json_data.items():
        # Check if the inner key exists
        if secondary_key in inner_json:
            inner_value = inner_json[secondary_key]

            # Create a copy of inner_json without the inner key
            rest_data = {key: value for key, value in inner_json.items() if key != secondary_key}

            # Create a tuple with outer key, inner key, and the rest of the data
            PaginationObjectList.append(PaginationObject(outer_key, [secondary_key, inner_value], rest_data))


    return PaginationObjectList

