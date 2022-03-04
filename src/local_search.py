from typing import List, Set, Tuple

import numpy as np
import random
from math import ceil 
import time

from graph import total_distance
from moves import swap, shift

def best_neighbor(
        distances: np.array, 
        solution:List[np.array], 
        dist_sol:float, 
        nodes:List[dict], 
        max_routes:int, 
        capacity:int, 
        tabu_list:List[Set], 
        tenure:int, 
        best_sol:float, 
        current_flag:bool
    ) -> Tuple[List[np.array], float, List[Set], bool]:
    """
    Função que realiza o algoritmo da busca local utilizando dois tipos de movimento 
    e retorna a melhor solução encontrada, que possua menor distancia ou seja feasible
    """
    current_sol_swap, current_dist_swap, current_move_swap, current_flag_swap = swap_loop(distances, solution, dist_sol, nodes, max_routes, capacity, tabu_list, best_sol, current_flag)
    current_sol_shift, current_dist_shift, current_move_shift, current_flag_shift = shift_loop(distances, solution, dist_sol, nodes, max_routes, capacity, tabu_list, best_sol, current_flag)

    if (current_flag_swap and not current_flag_shift) or (current_flag_swap and  current_dist_swap <= current_dist_shift) or (not current_flag_shift and  current_dist_swap <= current_dist_shift):
        if len(tabu_list) == tenure:
            tabu_list.pop(0)
        if current_move_swap not in tabu_list:
            tabu_list.append(current_move_swap)

        return current_sol_swap, current_dist_swap, tabu_list, current_flag_swap
    else:
        if len(tabu_list) == tenure:
            tabu_list.pop(0)
        
        if current_move_shift not in tabu_list:
            tabu_list.append(current_move_shift)

        return current_sol_shift, current_dist_shift, tabu_list, current_flag_shift


def swap_loop(
        distances: np.array,
        solution:List[np.array], 
        dist_sol:float, 
        nodes:List[dict], 
        max_routes:int, 
        capacity:int, 
        tabu_list:List[Set], 
        best_sol:float, 
        current_feasible_flag:bool
    ) -> Tuple[List[np.array], float, Set, bool]:
    """
    Verifica a vizinhança da solucao fazendo movimentos do tipo swap. 
    Ele troca um elemento de uma rota por um de outra. 
    É levado em consideracao se a solucao recebida eh feasible ou nao. 
    Caso a solucao seja feasible, ele nao aceita solucoes nao feasibles. 
    Retorna a melhor solucao encontrada, a distancia dela, o movimento tabu 
    e flag referente a se a solucao encontrada eh feasible. 
    """
    current_sol_swap, current_dist_swap = None, None
    
    inicio = time.time()
    for i in range(0, max_routes):
        # gera um sample aleatorio de cidades da rota 1
        c1_indexes = random.sample(range(len(solution[i])), k=int(ceil(len(solution[i]) / 2)))

        for j in range(i, max_routes):
            # Realiza o movimento swap

            for i_c1 in c1_indexes:
                # faz o swap entre todas as cidades e do sample e da rota 2
                for i_c2 in range(len(solution[j])):
                    if time.time() - inicio > 30:
                        return current_sol_swap, current_dist_swap, current_move_swap, current_feasible_flag
                        
                    aux_solution, movement = swap(solution, i, j, i_c1, i_c2)

                    dist_aux, feasible_flag = total_distance(distances, aux_solution, nodes, capacity)


                    if not feasible_flag:
                        # se a solução atual é feasible, não são aceitas soluções infeasible
                        continue

                    # atualiza a solução atual da vizinhança para a primeira vez que acha 
                    if current_sol_swap == None:
                        current_sol_swap = aux_solution.copy()
                        current_dist_swap = dist_aux
                        current_move_swap = movement
                        current_feasible_flag = feasible_flag
                    # caso em que a distancia seja menor q a atual da vizinhança
                    elif dist_aux < current_dist_swap:
                        # criterio de aspiração
                        if movement not in tabu_list or dist_aux < best_sol:
                            current_sol_swap = aux_solution.copy()
                            current_dist_swap = dist_aux
                            current_move_swap = movement
                            current_feasible_flag = feasible_flag

    return current_sol_swap, current_dist_swap, current_move_swap, current_feasible_flag

def shift_loop(
        distances: np.array,
        solution: List[np.array], 
        dist_sol: float, 
        nodes: List[dict], 
        max_routes: int, 
        capacity: int, 
        tabu_list: List[Set], 
        best_sol: List[np.array], 
        current_feasible_flag: bool
    ) -> Tuple[List[np.array], float, Set, bool]:
    """
    Verifica a vizinhança da solucao fazendo movimentos do tipo shift. Ele retira o elemento
    de uma rota e adiciona para o final de outra rota. Ele leva em consideracao se a solucao
    recebida eh feasible ou nao. Caso a solucao for feasible, ele nao aceita solucoes nao
    feasibles. Retorna a melhor solucao encontrada, a distancia dela, o movimento tabu e 
    flag se a solucao encontrada eh feasible. 
    """
    current_sol_shift, current_dist_shift = None, None
    
    inicio = time.time()
    for rota_1 in range(0, max_routes):

        # Não faz shift se a rota só tem um elemento 
        if len(solution[rota_1]) == 1:
            continue
        
        for rota_2 in range(0, max_routes):
            # Passa o loop caso rota 1 seja igual a rota 2
            if rota_1 == rota_2:
                continue
            
            # testa shift de todas as cidades da rota 1 para a rota 2
            for i_cidade in range(len(solution[rota_1])):
                
                # Para se ultrapassar o tempo limite de uma busca local
                if (time.time() - inicio) > 30:
                    return current_sol_shift, current_dist_shift, current_move_shift, current_feasible_flag
                
                aux_solution, movement = shift(solution, rota_1, rota_2, i_cidade)                    

                dist_aux, feasible_flag = total_distance(distances, aux_solution, nodes, capacity)

                # se a solução atual eh feasible, não são aceitas soluções infeasible
                if not feasible_flag:
                    continue

                # atualiza a solução atual da vizinhança
                # Se for a primeira solucao criada no loop
                if current_sol_shift == None:
                    current_sol_shift = aux_solution.copy()
                    current_dist_shift = dist_aux
                    current_move_shift = movement
                    current_feasible_flag = feasible_flag
                
                # Se a distancia da solucao atual for menor que a distancia ja encontrada
                elif dist_aux < current_dist_shift:
                    if movement not in tabu_list or dist_aux < best_sol:
                        current_sol_shift = aux_solution.copy()
                        current_dist_shift = dist_aux
                        current_move_shift = movement
                        current_feasible_flag = feasible_flag

    
    return current_sol_shift, current_dist_shift, current_move_shift, current_feasible_flag
    