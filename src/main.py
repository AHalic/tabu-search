import sys
from copy import copy

from read_input import *
from graph import *
from solution import *
from utils import *

def algorithm(file):
    nodes, vehicles, clients, vehicle_capacity = read_input(file)

    sorted_nodes = sort_nodes(nodes)

    current_sol = create_initial_sol(nodes, sorted_nodes, vehicles, vehicle_capacity)
    best_sol = copy(current_sol)

    for i, route in enumerate(current_sol):
        print(f"Route #{i+1}. Capacity: {sum_route_capacity(route, nodes)}")

if __name__ == '__main__':
    args = sys.argv

    if len(args) > 1:
        algorithm(args[1])
    else:
        print("File not informed")
    