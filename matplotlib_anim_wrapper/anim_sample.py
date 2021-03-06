from numpy import *
from matplotlib_anim_wrapper import *

#initial conditon
x0 = 2.0
t0 = 0.0

w  = 1.0 #frequency

dt = 0.05 #timestep
t1 = 2.0 

tvec = arange(t0, t1, dt)

def position(t):
 return(x0*cos(2.0*pi*w*t))

def verocity(t):
 return(x0*w*sin(2.0*pi*w*t))

# Set AnimPlot class as apm
apm = AnimPlot()

# Set fontsize
fnsz = 20

# Set subplot at 211
ax = apm.msubplot(211)
ax.set_title('orbit',fontsize=fnsz)
ax.set_xlabel('x',fontsize=fnsz)
ax.set_ylabel('x\'',fontsize=fnsz)
ax.set_xlim(-x0*1.5, x0*1.5)
ax.set_ylim(-x0*w*1.5, x0*w*1.5)


# Set subplot at 212
bx = apm.msubplot(212)
bx.set_title('',fontsize=fnsz)
bx.set_xlabel('t',fontsize=fnsz)
bx.set_ylabel('x',fontsize=fnsz)
bx.set_xlim(t0, t1-dt)
bx.set_ylim(-x0*1.5, x0*1.5)


for t in tvec:
 #apm.splot(ax,position(t),verocity(t),color='red',s=50.0)
 # Plot  particle position on ax->211
 apm.nplot(ax,position(t),verocity(t),c='r',marker='o',ms=10.0)
 # Plot  particle position on bx->212
 apm.nplot(bx,t,position(t),c='r',marker='o',ms=10.0)
 # Plot  particle history on bx->212
 apm.nplot(bx,tvec,x0*cos(2.0*pi*w*tvec),'r-')
 # Plot text on bx->212
 apm.tplot(bx,"orbit history", 1.25, 1, color = 'red',fontsize=fnsz)
 # Make frame with upper plots
 apm.makeframe()

 
apm.makemovie()


