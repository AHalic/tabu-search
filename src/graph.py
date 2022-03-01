from typing import Tuple, List

import numpy as np
from math import ceil

def create_node(coordinates:Tuple[int, float, float]) -> dict:
    """
    Dado o valor do indice e das coordenadas no formtato (indice, x, y),
    cria um dicionario com o valores das cidades. Em primeira instancia, 
    a capacidade de uma cidade eh igual a 0.
    """
    node = {
        'index': int(coordinates[0]) - 1,
        'x': float(coordinates[1]),
        'y': float(coordinates[2]),
        'capacity': 0 # initialized as 0
    }

    return node

def get_route(value: int, routes: List[np.array]) -> int:
    """
    Dado o valor da cidade e uma lista de rotas, pesquisa qual 
    eh o valor da rota que se encontra aquela cidade
    """
    for i, route in enumerate(routes):
        if value in route:
            return i
    
    return -1

def distance(node1: dict, node2: dict) -> float:
    """
    Dado dois nos, calcula a distancia euclediana
    """
    return ((node1['x'] - node2['x'])**2 + (node1['y'] - node2['y'])**2)**(1/2)

def route_distance(dist_array: np.array, route: np.array, nodes: List[dict], capacity: int) -> Tuple[float, bool]:
    """
    Calcula a distancia de uma rota e verifica se ela ultrapassa o limite da capacidade
    (se eh "feasible"). 
    """
    # Considera que a solucao nao ultrapassa o limite da capacidade
    feasible_flag = True

    # Pega distancia do depot para a primeria cidade da rota
    aux = dist_array[0][route[0]]

    for i in range(len(route) - 1): 
        if route[i] < route[i+1]:
            aux += dist_array[route[i]][route[i+1]]
        else:
            aux += dist_array[route[i+1]][route[i]]

    # Pega distancia da ultima cidade para o depot
    aux += dist_array[0][route[-1]]

    # Verifica a capacidade e se ultrapassa o limite adiciona uma penalidade
    capacity_r = sum_route_capacity(route, nodes)
    penalty = 1
    if capacity_r > capacity: 
        feasible_flag = False
        penalty += (capacity_r - capacity) / capacity 

    return aux * penalty, feasible_flag

def total_distance(dist_array: np.array, routes: List[np.array], nodes: np.array, capacity: int) -> Tuple[float, bool]:
    """
    Calcula a distancia total de todas as rotas e verifica se a solucao tem algum valor que
    ultrapassa o limite do veiculo. 
    """
    dist = 0
    feasible_flag = True
    for i in range(len(routes)):
        aux, feasible_flag_r = route_distance(dist_array, routes[i], nodes, capacity) 
        feasible_flag = feasible_flag and feasible_flag_r
        dist += aux
    
    return dist, feasible_flag

def clients_distance(nodes: List[dict], clients: int) -> np.array:
    """
    Cria matriz triangular tamanho clients x clients com a distancia entre
    os clientes.
    """
    distances = np.zeros((clients, clients),dtype=float)

    for i in range(clients):
        for j in range(i, clients):
            distances[i][j] = round(distance(nodes[i], nodes[j]), 0)

    return distances

def sum_route_capacity(route: np.array, nodes: List[dict]) -> float:
    """
    Soma a capacidade da rota. 
    """
    return sum([nodes[int(city)]['capacity'] for city in route])


def show_routes(distances:np.array, sol: List[np.array], nodes:np.array, capacity:int, file_writer) -> None:
    """
    Mostra rotas dado uma solucao e sua capacidade e distancia.s
    """
    dist = 0
    for i, route in enumerate(sol):
        # Mostra rota
        route_aux = route.flatten()
        file_writer.write(f'Rota #{i+1} - ')

        route_city = ""
        for route_i in route_aux.astype(int):

            route_city += f"{route_i} "

        file_writer.write(f'{route_city}\n')
        # Mostra capacidade

        file_writer.write(f'Capacidade: {sum_route_capacity(route, nodes)}\n')

        # Mostra distancia
        dist, _ = route_distance(distances, route, nodes, capacity)
        file_writer.write(f'Distancia da rota: {dist}\n')
    file_writer.write('\n')