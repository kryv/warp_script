#
# Warp plot movie maker : anm_plot.py
#
# matplotlib and ffmpeg is required
#
from warp import *
import matplotlib.pyplot as plt
import matplotlib.animation as anim

#plot step for all frames
init  = 0  # initial step of the frame
fin   = 501 # final step of the frame
intrv = 2  # frame interval
movie_step = arange(init,fin,intrv)

#Export file 
filename = "diag_movie.mp4"

#skip number for particle distribution plot
plt_skip = 3

#plot colors
cols=["black","blue","red","cyan","lightgreen","magenta"]

#font size 
fnsz=20 

#frame storage
ims=[]

#upper side (211) plot information
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(211)
ax.set_title("x-projection density ",fontname='serif',fontsize=fnsz)
ax.set_xlabel("$x$ [mm]",fontname='serif',fontsize=fnsz)
ax.set_ylabel(r"$\rho$ [particles/cm$^2$]",fontname='serif',fontsize=fnsz)
ax.set_yscale('log')
ax.set_xlim(-200.0,200.0)
ax.set_ylim(10.0**15,10.0**19.0)
plot_info_len = 6

#lower left side (223) plot information
bx = fig.add_subplot(223)
bx.set_title("$x-x'$ phase space",fontname='serif',fontsize=fnsz)
bx.set_xlabel("$x$ [mm]",fontname='serif',fontsize=fnsz)
bx.set_ylabel("$x'$ [mrad] ",fontname='serif',fontsize=fnsz)
bx.set_xlim(-100.0,100.0)
bx.set_ylim(-100.0,100.0)

#lower right side (224) plot information
cx = fig.add_subplot(224)
cx.set_title("Laboratory frame centroid",fontname='serif',fontsize=fnsz)
cx.set_xlabel("$z$ [m]",fontname='serif',fontsize=fnsz)
cx.set_ylabel("$x$ [m]",fontname='serif',fontsize=fnsz)

bc_str  = d5_tmp_s
bc_oo   = 0.895
bc_oi   = d5_cond_out
bc_io   = d5_cond_in
bc_ii   = 0.365
bc_cen  = (bc_oi + bc_io)/2.0
bc_off  = 0.03
bc_offt = 0.001
bcp_dx  = 0.0002
#plot range
cx.set_xlim( bc_str - 0.05,  bc_str + bc_oo + 0.005)
cx.set_ylim(-bc_cen - 0.05, -bc_cen + bc_oo + 0.005)
#lines for outer bend conductor plotting
x1  = arange(bc_str+bc_off, bc_str+bc_oi-bc_offt, bcp_dx)
y1a = (bc_oi**2.0 - (x1 - bc_str)**2.0)**0.5 - bc_cen
y1b = (bc_oo**2.0 - (x1 - bc_str)**2.0)**0.5 - bc_cen
x2  = arange(bc_str+bc_oi , bc_str+bc_oo-bc_offt, bcp_dx)
y2  = (bc_oo**2.0 - (x2 - bc_str)**2.0)**0.5 - bc_cen
#lines for inner bend conductor plotting
x3  = arange(bc_str+bc_off, bc_str+bc_ii-bc_offt, bcp_dx)
y3a = (bc_ii**2.0 - (x3 - bc_str)**2.0)**0.5 - bc_cen
y3b = (bc_io**2.0 - (x3 - bc_str)**2.0)**0.5 - bc_cen
x4  = arange(bc_str+bc_ii , bc_str+bc_io-bc_offt, bcp_dx)
y4  = (bc_io**2.0 - (x4 - bc_str)**2.0)**0.5 - bc_cen




