import numpy as np

def create_node(coordinates:tuple[int, float, float]) -> dict:
    node = {
        'index': int(coordinates[0]) - 1,
        'x': float(coordinates[1]),
        'y': float(coordinates[2]),
        'capacity': 0 # initialized as 0
    }

    return node

def sort_nodes(nodes:np.array) -> np.array:
    # Sorts list of dictionary by capacity key, from biggest to smallest value
    return sorted(nodes, key=lambda item: item["capacity"], reverse=True)

def get_city(nodes, value):
    # returns city position from nodes list by the value of the index key
    for i, dic in enumerate(nodes):
        if dic['index'] == value:
            return i
    return -1

def city_capacity(nodes, index):
    # return city capacity, using index ordered list
    return nodes[int(index)]['capacity']

def sum_route_capacity(route, nodes):
    # sum all of city's capacity in route array
    return sum([city_capacity(nodes, city) for city in route])

def distance(node1, node2):
    # returns eucledian distance between two nodes
    return ((node1['x'] - node2['x'])**2 + (node1['y']-node2['y'])**2)**1/2