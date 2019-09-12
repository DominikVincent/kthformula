from matplotlib import pyplot
import numpy as np
import time


"""
unfortunatly didnt have enough time to work probably on that, but that is what i could do in my limited time
next thing i wanted to do is the live data/plot update in the same figure. the ability to add/remove a (new) axe to the figure
without creating a whole new figure. I also wanted to enable live update of incoming data
"""


class visulatization:
    
    
    def __init__(self):
        self.x_min = 0
        self.x_max = 2
        self.steps = 100
        self.figure, axe = pyplot.subplots(1,1)
        self.axes = [axe]
        pyplot.ion()
        self.functions_name= []
        self.functions = []
        self.figures = []
        self.axes = []
       
       

    """
    calls pyplot show and shows the figure
    returns: none
    """
    def show(self):
        pyplot.show(block=False)

    """
    adds a new function to the displayed plots and draws the plot after that with self.draw()
    modifies: functions_name,    functions,    figures,    axes,
    returns: None
    """
    def plot(self, function, functions_name):
        self.functions.append(function)
        self.functions_name.append(functions_name)
        pyplot.close(self.figure)
        if len(self.functions) > 2:
            self.figure, self.axes = pyplot.subplots(len(self.functions), 1)
            
        elif len(self.functions) == 2:
            self.figure, self.axes = pyplot.subplots(2, 1)
            
        else:#first one to draw
            self.figure, self.axes = pyplot.subplots(1, 1)
            
            self.axes = [self.axes]
            x, y =self.calculate(function)
            self.axes[0].plot(x, y)
            
        self.axes[-1].set_title(functions_name)

        self.draw()
        
        
    """
    calculates x and y values and returns x and y data as np.array
    """
    def calculate(self, function):
        x = np.linspace(self.x_min, self.x_max, self.steps)
        y = function(x)
        print(x)
        print(y)
        return x, y

    """
    draws the canvas of self.figure
    """
    def draw(self):
        """self.figure.canvas.draw()
        pyplot.draw()
        
        pyplot.pause(0.0001)
        pyplot.clf()"""
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        for i in range(len(self.axes)):
            if self.functions_name[i][0:4] == "data":
                continue
            x,y = self.calculate(self.functions[i])
            #print(x)
            #print(y)
            self.axes[i].plot(x, y)
            self.axes[i].set_title(self.functions_name[i])
            #self.axes[i].draw()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        #self.show()
        
        """
        self.figure.canvas.draw()
        pyplot.draw()
        
        pyplot.pause(0.0001)
        pyplot.clf()"""
        
    """
    removes a function of the fucntions to plot and redraws the canvas
    """
    def remove(self, name):
        for i in range(len(self.axes)):
            if(name == self.functions_name[i]):
                print("found number 3")
                del self.functions_name[i]
                del self.functions[i]
                
                pyplot.delaxes(self.axes[i])
                self.axes = self.axes[self.axes != self.axes[i]]
                
                self.draw()
                

    def set_x_min(self, x):
        self.x_min = x

    def set_x_max(self, x):
        self.x_max = x
                
        
class better_visulatization(visulatization):
    hash_map_dataname_value = {}
    def __init__(self):
        visulatization.__init__(self)
        

    def draw_raw_data(self):
        for key in self.hash_map_dataname_value:
            i = self.functions_name.index(key)
            self.axes[i].plot(self.hash_map_dataname_value[key][0],self.hash_map_dataname_value[key][1])
            self.axes[i].set_title(self.functions_name[i])
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()        

    def plot_data(self, x, y, data_name):
        self.functions.append(lambda x: -1)
        self.functions_name.append("data_"+data_name)
        self.hash_map_dataname_value["data_"+data_name] = [x,y]
        np.concatenate(self.axes, [self.figure.add_subplot()])
        self.draw()
        self.draw_raw_data()
        
    def append_data(self, x, y, data_name):
        self.hash_map_dataname_value["data_"+data_name][0].append(x)
        self.hash_map_dataname_value["data_"+data_name][1].append(y)
        self.draw_raw_data()


a = better_visulatization()
a.plot(lambda x: 3* np.pi * np.exp( -1* 5* np.sin(2*np.pi*x)  ), "weird sin exp func")
a.show()
""""for i in range(500):
    time.sleep(0.01)"""
pyplot.pause(2)
a.plot(lambda x: 3*x, "3x")

"""for i in range(500):
    time.sleep(0.01)"""
pyplot.pause(2)
print("never left")
a.plot(lambda x: x*500, "fck")
pyplot.pause(2)


a.plot_data([0,1,2], [0,1,0], "kleien Zahl")
pyplot.pause(5)
