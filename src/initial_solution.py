from typing import List

import numpy as np

from graph import show_routes, sum_route_capacity
from utils import sort_with_key
from moves import shift

def create_n_routes(nodes: List[dict], clients: int) -> List[np.array]:
    """
    Cria lista de arrays em que cada array possui apenas o valor da cidade.
    """
    return [{"route": np.array([i]), "capacity": nodes[i]['capacity']} for i in range(1, clients)]

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
                aux['saving'] = dist[0][i] + dist[0][j] - dist[i][j]

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
    solution = create_n_routes(nodes, clients)

    count = 0

    # Junta rotas ate quantidade de rotas == veiculos. Permite penalidade
    while len(solution) > vehicles and len(best_savings) > 0:
        # Tupla de economia, com o valor da economia e as cidades que pertence
        saving_tuple = best_savings.pop(0)
        count += 1

        # Valores das cidades da economia
        i = saving_tuple['cities'][0]
        j = saving_tuple['cities'][1]

        
        # Nao foi encontrado rotas que tem as cidades i e j
        route_i = False
        route_j = False

        # Procura rotas que tem cidade i e j
        index = 0
        while index < len(solution) and not (route_i and route_j):
            route = solution[index]['route']
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
        aux_capacity = sum_route_capacity(route, nodes)

        # A rota unida esta vazia ou ultrapassou penalidade% da capacidade
        if not len(route) or aux_capacity > (limit * (1 + penalidade)):
            continue
        
        # Retira rota das solucoes e dps adiciona de novo
        if route_i[1] > route_j[1]:
            solution.pop(route_i[1])
            solution.pop(route_j[1])
        else:
            solution.pop(route_j[1])
            solution.pop(route_i[1])

        solution.append({'route': route, 'capacity': aux_capacity})

    return solution

def check_free_space(limit: int, solution: List[dict]) -> int:
    max_free_space = limit - solution[0]['capacity']
    for route in solution[1:]:
        aux_max = limit - route['capacity']

        if aux_max > max_free_space:
            max_free_space = aux_max

    return max_free_space

def find_city_less_capacity(nodes: List[dict], route: dict, max_free_space: int) -> int:

    for i, city in enumerate(route['route']):
        if nodes[city]['capacity'] <= max_free_space:
            return i

    return -1

def corrected_savings(distances: np.array, nodes:  List[dict], vehicles: int, clients: int, limit:int, penalidade:float=0.2) -> List[np.array]:
    # Cria solucao de savings e a ordena
    savings_solution = savings_initial_sol(distances, nodes, vehicles, clients, limit, penalidade)
    savings_solution_sorted = sort_with_key(savings_solution, 'capacity')  
    new_solution = [np.array(route['route']) for route in savings_solution_sorted]

    # Se a primeira rota ultrapassa em limite, a solucao nao eh feasible
    if savings_solution_sorted[0]['capacity'] > limit:
        index = 0

        # Contador de indices de rotas que estao feasible
        index_count = set()

        while True:
            max_free_space = check_free_space(limit, savings_solution_sorted)

            # Se verificou todas as rotas, voltar para o inicio
            if index == vehicles:
                index = 0
            
            # Se todas as rotas que contou sao feasibles
            if len(index_count) == vehicles:
                break
            
            # Se a rota atual eh feasible, atualiza o contador e o indice
            elif savings_solution_sorted[index]['capacity'] <= limit:
                index_count.add(index)
                index += 1
                continue                
            
            route_origin = savings_solution_sorted[index]
    
            # Escolhe qual cidade vai retirar da rota
            if nodes[route_origin['route'][-1]]['capacity'] <= max_free_space:
                city = -1
            elif nodes[route_origin['route'][0]]['capacity'] <= max_free_space:
                city = 0            
            else:
                city = find_city_less_capacity(nodes, route_origin, max_free_space)
                if city == -1:
                    print("Não tem rota com capacidade")

                    if penalidade == 2:
                        quit()
                    penalidade += 0.1
                    return corrected_savings(distances, nodes, vehicles, clients, limit, penalidade)

            aux_index = 0

            # Pega informacoes da cidade que vai ser modificada
            city_number = route_origin['route'][city]
            city_origin_capacity = nodes[city_number]['capacity']

            # Procura uma rota para adicionar
            while aux_index < vehicles:
                route_destiny = savings_solution_sorted[aux_index]

                # Se a capacidade da rota passa do limite
                if route_destiny['capacity'] > limit:
                    aux_index += 1
                    continue
                # Se a diferenca de limite e da capacidade for suficiente para adicionar a cidade
                elif limit - route_destiny['capacity'] >= city_origin_capacity:
                    # Atualiza origem e destino
                    route_destiny['route'] = np.concatenate((route_destiny['route'], city_number), axis=None)
                    route_origin['route'] = np.delete(route_origin['route'], city, axis=None)

                    route_destiny['capacity'] = sum_route_capacity(route_destiny['route'], nodes)
                    route_origin['capacity'] = sum_route_capacity(route_origin['route'], nodes)

                    savings_solution_sorted[aux_index] = route_destiny
                    savings_solution_sorted[index] = route_origin

                    # Atualiza nova solucao
                    new_solution, _ = shift(new_solution, index, aux_index, city)
                    break
                else:
                    aux_index += 1
                    
            index += 1

    return new_solution
    

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