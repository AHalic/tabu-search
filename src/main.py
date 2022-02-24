from typing import List
import time

import sys
from copy import copy
import numpy as np

from read_input import *
from solution import *
from graph import *

def show_route(sol: List[np.array], nodes:np.array) -> None:
    dist = 0
    for i, route in enumerate(sol):
        route = route.flatten()
        print(f'Route #{i+1} - ', end="")
        print(*route.astype(int), sep=" ")
        print(f'Capacity: {sum_route_capacity(route, nodes)}', end='\n')
        print(f'Total Distance: {route_distance(route, nodes)}')

def algorithm(file, tenure):
    nodes, vehicles, clients, vehicle_capacity = read_input(file)

    sorted_nodes = sort_nodes(nodes)
    distances_between_clients = clients_distance(nodes, clients)
    best_sol = savings_initial_sol(distances_between_clients, nodes, vehicles, clients, vehicle_capacity, 0.5)
    #best_sol = random_initial_sol(nodes, sorted_nodes, vehicles, vehicle_capacity)
    # best_sol = copy(best_sol)
    best_sol_dist = total_distance(best_sol, nodes)
    # best_sol_dist = total_distance(best_sol, nodes)

    current_sol = best_sol.copy()
    current_dist = best_sol_dist

    show_route(best_sol, nodes)
    print(f"best distance: {best_sol_dist}\n")
    #swap(best_sol, best_sol_dist, nodes)
    
    tabu_list = []
    inicio = time.time()
    tempo = 0

    while tempo < 50:
        aux_current_sol, aux_current_dist, tabu_list = best_neighbor(current_sol, current_dist, nodes, vehicles, vehicle_capacity, tabu_list, tenure)
        
        if aux_current_sol != None:
            current_sol, current_dist = aux_current_sol, aux_current_dist
            if current_dist < best_sol_dist:
                best_sol = current_sol.copy()
                best_sol_dist = current_dist 

            # show_route(current_sol, nodes)
            # print(f"current distance: {current_dist}\n")    

        fim = time.time()
        print(tempo)
        tempo = fim - inicio

    print('\nBest Solution:')
    show_route(best_sol, nodes)
    print(f"best distance: {best_sol_dist}\n")

if __name__ == '__main__':
    args = sys.argv

    if len(args) > 1:
        algorithm(args[1], 15)
    else:
        print("File not informed")
        algorithm('input/A-n32-k5.vrp', 8)

    