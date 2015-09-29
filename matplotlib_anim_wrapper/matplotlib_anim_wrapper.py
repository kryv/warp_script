#
# matplotlib_anim_wrapper.py
#
# matplotlib and ffmpeg is required
#
#from matplotlib.pyplot import *
#from matplotlib.animation import *
#from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
import matplotlib.animation as anm
from mpl_toolkits.mplot3d import Axes3D


class AnimPlot(object):
 
 #set initial values
 def __init__(self, filename = "animplot.mp4",size = (10,10)):
    fig = plt.figure(figsize=size)
    self.filename = filename
    self.fig = fig
    self.im =[]
    self.ims =[]
 
 #make subplot Axes instance 
 #example: pp = msubplot(111)
 def msubplot(self,pos,*args,**kwargs):
    return(self.fig.add_subplot(pos,*args,**kwargs))
 
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
    return(imtmp)

 #Make a colorbar for the plot
 #example: obj = splot(pp,x,y,options)
 #         cbars(obj,left, bottom, width, height)
 def cbars(self,im, left, bottom, width, height):
    cax = self.fig.add_axes([left, bottom, width, height])
    plt.colorbar(im,cax=cax)
       
 #Make a text plot to the Axes:pp
 #example: tplot(pp,x,y,'text message',options)   
 def tplot(self,pp,txt,x,y,*args,**kwargs):
    imtmp = pp.text(x,y,txt,*args,**kwargs)
    self.im.append(imtmp)
    
 #Make a frame
 def makeframe(self):
    #plt.tight_layout()
    self.ims.append(self.im)
    plt.draw()
    self.im =[]

 #Make a movie from the all frames    
 def makemovie(self,interval=1,writer='mencoder',fps=5,**kwargs):
    outanim = anm.ArtistAnimation(self.fig, self.ims, interval=interval,blit=False)
    converter = anm.writers[writer]
    writer = converter(fps=fps)
    outanim.save(self.filename,writer=writer)
