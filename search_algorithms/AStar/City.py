from p5 import *

class City(object):
    def __init__(self, name, location, neighbors = [],Gx = 0):
        self.name = name
        self.location = location
        self.neighbors = neighbors
        self.Gx = Gx

    def __str__(self):
        return "CITY "+str(self.name)+" Location: ["+str(self.location["x"])+","+str(self.location["y"])+"].\n"

    def getLocation(self):
        return self.location
    
    def getName(self):
        return self.name
    
    def getNeighbors(self):
        return self.neighbors

    #Returns true when the it is my neighbor
    def neighborOf(self,neighborName):
        temp = (neighborName in self.neighbors)
        return temp
    
    def getGx(self):
        return self.Gx
        
    def setGx(self,Gx):
        self.Gx = Gx