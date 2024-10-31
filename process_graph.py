import pandas as pd
import os
import json


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
        return 'output_json_data.json', secondary_key
    else:
        file_path, secondary_key = user_input.split(',')
        file_path = file_path.strip()
        secondary_key = secondary_key.strip()
        process_graph(G=G, file_path=file_path, secondary_key=secondary_key, index=index)
        return file_path, secondary_key, G


def paginate_json(output_json_data, secondary_key, index):
    paginationObject_list = create_paginationObject_list(json_data=output_json_data, secondary_key=secondary_key)
    paginated_json_list = []
    for i in range(5):
        sliced_PaginationObject_list = paginationObject_list[(i - 1) * 5:i * 5]
        paginated_json = {}
        for PagObj in sliced_PaginationObject_list:
            # Reminder: paginationObject is of structure [Outer_key, [Inner_key, [secondary_key]], rest_of_json {key:
            # value} pairs)
            outer_key = PagObj.get()[0]
            inner_key_value_pair = PagObj.get()[1]
            rest_of_json = PagObj.get()[2]
            rest_of_json[PagObj.get()[1][0]] = PagObj.get()[1][1]
            paginated_json[outer_key] = rest_of_json
        paginated_json_list.append(paginated_json)
    return paginated_json_list[index]


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
            paginated_json = paginate_json(output_json_data=output_json_data, secondary_key=secondary_key, index=index)
            for val, data in paginated_json.items():
                G.add_edge(val, data[secondary_key])
            return G

        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None


# Create (outer_key, secondary_key, JSON) structure, for pagination purposes
def create_paginationObject_list(json_data, secondary_key, n=25):
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

            # Stop if we have reached the upper limit
            if len(PaginationObjectList) >= n:
                break

    return PaginationObjectList

