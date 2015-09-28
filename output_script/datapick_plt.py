from warp import *
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
#from scipy.interpolate import *
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



zmnt = 70.0
zwdt = 10.05

if False :

 if True :
  fi = PRpickle.PR('allpart2_2952.pkl')

  allspx  = fi.allspx
  allspy  = fi.allspy
  allspz  = fi.allspz
  allspvx = fi.allspvx
  allspvy = fi.allspvy
  allspvz = fi.allspvz
  allspex = fi.allspex
  allspey = fi.allspey
  allspez = fi.allspez

  fi.close()

 if False :
  fi = PRpickle.PR('wosc/allpart1010.pkl')
  #fi = PRpickle.PR('allpart1010.pkl')

  allspx  = fi.allspx
  allspy  = fi.allspy
  allspz  = fi.allspz
  allspvx = fi.allspvx
  allspvy = fi.allspvy
  allspvz = fi.allspvz
  fi.close()

 pcnt = 0
 skipnum = 1
 for ii in sort(sp.keys()):
  tmp = allspz[pcnt][::skipnum]
  lcz = (tmp<=(zmnt+0.5*zwdt))*(tmp>=(zmnt-0.5*zwdt))
  sp[ii].zzz = allspz[pcnt][::skipnum][lcz]
  sp[ii].xxx = allspx[pcnt][::skipnum][lcz]
  sp[ii].yyy = allspy[pcnt][::skipnum][lcz]
  sp[ii].vxx = allspvx[pcnt][::skipnum][lcz]
  sp[ii].vyy = allspvy[pcnt][::skipnum][lcz]
  sp[ii].vzz = allspvz[pcnt][::skipnum][lcz]
  sp[ii].exx = allspex[pcnt][::skipnum][lcz]
  sp[ii].eyy = allspey[pcnt][::skipnum][lcz]
  sp[ii].ezz = allspez[pcnt][::skipnum][lcz]
  pcnt += 1


if False :
 fi = PRpickle.PR('lostpart2_2276.pkl')

 pcnt = 0
 skipnum = 70000
 for ii in ['U32','U33','U34']:
  sp[ii].ttt = fi.tlos[pcnt][skipnum:]
  sp[ii].xxx = fi.xlos[pcnt][skipnum:]
  sp[ii].yyy = fi.ylos[pcnt][skipnum:]
  sp[ii].zzz = fi.zlos[pcnt][skipnum:]
  sp[ii].vxx = fi.uxlos[pcnt][skipnum:]
  sp[ii].vyy = fi.uylos[pcnt][skipnum:]
  sp[ii].vzz = fi.uzlos[pcnt][skipnum:]
  sp[ii].exx  = fi.exlos[pcnt][skipnum:]
  sp[ii].eyy  = fi.eylos[pcnt][skipnum:]
  pcnt += 1
 fi.close()
 
