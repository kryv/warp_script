from warp import *
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib_anim_wrapper import *


U_charge_states = [33,34,25,26,27,28,29,30,31,32,35,36,37,38,39,40]
O_charge_states = [1,2,3,4]

U_species = [Species(type=Uranium,charge_state=i,name='U%d'%i) for i in U_charge_states]
O_species = [Species(type=Oxygen, charge_state=i,name='O%d'%i) for i in O_charge_states]

U_ns = len(U_species) 
O_ns = len(O_species) 

sp_U = {U_species[i].name:U_species[i] for i in range(U_ns)}
sp_O = {O_species[i].name:O_species[i] for i in range(O_ns)}

sp = {}
sp.update(sp_U)
sp.update(sp_O)

sp_targetr = ['U34','U33']
sp_Os = ['O'+str(i) for i in range(1,5)]
sp_U_low = ['U'+str(i) for i in range(25,33)]
sp_U_high = ['U'+str(i) for i in range(35,41)] 

sp['O1'].color = "blue"
sp['O2'].color = "blue"
sp['O3'].color = "blue"
sp['O4'].color = "blue"

sp['U25'].color = "red"
sp['U26'].color = "red"
sp['U27'].color = "red"
sp['U28'].color = "red"
sp['U29'].color = "red"
sp['U30'].color = "red"
sp['U31'].color = "red"
sp['U32'].color = "red"

sp['U33'].color = "magenta"
sp['U34'].color = "green"

sp['U35'].color = "cyan"
sp['U36'].color = "cyan"
sp['U37'].color = "cyan"
sp['U38'].color = "cyan"
sp['U39'].color = "cyan"
sp['U40'].color = "cyan"


