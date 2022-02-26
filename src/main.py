from typing import List
import time

import sys
from copy import copy
import numpy as np

from read_input import *
from solution import *
from graph import *

def show_route(sol: List[np.array], nodes:np.array, capacity:int) -> None:
    dist = 0
    for i, route in enumerate(sol):
        route = route.flatten()
        print(f'Route #{i+1} - ', end="")
        print(*route.astype(int), sep=" ")
        print(f'Capacity: {sum_route_capacity(route, nodes)}', end='\n')
        dist, _ = route_distance(route, nodes, capacity)
        print(f'Total Distance: {dist}')

def algorithm(file, tenure):
    nodes, vehicles, clients, vehicle_capacity = read_input(file)

    sorted_nodes = sort_nodes(nodes)
    distances_between_clients = clients_distance(nodes, clients)
    best_sol = savings_initial_sol(distances_between_clients, nodes, vehicles, clients, vehicle_capacity, 0.5)
    # best_sol = random_initial_sol(nodes, sorted_nodes, vehicles, vehicle_capacity)
    # best_sol = copy(best_sol)
    best_sol_dist, best_flag = total_distance(best_sol, nodes, vehicle_capacity)
    # best_sol_dist = total_distance(best_sol, nodes)

    current_sol = best_sol.copy()
    current_dist = best_sol_dist
    current_flag = best_flag

    show_route(best_sol, nodes, vehicle_capacity)
    print(f"best distance: {best_sol_dist}\n")
    #swap(best_sol, best_sol_dist, nodes)
    
    tabu_list = []
    inicio = time.time()
    tempo = 0
    iter = 0

    # while tempo < 300 and iter < 1000:
    aux_current_sol, aux_current_dist, tabu_list, aux_current_flag = best_neighbor(current_sol, current_dist, nodes, vehicles, vehicle_capacity, tabu_list, tenure, best_sol_dist, current_flag)
    
    if aux_current_sol != None:
        current_sol, current_dist, current_flag = aux_current_sol, aux_current_dist, aux_current_flag

        # (a and not b) or (a and c) or (not b and c)
        if (current_flag and not best_flag) or (current_flag and current_dist < best_sol_dist) or (not best_flag and current_dist < best_sol_dist):
        # if current_dist < best_sol_dist and current_flag or (not current_flag and not best_flag):
            best_sol = current_sol.copy()
            best_sol_dist = current_dist 
            best_flag = current_flag
            iter = 0
        else:
            iter += 1

        # show_route(current_sol, nodes)
        # print(f"current distance: {current_dist}\n")    

    fim = time.time()
    tempo = fim - inicio

    print('\nBest Solution:')
    show_route(best_sol, nodes, vehicle_capacity)
    print(f"best distance: {best_sol_dist}\n")
    print('numero de iterações sem melhora:', iter)

if __name__ == '__main__':
    args = sys.argv

    tenure = 15

    if len(args) > 1:
        algorithm(args[1], tenure)
    else:
        print("File not informed")
        algorithm('input/A-n32-k5.vrp', tenure)

    