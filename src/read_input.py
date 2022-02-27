from typing import Tuple, List
import re
import numpy as np

from graph import create_node

def read_input(file: str) -> Tuple[List[dict], int, int, int]:
    """
    Faz a leitura do arquivo de entrada. Arquivo deve ter a mesma estrutura
    que os arquivos de Augerat e Fisher do site http://vrp.atd-lab.inf.puc-rio.br/index.php/en/
    """
    # Expressao regular para obter numeros da string
    regex = re.compile(r'\d+')

    # Nome do arquivo deve ter formato X-n00-k00
    clients, vehicles = [int(k) for k in regex.findall(file)]

    with open(file) as f:
        # Pula as primeiras 4 linhas do arquivo
        for _ in range(5):
            next(f)
        
        vehicle_capacity = [int(k) for k in regex.findall(f.readline())][0]
        next(f)

        nodes = np.zeros(clients, dtype=object)

        # Leitura das coordenadas dos nos
        for i in range(clients):
            nodes[i] = create_node(f.readline().split())
        next(f)

        # Ler as capacidades das cidades
        for i in range(clients):
            nodes[i]['capacity'] = int(f.readline().split()[1])
        
    return nodes, vehicles, clients, vehicle_capacity