if False :
 fi = PRpickle.PR('ecfield_2952.pkl')
 ffxi = fi.xi *1000.0
 ffxf = fi.xf *1000.0
 ffyi = fi.yi *1000.0
 ffyf = fi.yf *1000.0
 ffzi = fi.zi
 z_launch = ffzi + 0.05
 ffzft = fi.zf 
 ffzf = (ffzft + z_launch)/2.0
 ffex = fi.ex
 ffey = fi.ey
 fi.close()
 fnx = len(ffex)
 fny = len(ffex[0])
 fnz = len(ffex[0][0])


 
 nxf = 31 
 nyf = 31
 xlf = linspace(-50,50,nxf)
 ylf = linspace(-40,40,nyf)
 
 apm = animplot(size=(10,10))
 ax = apm.msubplot(111)
 
 for ii in arange(68.68,ffzf-0.05,0.02):
 #for ii in [68.8]:
  zpl = ii
  xmf,ymf,zmf = meshgrid(xlf,ylf,zpl)
  fmfex = zeros(nxf*nyf)
  fmfey = zeros(nxf*nyf)
  
  getgrid3d(nxf*nyf,xmf.ravel(),ymf.ravel(),zmf.ravel(),fmfex,
            fnx-1,fny-1,fnz-1,ffex,ffxi,ffxf,ffyi,ffyf,ffzi,ffzf,0,0)
            
  getgrid3d(nxf*nyf,xmf.ravel(),ymf.ravel(),zmf.ravel(),fmfey,
            fnx-1,fny-1,fnz-1,ffey,ffxi,ffxf,ffyi,ffyf,ffzi,ffzf,0,0)
  
  pfex = fmfex.reshape(nxf,nyf)
  pfey = fmfey.reshape(nxf,nyf)
  xmf = xmf.ravel().reshape(nxf,nyf)
  ymf = ymf.ravel().reshape(nxf,nyf)
  
  tmp = abs(pfex) + abs(pfey)
  lw = 3.0*tmp/tmp.max()

  if True :
   #apm.stplot(ax,xmf,ymf,pfex,pfey,color='k',linewidth=lw,density=0.5, arrowsize=0.001)
   if ii == 68.68:
    scc = abs(pfex).max()
    vpbase = apm.vplot(ax,xmf,ymf,pfex/scc,pfey/scc)
   else :
    scc = abs(pfex).max()
    vpbase = apm.vplotu(vpbase,ax,xmf,ymf,pfex/scc,pfey/scc)
   #apm.cplot(ax,xmf,ymf,tmp,1,colors='none')
   apm.makeframe()
  
 apm.makemovie()
 
 if False :
  fig=figure(figsize=(10,10))
  aa=streamplot(xmf,ymf,pfex,pfey,color='k',linewidth=lw,density=0.5, arrowsize=1.5)
  bb = quiver(xmf,ymf,pfex,pfey,color='k',linewidth=1)
  cp = contour(xmf,ymf,tmp,1,colors='none')
  #clabel(cp, inline=1, fontsize=10)
  #show()
  
  
 raise Exception('to here')
 
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
 
 for jj in [0,50,100]:
  for ii in ['U32','U33','U34']:
   
   zmin = 68.68
   zmax = 68.68+100.0*0.02
   
   pxmax=pymax=50.0
   pxmin=pymin=-50.0
   
   apm = animplot(filename='dist-'+ii+'.mp4',size=(10,10))
   
   px1 = apm.msubplot(221)
   px1.set_xlabel('$x$ [mm]',fontsize=20)
   px1.set_ylabel('$y$ [mm]',fontsize=20) 
   px1.set_title('$x-y$ space',fontsize=20)
   px1.set_xlim(pxmin+20,pxmax-20)
   px1.set_ylim(pymin+20,pymax-20)

   px2 = apm.msubplot(222)
   px2.set_xlabel('$y$ [mm]',fontsize=20)
   px2.set_ylabel('$y\'$ [mrad]',fontsize=20) 
   px2.set_title('$y-y\'$ phase space',fontsize=20)
   px2.set_xlim(pxmin+20,pxmax-20)
   px2.set_ylim(pymin+20,pymax-20)
   
   px3 = apm.msubplot(223)
   px3.set_xlabel('$x$ [mm]',fontsize=20)
   px3.set_ylabel('$x\'$ [mrad]',fontsize=20) 
   px3.set_title('$x-x\'$ phase space',fontsize=20)
   px3.set_xlim(pxmin+20,pxmax-20)
   px3.set_ylim(pymin+20,pymax-20)
   
   px4 = apm.msubplot(224)
   px4.set_xlabel('$x\'$ [mrad]',fontsize=20)
   px4.set_ylabel('$y\'$ [mrad]',fontsize=20 )
   px4.set_title('$x\'-y\'$ phase space',fontsize=20)
   px4.set_xlim(pxmin+20,pxmax-20)
   px4.set_ylim(pymin+20,pymax-20)
   
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

   if False:
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
    
    #vx = vx-xslope*xx+(xbar*xslope -xpbar)    
    #vy = vy-yslope*yy+(ybar*yslope -ypbar)
    
    xybar = average(xx*yy)
    xyslope = (xybar - xbar*ybar)/xrms**2
    
    yys = yy-xyslope*xx+(xbar*xyslope -ybar)
    
    vxvybar = average(vx*vy)
    vxrms = sqrt(average(vx*vx))
    vxvyslope = (vxvybar - xpbar*ypbar)/vxrms**2
    vys = vy-vxvyslope*vx+(xpbar*vxvyslope -ypbar)
   else :
    yys = yy
    vys = vy
   
   cdxy   = getcdata(xx,yys)
   cdxvx  = getcdata(xx,vx)
   cdyvy  = getcdata(yy,vy)
   cdvxvy = getcdata(vx,vys)
   cdyvx = getcdata(yy,vx)
   

   pltint = 1
   #if jj == 0:
   obj=apm.splot(px1,xx[::pltint],yys[::pltint],c=cdxy[::pltint],s=1,lw=0)
   apm.cbars(obj)
   apm.splot(px2,yy[::pltint],vy[::pltint],c=cdyvy[::pltint],s=1,lw=0)
   apm.splot(px3,xx[::pltint],vx[::pltint],c=cdxvx[::pltint],s=1,lw=0)
   apm.splot(px4,vx[::pltint],vys[::pltint],c=cdvxvy[::pltint],s=1,lw=0)
   #apm.splot(px4,yy[::pltint],vx[::pltint],c=cdyvx[::pltint],s=2,lw=0)
   apm.tplot(px2,ii+" at z =" +str(zlsmnt[jj])+" [m]",-85,45,fontsize=30)
   #apm.tplot(px1,"$\hat{y} = $"+str(xyslope)[0:5]+"$x + y$",-25,max(yys)*0.9,fontsize=20)
   #apm.tplot(px4,"$\hat{y\'} = $"+str(vxvyslope)[0:5]+"$x\' + y\'$",-25,max(vys)*0.9,fontsize=20)
  #else :
   # apm.splot(px1,xx[::pltint],yy[::pltint],c=cdxy[::pltint],s=5,lw=0)
   # apm.splot(px2,yy[::pltint],vy[::pltint],c=cdxy[::pltint],s=5,lw=0)
   # apm.splot(px3,xx[::pltint],vx[::pltint],c=cdxy[::pltint],s=5,lw=0)
   # apm.splot(px4,vx[::pltint],vy[::pltint],c=cdxy[::pltint],s=5,lw=0)
   # apm.tplot(px1,ii+" at z =" +str(zlsmnt[jj])+" [m]",0,50,fontsize=30)
   #apm.makeframe()
   savefig('test'+str(jj)+'-'+ii+'.png')
   #apm.fig.remove()
   
   #apm.makemovie()
  #pdata=px.scatter(xx,yy, c=cdata,s=5,lw=0)
  #colorbar(pdata)
 
 raise Exception('to here')

 
 
 
 
 
 
 
 
