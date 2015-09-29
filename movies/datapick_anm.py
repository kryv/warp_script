from warp import *
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib_anim_wrapper import *
import os


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


fileflag1 = os.path.exists('zmnt_2952.pkl')
fileflag2 = os.path.exists('zmnt_3152.pkl')

if fileflag1 :
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
 
 cnt=0
 for ii in sort(sp.keys()):
  sp[ii].xbars = fi.xbars[cnt]
  sp[ii].ybars = fi.ybars[cnt]
  sp[ii].uxbars = fi.uxbars[cnt]
  sp[ii].uybars = fi.uybars[cnt]
  sp[ii].uzbars = fi.uzbars[cnt]
  cnt+=1
 
 fi.close()
 
 if fileflag2 :
   fi = PRpickle.PR('zmnt_3152.pkl')
   cnt=0
   for ii in ['U32','U33','U34']:
    sp[ii].xxx2 = fi.xmnt[cnt]
    sp[ii].yyy2 = fi.ymnt[cnt]
    sp[ii].vxx2 = fi.uxmnt[cnt]
    sp[ii].vyy2 = fi.uymnt[cnt]
    sp[ii].vzz2 = fi.uzmnt[cnt]
    cnt+=1
    
   cnt=0
   for ii in sort(sp.keys()):
    sp[ii].xbars2 = fi.xbars[cnt]
    sp[ii].ybars2 = fi.ybars[cnt]
    sp[ii].uxbars2 = fi.uxbars[cnt]
    sp[ii].uybars2 = fi.uybars[cnt]
    sp[ii].uzbars2 = fi.uzbars[cnt]
    cnt+=1
   
   fi.close()
   
   for ii in sort(sp.keys()):
    sp[ii].xbars = 0.5*(array(sp[ii].xbars) + array(sp[ii].xbars2))
    sp[ii].ybars = 0.5*(array(sp[ii].ybars) + array(sp[ii].ybars2))
    sp[ii].uxbars = 0.5*(array(sp[ii].uxbars) + array(sp[ii].uxbars2))
    sp[ii].uybars = 0.5*(array(sp[ii].uybars) + array(sp[ii].uybars2))
    sp[ii].uzbars = 0.5*(array(sp[ii].uzbars) + array(sp[ii].uzbars2))
 
 
 
 zmin = 68.68
 zmax = 68.68+100.0*0.02
 
 pxmax=pymax=50.0
 pxmin=pymin=-50.0
 
 apm = AnimPlot(filename='dset_u33u34.mp4',size=(10,10))

 rcParams['font.size'] = 15
 rcParams['font.family'] = 'serif'
 
 px1 = apm.msubplot(221)
 px1.set_xlabel('$z$ [m]')
 px1.set_ylabel('$x$ [mm]') 
 px1.set_title('Beam frame centroid')
 px1.set_xlim(68.66,zlsmnt.max()+0.02)
 px1.set_ylim(pymin+0,pymax-0)
 
  
 px2 = apm.msubplot(222)
 px2.set_xlabel('$x$ [mm]')
 px2.set_ylabel('$x\'$ [mrad]') 
 px2.set_title('U$^{33+}$ $x-x\'$ phase space',fontsize=20)
 px2.set_xlim(pxmin+0,pxmax-0)
 px2.set_ylim(pymin+0,pymax-0)
 
 px3 = apm.msubplot(223)
 px3.set_xlabel('$z$ [m]')
 px3.set_ylabel('$x$ [m]') 
 px3.set_title('Laboratory frame centroid')
 px3.set_xlim(68.66,70.08)
 px3.set_xticks(arange(68.8,70.1,0.2))
 px3.set_xticklabels(arange(68.8,70.1,0.2),rotation=-45)
 px3.set_ylim(-1.15,0.27)
 
 px4 = apm.msubplot(224)
 px4.set_xlabel('$x$ [mrad]')
 px4.set_ylabel('$x\'$ [mrad]') 
 px4.set_title('U$^{34+}$ $x-x\'$ phase space',fontsize=20)
 px4.set_xlim(pxmin+0,pxmax-0)
 px4.set_ylim(pymin+0,pymax-0)
 
 plt.subplots_adjust(wspace=0.4,hspace=0.4,top=0.85,right=0.87)
 
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
  
 def conv(z,x):
  rc = 0.635
  ini = 69.2
  fin = ini + 0.5*pi*rc
  if isnan(x):
   return(nan,nan)
  if z <ini: 
   return(z,x)
  elif z < fin:
   phi = (z-ini)/rc
   zt = ini+(rc+x)*sin(phi)
   xt = -rc+ (rc+x)*cos(phi)
   return(zt,xt)
  else :
   zt = x + rc + ini
   xt = -rc - (z-fin) 
   return(zt,xt)
 
 for jj in range(0,101,2):
  
  rcParams['font.size'] = 15
  
  for ii in sp_Os+sp_U_low+sp_U_high+['U34','U33']:
   bzlen = 0.5*pi*0.635
   apm.nplot(px1,zlsmnt,1000*sp[ii].xbars,c=sp[ii].color)
  
  apm.nplot(px1,[69.2,69.2],[-50,50],'k--',lw=0.8)
  apm.nplot(px1,[69.2+bzlen,69.2+bzlen],[-50,50],'k--',lw=0.8)
  apm.nplot(px1,ones(2)*zlsmnt[jj],[-50,50],'-',color='orange',lw=1.5)
 
  for ii in sp_Os+sp_U_low+sp_U_high+['U34','U33']:
   ans=array(map(conv,zlsmnt,sp[ii].xbars))
   apm.nplot(px3,ans[:,0],ans[:,1],c=sp[ii].color)

  apm.nplot(px3,[69.2,69.2],[-5,5],'k--',lw=0.8)
  apm.nplot(px3,[50,100],[-0.635,-0.635],'k--',lw=0.8)
  
  ans=array(map(conv,zlsmnt,0.215*ones(len(zlsmnt))))
  apm.nplot(px3,ans[:,0],ans[:,1],'k-',lw=5)
  ans=array(map(conv,zlsmnt,-0.225*ones(len(zlsmnt))))
  apm.nplot(px3,ans[:,0],ans[:,1],'k-',lw=5)
  ans=array(map(conv,zlsmnt,0.0*ones(len(zlsmnt))))
  apm.nplot(px3,ans[:,0],ans[:,1],'k--',lw=0.8)
  
  ans=array(map(conv,ones(2)*zlsmnt[jj],[-0.21,0.21]))
  apm.nplot(px3,ans[:,0],ans[:,1],'-',color='orange',lw=1.5)
  
  offx = 68.7
  offy = 66
  apm.tplot(px1,"z =" +str(zlsmnt[jj])+" [m]",70.3,82,fontsize=30)
  apm.tplot(px1,"O$^{1 \sim 4+}$",offx,offy,color=sp['O1'].color,fontsize=30)
  apm.tplot(px1,"U$^{33+}$",offx+1,offy,color=sp['U33'].color,fontsize=30)
  apm.tplot(px1,"U$^{34+}$",offx+1.8,offy,color=sp['U34'].color,fontsize=30)
  apm.tplot(px1,"U$^{25 \sim 32+}$",offx+2.8,offy,color=sp['U25'].color,fontsize=30)
  apm.tplot(px1,"U$^{35 \sim 40+}$",offx+4,offy,color=sp['U40'].color,fontsize=30)

  apm.tplot(px2,"U$^{32+}$",-45,35,color=sp['U32'].color,fontsize=20)
  apm.tplot(px2,"U$^{34+}$",-45,25,color=sp['U34'].color,fontsize=20)
  
  apm.tplot(px4,"U$^{32+}$",-45,35,color=sp['U32'].color,fontsize=20)
  apm.tplot(px4,"U$^{33+}$",-45,25,color=sp['U33'].color,fontsize=20)
 
 
  for kk in [0,1]:
   for ii in ['U32','U33','U34']:
    if True :
     xx = 1000.0*np.append(sp[ii].xxx[jj],sp[ii].xxx2[jj])
     vx = 1000.0*np.append(sp[ii].vxx[jj]/sp[ii].vzz[jj],sp[ii].vxx2[jj]/sp[ii].vzz2[jj])
    else :
     xx = 1000.0*sp[ii].xxx[jj]
     vx = 1000.0*sp[ii].vxx[jj]/sp[ii].vzz[jj]

    pltint = 5
    dsize = 2    
    
    if kk == 0 :
     if ii == 'U33':
      apm.splot(px4,xx[::pltint],vx[::pltint],c=sp[ii].color,s=dsize,lw=0)
     elif ii == 'U34':
      apm.splot(px2,xx[::pltint],vx[::pltint],c=sp[ii].color,s=dsize,lw=0)
     elif ii == 'U32':
      apm.splot(px2,xx[::pltint],vx[::pltint],c=sp[ii].color,s=dsize,lw=0)
      apm.splot(px4,xx[::pltint],vx[::pltint],c=sp[ii].color,s=dsize,lw=0)
    
    elif kk == 1:
     cdxvx  = getcdata(xx,vx)
     if ii == 'U33':
      if jj == 0:
       obj=apm.splot(px2,xx[::pltint],vx[::pltint],c=cdxvx[::pltint],s=dsize,lw=0)
       apm.cbars(obj,0.9, 0.1, 0.05, 0.75)
      else :
       apm.splot(px2,xx[::pltint],vx[::pltint],c=cdxvx[::pltint],s=dsize,lw=0)
     
     elif ii == 'U34':
      apm.splot(px4,xx[::pltint],vx[::pltint],c=cdxvx[::pltint],s=dsize,lw=0)
   
  
  apm.makeframe()
   
 apm.makemovie()


 raise Exception('to here')

 
 
 
                                         
