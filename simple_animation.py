#
# simple animation script : simple_animation.py
#
# matplotlib (for plotting) and ffmpeg (for making .mp4 file) is required
#
from warp import *
import matplotlib.pyplot as plt
import matplotlib.animation as anim

#initial conditon
x0 = 2.0
t0 = 0.0

w  = 1.0 #frequency

dt = 0.01 #timestep

t1 = 1.0 

def position(t):
 return(x0*cos(2*pi*w*t))

def verocity(t):
 return(x0*w*sin(2*pi*w*t))

#frame info
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
ax.set_title('orbit')
ax.set_xlabel('x')
ax.set_ylabel('x\'')
ax.set_xlim(-x0*1.5, x0*1.5)
ax.set_ylim(-x0*w*1.5, x0*w*1.5)

ims = [] #frame container

#make frames of the animation
for t in arange(t0, t1, dt):
 im, = ax.plot(position(t),verocity(t),c='r',marker='o',ms=10.0)
 ims.append([im])

#make the animation from frames
outanim = anim.ArtistAnimation(fig, ims,interval=1)

#show the animation 
plt.show()


# -- save animation in mp4
if False:
 # -- export file name
 filename = "orbit.mp4"
 print "making mp4 file"
 Writer = anim.writers['ffmpeg']
 writer = Writer(fps=10)
 outanim.save(filename,writer=writer)
 
 