from typing import List

import numpy as np
import random
from math import ceil

from graph import sum_route_capacity, route_distance

ITER_SIZE = 100

def create_initial_sol(nodes:np.array, sorted_nodes:np.array, vehicles:int, limit:int) -> List[np.array]:
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

#TO DO:
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

def swap(solution, dist_sol, nodes, i_r1=-1, i_r2=-1, i_c1=-1, i_c2=-1):
    new_solution = solution.copy()

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

    # Swap and create tabu move and solution
    route1[i_c1], route2[i_c2] = city2, city1
    new_solution[i_r1], new_solution[i_r2] = route1, route2
    
    tabu_move = set([city1, city2])

    return new_solution, tabu_move, (i_r1, i_r2)



    # dist_aux = dist_sol - route_distance(route1, nodes) - route_distance(route2, nodes) 
    # dist_aux += route_distance(route1, nodes) + route_distance(route2, nodes) 
    # print('dist', dist_aux) 
    
# No best neighbor -> realiza o swap calcula para a nova solução a nova distancia e
# a capacidade das rotas modificadas, se a capacidade for maior então refaz o movimento

def best_neighbor(solution, best_solution, nodes, max_routes):
    # swap cidades 1 e 9
    # swap {c1, c2}
    # lista tabu
    # 10 rotas
    # 10 + 9 + 8 + 7 + 6 + 5 + 4 + 3+ 2 + 1 = 55 swaps
    # 10 interswaps, 45 outerswaps

    # 4 rotas
    # 4 + 3 + 2 + 1 = 10 swaps
    # 4 interswaps, 6 outerswaps

    # shift {c3}
    # {c1}



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
