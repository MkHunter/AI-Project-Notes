# Install GLFW Before anything else...
# https://github.com/p5py/p5/issues/54
# https://github.com/p5py/p5/issues/76
from p5 import *
import pandas as pd
import City
import MapDisplay
from collections import OrderedDict 
from operator import getitem
import sys

def citiesNameToList(set_cities):
    c_set = []
    for item in set_cities:
        c_set.append(item.getName())
    c_set = np.array(c_set) 
    return list(np.unique(c_set))

def getcities(city_coords,neighbors):
    cities = []
    for city_id in range(0,len(city_coords)):
        city = city_coords.iloc[city_id]
        name = city.Name
        neighbor = neighbors[name]
        location = {"x":city.Location_x,"y":city.Location_y}
        cities.append(City.City(name,location,neighbor,Gx=0))
    return cities

def getCityByName(city_name):
    global cities
    for city in cities:
        if city.getName() == city_name:
          return city
    return None

def getneighbors(city_routes, unique_cities):
    neighbors = {}
    for name_id in range(0,len(unique_cities)):
        neighbors.update({unique_cities[name_id]:[]})
        
    for city_id in range(0,len(city_routes)):
        city   = city_routes.iloc[city_id]
        city_0 = city[0]
        city_1 = city[1]
        neighbors[city_0].append(city_1)
        neighbors[city_1].append(city_0)
    return neighbors

def initialize():
    global city_routes, neighbors,cities
    global Actual_City, End_City,OpenSet
    # It is assumed that cities.csv contains just 
    unique_cities = city_coords["Name"]
    neighbors = getneighbors(city_routes,unique_cities)
    cities = getcities(city_coords,neighbors)
    
    Start_City = input("Type the Name of the City where you want to start searching: ")#"Baja California"
    End_City = input("Type the Name of the City you would like to travel to: ")#"Yucatan"
    Start_City = getCityByName(Start_City)
    End_City = getCityByName(End_City)
    Actual_City = Start_City
    OpenSet = [Actual_City]


map_img = load_image("Map.jpg")
city_coords = pd.read_csv("cities.csv")
city_routes = pd.read_csv("routes.csv")

Gx = 0
Actual_City = ""
End_City = ""
OpenSet = []
ClosedSet = []
neighbors = []
cities = []

def setup():
    size(1050,700)
    initialize()
    no_stroke()
    title("A * Algorithm")

def heuristicNeighbor(actual_city,end_city,Gx,cities,openset,closedset):
    # Recover the location and neighbors of the actual_city
    a_city = actual_city
    a_city_loc = a_city.getLocation()
    a_city_Gx = a_city.getGx()
    # Recover the location of the end_city
    e_city = end_city
    e_city_loc = e_city.getLocation()
    print("=============== Calculate cost path ======================")
    print("Actual_city: ",a_city_loc,"\nEnd_city: ",e_city_loc)
    neigh_heuristics = []
    for n_city in cities:
        # For every city, check if it's a city of the actual city.
        # In the same way, check if you have not visited it before.
        if n_city.neighborOf(a_city.getName()) and not n_city in closedset:
            #Reeover the location of the neighbor_city
            n_city_loc = n_city.getLocation()

            n_city_Gx = n_city.getGx()
            print("Neighbor_city of ",n_city.getName(),": ",n_city_loc)
            # Heuristic used in A Star Algorithm.
            # f(x) = g(x) + h(x)
            # Distance from the actual city to the neighbor city
            _gx = a_city_Gx + int(dist((a_city_loc["x"],a_city_loc["y"]), (n_city_loc["x"],n_city_loc["y"])))
            n_city.setGx(_gx)
            # Distance from the neighbor city to the end city
            _hx = int(dist((e_city_loc["x"],e_city_loc["y"]), (n_city_loc["x"],n_city_loc["y"])))

            _fx = _gx + _hx
            #print("Fx: ",_fx," = Gx: ",_gx," + Hx: ",_hx)
            neigh_heuristics.append([n_city.name,_fx,_gx,_hx])
    return neigh_heuristics

visited_cities   = []
Offspring = []

def AStar():
    global map_img, city_coords,city_routes,cities,neighbors
    global ClosedSet, OpenSet, Actual_City,End_City,Gx,Offspring

    visited_cities = ClosedSet
    visited_cities.append(Actual_City)
    #printset(visited_cities)
    # Display the map
    MapDisplay.displayMap(map_img,neighbors,cities,visited_cities)
    # Check if you get to the goal...
    if Actual_City.getName() == End_City.getName():
        print(str(Actual_City)+"You arrived to your desired location\n"+str(End_City))
        no_loop()
        return
    
    # Check if you con continue searching...
    if not bool(OpenSet):
        print("The desired location is out of reach")
        no_loop()
        return

    OpenSet.remove(Actual_City)
    ClosedSet.append(Actual_City)
    print("Visited Cities: "+str(citiesNameToList(ClosedSet)))

    Offspring = Offspring + heuristicNeighbor(Actual_City,End_City,Gx,cities,OpenSet,ClosedSet)
    Sorted_Offspring = pd.DataFrame(Offspring, columns=["Name","Fx","Gx","Hx"])
    Sorted_Offspring = Sorted_Offspring.sort_values(by ="Fx" , ascending=True)
    #We filter the Cities that have already been visited
    #Sorted_Offspring = Sorted_Offspring  #list(OrderedDict(sorted(Offspring.items(),key = lambda x: getitem(x[1], "Fx"))).items())
    Sorted_Offspring = Sorted_Offspring[~Sorted_Offspring["Name"].isin(citiesNameToList(ClosedSet))]
    print("Sorted OffSpring = ")
    print(Sorted_Offspring)
    #The new Actual_City has the lowest Cost Path (Fx)
    Actual_City = getCityByName(Sorted_Offspring.iloc[0]["Name"])
    Gx = Sorted_Offspring.iloc[0]["Gx"]
    OpenSet.append(Actual_City)
    print("New Actual_City: ",Actual_City.getName()," New Gx= ",Gx)
    #Actual_City,Gx = 
    
def draw():
    AStar()

run(frame_rate=2)