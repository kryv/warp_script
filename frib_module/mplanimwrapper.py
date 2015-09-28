"""
mplanimwrapper.py
matplotlib and ffmpeg/mencoder is required

Python script for making animations.  

For help and/or additional information contact:

    Kei Fukushima       k.fksm.ryv@gmail.com

"""

#Load packages
from matplotlib.pyplot import *
from matplotlib.animation import *

class AnimPlot(object):

    #set initial values
    def __init__(self, filename = "animplot.mp4", fig = figure(figsize=(10, 10))):
        self.filename = filename
        self.fig = fig
        self.im =[]
        self.ims =[]

    #make subplot Axes instance 
    #example: pp = msubplot(111)
    def msubplot(self,pos):
        return(self.fig.add_subplot(pos))

    #Make lines and/or markers plot to the Axes:pp
    #example: nplot(pp,x,y,options)
    def nplot(self,pp,x,y,*args,**kwargs):
        imtmp, = pp.plot(x,y,*args,**kwargs)
        self.im.append(imtmp)

    #Make a scatter plot to the Axes:pp
    #example: splot(pp,x,y,options)   
    def splot(self,pp,x,y,*args,**kwargs):
        imtmp = pp.scatter(x,y,*args,**kwargs)
        self.im.append(imtmp)

    #Make a text plot to the Axes:pp
    #example: tplot(pp,x,y,'text message',options)   
    def tplot(self,pp,txt,x,y,*args,**kwargs):
        imtmp = pp.text(x,y,txt,*args,**kwargs)
        self.im.append(imtmp)

    #Make a frame
    def makeframe(self):
        tight_layout()
        self.ims.append(self.im)
        self.im =[]

    #Make a movie from the all frames    
        def makemovie(self,interval=1,writer='ffmpeg',fps=10,**kwargs):
        outanim = ArtistAnimation(self.fig, self.ims, interval=interval)
        converter = writers[writer]
        writer = converter(fps=fps)
        outanim.save(self.filename,writer=writer)
