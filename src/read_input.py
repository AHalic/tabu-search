from pydoc import cli
import re
import numpy as np

def create_node(coordinates):
    node = {
        'index': int(coordinates[0]) - 1,
        'x': float(coordinates[1]),
        'y': float(coordinates[2]),
        'capacity': 0 # initialized as 0
    }

    return node

def read_input(file):
    # regular expressions to get numbers from string
    regex = re.compile(r'\d+')

    # filename must be as X-n00-k00
    clients, vehicles = [int(k) for k in regex.findall(file)]

    with open(file) as f:
        # skips four first lines in file
        for _ in range(5):
            next(f)
        
        vehicle_capacity = [int(k) for k in regex.findall(f.readline())][0]
        next(f)

        nodes = np.zeros(clients, dtype=object)

        # reading nodes coordinates
        for i in range(clients):
            # TODO - usar map pra converter? mesmo que o primeiro n seja float
            nodes[i] = create_node(f.readline().split())
        next(f)

        # reading capacities
        for i in range(clients):
            nodes[i]['capacity'] = int(f.readline().split()[1])
        
        print(nodes)

