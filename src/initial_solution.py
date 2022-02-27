from typing import List

import numpy as np

from graph import sum_route_capacity
from utils import sort_with_key

def create_n_routes(clients: int) -> List[np.array]:
    """
    Cria lista de arrays em que cada array possui apenas o valor da cidade.
    """
    return [np.array([i]) for i in range(1, clients)]

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

def savings_initial_sol(dist: np.array, nodes:  List[dict], vehicles: int, clients: int, limit:int, penalidade:float=0.2) -> List[np.array]:
    """
    Cria solucao inicial considerando penalidade usando o metodo de Economia para criacao de solucoes.
    """
    # Calcula todas as economias
    best_savings = calculate_savings(nodes, dist, clients)

    # Ordena as economias por capacidade e o valor da economia, maior pro menor
    best_savings = sort_with_key(best_savings, 'saving')

    # Cria n rotas, com n = clients
    solution = create_n_routes(clients)

    # Junta rotas ate quantidade de rotas == veiculos. Permite penalidade
    while len(solution) > vehicles and len(best_savings) > 0:
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

def corrected_savings(distances: np.array, nodes:  List[dict], vehicles: int, clients: int, limit:int, penalidade:float=0.2) -> List[np.array]:
    savings_solution = savings_initial_sol(distances, nodes, vehicles, clients, limit, penalidade)

    # ordenar por capacidade

    # achar maior espaco livre

    # loop
    # pegar do inicio ou do fim, se for menor que o maior espaco livre
    # atualizar maior espaco livre    
    

def random_initial_sol(nodes: List[dict], vehicles:int, limit:int) -> List[np.array]:
    """
    Gera uma solucao inicial sem ultrapassar a capacidade maxima de cada veiculo. 
    Organiza os nos de forma da maior a menor capacidade e vai acrescentando nas rotas. 
    """
    sorted_nodes = sort_with_key(nodes.copy(), 'capacity')
    
    solution = [np.zeros(1).astype(int) for i in range(vehicles)]

    route = 0
    for node in sorted_nodes:
        # Se for o depot, pula
        if node['index'] == 0:
            break
        
        not_found = True
        while not_found:
            # Se a soma da capacidade da cidade com a rota eh menor que ou igual ao limite de
            # veicles, adiciona a rota e termina de procurar para qual rota a adiciona
            # caso contraio, ve se a cidade encaixa na proxima rota
            if sum_route_capacity(solution[route], nodes) + node['capacity'] <= limit:
                if solution[route][0] != 0:
                    solution[route] = np.append(solution[route], node['index'])
                else: 
                    solution[route][0] = node['index']
                not_found = False

            # Se todas rotas foram adicionada, vai para rota 0. 
            if route == vehicles - 1:
                route = 0
            # Caso contrario, vai para a proxima rota
            else:
                route += 1
            
    return solution