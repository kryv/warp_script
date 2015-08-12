#
# Warp plot movie maker : anm_plot.py
#
from warp import *
import matplotlib.pyplot as plt
import matplotlib.animation as anim

#plot step for all frames
init  = 0  # initial step of the frame
fin   = 1279 # final step of the frame
intrv = 2  # frame interval
movie_step = arange(init,fin,intrv)

#Export file 
filename = "diag_movie.mp4"

#skip number for particle distribution plot
plt_skip = 5

#plot colors
cols=["black","blue","red","cyan","magenta","lightgreen"]

#font size 
fnsz=20 

#frame storage
ims=[]

#upper side (211) plot information
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(211)
ax.set_title("Radial Number Density",fontname='serif',fontsize=fnsz)
ax.set_xlabel("radius $r$ [mm]",fontname='serif',fontsize=fnsz)
ax.set_ylabel(r"$\rho$ [particles/cm$^3$]",fontname='serif',fontsize=fnsz)
ax.set_yscale('log')
ax.set_xlim(0.0002,50.0)
ax.set_ylim(10.0**15,10.0**20.0)

#lower left side (223) plot information
bx = fig.add_subplot(223)
bx.set_title("$x-x'$ phase space",fontname='serif',fontsize=fnsz)
bx.set_xlabel("$x$ [mm]",fontname='serif',fontsize=fnsz)
bx.set_ylabel("$x'$ [mrad] ",fontname='serif',fontsize=fnsz)
bx.set_xlim(-50.0,50.0)
bx.set_ylim(-50.0,50.0)

#lower right side (224) plot information
cx = fig.add_subplot(224)
cx.set_title("Scaled Axial Field of Elements",fontname='serif',fontsize=fnsz)
cx.set_xlabel("$z$ [m]",fontname='serif',fontsize=fnsz)
cx.set_ylabel("$B_z$ and $E_z$",fontname='serif',fontsize=fnsz)
cx.set_xlim(66.5,69.3)
cx.set_ylim(0.0,1.1)


#make 1 frame -> append to ims   
def outplt1(a,b,c,d,e,f,g,h): 
 # drawing object storage
 im=[None for i in range(len(a)+len(c)+10)]
 imcnt = 0
 #-- drawing object tips
 # plot function must be "unpack" to append to ims
 # e.g    
 #     im, = plt.plot(xlist,ylist)
 #      #^ this "," is unpack option
 #     ims.append([im])
 # scatter and text function must not be unpack
 #
 print "-- making frame at step "+str(top.it)
 #drawing subplot(211) 
 for i in range(len(a)):
  im[imcnt], = ax.plot(a[i],b[i],cols[i],lw=2.5)
  imcnt += 1
   
 #drawing subplot(223)
 (slp,xofs,xpofs,vz) = getxxpslope()
 for i in range(len(c)):
  #im[imcnt],= bx.plot(c[i],d[i]-slp*c[i]+(xofs*slp - xpofs),".",color=cols[i])
  im[imcnt] = bx.scatter(c[i],d[i]-slp*c[i]+(xofs*slp - xpofs), s = 1.0, color=cols[i+1], alpha=1.0,edgecolors='none')
  # you can also use plot function for the distribution plot.
  # plot function -> use many memory resources but quick conversion to .mp4 file 
  # scatter function -> use few memory resources but slow conversion to .mp4 file 
  imcnt += 1
 
 #drawing subplot(224)
 im[imcnt],= cx.plot(e,f,color="k")
 im[imcnt+1],= cx.plot(e,g,color="b")
 im[imcnt+2],= cx.plot((h,h),(0,1.1),"--",lw=3.0,color="r")
 im[imcnt+3] = cx.text(h-0.2,0.9, "slice position",fontsize=fnsz,rotation=90,color="r")
 
 #add plot information
 im[imcnt+4] = ax.text(35.0,10.0**19.0, "- All species",fontsize=fnsz,color=cols[0],fontname='serif')
 im[imcnt+5] = ax.text(35.0,10.0**18.6, "- O$^{1-4}$",fontsize=fnsz,color=cols[1],fontname='serif')
 im[imcnt+6] = ax.text(35.0,10.0**18.2, "- U$^{<33}$",fontsize=fnsz,color=cols[2],fontname='serif')
 im[imcnt+7] = ax.text(35.0,10.0**17.8, "- U$^{>34}$",fontsize=fnsz,color=cols[3],fontname='serif')
 im[imcnt+8] = ax.text(35.0,10.0**17.4, "- U$^{33}$",fontsize=fnsz,color=cols[4],fontname='serif')
 im[imcnt+9] = ax.text(35.0,10.0**17.0, "- U$^{34}$",fontsize=fnsz,color=cols[5],fontname='serif')
 
 plt.tight_layout()
 ims.append(im)
 #plt.savefig('plt'+str(c)+'.png')

