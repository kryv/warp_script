import os
import sys
from numpy import *
from scipy.optimize import *


#step counter
ncount = 0

#xvx storage
stans = ones(2)
#scale factor and placement storage
sttmp = 0.0*ones(2)

def optfnc(a) :
  global ncount,stans,sttmp
  #make input data file 
  savetxt("sfdr.dat",a)
  
  #warp script reads 'tmp.dat'
  os.system("python frib-front-3d.py > log")
  os.system("rm frib-front-3d.*.pkl")
  
  #load final state data (x,vx)  
  ans=loadtxt("tmpxvx.lst")
  
  print "step-" + str(ncount) +"   input -> "+str(a)
  print "         output(x,vx) -> "+str(ans)
  
  #save smallest answer
  if abs(stans[0]*stans[1]) > abs(ans[0]*ans[1]) :
    stans = ans
    sttmp = a
  ncount +=1
  return(ans)

#initial values (sc, ox, oy, ot)
init = [0.0, 0.0]

#quasi-Newton method for finding roots in k variables
ans = broyden2(optfnc,init,iter=20)

optfnc(stans)
savetxt("stpl.dat",sttmp)
print sttmp
print stans