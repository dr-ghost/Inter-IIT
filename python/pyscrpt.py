import pandas as pd
import numpy as np
from datetime import time

import queue

dem_lst = []
drone_type_instances = []
successful_drone_type_instances = []

class Point:
    def __init__(self,X,Y,Z):
        self.x = X
        self.y = Y
        self.z = Z
    
    def distance(self,other):
        A = (self.x - other.x)**2
        B = (self.y - other.y)**2
        C = (self.z - other.z)**2
        distance = (A + B + C)**0.5
        return distance
    
    def neighbours(self):
        return [Point(self.x+1,self.y,self.z),Point(self.x-1,self.y,self.z),Point(self.x,self.y+1,self.z),Point(self.x,self.y-1,self.z),Point(self.x,self.y,self.z+1),Point(self.x,self.y,self.z-1)]
    
    def __str__(self):
        return "({x},{y},{z})".format(x = self.x,y = self.y,z = self.z)
    

def edge_weight(p1:Point,p2:Point, max_speed_xy:float,max_speed_z:float,A:float,B:float,C:float,W:float):
    del_x = abs(p2.x - p1.x)
    del_y = abs(p2.y - p1.y)
    del_z = abs(p2.z - p1.z)
    del_xy = del_x + del_y
    time1 = del_xy/max_speed_xy
    energy1 = W*(A*time1 + B*del_xy)

    time2 = del_z/max_speed_z
    energy2 = W*((A+C)*time2 + B*del_z)

    total_energy = energy1 + energy2
    return total_energy

class Drone:
    def __init__(self, droneType:str, base_weight:float, weight:float,  battery_capacity:float, remaining_battery:float, payload_vol:float, num_slots:int, max_speed:float, time = 4 * 60 * 60, position = Point(0,0,0), recharge_energy = 0.0, path_summary = []):
        self.type = droneType
        self.battery_capacity = battery_capacity
        self.num = num_slots
        self.speed = max_speed
        self.cap = payload_vol
        self.position = position
        self.base_weight = base_weight
        self.weight = weight
        self.time = time

        self.recharge_energy = recharge_energy
        self.remaining_time = self.time
        self.remaining_battery = remaining_battery
        self.path_summary = path_summary

        self.a = 0.1
        self.b = 0.1
        self.c = 0.1
    
    def bfs(self, node:Point, visited:dict):

        q = queue.Queue()
        q.put((node, self.remaining_time, self.remaining_battery))

        while(not q.empty()):
            n = q.get()

            if (n[0] in dem_lst):
                if (n[0] == Point(0,0,0) and n[2] != 4 * 60 * 60):
                    successful_drone_type_instances.append(Drone(self.type, self.base_weight, self.weight, self.battery_capacity, self.remaining_battery, self.cap, self.num, self.speed, n[2], n[0], self.recharge_energy, self.path_summary))
                drone_type_instances.append(Drone(self.type, self.base_weight, self.weight - (), n[2], self.cap, self.num, self.speed, n[1], n[0]))


            visited[n[0]] = 1
            for neighbour in n.neighbours():
                if neighbour not in visited.keys() and n[1] - 1/self.speed >= 0 and n[2] - self.weight * (self.a + self.b * self.speed + self.c * n.z) >= 0:
                    q.put((neighbour, n[1] - 1/self.speed, n[2] - self.weight * (self.a + self.b * self.speed + self.c * n.z)))
        
        
#energy = W(A + Bs + Ch) 



#set attributes acc to droneType - battery capaacity ,num slots,max speed M for all

class Warehouse:
    def __init__(self,stationID,charging_current,X,Y):
        self.ID = stationID
        self.cc = charging_current
        self.position = Point(X,Y,0)
    def __str__(self):
        return "{ID}".format(ID = self.ID)

class RechargeStation:
  #anshul
  def __init__(self):
    #Station ID	Charging Slots	Charging Current=3A	X	Y
    pass

class Item:
  #nikhil
  def __init__(self,ItemId,Weight,Length,Breadth,Height):
    self.ItemId=ItemId
    self.Weight=Weight
    self.Length=Length
    self.Breadth=Breadth
    self.Height=Height
    self.volume = Length*Breadth*Height

class Demand:
  
    def __init__(self,DemandID,ServingWH,Item,Day,X,Y,Z,startTime,Endtime):
        
        self.ID=DemandID
        self.WH=ServingWH
        self.Position=Point(X,Y,Z)
        self.Item=Item
        self.day=Day
        starth,startm,starts=list(map(int,startTime.split(':')))
        self.startTime=time(starth,startm,starts)
        endh,endm,ends=list(map(int,Endtime.split(':')))
        self.EndTime=time(endh,endm,ends)
        self.failure=0
    def failed(self):
        self.failure=1
    def __str__(self):
        
        return ("ID={}\nWH={}\nPosition={}\nItem={}\nday={}\nstartTime={}\nendTime={}\nfailure={}".format
    (self.ID,self.WH,self.Position,self.Item,self.day,self.startTime,self.EndTime
       ,self.failure         ))
#Energy = W(A + Bs + Ch)
class Path:
    def __init__(self,p1:Point,p2:Point):
        pass
            

def main():
    global dem_lst
    
    Item1 = Item('Item-1',1,5,8,5)
    Item2 = Item('Item-2',6,5,10,8)
    Item3 = Item('Item-3',4,5,10,15)
    Item4 = Item('Item-4',2,15,10,8)
    Item5 = Item('Item-5',5,20,15,10)
    
    pass

if __name__ == '__main__':
    main()