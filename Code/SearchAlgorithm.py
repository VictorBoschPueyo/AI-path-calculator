from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    path_list = []
    station = path.last
    connections = map.connections[station]

    for conn in connections.keys():
        copy_path = copy.deepcopy(path)
        copy_path.add_route(conn)
        path_list.append(copy_path)
    return path_list


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    new_path_list = []
    
    for path in path_list:
        ruta = path.route
        last = ruta[-1]
        pre = ruta[: len(ruta)-1 ]
        if last not in pre:
            new_path_list.append(path)

    return new_path_list


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    
    return expand_paths + list_of_path


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    cami = Path(origin_id)
    llista =[cami]
    while (llista[0].last != destination_id and len(llista) != 0):
        head = llista[0]
        e = expand(head, map)
        llista.pop(0)
        r = remove_cycles(e)
        llista = insert_depth_first_search(r, llista)
           
    return llista[0]


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return list_of_path + expand_paths


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    cami = Path(origin_id)
    llista =[cami]
    while (llista[0].last != destination_id and len(llista) != 0):
        head = llista[0]
        e = expand(head, map)
        llista.pop(0)
        r = remove_cycles(e)
        llista = insert_breadth_first_search(r, llista)
           
    return llista[0]


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    
    for path in expand_paths:
        ult = path.last
        penult = path.penultimate
        
        if type_preference == 0: #adjacency
            if (len(path.route) > 1):
                path.update_g(1)
        elif type_preference == 1: #minimum time
            path.update_g(map.connections[penult][ult])  
        elif type_preference == 2: #minimum dist
            if map.stations[ult]['line'] == map.stations[penult]['line']:
                t = map.connections[penult][ult]
                v = map.velocity[map.stations[ult]['line']]
                dist = t * v
                path.update_g(dist)
        elif type_preference == 3: #minimum transf
            if map.stations[ult]['line'] != map.stations[penult]['line']:
                path.update_g(1)
    
    return expand_paths


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    paths = expand_paths + list_of_path
    paths.sort(key=lambda x: x.g, reverse=False)
    paths.sort(key=lambda x: len(x.route), reverse=False)
    
    return paths


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    cami = Path(origin_id)
    llista =[cami]
    while (llista[0].last != destination_id and len(llista) != 0):
        head = llista[0]
        e = expand(head, map)
        llista.pop(0)
        r = remove_cycles(e)
        llista_costos = calculate_cost(r, map, type_preference)
        llista = insert_cost(llista_costos, llista)
           
    return llista[0]


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    
    velMax = 0
    velocitats = map.velocity
    for vel in velocitats.values():
            if velMax < vel:
                velMax = vel
    
    for path in expand_paths:
        ult = path.last
        
        if type_preference == 0: #adjacency
            if ult != destination_id:
                path.update_h(1)
            else:
                path.update_h(0)
                
        elif type_preference == 1: #minimum time
            if ult != destination_id:
                x = (map.stations[ult]['x'], map.stations[ult]['y'])
                y = (map.stations[destination_id]['x'], map.stations[destination_id]['y'])
                distEucl = euclidean_dist(x, y)
                path.update_h(distEucl / velMax)
            else:
                path.update_h(0)
             
        elif type_preference == 2: #minimum dist
            if ult != destination_id:
                x = (map.stations[ult]['x'], map.stations[ult]['y'])
                y = (map.stations[destination_id]['x'], map.stations[destination_id]['y'])
                distEucl = euclidean_dist(x, y)
                path.update_h(distEucl)
            else:
                path.update_h(0)
            
        elif type_preference == 3: #minimum transf
            if map.stations[ult]['line'] != map.stations[destination_id]['line']:
                path.update_h(1)
            else:
                path.update_h(0)
    
    return expand_paths


def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.update_f()
        
    return expand_paths


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g in this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
    """
    exp_path_ret = []
    list_of_path_ret = copy.deepcopy(list_of_path)
    for exp_path in expand_paths:
        cost = exp_path.g
        ult = exp_path.last
        if (ult not in visited_stations_cost.keys()):
            visited_stations_cost[ult] = cost
            exp_path_ret.append(exp_path)
        elif (visited_stations_cost[ult] > cost):
            visited_stations_cost[ult] = cost
            exp_path_ret.append(exp_path)
            
            aux = []
            for path in list_of_path_ret:
                if ult not in path.route:
                    aux.append(path)
                    
            list_of_path_ret = copy.deepcopy(aux)
            
    return exp_path_ret, list_of_path_ret, visited_stations_cost


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    paths = expand_paths + list_of_path
    paths.sort(key=lambda x: x.f, reverse=False)
    paths.sort(key=lambda x: len(x.route), reverse=False)
    
    return paths


def coord2station(coord, map):
    """
        From coordinates, it searches the closest station.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """
    
    distMin = 9999
    for estacio in map.stations.keys():
        x = map.stations[estacio]['x']
        y = map.stations[estacio]['y']
        dist = math.sqrt( ((x - coord[0])**2) + ((y - coord[1])**2) )
        if distMin > dist:
            distMin = dist
            
    retorn = []
    
    for estacio in map.stations.keys():
        x = map.stations[estacio]['x']
        y = map.stations[estacio]['y']
        dist = math.sqrt( ((x - coord[0])**2) + ((y - coord[1])**2) )
        if distMin == dist:
            retorn.append(estacio)
    
    return retorn


def Astar(origin_coor, dest_coor, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (list): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    est_origen = coord2station(origin_coor, map)[0]
    est_dest = coord2station(dest_coor, map)[0]
    visited_stations_cost = {}
    cami = Path(est_origen)
    llista =[cami]
    while (llista[0].last != est_dest and len(llista) != 0):
        head = llista[0]
        e = expand(head, map)
        r = remove_cycles(e)
        h = calculate_heuristics(r, map, est_dest, type_preference)
        c = calculate_cost(h, map, type_preference)
        f = update_f(c)
        camins_no_redu, llista, visited_stations_cost  = remove_redundant_paths(f, llista, visited_stations_cost)
        llista.pop(0)
        llista = insert_cost_f(camins_no_redu, llista)
        
    return llista[0]
    
    















