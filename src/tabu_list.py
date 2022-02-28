from typing import List, Tuple
import time

from initial_solution import *
from local_search import *
from graph import *

def algorithm(nodes: List[dict], vehicles: int, clients: int, vehicle_capacity: int, tenure: int, iter_max:int=1000, savings:bool=True) -> None:
    """
    Aplica o algoritmo de tabu list utilizando ou uma solucao inicial aleatoria ou uma solucao utilizando o metodo de
    Clarke Wright de economia. 
    """
    inicio = time.time()

    # Cria matriz de distancia entre as cidades
    distances_between_clients = clients_distance(nodes, clients)

    # Escolhe a solucao inicial
    if savings:
        best_sol = corrected_savings(distances_between_clients, nodes, vehicles, clients, vehicle_capacity, 0.1)
    else:
        best_sol = random_initial_sol(nodes, vehicles, vehicle_capacity)
    
    best_sol_dist, best_feasible_flag = total_distance(distances_between_clients, best_sol, nodes, vehicle_capacity)
    
    current_sol = best_sol.copy()
    current_dist = best_sol_dist
    current_feasible_flag = best_feasible_flag
    
    # Mostra a rota inicial e a distancia
    show_routes(distances_between_clients, best_sol, nodes, vehicle_capacity)
    print(f"Distancia: {best_sol_dist}\n")
    
    # Inicializa lista tabu e condicoes de parada
    tabu_list = []
    tempo = 0
    iter = 0

    while tempo < 300 and iter < iter_max:
        aux_current_sol, aux_current_dist, tabu_list, aux_current_feasible_flag = best_neighbor(distances_between_clients, current_sol, current_dist, nodes, vehicles, vehicle_capacity, tabu_list, tenure, best_sol_dist, current_feasible_flag)
        
        if aux_current_sol != None:
            current_sol, current_dist, current_feasible_flag = aux_current_sol, aux_current_dist, aux_current_feasible_flag
            
            if (current_feasible_flag and not best_feasible_flag) or (current_feasible_flag and current_dist < best_sol_dist) or (not best_feasible_flag and current_dist < best_sol_dist):
                best_sol = current_sol.copy()
                best_sol_dist = current_dist 
                best_feasible_flag = current_feasible_flag
                iter = 0
            else:
                iter += 1


        fim = time.time()
        tempo = fim - inicio

    print("", "*"*20, sep='\n', end='\n\n\n')
    
    show_routes(distances_between_clients, best_sol, nodes, vehicle_capacity)
    print(f"Distancia: {best_sol_dist}", end='\n\n')

    print('Numero de iterações sem melhora:', iter)
    print('Tempo de execucao do algoritmo:', tempo)