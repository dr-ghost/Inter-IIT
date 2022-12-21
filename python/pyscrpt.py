import pandas as pd
import numpy as np
from datetime import time

import queue

node_lst = []
drone_type_instances = []
successful_drone_type_instances = []
const_time = 4 * 60 * 60

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


class Node:
    def __init__(self,NodeID,X,Y,Z):
        self.ID = NodeID
        self.position = Point(X,Y,Z)
    def __str__(self):
        return "{ID}".format(ID = self.ID)


class Warehouse(Node):
    def __init__(self,stationID,charging_current,X,Y):
        self.ID = stationID
        self.cc = charging_current
    def __str__(self):
        return "{ID}".format(ID = self.ID)


class RechargeStation(Node):
  def __init__(self):
    pass


class Item:
  def __init__(self,ItemId,Weight,Length,Breadth,Height):
    self.ItemId=ItemId
    self.Weight=Weight
    self.Length=Length
    self.Breadth=Breadth
    self.Height=Height
    self.volume = Length*Breadth*Height


class Demand(Node):
    def __init__(self,DemandID,ServingWH,Item,Day,X,Y,Z,startTime,Endtime):
        self.id = DemandID
        self.wh = ServingWH
        self.position = Point(X,Y,Z)
        self.item = Item
        self.day = Day
        starth, startm, starts = list(map(int,startTime.split(':')))
        self.start_time = time(starth,startm,starts)
        endh,endm,ends = list(map(int,Endtime.split(':')))
        self.end_time = time(endh,endm,ends)
        self.failure = 0
    def failed(self):
        self.failure=1
    def __str__(self):
        return ("ID={}\nWH={}\nPosition={}\nItem={}\nday={}\nstartTime={}\nendTime={}\nfailure={}".format (self.ID,self.WH,self.Position,self.Item,self.day,self.startTime,self.EndTime,self.failure))


class Drone:
    def __init__(self, droneType:str, base_weight:float, weight_capacity:float,  battery_capacity:float, remaining_battery:float, payload_vol:float, num_slots:int, max_speed:float, time = 4 * 60 * 60, position = Point(0,0,0), recharge_energy = 0.0,a:float,b:float,c:float,p:float,q:float, path_summary = []):
        self.type = droneType
        self.battery_capacity = battery_capacity
        self.slots = num_slots
        self.speed = max_speed
        self.volume_capacity = payload_vol
        self.position = position
        self.base_weight = base_weight
        self.weight_capacity = weight_capacity
        self.time = time

        self.recharge_energy = recharge_energy
        self.remaining_time = self.time
        self.remaining_battery = remaining_battery
        self.path_summary = path_summary

        self.a = a
        self.b = b
        self.c = c
        self.p = p
        self.q = q


class Path:
    def __init__(self,p1:Point,p2:Point,drone:Drone):
        self.drone = drone
    def get_path(self,p1:Point,p2:Point):
        lst = []
        for i in range(p1.x, p2.x, self.drone.speed):
            lst.append(Point(i,p1.y,p1.z))
        for i in range(p1.y, p2.y, self.drone.speed):
            lst.append(Point(p2.x,i,p1.z))
        for i in range(p1.z, p2.z, self.drone.speed):
            lst.append(Point(p2.x,p2.y,i))
        return lst
    def get_energy(self,p1:Point,p2:Point):
        return self.drone.weight * (self.drone.a + self.drone.b * self.drone.speed + self.drone.c * p1.z)
    def get_time(self,p1:Point,p2:Point):
        return (p2.x - p1.x + p2.y - p1.y + p2.z - p1.z) / self.drone.speed
    def __str__(self):
        return "Path: {}\nEnergy: {}\nTime: {}".format(self.lst, self.energy, self.time)

