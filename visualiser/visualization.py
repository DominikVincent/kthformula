from matplotlib import pyplot
import numpy as np
import time


"""
unfortunatly didnt have enough time to work probably on that, but that is what i could do in my limited time
next thing i wanted to do is the live data/plot update in the same figure. the ability to add/remove a (new) axe to the figure
without creating a whole new figure. I also wanted to enable live update of incoming data
"""


class visulatization:
    functions_name= []
    functions = []
    figures = []
    axes = []
    
    def __init__(self):
       self.x_min = 0
       self.x_max = 2
       self.steps = 100
       self.figure, axe = pyplot.subplots(1,1)
       self.axes = [axe]
       pyplot.ion()
       


    def show(self):
        pyplot.show()

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

    def draw(self):
        """self.figure.canvas.draw()
        pyplot.draw()
        
        pyplot.pause(0.0001)
        pyplot.clf()"""
        for i in range(len(self.axes)):
            x,y = self.calculate(self.functions[i])
            #print(x)
            #print(y)
            self.axes[i].plot(x, y)
            #self.axes[i].draw()
        pyplot.draw()
        """self.figure.canvas.draw()
        pyplot.draw()
        
        pyplot.pause(0.0001)
        pyplot.clf()"""
        

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
                
        
class bettter_visulatization(visulatization):
    def __init__(self):
        color ="red"

a = visulatization()
a.plot(lambda x: 3* np.pi * np.exp( -1* 5* np.sin(2*np.pi*x)  ), "weird sin exp func")
a.plot(lambda x: 3*x, "3x")
a.show()
#time.sleep(5)
#print("never left")
#a.plot(lambda x: x*500, "fck")


