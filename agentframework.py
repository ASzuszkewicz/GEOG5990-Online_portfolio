"""
@author: 201280898
"""
import random


#defining/naming/grouping
class Agent():
    def __init__(self, environment, agents, y, x, ly, lx):
        self.environment = environment #lets all agents know about environment
        self.agents = agents #giving agent list to agents
        self.store = 0 #gives a store of information
        self.nottoshare = 0 #dont share again when shared once
        self.y = random.randint(0,100) #give agents (sheep) value 
        self.x = random.randint(0,100) #give agents (sheep) value
        self.ly = self.y + 1 #give agents (lambs) value which means they will follow origional agents (sheep)
        self.lx = self.x + 1 #give agents (lambs) value which means they will follow origional agents (sheep)
        if (x == None):
            self._x = random.randint(0,100) #if agents have no value assign random value
        else:
            self._x = x 
          #interacting with environment    
    def eat(self): 
        if self.environment[self.y][self.x] > 10: #agents eat from the environment
            self.environment[self.y][self.x] -= 10 #agents eat from the environment
            self.store += 10 #tell store how much eaten
        if self.environment[self.ly][self.lx] > 5: #agents eat from the environment - but only eat half as much as origional agents
            self.environment[self.ly][self.lx] -= 5 #agents eat from the environment - but only eat half as much as origional agents
            self.store += 5 #tell store how much eaten
        #move/interact with self
    def move (self):
        if random.random() < 0.5:
            self.y = self.y + 1 #agents move based upon the next position they are given
        else:
            self.y = self.y - 1 #agents move based upon the next position they are given
    
        if random.random() < 0.5:
            self.x = self.x + 1 #agents move based upon the next position they are given
        else:
            self.x = self.x - 1 #agents move based upon the next position they are given    
        if random.random() < 0.5:
            self.ly = self.ly - 1 #agents move based upon the next position they are given
        else:
            self.ly = self.ly + 1 #agents move based upon the next position they are given
    
        if random.random() < 0.5:
            self.lx = self.lx - 1 #agents move based upon the next position they are given
        else:
            self.lx = self.lx + 1 #agents move based upon the next position they are given
            
    def distance(self, agent):
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5 #working out distance between each agent
#sharing information with each other to find out which other agents are nearby to them
    def share(self, neighbourhood):
        for i in range(0, len(self.agents)):
            distance = self.distance(self.agents[i])
            if (distance < neighbourhood):
                total = self.store + self.agents[i].store # Share information from the store on how much they have eaten
                print("total",total) #print how much each has eaten
                ave = total/2
                self.store = ave #average amount eaten calculated
                self.agents[i].nottoshare = ave #no longer sharing information now it has been shared
    
