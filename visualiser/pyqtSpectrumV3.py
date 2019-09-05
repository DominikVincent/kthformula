import numpy as np

from pyqtgraph.Qt import QtGui, QtCore

import pyqtgraph as pg



import struct

import pyaudio

from scipy.fftpack import fft



import sys

import time





class AudioStream(object):

    def __init__(self):


        self.angle = 0
        self.brightness = np.zeros((10,2))
        self.saturation = 0
        # pyqtgraph stuff

        pg.setConfigOptions(antialias=True)

        self.traces = dict()

        self.app = QtGui.QApplication(sys.argv)

        self.win = pg.GraphicsWindow(title='Spectrum Analyzer')

        self.win.setWindowTitle('Spectrum Analyzer')

        self.win.setGeometry(5, 115, 1910, 1070)

        

        wf_xlabels = [(0, '0'), (2048, '2048'), (4096, '4096')]

        wf_xaxis = pg.AxisItem(orientation='bottom')

        wf_xaxis.setTicks([wf_xlabels])



        wf_ylabels = [(0, '0'), (127, '128'), (255, '255')]

        wf_yaxis = pg.AxisItem(orientation='left')

        wf_yaxis.setTicks([wf_ylabels])



        sp_xlabels = [

            (np.log10(10), '10'), (np.log10(100), '100'),

            (np.log10(1000), '1000'), (np.log10(22050), '22050')

        ]

        sp_xaxis = pg.AxisItem(orientation='bottom')

        sp_xaxis.setTicks([sp_xlabels])

        




        fr_xlabels = [

            (np.log10(10), '10'), (np.log10(100), '100'),

            (np.log10(1000), '1000'), (np.log10(22050), '22050')

        ]

        fr_xaxis = pg.AxisItem(orientation='bottom')

        fr_xaxis.setTicks([fr_xlabels])



        self.waveform = self.win.addPlot(

            title='WAVEFORM', row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis},

        )

        self.spectrum = self.win.addPlot(

            title='SPECTRUM', row=2, col=1, axisItems={'bottom': sp_xaxis},

        )
        #stuff with the bargraph
        
        self.frequenciesChart = self.win.addPlot(

            title='FREQUENZEN', row=3, col=1

        )

        self.colorDiagram = self.win.addPlot(

            title='colors', row=4, col=1

        )

        

        


        # pyaudio stuff

        self.FORMAT = pyaudio.paInt16

        self.CHANNELS = 1

        self.RATE = 44100

        self.CHUNK = 1024 * 2

        self.fftData = [0 for i in range(self.CHUNK)]

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(

            format=self.FORMAT,

            channels=self.CHANNELS,

            rate=self.RATE,

            input=True,

            output=True,

            frames_per_buffer=self.CHUNK,

        )


        #BARCHART
        
        self.INTERVALS = [128,1024,2048,4096,8192,16284]
        #self.INTERVALS = [ i for i in range(0,20000, 50)]
        self.getFrequnzies(self.INTERVALS)

        
        #print(self.frequencies)
        self.bg1 = pg.BarGraphItem(x=np.arange(len(self.INTERVALS)+3),height=self.frequencies+[0] +[30], width=0.6, brush='r')
        #self.bg1.setPen(pg.mkPen(color=pg.hsvColor(0.33, sat=1, val=1.0, alpha=1.0), width=2))
        #self.bg1.setYRange(0,10)
        
        """
        y1 = np.linspace(0, 20, num=20)

        # create horizontal list
        x = np.arange(20)

        # create bar chart
        bg1 = pg.BarGraphItem(x=x, height=y1, width=0.6, brush='r')
        """
        self.frequenciesChartAddReturnObject = self.frequenciesChart.addItem(self.bg1)

        # waveform and spectrum x points

        self.x = np.arange(0, 2 * self.CHUNK, 2)

        self.f = np.linspace(0, self.RATE / 2, self.CHUNK / 2)

    #stuff for barchart
    """
    sums up all the fft data in n intervals(frequenzies) given as parameter
    0-intervals[0] , ... , interval[n]-22050
    """
    def getFrequnzies(self, intervals):
        self.frequencies = [1 for i in range(len(intervals)+1)]
        for i in range(-1, len(intervals) ):
            #set lower bound
            if i< 0:
                lowerBound = 0
            else:
                lowerBound = int(intervals[i]/self.RATE*self.CHUNK)
            #set upperbound
            if i+1 >= len(intervals):
                upperbound = self.CHUNK-1
            else:
                #print(i)
                upperbound = int(intervals[i+1]/self.RATE*self.CHUNK)
            
            #calculate Sum of Frequncies in the Interval
            #print("i: ",i,"lowerbound",lowerBound,"upperbound", upperbound)
            
            self.frequencies[i] =np.sum( self.fftData[ lowerBound:upperbound])






    def start(self):

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):

            QtGui.QApplication.instance().exec_()

    def clean(self, arr):
        arr = np.array(arr)
        
        #arr = np.log(arr)
        arr[arr < 0] = 0
        return arr

    def set_plotdata(self, name, data_x, data_y):
        self.getFrequnzies(self.INTERVALS)
        if name in self.traces:
            #print(self.frequencies)
            if name == 'frequenciesChart':
                self.getFrequnzies(self.INTERVALS)
                self.bg1.setOpts(height=   self.clean( self.frequencies+[np.sum(self.frequencies)] + [30]))
                #print(self.frequencies)
            elif name == 'colorDiagram':
                pen = pg.mkPen('y', width=3, style=QtCore.Qt.DashLine) 
                self.traces[name].setPen(pg.mkPen(color=pg.hsvColor(self.angle/360, sat=1, val=self.brightness[-1][0], alpha=1.0), width=100))
                self.traces[name].setData(data_x, data_y)
            else:
                self.traces[name].setData(data_x, data_y)
                

        else:

            if name == 'waveform':
                pen = pg.mkPen(color=pg.hsvColor(0.66, sat=1, val=1.0, alpha=1.0))
                self.traces[name] = self.waveform.plot(pen=pen, width=3)
                

                self.waveform.setYRange(0, 255, padding=0)

                self.waveform.setXRange(0, 2 * self.CHUNK, padding=0.005)

            if name == 'spectrum':

                self.traces[name] = self.spectrum.plot(pen='m', width=3)

                self.spectrum.setLogMode(x=True, y=True)

                self.spectrum.setYRange(-4, 0, padding=0)

                self.spectrum.setXRange(

                    np.log10(20), np.log10(self.RATE / 2), padding=0.005)

            if name == 'frequenciesChart':

                self.traces[name] = self.bg1

            if name == 'colorDiagram':

                self.traces[name] = self.traces[name] = self.colorDiagram.plot(pen='m', width=3)
                self.colorDiagram.setYRange(0, 2, padding=0)

                self.colorDiagram.setXRange(0, 3, padding=0.005)


    """def getAngle(self, arrayOfFrequencies):
        
        angle = 0
        for i in range(len(arrayOfFrequencies)-1):
            angle += np.arctan(np.arctan(i*(arrayOfFrequencies[i]))-2) 
        
        print(angle)
"""
    def getAngle(self, arrayOfFrequencies):
        self.angle += (np.sum(arrayOfFrequencies[-4:-1])/3)
        self.angle %= 360
        #print(self.angle/360)
    
    def getBrightness(self, arrayOfFrequencies):
        median = np.sum(self.brightness.take(1, axis = 1)) / self.brightness.shape[0]
        print(median)
        if median == 0:
            median = 1
        percent = np.sum(arrayOfFrequencies)/ median
        if percent < 1:
            percent = - percent *1
        else:
            percent = percent*1.1
        print(percent)
        
        newBrightness= self.brightness[-1][0] + percent* 0.1
        print(newBrightness)
        if newBrightness <= 0.001 :
            newBrightness = 0.001
        if newBrightness>=1.5:
            newBrightness = 1.5

        newValue =  min(np.arctan(1.2* newBrightness),1)
        
        self.brightness = np.append(self.brightness[1:], [[ newValue ,np.sum(arrayOfFrequencies) ]], axis = 0)
        #print(arrayOfFrequencies[-1])
        print(self.brightness)


    def update(self):
        self.getAngle(self.frequencies)
        self.getBrightness(self.frequencies)
        wf_data = self.stream.read(self.CHUNK)

        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)

        wf_data = np.array(wf_data, dtype='b')[::2] 

        self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data,)



        sp_data = fft(np.array(wf_data, dtype='int8') - 128)

        sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]

                         ) * 2 / (128 * self.CHUNK)
        self.fftData = sp_data
        self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)
        self.set_plotdata(name='frequenciesChart', data_x=[], data_y=[])
        self.set_plotdata(name='colorDiagram', data_x=[1,2], data_y=[1,1])



    def animation(self):

        timer = QtCore.QTimer()

        timer.timeout.connect(self.update)

        timer.start(2)

        self.start()





if __name__ == '__main__':



    audio_app = AudioStream()

    audio_app.animation()