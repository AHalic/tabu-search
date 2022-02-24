from typing import List, Tuple

import numpy as np
import random
from math import ceil 

from graph import sum_route_capacity, route_distance, total_distance

ITER_SIZE = 100

def sort_with_key(routes: List[dict], key: str, reverse:bool=True) -> List[dict]:
    """
    Ordena lista de dicionario de forma descresncete com base no string utilizada
    Caso reverse=False, os valores estarao em ordem crescente.
    """
    return sorted(routes, key=lambda item: item[key], reverse=reverse) 

def calculate_savings(nodes: List[dict], dist: np.array, clients: int) -> List[dict]:
    """
    Dado uma lista de nos, uma matriz de distancias e quantidade de clientes, cria
    uma lista de dicionarios com as economias de cada combinacao de dupla.

    Cada indice possui um dicionario com as chaves: 
    - "saving": float
    - "cities": Tuple[int, int]
    - "capacity": float

    """
    best_savings = []
    for i in range(clients):
            for j in range(i+1, clients):
                aux = dict()
                # Calculo de economia di0 + doj - dij
                aux['saving'] = dist[i][0] + dist[0][j] - dist[i][j]

                # Valor negativo de economia nao eh triangulo
                # Valor nulo de economia eh ligacao depot - cidade - depot
                if aux['saving'] <= 0:
                    continue 

                aux['cities'] = (i, j)
                aux['capacity'] = sum_route_capacity([i, j], nodes)

                best_savings.append(aux)
    
    return best_savings

"""
(8, 11)

8 2 3 1
11 5 6 7
1 3 2 8 11 5 6 7

8 2 3 1
7 5 6 11
7 5 6 11 8 2 3 1

1 2 3 8
7 5 6 11
1 2 3 8 11 6 5 7

1 2 3 8
11 5 6 7
1 2 3 8 11 5 6 7

"""


def join_route(route1, route2, value1, value2):
    """
    Une rotas quando os valores se encontram no inicio ou no fim das listas.
    Se valor estiver no meio da lista, nao tem como unir, pois nao estaria
    respeitando as economias anteriores. Conforme isso, retorna uma lista 
    vazia para representar esta situacao.
    """

    if route1[0] == value1 and route2[0] == value2:
        route = np.concatenate((np.flipud(route1), route2), axis=None)
    elif route1[0] == value1 and route2[-1] == value2:
        route = np.concatenate((route2, route1), axis=None)
    elif route1[-1] == value1 and route2[-1] == value2:
        route = np.concatenate((route1, np.flipud(route2)), axis=None)
    elif route1[-1] == value1 and route2[0] == value2:
        route = np.concatenate((route1, route2), axis=None)  
    else:
        return []
    
    return np.array(list(dict.fromkeys(route)))

def create_n_routes(clients: int) -> List[np.array]:
    """
    Cria lista de arrays em que cada array possui apenas o valor da cidade.
    """
    return [np.array([i]) for i in range(1, clients)]

def savings_initial_sol(dist: np.array, nodes:  List[dict], vehicles: int, clients: int, limit:int, penalidade:float=0.2) -> List[np.array]:
    """
    Cria solucao inicial considerando penalidade usando o metodo de Economia para criacao de solucoes.
    """
    # Calcula todas as economias
    best_savings = calculate_savings(nodes, dist, clients)

    # Ordena as economias por capacidade e o valor da economia, maior pro menor
    # best_savings = sort_with_key(best_savings, 'capacity', reverse=False)
    best_savings = sort_with_key(best_savings, 'saving')

    # Cria n rotas, com n = clients
    solution = create_n_routes(clients)

    # Junta rotas ate quantidade de rotas == veiculos. Permite penalidade
    savings_penalty = []
    while len(solution) > vehicles:
        # Tupla de economia, com o valor da economia e as cidades que pertence
        saving_tuple = best_savings.pop(0)

        # Valores das cidades da economia
        i = saving_tuple['cities'][0]
        j = saving_tuple['cities'][1]
        
        # Nao foi encontrado rotas que tem as cidades i e j
        route_i = False
        route_j = False

        # Procura rotas que tem cidade i e j
        index = 0
        while index < len(solution) and not (route_i and route_j):
            route = solution[index]
            if i in route:
                route_i = (route, index)
            if j in route:
                route_j = (route, index)
            index += 1

        # Caso em que cidades i e j estao na mesma rota
        if route_i[1] == route_j[1]:
            continue

        # Une cidades
        route = join_route(route_i[0], route_j[0], i, j)

        # A rota unida esta vazia ou ultrapassou penalidade% da capacidade
        if not len(route) or sum_route_capacity(route, nodes) > (limit * (1 + penalidade)):
            continue
        
        # Retira rota das solucoes e dps adiciona de novo
        if route_i[1] > route_j[1]:
            solution.pop(route_i[1])
            solution.pop(route_j[1])
        else:
            solution.pop(route_j[1])
            solution.pop(route_i[1])

        solution.append(route)

    return solution

