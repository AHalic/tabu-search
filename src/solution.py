import numpy as np
import random

from graph import sum_route_capacity

ITER_SIZE = 100

def create_initial_sol(nodes:np.array, sorted_nodes:np.array, vehicles:int, limit:int) -> list[np.array]:
    solution = [np.zeros(1) for i in range(vehicles)]

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
# Faz o vizinho se n é tabuu -> vertifica se é melhor q o vizinho atual
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

def swap(routes, current_sol, best_sol, dist_sol, dist_best_sol):
    routes_flattened = routes.flatten()
    solution = np.copy(current_sol)
    
    for i in range(ITER_SIZE):
        city1 = random.choice(routes_flattened)
        city2 = city1
        while city2 != city1:
            city2 = random.choice(routes_flattened)

        tabu_move = set([city1, city2])
        print(solution[np.where(solution == city1)[0]])
        break



# def best_neighbor():
#     # of all neighbors, finds the one with the least time (distance)


#     aux = (solution, distance, tabu_move)
#     current = (solution, distance, tabu_move)
#     # find swap solutions (notall of them)    # find add/remotabu 
#     pass