zmax = 69.2 + 0.635*2.0*pi*0.25 + 0.4 
zmin = 69.2 - 0.54
rcParams['font.size'] = 30
rcParams['font.family'] = 'serif'

#fig=figure(figsize=(10,10))
fig=figure(figsize=(12,10))
#px = fig.add_subplot(111,projection='3d')
px = fig.add_subplot(111)

px.set_xlabel('$x$ [m]')
px.set_ylabel('$y$ [mrad]')
#px.set_ylabel('$x\'$ [mrad]')
#px.set_zlabel('$y$ [mm]')


pxmax=pymax=50.0
pxmin=pymin=-50.0
#px.set_xlim(zmin,zmax)
px.set_xlim(pxmin-0,pxmax-0)
px.set_ylim(pymin+20,pymax-20)

if False :
 tight_layout() 
 for ii in sp_Os + sp_U_low + sp_U_high + sp_targetr :
  px.scatter(sp[ii].zzz,sp[ii].xxx*1000.0,color=sp[ii].color,s=3)
 savefig("graph_zx.png")
 #show()

#raise Exception('to here')
if True :
 ii = 'U33'
 xx = 1000.0*sp[ii].xxx
 #xx = 1000.0*sp[ii].vxx/sp[ii].vzz
 yy = 1000.0*sp[ii].yyy
 #zz = 1000.0*sp[ii].xxx
 #yy = 1000.0*sp[ii].vyy/sp[ii].vzz

 npp = len(xx)
 ngx = 20
 ngy = 20
 xmin=xx.min()
 xmax=xx.max()
 ymin=yy.min()
 ymax=yy.max()

 if False :
  cdata = sp[ii].exx
 else:
  dgxy = zeros((ngx+1,ngy+1))
  setgrid2d(npp,xx,yy,ngx,ngy,dgxy,xmin,xmax,ymin,ymax)
  cdata=zeros(npp)
  getgrid2d(npp,xx,yy,cdata,ngx,ngy,dgxy,xmin,xmax,ymin,ymax)
  cdata = cdata/cdata.max()

 tight_layout()
 pdata=px.scatter(xx,yy, c=cdata,s=5,lw=0)
 colorbar(pdata)
 savefig("g"+ii+"_mxy.png")
 #show()

raise Exception('to here')
#zmax = max(sp['U33'].zzz)
#zmin = min(sp['U33'].zzz)
zmax = 69.2 + 0.635*2.0*pi*0.25 + 0.5 
zmin = 69.2 - 0.54
nnz = 200

for jj in sort(sp.keys()):
 sp[jj].xls = []
 sp[jj].yls = []
 sp[jj].zls = []
 sp[jj].vxls = []
 sp[jj].vyls = []
 sp[jj].vzls = []

 iniz = zmin
 for ii in linspace(zmin,zmax,nnz)[1:] :
  blz = (sp[jj].zzz >= iniz)*(sp[jj].zzz <= ii)
  sp[jj].xls.append(average(sp[jj].xxx[blz]))
  sp[jj].yls.append(average(sp[jj].yyy[blz]))
  sp[jj].zls.append(average(sp[jj].zzz[blz]))
  sp[jj].vxls.append(average(sp[jj].vxx[blz]))
  sp[jj].vyls.append(average(sp[jj].vyy[blz]))
  sp[jj].vzls.append(average(sp[jj].vzz[blz]))
  iniz = ii

 savetxt('hstdata-'+jj+'.dat',transpose((sp[jj].xls, sp[jj].yls, sp[jj].zls,
                                         sp[jj].vxls, sp[jj].vyls, sp[jj].vzls)))
                                         
                                         
                                         
