from copy import copy
from read_input import *
from graph import *
from solution import *

file = "./input/Augerat/A-VRP/A-n33-k6.vrp"

nodes, vehicles, clients, vehicle_capacity = read_input(file)

sorted_nodes = sort_nodes(nodes)

current_sol = create_initial_sol(nodes, sorted_nodes, vehicles, vehicle_capacity)
best_sol = copy(current_sol)

#print(current_sol)

for i, route in enumerate(current_sol):
    print(f"Route #{i+1}. Capacity: {sum_route_capacity(route, nodes)}")