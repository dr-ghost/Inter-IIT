import pandas as pd
import numpy as np
from datetime import time

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
    def __str__(self):
        return "({x},{y},{z})".format(x = self.x,y = self.y,z = self.z)
    
class Drone:
  #ayush 
  def __init__(self,droneType,battery_capacity,payload_capacity,num_slots,max_speed):
    self.type=droneType
    self.battery=battery_capacity
    self.num=num_slots
    self.speed=max_speed
    self.cap=payload_capacity
  

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
    
def main():
    pass

if __name__ == '__main__':
    main()