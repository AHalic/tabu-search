from platform import node
import sys
from copy import copy
import numpy as np

from read_input import *
from graph import *
from solution import *
from utils import *

def show_route(solution: list[np.array], nodes:np.array) -> None:
    dist = 0
    for i, route in enumerate(solution):
        route = route.flatten()
        print(f'Route #{i+1} - ', end="")
        print(*route.astype(int), sep=" ")
        print(f'Total Distance: {total_distance(route, nodes)} - Capacity: {sum_route_capacity(route, nodes)}', end='\n\n')

def algorithm(file):
    nodes, vehicles, clients, vehicle_capacity = read_input(file)

    sorted_nodes = sort_nodes(nodes)

    current_sol = create_initial_sol(nodes, sorted_nodes, vehicles, vehicle_capacity)
    best_sol = copy(current_sol)

    show_route(current_sol, nodes)

if __name__ == '__main__':
    args = sys.argv

    if len(args) > 1:
        algorithm(args[1])
    else:
        print("File not informed")
    