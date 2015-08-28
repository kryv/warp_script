from warp import *
from singleparticle import TraceParticle

# --- Set four-character run id, comment lines, user's name.
top.pline2   = "Test of bending"
top.pline1   = "Single particles, no space-charge"
top.runmaker = "David P. Grote"

outid = 4
# --- Invoke setup routine - it is needed to created a cgm file for plots
setup()

# --- Create the beam species
beam = Species(type=Potassium,charge_state=+1,name="Beam species")
beam2 = Species(type=Potassium,charge_state=+1,name="Beam species")

vz0 = 0.01*10.0**9

top.vbeam = vz0

top.diposet = false

bend_len = 0.5*pi
addnewbend(0.0, 0.0+bend_len, rc=1.0)

by0 = beam.mass/beam.sq*vz0/top.bendrc[0]

nx = 100
ny = 10
nz = 100

bxgrid = full((nx,ny,nz), 0.)
bygrid = full((nx,ny,nz), by0)
bzgrid = full((nx,ny,nz), 0.)
bg_len = bend_len + 0.4

ibgrd = addnewbgrddataset(dx=0.01, dy=0.1, zlength=bg_len, bx=bxgrid, by=bygrid, bz=bzgrid)
addnewbgrd(dx=0.01,dy=0.01,zs=-0.2,ze=-0.2+bg_len, id=ibgrd, xs=-0.5, ys=-0.5, he=true,lb=1)

# +++ Set input parameters describing the 3d simulation.
w3d.nx = 4
w3d.ny = 4
w3d.nz = 8
top.dt = 0.1*10**-9

# --- Set to finite beam.
w3d.xmmin = -1.
w3d.xmmax =  1.
w3d.ymmin = -2.
w3d.ymmax =  2.
w3d.zmmin = -1.5
w3d.zmmax = +3.

top.pboundxy = absorb
top.pbound0 = absorb
top.pboundnz = absorb

# --- turn off field solver
top.fstype = -1

def inj():
 # --- inject a stable particles
 for zi in linspace(-1.0,3.0,10):
  for xi in linspace(-1.0,1.0,10):
    beam.addpart(x=xi,z=zi,vz=0.0,gi=1)
 
 # --- inject a moving particles
 for xi in linspace(-0.4,0.4,3):
  beam2.addpart(x=xi,z=-1.0,vz=vz0,gi=1)

top.zbeam = -1.0  
installparticleloader(inj)

  
# save the history of x, z and  by
outx = []
outz = []
outb = []
outx2 = []
outz2 = []
outb2 = []

def checkvb():
  for ii in range(beam.getn()):
   outx.append(beam.getx()[ii])
   outz.append(beam.getz()[ii])
   outb.append(beam.getby()[ii])
  for ii in range(beam2.getn()):
   outx2.append(beam2.getx()[ii])
   outz2.append(beam2.getz()[ii])
   outb2.append(beam2.getby()[ii])

installafterstep(checkvb)
  
# --- Generate the PIC code (allocate storage, load ptcls, t=0 plots, etc.).

if True :
 package("w3d"); generate()

else :
 top.depos = 'none'
 wxy.ds = 1.0*mm
 wxy.lvzchang = true
 top.ibpush   = 2
 w3d.solvergeom = w3d.XYgeom
 package("wxy"); generate()

palette('blueorange.gp')


nz = 150
nx = 150
ny = 1

zmesh=[]
xmesh=[]
ymesh=[]

for zz in linspace(-1.0,3.0,nz):
 for xx in linspace(-1.0,1.0,nx):
  for yy in [0]:
   xmesh.append(xx)
   ymesh.append(0.0)
   zmesh.append(zz)

(ex_mesh,ey_mesh,ez_mesh,bx_mesh,by_mesh,bz_mesh) = getappliedfields(x=xmesh,y= ymesh,z=zmesh)

#plot grid data from getappliedfields()
xmb0 = array(xmesh)[by_mesh<0.1]
zmb0 = array(zmesh)[by_mesh<0.1]
xmb = array(xmesh)[by_mesh>=0.1]
zmb = array(zmesh)[by_mesh>=0.1]
ppgeneric(xmb0,zmb0,msize=2,color='blue',pplimits=(-1,3,-1,1),titlet='getappliedfields()',titleb='z',titlel='x',lframe=1)
ppgeneric(xmb,zmb,msize=2,color='red')
fma()

savetxt('xzb'+str(outid)+'.dat',transpose((xmesh,zmesh,by_mesh*10000)))

step(1)

#plot grid data from stable particles
xsb0 = array(outx)[array(outb)<0.1]
zsb0 = array(outz)[array(outb)<0.1]
xsb = array(outx)[array(outb)>=0.1]
zsb = array(outz)[array(outb)>=0.1]
ppgeneric(xsb0,zsb0,msize=2,color='blue',pplimits=(-1,3,-1,1),titlet='getby() from stable particles',titleb='z',titlel='x',lframe=1)
ppgeneric(xsb,zsb,msize=2,color='red')
fma()

beam.gaminv = 0

step(4000)

#plot grid data from moving particles
xgb0 = array(outx2)[array(outb2)<0.1]
zgb0 = array(outz2)[array(outb2)<0.1]
xgb = array(outx2)[array(outb2)>=0.1]
zgb = array(outz2)[array(outb2)>=0.1]
ppgeneric(xgb0,zgb0,msize=2,color='blue',pplimits=(-1,3,-1,1),titlet='getby() from moving particles',titleb='z',titlel='x',lframe=1)
ppgeneric(xgb,zgb,msize=2,color='red')
fma()

savetxt('torbit'+str(outid)+'.dat',transpose((array(outz2),array(outx2))))

#ff = PWpickle.PW('pporig.pkl')
#ff.pporig = pp
#ff.close()