def random_initial_sol(nodes: List[dict], sorted_nodes: List[dict], vehicles:int, limit:int) -> List[np.array]:
    solution = [np.zeros(1).astype(int) for i in range(vehicles)]

    route = 0
    for node in sorted_nodes:
        # if depot, skip
        if node['index'] == 0:
            break
        
        not_found = True
        while not_found:
            # if city's capacity plus route's capacity is less than or equal to the vehicles limit,
            # add it to route and finish searching for which route to add
            # else, see if city fits in next route
            if sum_route_capacity(solution[route], nodes) + node['capacity'] <= limit:
                if solution[route][0] != 0:
                    solution[route] = np.append(solution[route], node['index'])
                    # solution[route] = np.vstack([solution[route], node['index']])
                else: 
                    solution[route][0] = node['index']
                not_found = False
                
            # once all routes have been added something, go to the route #0,
            # elsewise, continue to next route
            if route == vehicles - 1:
                route = 0
            else:
                route += 1
            
    return solution


def swap(solution, i_r1=-1, i_r2=-1, i_c1=-1, i_c2=-1, nodes=None):
    # new_solution = solution.copy()
    new_solution = [np.copy(route) for route in solution]

    # Choose random routes to swap
    if i_r1 == -1:
        i_r1 = random.randrange(0, len(solution))
    if i_r2 == -1:
        i_r2 = random.randrange(0, len(solution))

    route1 = new_solution[i_r1]
    route2 = new_solution[i_r2]

    # Choose random cities in routes to swap
    if i_c1 == -1:
        i_c1 = random.randrange(0, len(route1))
    
    if i_c2 == -1:
        i_c2 = random.randrange(0, len(route2))

    city1 = route1[i_c1]
    city2 = route2[i_c2]
    # print('swap:', city1, city2)

    # Swap and create tabu move and solution
    route1[i_c1], route2[i_c2] = city2, city1
    new_solution[i_r1], new_solution[i_r2] = route1, route2

    tabu_move = set([city1, city2])

    return new_solution, tabu_move
    
def shift(solution, r_o, r_d, i_c):
    new_solution = [np.copy(route) for route in solution]
    new_solution[r_d] = np.concatenate((solution[r_d], solution[r_o][i_c]),axis=None)
    new_solution[r_o] = np.delete(new_solution[r_o], i_c, axis=None)
    tabu_move = (solution[r_o][i_c])
    return new_solution, tabu_move


