import sys

from read_input import read_input
from tabu_list import algorithm

if __name__ == '__main__':
    args = sys.argv

    tenure = 8
    num_iteration = 500

    if len(args) > 1:
        nodes, vehicles, clients, vehicle_capacity = read_input(args[1])
        algorithm(nodes, vehicles, clients, vehicle_capacity, tenure, num_iteration)
    else:
        print("File not informed")
        nodes, vehicles, clients, vehicle_capacity = read_input('input/A-n32-k5.vrp')
        algorithm(nodes, vehicles, clients, vehicle_capacity, tenure, num_iteration)

    