if True :
 fi = PRpickle.PR('zmnt_2952.pkl')
 cnt=0
 for ii in ['U32','U33','U34']:
  sp[ii].xxx = fi.xmnt[cnt]
  sp[ii].yyy = fi.ymnt[cnt]
  sp[ii].vxx = fi.uxmnt[cnt]
  sp[ii].vyy = fi.uymnt[cnt]
  sp[ii].vzz = fi.uzmnt[cnt]
  cnt+=1
 zlsmnt        = fi.zls
 fi.close()
 
 if True :
   fi = PRpickle.PR('zmnt_3152.pkl')
   cnt=0
   for ii in ['U32','U33','U34']:
    sp[ii].xxx2 = fi.xmnt[cnt]
    sp[ii].yyy2 = fi.ymnt[cnt]
    sp[ii].vxx2 = fi.uxmnt[cnt]
    sp[ii].vyy2 = fi.uymnt[cnt]
    sp[ii].vzz2 = fi.uzmnt[cnt]
    cnt+=1
   fi.close()
 
 
 rcParams['font.size'] = 15
 rcParams['font.family'] = 'serif'
 
 for jj in [0,100]:
  for ii in ['U33']:
   
   zmin = 68.68
   zmax = 68.68+100.0*0.02
   
   pxmax=pymax=50.0
   pxmin=pymin=-50.0
   
   apm = animplot(filename='dist-'+ii+'.mp4',size=(10,10))
   
   px1 = apm.msubplot(221)
   px1.set_xlabel('$x$ [mm]',fontsize=20)
   px1.set_ylabel('$\hat{y}$ [mm]',fontsize=20) 
   px1.set_title('$x-y$ space',fontsize=20)
   px1.set_xlim(pxmin+20,pxmax-20)
   #px1.set_ylim(pymin+20,pymax-20)

   px2 = apm.msubplot(222)
   px2.set_xlabel('$y$ [mm]',fontsize=20)
   px2.set_ylabel('$\hat{y\'}$ [mrad]',fontsize=20) 
   px2.set_title('$y-y\'$ phase space',fontsize=20)
   px2.set_xlim(pxmin+20,pxmax-20)
   #px2.set_ylim(pymin+20,pymax-20)
   
   px3 = apm.msubplot(223)
   px3.set_xlabel('$x$ [mm]',fontsize=20)
   px3.set_ylabel('$\hat{x\'}$ [mrad]',fontsize=20) 
   px3.set_title('$x-x\'$ phase space',fontsize=20)
   px3.set_xlim(pxmin+20,pxmax-20)
   #px3.set_ylim(pymin+20,pymax-20)
   
   px4 = apm.msubplot(224)
   px4.set_xlabel('$x\'$ [mrad]',fontsize=20)
   px4.set_ylabel('$\\tilde{y\'}$ [mrad]',fontsize=20 )
   px4.set_title('$x\'-y\'$ phase space',fontsize=20)
   px4.set_xlim(pxmin+20,pxmax-20)
   #px4.set_ylim(pymin+20,pymax-20)
   
   plt.subplots_adjust(wspace=0.4,hspace=0.5,top=0.8,right=0.8)
   
   rcParams['font.size'] = 15
   rcParams['font.family'] = 'serif'
   
   def getcdata(xx,yy):
    npp = len(xx)
    ngx = 30
    ngy = 30
    
    xmin=xx.min()
    xmax=xx.max()
    ymin=yy.min()
    ymax=yy.max()

    dgxy = zeros((ngx+1,ngy+1))
    setgrid2d(npp,xx,yy,ngx,ngy,dgxy,xmin,xmax,ymin,ymax)
    cdata=zeros(npp)
    getgrid2d(npp,xx,yy,cdata,ngx,ngy,dgxy,xmin,xmax,ymin,ymax)
    return(cdata/cdata.max())
   
   
   if True :
    xx = 1000.0*np.append(sp[ii].xxx[jj],sp[ii].xxx2[jj])
    yy = 1000.0*np.append(sp[ii].yyy[jj],sp[ii].yyy2[jj])
    vx = 1000.0*np.append(sp[ii].vxx[jj]/sp[ii].vzz[jj],sp[ii].vxx2[jj]/sp[ii].vzz2[jj])
    vy = 1000.0*np.append(sp[ii].vyy[jj]/sp[ii].vzz[jj],sp[ii].vyy2[jj]/sp[ii].vzz2[jj])
   else :
    xx = 1000.0*sp[ii].xxx[jj]
    yy = 1000.0*sp[ii].yyy[jj]
    vx = 1000.0*sp[ii].vxx[jj]/sp[ii].vzz[jj]
    vy = 1000.0*sp[ii].vyy[jj]/sp[ii].vzz[jj]

   
   vx = vx-average(vx)
   vy = vy-average(vy)

   if True:
    xbar = average(xx)
    xpbar = average(vx)
    xrms = sqrt(average(xx*xx))
    xxpbar = average(xx*vx)
    xslope = (xxpbar-xbar*xpbar)/xrms**2

   
    ybar = average(yy)
    ypbar = average(vy)
    yrms = sqrt(average(yy*yy))
    yypbar = average(yy*vy)
    yslope = (yypbar-ybar*ypbar)/yrms**2
    
    
    xybar = average(xx*yy)
    xyslope = (xybar - xbar*ybar)/xrms**2
    
    vxvybar = average(vx*vy)
    vxrms = sqrt(average(vx*vx))
    vxvyslope = (vxvybar - xpbar*ypbar)/vxrms**2
    
    vxs0 = vx-xslope*xx #+(xbar*xslope -xpbar)    
    vys0 = vy-yslope*yy #+(ybar*yslope -ypbar)
      
      
    yys = yy-xyslope*xx #+(xbar*xyslope -ybar)
    vys = vy-vxvyslope*vx #+(xpbar*vxvyslope -ypbar)
    
   else :
    yys = yy
    vys = vy
   
   cdxy   = getcdata(xx,yys)
   cdxvx  = getcdata(xx,vxs0)
   cdyvy  = getcdata(yy,vys0)
   cdvxvy = getcdata(vx,vys)
   cdyvx = getcdata(yy,vx)
   

   pltint = 1
   obj=apm.splot(px1,xx[::pltint],yys[::pltint],c=cdxy[::pltint],s=1,lw=0)
   apm.cbars(obj)
   apm.splot(px2,yy[::pltint],vys0[::pltint],c=cdyvy[::pltint],s=1,lw=0)
   apm.splot(px3,xx[::pltint],vxs0[::pltint],c=cdxvx[::pltint],s=1,lw=0)
   apm.splot(px4,vx[::pltint],vys[::pltint],c=cdvxvy[::pltint],s=1,lw=0)
   apm.tplot(px1,ii+" at z =" +str(zlsmnt[jj])+" [m]",0.5,1.25,fontsize=30,transform=px1.transAxes)
   apm.tplot(px1,"$\hat{y} = $"+str(xyslope)[0:5]+"$x + y$",0.05,0.9,fontsize=20,transform=px1.transAxes)
   apm.tplot(px2,"$\hat{y\'} = $"+str(yslope)[0:5]+"$y + y\'$",0.05,0.9,fontsize=20,transform=px2.transAxes)
   apm.tplot(px3,"$\hat{x\'} = $"+str(xslope)[0:5]+"$x + x\'$",0.05,0.9,fontsize=20,transform=px3.transAxes)
   apm.tplot(px4,"$\\tilde{y\'} = $"+str(vxvyslope)[0:5]+"$x\ + y\'$",0.05,0.9,fontsize=20,transform=px4.transAxes)
   savefig('sl2test'+str(jj)+'-'+ii+'.png')
