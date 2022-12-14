#include <bits/stdc++.h>

using namespace std;

class Node
{
    int x = 0,y = 0,z = 0;
    public:
        Node(int x,int y,int z)
        {
            this->x = x;
            this->y = y;
            this->z = z;
        } 
        vector<Node> getNeighbours()
        {
            vector<Node> v = {Node(x+1,y,z),Node(x-1,y,z),Node(x,y+1,z),Node(x,y-1,z),Node(x,y,z+1),Node(x,y,z-1)};
            return v;
        } 
};

class Drone
{
    string droneType;
    float baseWeight, weight, batteryCapacity, payloadVol, maxSpeed;
    int numSlots;

    float remainingBattery, time;

    Node position;

    public:
        Drone(string droneType, float baseWeight, float weight, float batteryCapacity, float payloadVol, float maxSpeed, int numSlots) : position(0,0,0)
        {
            this->droneType = droneType;
            this->baseWeight = baseWeight;
            this->weight = weight;
            this->batteryCapacity = batteryCapacity;
            this->payloadVol = payloadVol;
            this->maxSpeed = maxSpeed;
            this->numSlots = numSlots;
        }
        float getRemainingBattery()
        {
            return remainingBattery;
        }
        float getTime()
        {
            return time;
        }
        void setRemainingBattery(float remainingBattery)
        {
            this->remainingBattery = remainingBattery;
        }
        void setTime(float time)
        {
            this->time = time;
        }
        void setWeight(float weight)
        {
            this->weight = weight;
        }
        float getWeight()
        {
            return weight;
        }
        float getBatteryCapacity()
        {
            return batteryCapacity;
        }
        float getPayloadVol()
        {
            return payloadVol;
        }
        float getMaxSpeed()
        {
            return maxSpeed;
        }
        int getNumSlots()
        {
            return numSlots;
        }
        string getDroneType()
        {
            return droneType;
        }
        float getBaseWeight()
        {
            return baseWeight;
        }

        void bfs(set <Node>  & s)
        {
            queue <Node> q;
            q.push(this->position);

            while (!q.empty())
            {
                Node node = q.front();
                q.pop();
                s.insert(node);

                vector <Node> v = node.getNeighbours();
            }
        }
};

// Energy cost per sec = W(A + Bs + Ch)
// Speed = M -pf , f=m/W in XY
int main(){
    
}
//herer
//bolo
