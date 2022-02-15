import numpy as np

def get_city(nodes:np.array, value:int) -> int:
    # returns city position from nodes list by the value of the index key
    for i, dic in enumerate(nodes):
        if dic['index'] == value:
            return i
    return -1

def city_capacity(nodes: np.array, index:int) -> float:
    # return city capacity, using index ordered list
    return nodes[get_city(nodes, index)]['capacity']

def sum_route_capacity(route:list[np.array], nodes:np.array) -> float:
    # sum all of city's capacity in route array
    return sum([city_capacity(nodes, city) for city in route])

def create_initial_sol(nodes:np.array, sorted_nodes:np.array, vehicles:int, limit:int) -> list[np.array]:
    solution = [np.zeros(1) for i in range(vehicles)]

    route = 0
    for node in sorted_nodes:
        while True:
            # if depot, skip
            if node['index'] == 0:
                break
            
            # if city's capacity plus route's capacity is less than or equal to the vehicles limit,
            # add it to route and finish searching for which route to add
            # else, see if city fits in next route
            if sum_route_capacity(solution[route], nodes) + node['capacity'] <= limit:
                if solution[route][0] != 0:
                    solution[route] = np.vstack([solution[route], node['index']])
                else: 
                    solution[route][0] = node['index']
                
                break
            else:
                route += 1

        # once all routes have been added something, go to the route #0,
        # elsewise, continue to next route
        if route == vehicles - 1:
            route = 0
        else:
            route += 1

    return solution
