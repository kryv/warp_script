import os
import sys
from numpy import *
from scipy.optimize import *



ncount = 0
def optfnc(a) :
  global ncount
  #make input data file 
  savetxt("tmp.dat",a)
  
  #warp script reads 'tmp.dat'
  os.system("python frib-front-3d_l2.py > log")
  os.system("rm *.cgm*")
  
  #load final state data (x,vx,y,vy)  
  ans=loadtxt("zxyv.lst")
  
  print "step-" + str(ncount) +"   input -> "+str(a)+"   output(x,vx) ->"+str(ans)
  ncount +=1
  return(ans)

#initial values (sc, ox, oy, ot)
init = [0.0, 0.0, 0.0, 0.0]

#quasi-Newton method for finding roots in k variables
ans = broyden2(optfnc,init,iter=20)

optfnc(ans)
print ans