def node_path(drone:Drone, node:Node, r_time:float, battery:float, visited:dict = {i : -1 for i in node_lst if type(i) == Warehouse or type(i) == RechargeStation}, dest_visited:int = 0, path_summary:list = [], pkg_weight:float = 0.0, pkg_vol:float = 0.0):
    if type(node) == Warehouse:
        successful_drone_type_instances.append((drone, r_time, battery, visited, dest_visited, path_summary))
    for i in node_lst:
        if type(i) == Warehouse:
           if visited[i] < dest_visited:
                t_p = Path(node.position, i.position, drone)
                if battery - t_p.get_energy(node.position, i.position) > 0 and r_time + t_p.get_time(node.position, i.position) < const_time:
                   node_path(drone, i, r_time + t_p.get_time(node.position, i.position), battery - t_p.get_energy(node.position, i.position), visited, dest_visited, path_summary + [t_p])
        elif type(i) == RechargeStation:
            if visited[i] < dest_visited:
                t_p = Path(node.position, i.position, drone)
                if battery - t_p.get_energy(node.position, i.position) > 0 and r_time + t_p.get_time(node.position, i.position) < const_time:
                   node_path(drone, i, r_time + t_p.get_time(node.position, i.position), battery - t_p.get_energy(node.position, i.position), visited, dest_visited, path_summary + [t_p])
        elif type(i) == Demand:
           if dest_visited + 1 <= drone.slots and i.item.weight + pkg_weight <= drone.weight_capacity and i.item.volume + pkg_vol <= drone.volume_capacity and  r_time + t_p.get_time(node.position, i.position) < i.end_time:
                t_p = Path(node.position, i.position, drone)
                if battery - t_p.get_energy(node.position, i.position) > 0 and r_time + t_p.get_time(node.position, i.position) < const_time:
                   node_path(drone, i, r_time + t_p.get_time(node.position, i.position), battery - t_p.get_energy(node.position, i.position), visited, dest_visited + 1, path_summary + [t_p], pkg_weight + i.item.weight, pkg_vol + i.item.volume)

  
def main():
    global dem_lst
    
    Item1 = Item('Item-1',1,5,8,5)
    Item2 = Item('Item-2',6,5,10,8)
    Item3 = Item('Item-3',4,5,10,15)
    Item4 = Item('Item-4',2,15,10,8)
    Item5 = Item('Item-5',5,20,15,10)
    
    demand = pd.read_csv("Demand.csv")
    parameter = pd.read_csv("Parameters.csv")
    demands = []        #Demand List
    W1 = Warehouse('WH1',5,0,0)
    for i in range(len(demand['Demand ID'])):
        D = Demand(demand['Demand ID'][i],W1,demand['Item'][i],demand['Day'][i][-1],demand['X'][i],demand['Y'][i],demand['Z'][i],demand['DeliveryFrom'][i],demand['DeliveryTo'][i])
        demands.append(D)
    #listed all the demands
    a_values=[]
    b_values=[]
    c_values=[]
    p_values=[]
    q_values=[]
    
    for i in range(len(parameter)):
        if(parameter["Parameter_ID"][0]=="P"):
            p_values.append(parameter["Value"][i])
        if(parameter["Parameter_ID"][0]=="Q"):
            q_values.append(parameter["Value"][i])
        if(parameter["Parameter_ID"][0]=="A"):
            a_values.append(parameter["Value"][i])
        if(parameter["Parameter_ID"][0]=="B"):
            b_values.append(parameter["Value"][i])
        if(parameter["Parameter_ID"][0]=="C" and parameter["Parameter_ID"] !="Cost(C)"):
            c_values.append(parameter["Value"][i])
        if(parameter["Parameter_ID"]=="Cost(C)"):
            cost=parameter["Value"][i]
        if(parameter["Parameter_ID"]=="MaxSpeed (M)"):
            max_speed=parameter["Value"][i]
        
        
            
    # taken values of a,b,c,p,q for each drone type in 5 separate list and cost and max_speed
    
    drone_count=[]
    for i in range(len(parameter)):
        if(parameter["Parameter_ID"][0]=="D"):
            drone_count.append(parameter["Value"][i])
    # taken drone count of each ddrone type

    



    

    
if __name__ == '__main__':
    main()
