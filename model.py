"""
@author: 201280898
"""
#import external libraries
import matplotlib
matplotlib.use('TkAgg') #importing backend to allow render of graphics in different ways depending on output and needs to be before any imports
import tkinter
import random 
import agentframework #bring in the agent framework list
import matplotlib.pyplot
import matplotlib.animation
import csv #ability to read text file as a csv file
import time #allows to read/track time taken for program to run
import requests #ability to get data from the web
import bs4 #exracts data from html

start = time.perf_counter()

#start an empty list for environment
environment = []

#importing environment data from a text file
with open('in.txt', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC) 
    for row in reader:
        rowlist = [] 
        for value in row:  
            rowlist.append(value)
        environment.append(rowlist)

#set up figure window
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])
      
#import data from the web for agent starting locations
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})

#making agents/bringing in framework
num_of_agents = 10 #how many agents required
num_of_iterations = 100 #how many iterations for the model
neighbours = 10 #set up how many neighbours the agents associate with
agents = [] #start an empty list for agents
for i in range(num_of_agents):
    y = int(td_ys[i].text) #set up starting location for sheep agents using imported data
    x = int(td_xs[i].text) #set up starting location for sheep agents using imported data
    ly = y + 1 #set up starting location for lamb agents so they are within 1 cell of the sheep agents
    lx = x + 1 #set up starting location for lamb agents so they are within 1 cell of the sheep agents
    agents.append(agentframework.Agent(environment, agents, y, x, ly, lx)) #make desired agents using framework as a standard
    random.shuffle(agents) #agents starting location is randomly selected

carry_on = True	#make sure all agents start

def update(frame_number): #set up model with a clear start
    fig.clear() 
    global carry_on

#get agents to do something   
    for i in range(num_of_agents): #telling agents to move, eat environment and share according to the agent framework
        agents[i].move()
        agents[i].eat()
        agents[i].share(4) #how many times wanting to share information
    for i in range(num_of_agents): #tell agents to share according to the agent framework and reset store of information to 0 each time the data is shared once
        agents[i].store = agents[i].store + agents[i].nottoshare
        agents[i].nottoshare = 0
    if random.random() < 0.1:
        carry_on = False
        print("stopping condition") #automatic stopping of the model if any agent is going to go outside of the area
        end = time.perf_counter()
        print("time = " + str(end - start)) #print the time the model has been running for

    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y, color='red') #show agents in a specific colour - sheep red
        matplotlib.pyplot.scatter(agents[i].lx,agents[i].ly, color='pink') #show agents in a specific colour - lambs pink
        matplotlib.pyplot.imshow(environment) #show environment in background

def gen_function(b = [0]):
    a = 0
    global carry_on #telling model to carry on
    while (a < 100) & (carry_on) :
        yield a			#Wait for next call before continuing.
        a = a + 1

def run(): #run model as an animated visual
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()

def stop():
    carry_on = False
    print("stopping condition") #manual stopping of the model
    end = time.perf_counter()
    print("time = " + str(end - start)) #print the time the model has been running for

#create model window
root = tkinter.Tk()
root.wm_title("Sheep and Lamb model") #name model window
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
c = tkinter.Canvas(root, width=200, height=200) #set size of the model window
c.pack() 

#Show menu elements in model window
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar) 
model_menu = tkinter.Menu(menu_bar) #add in a menu bar
menu_bar.add_cascade(label="Model menu", menu=model_menu) #name model
model_menu.add_command(label="Run model", command=run) #name menu command to run model
model_menu.add_command(label="Stop model", command=stop) #name menu command to stop model

tkinter.mainloop() #Wait for interactions