# make .mp4 file by ffmpeg converter
def makemovie(inp):
 print "making " + inp + " file"
 Writer = anim.writers['ffmpeg']
 writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)
 outanim = anim.ArtistAnimation(fig, ims, interval=50, repeat_delay=1000,blit=False)
 outanim.save(inp,writer=writer)

 
# make plot data (rely on frib-front.py)
def diag_movie():
    # --- radial mesh reflecting x-y grid structure to illustrate simulation noise
    nr    = nint(sqrt(w3d.nx/(2.*sym_x)*w3d.ny/(2.*sym_y)))
    rmax  = sqrt(w3d.xmmax*w3d.ymmax)
    dr    = rmax/nr 
    rmesh = linspace(0.,rmax,num=nr+1)
    #
    sp_list = sp_target #+ ["All"] 
    ns   = len(sp_list) 
    # --- density as a function or r on mesh array 
    den  = zeros(nr+1)
    #   
    weightr = zeros(nr+1)   
    count   = zeros(nr+1)

    out_plt_lst_x = []
    out_plt_lst_y = []

    # --- for all species on mesh 
    for ls in [sp.keys(),sp_Os,sp_U_low,sp_U_high]:
     for ii in ls:
       s  = sp[ii]
       #
       np = s.getn() 
       rp = s.getr() 
       wp = s.sw0*(1.0-neut_f1)*ones(np)
       #
       deposgrid1d(1,np,rp,wp,nr,weightr,count,0.,rmax)
     #
     den[1:nr+1] = weightr[1:nr+1]/(2.*pi*dr*rmesh[1:nr+1])
     den[0]      = den[1]   # set origin by next grid up to remove distraction
     #
     out_plt_lst_x.append(rmesh/mm)
     out_plt_lst_y.append(den/cm**3)
     weightr = zeros(nr+1)    # reset for clean accumulation/count with itask = 1 
     count   = zeros(nr+1)
     #
    # --- for target species on mesh 
    for ii in sp_target:
       s  = sp[ii]
       #
       np = s.getn() 
       rp = s.getr() 
       wp = s.sw0*(1.0-neut_f1)*ones(np)
       #
       weightr = zeros(nr+1)   # reset for clean accumulation/count with itask = 1 
       count   = zeros(nr+1)   
       deposgrid1d(1,np,rp,wp,nr,weightr,count,0.,rmax)
       # 
       den[1:nr+1] = weightr[1:nr+1]/(2.*pi*dr*rmesh[1:nr+1])
       den[0]      = den[1]   # set origin by next grid up to remove distraction
       #
       out_plt_lst_y.append(den/cm**3)
       out_plt_lst_x.append(rmesh/mm)

    outpc_x, outpc_xp = [], []
    #outpc_y, outpc_yp = [], []   

    # ---  distribution data to pass the frame
    for ls in [sp_Os,sp_U_low,sp_U_high]:
     tmpx = tmpxp = arange(0.0)
     #tmpy = tmpyp = arange(0.0)
     for i in ls:
      tmpx  = concatenate((tmpx ,sp[i].getx() /mm))
      tmpxp = concatenate((tmpxp,sp[i].getxp()/mr))
      #tmpy  = concatenate((tmpy ,sp[i].gety() /mm))
      #tmpyp = concatenate((tmpyp,sp[i].getyp()/mr))

     outpc_x.append(tmpx[::plt_skip])
     outpc_xp.append(tmpxp[::plt_skip])
     #outpc_y.append(tmpy)
     #outpc_yp.append(tmpyp)

    for i in sp_target:
     outpc_x.append((sp[i].getx()/mm)[::plt_skip])
     outpc_xp.append((sp[i].getxp()/mr)[::plt_skip])
     #outpc_y.append(sp[i].gety()/mm)
     #outpc_yp.append(sp[i].getyp()/mr)
     
    nz = 1000  
    z_mesh = linspace(ecr_z_extr,z_adv,nz+1)

    x_mesh = zeros(nz+1)
    y_mesh = zeros(nz+1) 

    (ex_mesh,ey_mesh,ez_mesh,bx_mesh,by_mesh,bz_mesh) = getappliedfields(x=x_mesh,y= y_mesh,z=z_mesh)

    ez_max = maxnd( abs(ez_mesh) ) 
    bz_max = maxnd( abs(bz_mesh) ) 
     
    outplt1(out_plt_lst_x, out_plt_lst_y, \
                     outpc_x, outpc_xp, \
                     z_mesh, bz_mesh/bz_max, ez_mesh/ez_max, top.zbeam)
                     
# call diag_movie at a timestep in movie_step
def movie_call():
  if top.it in movie_step:
    diag_movie()
  if top.it == movie_step[-1]:
    makemovie(filename)
    
installafterstep(movie_call)