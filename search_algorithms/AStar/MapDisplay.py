from p5 import *
import City

def cit_visited(cityname,visited_list):
    for visit in visited_list:
        if visit.getName() == cityname:
            return True
    return False

def displayRoutes(cities,visited_cities):
    stroke(255,164,27)
    stroke_weight(2)
    for city in cities:
        _city_location = city.getLocation()
        _city_location = (_city_location["x"],_city_location["y"])

        _neighbors     = city.getNeighbors()
        for neighbor in _neighbors:
            #Search the element inside the list
            for _city in cities:
                if _city.getName() == neighbor:
                    neighbor = _city
                    break
            _neighbor_location = neighbor.getLocation()
            _neighbor_location = (_neighbor_location["x"],_neighbor_location["y"])
            if cit_visited(city.getName(),visited_cities):
                stroke(25,23,28)
            else:
                stroke(255,164,27)
            line(_city_location,_neighbor_location)
    no_stroke()

def displayCities(list_cities,visited_cities):
    rect_mode(CENTER)
    for city_id in range(0,len(list_cities)):
        if cit_visited(list_cities[city_id].getName(),visited_cities):
            fill(100, 65, 164)
            stroke(25,23,28)
        else:
            stroke(255,164,27)
            fill(0,8,57)
        city_loc = list_cities[city_id].getLocation()
        x = city_loc["x"]
        y = city_loc["y"]
        rect((x,y),15,15)
    no_fill()
    no_stroke()

def displayMap(map_img, neighbors,list_cities,visited_cities):
    image(map_img,(0,0),(1050,700))
    displayRoutes(list_cities,visited_cities)
    displayCities(list_cities,visited_cities)
