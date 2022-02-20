from typing import Tuple, List

import numpy as np

def create_node(coordinates:Tuple[int, float, float]) -> dict:
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

def distance(node1: dict, node2:dict) -> float:
    return ((node1['x'] - node2['x'])**2 + (node1['y'] - node2['y'])**2)**1/2

def get_route(value: int, routes: List[np.array]):
    for i, route in enumerate(routes):
        if value in route:
            return i

def route_distance(route: np.array, nodes: np.array) -> float:
    aux = distance(nodes[0], nodes[route[0]])
    for i in range(len(route) - 1): 
        aux += distance(nodes[route[i]], nodes[route[i+1]])

    aux += distance(nodes[0], nodes[route[-1]])
    return aux

def total_distance(routes: List[np.array], nodes: np.array) -> float:
    dist = 0
    for i in range(len(routes)):
        aux = route_distance(routes[i], nodes)
        dist += aux
    
    return dist
    
def get_city(nodes, value):
    # returns city position from nodes list by the value of the index key
    for i, dic in enumerate(nodes):
        if dic['index'] == int(value):
            return i
    return -1

def city_capacity(nodes, index):
    # return city capacity, using index ordered list
    return nodes[int(index)]['capacity']

def sum_route_capacity(route, nodes):
    # sum all of city's capacity in route array
    return sum([city_capacity(nodes, city) for city in route])
