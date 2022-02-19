import sys
from copy import copy
import numpy as np

from read_input import *
from solution import *
from graph import *

def show_route(sol: list[np.array], nodes:np.array) -> None:
    dist = 0
    for i, route in enumerate(sol):
        route = route.flatten()
        print(f'Route #{i+1} - ', end="")
        print(*route.astype(int), sep=" ")
        print(f'Capacity: {sum_route_capacity(route, nodes)}', end='\n')
        #print(f'Total Distance: {total_distance(route, nodes)}')

def algorithm(file):
    nodes, vehicles, clients, vehicle_capacity = read_input(file)

    sorted_nodes = sort_nodes(nodes)

    current_sol = create_initial_sol(nodes, sorted_nodes, vehicles, vehicle_capacity)
    best_sol = copy(current_sol)
    current_sol_dist = total_distance(current_sol, nodes)
    best_sol_dist = total_distance(best_sol, nodes)
    
    show_route(current_sol, nodes)
    print(f"Current distance: {current_sol_dist}")

if __name__ == '__main__':
    args = sys.argv

    if len(args) > 1:
        algorithm(args[1])
    else:
        print("File not informed")
        algorithm('input\A-n32-k5.vrp')

    