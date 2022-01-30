def create_node(coordinates):
    node = {
        'index': int(coordinates[0]) - 1,
        'x': float(coordinates[1]),
        'y': float(coordinates[2]),
        'capacity': 0 # initialized as 0
    }

    return node

def sort_nodes(nodes):
    # Sorts list of dictionary by capacity key, from biggest to smallest value
    return sorted(nodes, key=lambda item: item["capacity"], reverse=True)