def best_neighbor(solution, dist_sol, nodes, max_routes, capacity, tabu_list, tenure):
    current_sol_swap, current_dist_swap = None, None
    count_swaps = 0
    for i in range(0, max_routes):
        # print(int(ceil(len(solution[i]) / 2)))
        c1_indexes = random.sample(range(len(solution[i])), k=int(ceil(len(solution[i]) / 2)))
        # print('c1', c1_indexes)
        for j in range(i, max_routes):
            # Realiza o movimento swap
            # print('r2', solution[j])
            for i_c1 in c1_indexes:
                for i_c2 in range(len(solution[j])):
                    count_swaps += 1
                    aux_solution, movement = swap(solution, i, j, i_c1, i_c2, nodes=nodes)
                    # show_route(aux_solution, nodes)
                    # print()

                    # Calcula a capacidade das novas rotas
                    penalty_r1 = 1
                    penalty_r2 = 1
                    capacity_r1 = sum_route_capacity(aux_solution[i], nodes)
                    capacity_r2 = sum_route_capacity(aux_solution[j], nodes)
                    
                    if capacity_r1 > capacity: 
                        penalty_r1 += (capacity_r1 - capacity) / capacity 
                    if capacity_r2 > capacity:
                        penalty_r2 += (capacity_r2 - capacity) / capacity 


                    
                    # Calcula a distancia das novas rotas
                    if i != j:
                        dist_aux = dist_sol - route_distance(solution[i], nodes) - route_distance(solution[j], nodes) 
                        dist_aux += route_distance(aux_solution[i], nodes) * penalty_r1 + route_distance(aux_solution[j], nodes) * penalty_r2
                    if i == j:
                        dist_aux = dist_sol - route_distance(solution[i], nodes)
                        dist_aux += route_distance(aux_solution[i], nodes) * penalty_r1
                    # print('\ndist: ', dist_aux, 'sol 1', route_distance(solution[i], nodes), 'sol2', route_distance(solution[j], nodes) )
                    # print('result dist: ', dist_aux)

                    # atualiza a solução atual da vizinhança para a primeira vez que acha 
                    if current_sol_swap == None:
                        current_sol_swap = aux_solution.copy()
                        current_dist_swap = dist_aux
                        current_move_swap = movement
                    elif dist_aux < current_dist_swap:
                        if movement not in tabu_list or dist_aux < dist_sol:
                            current_sol_swap = aux_solution.copy()
                            current_dist_swap = dist_aux
                            current_move_swap = movement


    count_shifts = 0
    current_sol_shift, current_dist_shift = None, None
    for i in range(0, max_routes):
        # Não faz shift se a rota só tem um elemento 
        if len(solution[i]) == 1:
            continue
        for j in range(i + 1, max_routes):
            for i_c in range(len(solution[i])):
                count_shifts += 1

                aux_solution, movement = shift(solution, i, j, i_c1)
                    

                penalty_r1 = 1
                penalty_r2 = 1
                capacity_r1 = sum_route_capacity(aux_solution[i], nodes)
                capacity_r2 = sum_route_capacity(aux_solution[j], nodes)
                
                if capacity_r1 > capacity: 
                    penalty_r1 += (capacity_r1 - capacity) / capacity 
                if capacity_r2 > capacity:
                    penalty_r2 += (capacity_r2 - capacity) / capacity 

                # Calcula a distancia das novas rotas
                dist_aux = dist_sol - route_distance(solution[i], nodes) - route_distance(solution[j], nodes) 
                dist_aux += route_distance(aux_solution[i], nodes) *penalty_r1 + route_distance(aux_solution[j], nodes) * penalty_r2

                # atualiza a solução atual da vizinhança
                if current_sol_shift == None:
                    current_sol_shift = aux_solution.copy()
                    current_dist_shift = dist_aux
                    current_move_shift = movement
                elif dist_aux < current_dist_shift:
                    if movement not in tabu_list or dist_aux < dist_sol:
                        current_sol_shift = aux_solution.copy()
                        current_dist_shift = dist_aux
                        current_move_shift = movement

    # print('shift')
    # print(current_sol_shift, current_dist_shift)
    # print('swap')
    # print(current_sol_swap, current_dist_swap)

    if current_dist_swap < current_dist_shift:
        if len(tabu_list) == tenure:
            tabu_list.pop(0)
        tabu_list.append(current_move_swap)
        return current_sol_swap, current_dist_swap, tabu_list
    else:
        if len(tabu_list) == tenure:
            tabu_list.pop(0)
        tabu_list.append(current_move_shift)
        return current_sol_shift, current_dist_shift, tabu_list
        


    




#     Retorno de swap e shift: (solution, tabu_move)

# TODO
# - func shift
# - calcular capacidade e distancia da solucao criada
# - verificar se eh uma solucao dentro do limite de capacidade
# - ver se o movimento eh tabu
# - se for tabu, considerar como solucao se for melhor que a melhor solucao
# - melhor solucao da vizinhança vira a current_solucao
# - tempo para delimitar o algoritmo
# - decidir outras condicoes paradas 

# TODO
# Na busca de soluções:
# Faz o vizinho se n é tabu -> verifica se é melhor q o vizinho atual
#   se é tabu -> calcula a distancia e ve se é melhor q a melhor solução (aspiration)
#  apenas armazena a melhor e o atual, as distancias e o movimento tabu
# Movimentos -> primeiro y swaps (escolher melhor movimento)
# Verificar tempo para swap com:
#   - todas possibilidades de swap
#   - x iterações, com x variando entre x1 = 10 x2 = 50 x3 = 100 x4 = 1000
# Melhor solução atual sempre é o resultado da busca de vizinhaça
# Melhor solução geral precisa ser sempre compara a melhor solução atual

# Lista tabu:
# Tupla: (cidade1, rota_destino), ([c1, c2], rt1, rt2), (rt1, rt2), {c1, c2}
#      - escolher só (c1, c2)
# Tenure: 15, static

# Critério de parada:
# - Tempo max: 300s
# - x iterações sem modificação. x1 = 10 x2 = 50 x3 = 100 x4 = 1000