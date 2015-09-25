from warp import *
from extpart import ZCrossingParticles

fo = PWpickle.PW("zmnt_"+str(top.it)+".pkl")
fo.xmnt = [[None for col in range(len(zmps))] for row in range(3)]
fo.ymnt = [[None for col in range(len(zmps))] for row in range(3)]
fo.uxmnt = [[None for col in range(len(zmps))] for row in range(3)]
fo.uymnt = [[None for col in range(len(zmps))] for row in range(3)]
fo.uzmnt = [[None for col in range(len(zmps))] for row in range(3)]
fo.exmnt = [[None for col in range(len(zmps))] for row in range(3)]
fo.eymnt = [[None for col in range(len(zmps))] for row in range(3)]
fo.zls = zmps
splen = len(sp.keys())
fo.xbars = [[None for col in range(len(zmps))] for row in range(splen)]
fo.ybars = [[None for col in range(len(zmps))] for row in range(splen)]
fo.uxbars = [[None for col in range(len(zmps))] for row in range(splen)]
fo.uybars = [[None for col in range(len(zmps))] for row in range(splen)]
fo.uzbars = [[None for col in range(len(zmps))] for row in range(splen)]

for cnt,ii in enumerate(sort(sp.keys())):
 for jj in range(len(zmps)):
  fo.xbars[cnt][jj] = average(zmnt[jj].getx(js=sp[ii].js))
  fo.ybars[cnt][jj] = average(zmnt[jj].gety(js=sp[ii].js))
  fo.uxbars[cnt][jj] = average(zmnt[jj].getux(js=sp[ii].js))
  fo.uybars[cnt][jj] = average(zmnt[jj].getuy(js=sp[ii].js))
  fo.uzbars[cnt][jj] = average(zmnt[jj].getuz(js=sp[ii].js))


for cnt,ii in enumerate(['U32','U33','U34']):
 for jj in range(len(zmps)):
  fo.xmnt[cnt][jj] = zmnt[jj].getx(js=sp[ii].js)
  fo.ymnt[cnt][jj] = zmnt[jj].gety(js=sp[ii].js)
  fo.uxmnt[cnt][jj] = zmnt[jj].getux(js=sp[ii].js)
  fo.uymnt[cnt][jj] = zmnt[jj].getuy(js=sp[ii].js)
  fo.uzmnt[cnt][jj] = zmnt[jj].getuz(js=sp[ii].js)
  fo.exmnt[cnt][jj] = zmnt[jj].getex(js=sp[ii].js)
  fo.eymnt[cnt][jj] = zmnt[jj].getey(js=sp[ii].js)

if True :
 fo.denx = [[None for col in range(len(zmps))] for row in range(splen)]
 fo.denxl = [[None for col in range(len(zmps))] for row in range(splen)]
 nx = 1000
 for cnt,ii in enumerate(sort(sp.keys())):
  for jj in range(len(zmps)): 
   xx = zmnt[jj].getx(js=sp[ii].js)
   npp = len(xx)
   if npp > 1 :
    xmin = -20*cm
    xmax = +20*cm
    denx = zeros(nx+1)
    setgrid1d(npp,xx,nx,denx,xmin,xmax)
    denxl = linspace(xmin,xmax,nx+1)
    fo.denx[cnt][jj] = denx
    fo.denxl[cnt][jj] = denxl

fo.close()

for jj in range(len(zmps)):
 zmnt[jj].clear()