#make 1 frame -> append to ims   
def outplt1(a,b,c,d,e,f,g,h): 
 # drawing object storage
 im=[None for i in range(len(a)+len(c)+plot_info_len+f+ 9)]
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
  im[imcnt] = bx.scatter(c[i],d[i]-slp*c[i]+(xofs*slp - xpofs), s = 0.5, color=cols[i+1], alpha=1.0,edgecolors='none')
  # you can also use plot function for the distribution plot.
  # plot function -> use many memory resources but quick conversion to .mp4 file 
  # scatter function -> use few memory resources but slow conversion to .mp4 file 
  imcnt += 1

 #add plot information
 im[imcnt] = ax.text(108.0,10.0**18.5, "- All species",fontsize=fnsz,color=cols[0],fontname='serif')
 imcnt += 1
 im[imcnt] = ax.text(108.0,10.0**18.1, "- O$^{1-4}$",fontsize=fnsz,color=cols[1],fontname='serif')
 imcnt += 1
 im[imcnt] = ax.text(108.0,10.0**16.9, "- U$^{<33}$",fontsize=fnsz,color=cols[2],fontname='serif')
 imcnt += 1
 im[imcnt] = ax.text(108.0,10.0**16.5, "- U$^{>34}$",fontsize=fnsz,color=cols[3],fontname='serif')
 imcnt += 1
 im[imcnt] = ax.text(108.0,10.0**17.7, "- U$^{33}$",fontsize=fnsz,color=cols[5],fontname='serif')
 imcnt += 1
 im[imcnt] = ax.text(108.0,10.0**17.3, "- U$^{34}$",fontsize=fnsz,color=cols[4],fontname='serif')
 imcnt += 1
 
 #drawing subplot(224)
 for ii in range(len(e)-1):
  for jj in range(len(e[ii])):
   xbar = e[ii][jj]
   xtor = (xbar+bc_cen)*sin((g-bc_str)/bc_cen) + bc_str
   ytor = (xbar+bc_cen)*cos((g-bc_str)/bc_cen) - bc_cen
   plen = sum(abs(xbar) > smallpos)
   im[imcnt], = cx.plot(xtor[:plen],ytor[:plen],color=cols[ii+1],lw=1.5)
   imcnt += 1
    
 for jj in range(len(e[-1])):
  xbar = e[-1][jj]
  xtor = (xbar+bc_cen)*sin((g-bc_str)/bc_cen) + bc_str
  ytor = (xbar+bc_cen)*cos((g-bc_str)/bc_cen) - bc_cen
  plen = sum(abs(xbar) > smallpos)
  im[imcnt], = cx.plot(xtor[:plen],ytor[:plen],color=cols[-2+jj],lw=2.0)
  imcnt += 1
   
 im[imcnt]= cx.fill_between(x1,y1a,y1b,color="k")
 im[imcnt+1]  = cx.fill_between(x2,y2,-bc_cen+bc_off,color="k")
 im[imcnt+2]  = cx.fill_between(x3,y3a,y3b,color="k")
 im[imcnt+3]  = cx.fill_between(x4,y4,-bc_cen+bc_off,color="k")
 im[imcnt+4], = cx.plot((bc_str,bc_str),(-1,1),"k-")
 im[imcnt+5], = cx.plot((69.0,71.0),(-bc_cen,-bc_cen),"k-")
 im[imcnt+6], = cx.plot((bc_str+bc_off,bc_str+bc_off),(-1,1),"k--")
 im[imcnt+7], = cx.plot((69.0,71.0),(-bc_cen+bc_off,-bc_cen+bc_off),"k--")
 refz = h-bc_str
 x_in  = bc_io*sin(refz/bc_cen) + bc_str
 x_out = bc_oi*sin(refz/bc_cen) + bc_str
 y_in  = bc_io*cos(refz/bc_cen) - bc_cen
 y_out = bc_oi*cos(refz/bc_cen) - bc_cen
 im[imcnt+8], = cx.plot((x_in,x_out),(y_in,y_out),":",lw=3.0,color="r")
 
 

 
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

    # --- for x-projection density
    out_plt_lst_x = []
    out_plt_lst_y = []
    nx = w3d.nx + 1
    
    for ls in [sp.keys(),sp_Os,sp_U_low,sp_U_high]:
     denx = zeros(nx)
     for ii in ls:
       s  = sp[ii]
       if s.getn != 0:
        den = s.get_density()/cm**2
        denx += [sum(den[jj]) for jj in range(nx)]
     out_plt_lst_x.append(w3d.xmesh/mm)
     out_plt_lst_y.append(denx)
     
    for ii in sp_targetr:
     denx = zeros(nx)
     s  = sp[ii]
     den = s.get_density()/cm**2
     denx += [sum(den[jj]) for jj in range(nx)]
     out_plt_lst_x.append(w3d.xmesh/mm)
     out_plt_lst_y.append(denx)

    # --- for x-x' distribution
    outpc_x, outpc_xp = [], []
    #outpc_y, outpc_yp = [], []   

    # ---  distribution data to pass the frame
    for ls in [sp_Os,sp_U_low,sp_U_high]:
     tmpx = tmpxp = arange(0.0)
     #tmpy = tmpyp = arange(0.0)
     for i in ls:
      if sp[i].getn() != 0 : 
       tmpx  = concatenate((tmpx ,sp[i].getx() /mm))
       tmpxp = concatenate((tmpxp,sp[i].getxp()/mr))
       #tmpy  = concatenate((tmpy ,sp[i].gety() /mm))
       #tmpyp = concatenate((tmpyp,sp[i].getyp()/mr))

     outpc_x.append(tmpx[::plt_skip])
     outpc_xp.append(tmpxp[::plt_skip])
     #outpc_y.append(tmpy)
     #outpc_yp.append(tmpyp)

    for i in sp_targetr:
     outpc_x.append((sp[i].getx()/mm)[::plt_skip])
     outpc_xp.append((sp[i].getxp()/mr)[::plt_skip])
     #outpc_y.append(sp[i].gety()/mm)
     #outpc_yp.append(sp[i].getyp()/mr)
     
    sp_xbars = []
    for ls in [sp_Os,sp_U_low,sp_U_high,sp_targetr]:
     sp_xbars.append([sp[ii].hxbar[0] for ii in ls])
    
    #throw the plot data to making frame function 
    outplt1(out_plt_lst_x, out_plt_lst_y, \
            outpc_x, outpc_xp, \
            sp_xbars, len(sp.keys()), top.hzbeam[0:top.jhist+1], top.zbeam)
                     
# call diag_movie at a timestep in movie_step
def movie_call():
  if top.it in movie_step:
    diag_movie()
  if top.it == movie_step[-1]:
    makemovie(filename)
    
installafterstep(movie_call)