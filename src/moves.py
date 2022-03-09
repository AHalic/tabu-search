from typing import List, Set, Tuple
import numpy as np
import random

def swap(solution:List[np.array], i_r1:int=-1, i_r2:int=-1, i_c1:int=-1, i_c2:int=-1) -> Tuple[List[np.array], Set]:
    """
    Recebe a solução atual, os indices das rotas e das cidades de cada rota que serão trocadas
    É retornada a nova solução e o movimento feito para gerar esta
    """
    new_solution = [np.copy(route) for route in solution]

    # Escolhe rotas aleatorias para trocar
    if i_r1 == -1:
        i_r1 = random.randrange(0, len(solution))
    if i_r2 == -1:
        i_r2 = random.randrange(0, len(solution))

    route1 = new_solution[i_r1]
    route2 = new_solution[i_r2]

    # Escolhe cidades aleatorias para trocar
    if i_c1 == -1:
        i_c1 = random.randrange(0, len(route1))
    
    if i_c2 == -1:
        i_c2 = random.randrange(0, len(route2))

    city1 = route1[i_c1]
    city2 = route2[i_c2]

    # Troca as cidades e cria o movimento tabu
    route1[i_c1], route2[i_c2] = city2, city1
    new_solution[i_r1], new_solution[i_r2] = route1, route2

    tabu_move = set([city1, city2])

    return new_solution, tabu_move
    
def shift(solution:List[np.array], r_o:int, r_d:int, i_c:int) -> Tuple[List[np.array], Set]:
    """
    Recebe a solução atual, os indices das rotas de origem e destino e o indice da cidade
    A cidade é removida da rota de origem e inserida ao fim da rota de destino
    É retornada a nova solução e o movimento feito para gerar esta
    """
    new_solution = [np.copy(route) for route in solution]
    new_solution[r_d] = np.concatenate((solution[r_d], solution[r_o][i_c]),axis=None)
    new_solution[r_o] = np.delete(new_solution[r_o], i_c, axis=None)
    
    # cria o movimento tabu
    tabu_move = set([solution[r_o][i_c]])

    return new_solution, tabu_move
