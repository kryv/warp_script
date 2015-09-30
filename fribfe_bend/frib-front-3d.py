"""
Python input script for a Warp xy slice simulation of 
the FRIB front end.  For help and/or additional information contact:

     Steve Lund     lund@frib.msu.edu    (517) 908-7291

For documentation see the Warp web-site:

     https://warp.lbl.gov

All code inputs are mks with the exception of particle kinetic energy (eV).   

To run this Warp script:
  Interactive (return to interpreter after executing):

    % python -i frib-front-xy.py 

  Non-interactive (exit interpreter after executing):

    % python frib-front-xy.py
"""

# Load Warp and various script packages 
from warp        import *               # Warp code 
from errorcheck  import checksymmetry   # Check for input errors
from extpart import ZCrossingParticles
#from matplotlib_anim_wrapper import *
random.seed(100)  

#dist_load_type = 0  # load reference orbit
dist_load_type = 1  # load DC beam

#find convergence values by scale factor and shifting center
find_conv = False
if find_conv:
    tmpload = loadtxt('sfdr.dat')
    dltr = tmpload[0]    # r offset of the bend
    sclf = tmpload[1]    # B field scale factor of the bend

else:    
    # Convergence values for dt = 0.5e-9
    #dltr = -1.49315359e-5    # r offset of the bend
    #sclf =  1.11253776e-3    # B field scale factor of the bend

    # Convergence values for dt = 1e-9
    dltr = -1.20575783e-6    # r offset of the bend
    sclf =  1.11386387e-3    # B field scale factor of the bend

offy =  0.0    # y offset of the bend
bnka =  0.0    # bank angle of the bend

# Grid data and distribution data setting
pfld = ''
sfld = ''
dfld = ''

if dist_load_type == 1:
    slice_dist0 = dfld+'allpart1010.pkl'
    slice_dist1 = dfld+'allpart1011.pkl'
    
ecr_grid_lin = pfld+'lat_ecr_venus.lin.20150813.pkl'
sol_grid_lin = pfld+'s4.lin.20150907.pkl'
sol_grid_rz = pfld+'s4.rz.20150907.pkl'
sol_grid_at = pfld+'s4.at.20150907.pkl'
gag_grid_lin = pfld+'lat_gag.lin.20141029.pkl'
gag_grid_rz = pfld+'lat_gag.rz.20141029.pkl'
bnd_grid_tr = pfld+'bend_tri.table'
bnd_grid_3d = pfld+'lat_d5.3d.20140527.pkl'


# Set informational labels included on all output cgm plots.   
top.pline2   = "xy Slice Simulation: FRIB Front End" 
top.pline1   = " "   # Add more info, if desired.  

# Invoke setup routine for graphics and output files (THIS IS MANDATORY)
setup(writetodatafile=1, cgmlog=0)

# Set runmaker - included in informational labels on output plots
top.runmaker = "KFukushima"

# Beam parameters for simulation
#
#   Other than numerical parameters, the physical simulation is specified
#   by the numbers input immediately below.  

# --- Define species
# 
#     Syntax of later use:
#
#       for us in U_species:
#         us.ppzx()
#
#     Dictionaries also setup later. 


# Setup handling for species weights 
# Via Dave Grote: need to setup scaling by hand for multi-species 
#  top.wpid = nextpid()     # setup/allocate pid array on generate 
#
#  species.getw()  = s.w   gets weights of species  [equivalent to species.w] (top.wpid must be set to work)  
#  species.getweights() returns product of species.sw*species.w 
#
#  put in adjustment using beforeloadrho() 
# 
#  beam.w * beam.sw = total weight = beam.getweights() 
# 

U_charge_states = [33,34,25,26,27,28,29,30,31,32,35,36,37,38,39,40]
O_charge_states = [1,2,3,4]

U_species = [Species(type=Uranium,charge_state=i,name='U%d'%i) for i in U_charge_states]
O_species = [Species(type=Oxygen, charge_state=i,name='O%d'%i) for i in O_charge_states]

U_ns = len(U_species) 
O_ns = len(O_species) 

# --- --- make abbreviated dictionary of species for later diagnostics 
#         sp.keys()
sp_U = {U_species[i].name:U_species[i] for i in range(U_ns)}
sp_O = {O_species[i].name:O_species[i] for i in range(O_ns)}

sp = {}
sp.update(sp_U)
sp.update(sp_O)

# --- Setup for variable particle weights on generate.
#       Note: pid array elements hold particle properties and are consistently mirrored when particles scraped  
#             nextpid() gets next pid array index 

top.wpid = nextpid()       # set pid index for variable weights: will initialize on generate when set  
uzp0pid  = nextpid() - 1   # set pid index to hold particle initial uz to scale weights (set after generate)  
sw0pid   = nextpid() - 1

# --- --- assign species colors using values which may help distinguish on plots: target magenta/green
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

# --- Target species tuple for later use 
sp_target = ['U33','U34']
sp_targetr = ['U34','U33']
sp_Os = ['O'+str(i) for i in range(1,5)]
sp_U_low = ['U'+str(i) for i in range(25,33)]
sp_U_high = ['U'+str(i) for i in range(35,41)]


# --- Reference species as average of target 
A_ref = 0. 
Q_ref = 0. 
for ii in sp_target:
    s = sp[ii]
    A_ref += s.mass/amu 
    Q_ref += s.charge/echarge 
A_ref = A_ref/len(sp_target) 
Q_ref = Q_ref/len(sp_target)  

m_ref = A_ref*amu 

SourceBias = 35.*keV  # source voltage: set for Q_ref*SourceBias/A =>  4.9264706 keV/u for U 
  
#
# Setup Lattice  
#

ekin_per_u = 12.*keV                             # target kinetic energy/u for LEBT 
StandBias = A_ref*ekin_per_u/Q_ref - SourceBias  # Bias of Injector Column  

Bias = StandBias + SourceBias

top.lrelativ   = 1                # turn on relativity 

# --- Venus ECR Source 
#     Comment: Must have same z-grids for linear and nonlinear forms.  Minimal error checking to enforce this. 

# --- --- element specification 

ecr_shift  = 11.*cm                 # shift of ecr from lattice file spec to make room for s4p1 
ecr_z_extr = 66.650938 - ecr_shift # z-location of beam extraction aperture in simulation coordinates     
ecr_sc     = 0.0                    # scale factor to muliply field data by 
ecr_typ    = "lin"                  # type: "lin" = linear optics fields or "nl" = nonlinear r-z field  

# --- --- linear element data  
fi = PRpickle.PR(ecr_grid_lin)
ecr_bz_extr = fi.ecr_venus_bz_extr
ecr_dz = fi.ecr_venus_dz 
ecr_nz = fi.ecr_venus_nz  
ecr_z_m     = fi.ecr_venus_z_m
ecr_zm_extr = fi.ecr_venus_z_extr  # extraction location on z_m mesh field    
ecr_bz0_m   = fi.ecr_venus_bz0_m
ecr_bz0p_m  = fi.ecr_venus_bz0p_m
fi.close() 

ecr_zlen  = ecr_z_m.max() - ecr_z_m.min()                 # length ecr field mesh  
ecr_zmmin = ecr_z_extr - (ecr_zm_extr - ecr_z_m.min())    # start point of ecr field mesh in sim coordinates 
ecr_zmmax = ecr_z_extr + (ecr_z_m.max() - ecr_zm_extr)    # end   point of ecr field mesh in sim coordinates

ecr_lin_id = addnewmmltdataset(zlen=ecr_zlen,ms=ecr_bz0_m,msp=ecr_bz0p_m,nn=0,vv=0)

# --- --- define venus ecr fields  
if ecr_typ == "lin":
    ecr = addnewmmlt(zs=ecr_zmmin,ze=ecr_zmmax,id=ecr_lin_id,sc=ecr_sc) 
elif ecr_typ == "nl":
    #addnewbgrd(xs=0.,zs=s41_zc-s4_zlen/2.,ze=s41_zc+s4_zlen/2.,id=s4_nl_id,func=s41_scale)
    raise Exception("No ECR Venus Nonlinear Applied Fields Defined") 
    ecr = None
else:
    print("Warning: No ECR Applied Fields Defined") 
    ecr = None


# --- S4 solenoids 
#     Comment: linear and nonlinear variants must have same z-grid.  Minimal error checking only for input 
#              consistency.   

# --- --- element specification 

s4p1_zc  = 66.956900   # S4 1: z-center  
s4p1_str = 0.0 # 0.754 # S4 1: peak on-axis B_z field strength [Tesla]
s4p1_typ = "nl"        # S4 1: type: "lin" = linear optics fields or "nl" = nonlinear r-z field  

s4p2_zc  = 68.306900   # S4 2: z-center 
s4p2_str = 0.0 # 0.617 # s4 2: peak on-axis B_z field strength [Tesla]
s4p2_typ = "nl"        # S4 1: type: "lin" = linear optics fields or "nl" = nonlinear r-z field  

# --- --- linear element data  
fi = PRpickle.PR(sol_grid_lin)
s4_dz  = fi.s4_dz 
s4_nz  = fi.s4_nz  
s4_z_m = fi.s4_z_m 
s4_bz0_m   = fi.s4_bz0_m
s4_bz0p_m  = fi.s4_bz0p_m
fi.close() 

s4_zlen = s4_z_m.max() - s4_z_m.min() 
s4_lin_id = addnewmmltdataset(zlen=s4_zlen,ms=s4_bz0_m,msp=s4_bz0p_m,nn=0,vv=0)

# --- --- nonlinear element field data 
fi = PRpickle.PR(sol_grid_rz)
#
s4_len_coil   = fi.s4_len_coil 
s4_len_magnet = fi.s4_len_magnet 
s4_r_coil_i   = fi.s4_r_coil_i 
s4_r_coil_o   = fi.s4_r_coil_o
#
if fi.s4_nz != s4_nz: raise Exception("S4: Nonlinear field model nz not equal to linear field model nz") 
s4_dr   = fi.s4_dr
s4_nr   = fi.s4_nr 
s4_r_m  = fi.s4_r_m 
s4_br_m_in = fi.s4_br_m
s4_bz_m_in = fi.s4_bz_m
fi.close() 

# --- --- nonlinear element vector potential data 
fi = PRpickle.PR(sol_grid_at)
#
if fi.s4_nz != s4_nz: raise Exception("S4: Nonlin Vector potential model nz not equal to nonlinear/linear model nz")
if fi.s4_nr != s4_nr: raise Exception("S4: Nonlin Vector potential model nr not equal to nonlinear model nr")
s4_at_m  = fi.s4_at_m
fi.close() 

# Axisymmetric b-field arrays must be 3d shape (nr+1,arb,nz+1) to load into Warp  
s4_br_m = fzeros((s4_nr+1,1,s4_nz+1))  
s4_br_m[:,0,:] = s4_br_m_in
s4_bz_m = fzeros((s4_nr+1,1,s4_nz+1))
s4_bz_m[:,0,:] = s4_bz_m_in

s4_nl_id = addnewbgrddataset(dx=s4_dr,dy=1.,zlength=s4_zlen,bx=s4_br_m,bz=s4_bz_m,rz = true)  # pass arb dy to avoid error trap  

s4_aspect = s4_r_coil_i/s4_len_coil 

# --- --- define solenoid s4 1 
if s4p1_typ == "lin":
    s4p1 = addnewmmlt(zs=s4p1_zc-s4_zlen/2.,ze=s4p1_zc+s4_zlen/2.,id=s4_lin_id,sc=s4p1_str) 
elif s4p1_typ == "nl":
    s4p1 = addnewbgrd(xs=0.,zs=s4p1_zc-s4_zlen/2.,ze=s4p1_zc+s4_zlen/2.,id=s4_nl_id,sc=s4p1_str)
else:
    print("Warning: No S4 1st Solenoid Applied Fields Defined") 
    s4p1 = None

# --- --- define solenoid s4 2 
if s4p2_typ == "lin":
    s4p2 = addnewmmlt(zs=s4p2_zc-s4_zlen/2.,ze=s4p2_zc+s4_zlen/2.,id=s4_lin_id,sc=s4p2_str) 
elif s4p2_typ == "nl":
    s4p2 = addnewbgrd(xs=0.,zs=s4p2_zc-s4_zlen/2.,ze=s4p2_zc+s4_zlen/2.,id=s4_nl_id,sc=s4p2_str)
else:
    print("Warning: No S4 2nd Solenoid Applied Fields Defined") 
    s4p2 = None

  
# --- Grated Acceleration Gap
#   Note: for ideal zero-length gap:  top.lacclzl=true for zero length gap.  Accel given given by acclez*(accelze-acclzs) 
#   see dave grote email on caution on setting top.acclsw for gaps.   
#   Comment: Linear and nonlinear forms must have same axial grid.  Miminal error checking only for this.  

# --- --- element specification 
gag_zc  = 67.811564  # Grated Accel Gap: z-center  
gag_typ = "no"       # Grated Accel Gap: type: "ideal" = Short gap kick, "lin" = linear r-z field imported, "nl" = nonlinear r-z field imported   

# --- --- linear element data  
# fi = PRpickle.PR("lat_gag.lin.20140624.pkl")  # Original Warp model with simplified geometry  
fi = PRpickle.PR(gag_grid_lin)    # Poisson model with high detail 
gag_dz = fi.gag_dz0 
gag_nz = fi.gag_nz0  
gag_z_m     = fi.gag_z0_m  
gag_ez0_m   = fi.gag_ez0_m
gag_ez0p_m  = fi.gag_ez0p_m
fi.close() 

gag_zlen = gag_z_m.max() - gag_z_m.min() 

gag_lin_id = addnewemltdataset(zlen=gag_zlen,es=gag_ez0_m,esp=gag_ez0p_m,nn=0,vv=0)

# --- --- nonlinear element data
#fi = PRpickle.PR('lat_gag.rz.20140624.pkl')  # Original Warp model with simplified geometry  
fi = PRpickle.PR(gag_grid_rz)   # Poisson model with high detail 
if fi.gag_nz != gag_nz: raise Exception("GAG: Nonlinear and linear field model nz not equal") 
gag_nr = fi.gag_nr
gag_dr = fi.gag_dr
gag_r_m = fi.gag_r_m
gag_z_m_cen = fi.gag_z_m_cen
gag_phi_m    = fi.gag_phi_m 
gag_er_m_in  = fi.gag_er_m
gag_ez_m_in  = fi.gag_ez_m
fi.close() 

gag_zlen = gag_z_m.max()-gag_z_m.min()          # axial length nonlin/lin structure on mesh 

gag_zs   = gag_zc - (gag_z_m_cen-gag_z_m.min()) # z_start of nonlin/lin mesh structure  
gag_ze   = gag_zc + (gag_z_m.max()-gag_z_m_cen) # z_end   of nonlin/lin mesh structure 

# Geometry parameters ?? Read these in grated gap file to be safe .. ** must be consistent with input data ** ?? 
gag_rp = 7.3*cm                  # pipe radius of inner extent of rings in grated gap 
gag_col_zs = gag_zc - 11.989*cm  # z-start (at end   of biased upstream pipe)     of grated gap mechanical structure 
gag_col_ze = gag_zc + 15.611*cm  # z-end   (at start of grounded downstream pipe) of grated gap mechanical structure  

gag_er_m = fzeros((gag_nr+1,1,gag_nz+1)) # Axisymmetric e-field arrays must be 3d shape (nr+1,arb,nz+1) to load into Warp  
gag_er_m[:,0,:] = gag_er_m_in
gag_ez_m = fzeros((gag_nr+1,1,gag_nz+1))
gag_ez_m[:,0,:] = gag_ez_m_in

gag_nl_id = addnewegrddataset(dx=gag_dr,dy=1.,zlength=gag_zlen,ex=gag_er_m,ez =gag_ez_m,rz = true) 

# --- --- define grated acceleration gap  
if gag_typ == "ideal":
    print("Wanning: No Ideal Acceleration Gap model yet implemented")  
    gag = None 
elif gag_typ == "lin":
    gag = addnewemlt(zs=gag_zs,ze=gag_ze,id=gag_lin_id,sc=StandBias) 
elif gag_typ == "nl":
    gag = addnewegrd(xs=0.,zs=gag_zs,ze=gag_ze,id=gag_nl_id,sc=StandBias)
    #gag = addnewegrd(xs=0.,zs=gag_zs,ze=gag_ze,id=gag_nl_id,sc=0.0)
else:
    print("Warning: No Grated Acceleration Gap Applied Fields Defined") 
    gag = None 


# --- D5 Bending Dipole 

# --- --- element specification 

d5p1_str = 0.6015157305571277 + sclf # D5 1: Input field scale factor
d5p1_typ = "nl"        # D5 1: type: "lin" = linear optics fields or "3d" = 3d field  

# --- --- nonlinear element data 
#Bend magnet section info
d5_cond_in = 43.0*cm
d5_cond_out = 84.0*cm
d5_x_ap = (d5_cond_out - d5_cond_in)/2.0
d5_y_ap = 5.0*cm
d5_tmp_rc = (d5_cond_out + d5_cond_in)/2.0
d5_tmp_s = 69.2
d5_tmp_e = d5_tmp_s + (d5_tmp_rc*2.0*pi)*0.25

#bgrd data info

d5a_nx = 150
d5a_ny = 20
d5a_nz = 300

d5a_xw = (75.0)*cm
d5a_yw = 10.0*cm
d5a_zlen = (150.0)*cm 

d5a_cen = (d5_tmp_s + d5_tmp_e)/2.0
d5a_s = d5a_cen - d5a_zlen/2.0
d5a_e = d5a_cen + d5a_zlen/2.0
d5a_xs = -d5_tmp_rc +15.0*cm  + dltr

d5a_dx = d5a_xw/float(d5a_nx)
d5a_dy = d5a_yw/float(d5a_ny)
d5a_dz = d5a_zlen/float(d5a_nz)

d5a_oy = offy
d5a_ph = bnka


if d5p1_typ == "nl" :
    print "--- loading bend bgrid"

    fi = PRpickle.PR(bnd_grid_3d) 
    d5a_bx = fi.d5_bx_m*gauss
    d5a_by = fi.d5_by_m*gauss
    d5a_bz = fi.d5_bz_m*gauss
    fi.close()
  
    d5a_3d_id = addnewbgrddataset(dx=d5a_dx ,dy=d5a_dy ,zlength=d5a_zlen ,bx=d5a_bx, by=d5a_by ,bz=d5a_bz)

# --- --- define dipole d5 
if d5p1_typ == "lin":
    print("Warning: No D5 1st Dipole Linear Applied Fields Defined")
    d5p1 = addnewbend(zs=d5_tmp_s,ze=d5_tmp_e,rc=d5_tmp_rc)
  
elif d5p1_typ == "nl":
    top.diposet = false
    d5p1 = addnewbend(zs=d5_tmp_s,ze=d5_tmp_e,rc=d5_tmp_rc)
    d5p2 = addnewbgrd(dx=d5a_dx, dy=d5a_dy, xs=d5a_xs, ys=-0.5*d5a_yw,
                      zs=d5a_s, ze=d5a_e, id=d5a_3d_id, sc=d5p1_str, 
                      he=0, lb=1, oy = d5a_oy, op = d5a_ph,ph = d5a_ph)
else:
    print("Warning: No D5 1st Dipole Applied Fields Defined") 
    d5p1 = None


# --- Neutralization specifications 
neut_f = 100.0/100.0                 # corresponding electron neutralization factors 

if neut_f == 1.0 :
    top.depos = 'none'
    wmlti = 1.0
    fsflag = 1
else :
    wmlti = 1.0 - neut_f
    fsflag = 0


# --- Aperture specfications 
#     load scraper after generation of pic code  

xpwall=XPlane(x0=0,xsign=1,voltage=0.,xcent= d5_x_ap,condid="next")
xmwall=XPlane(x0=0,xsign=-1,voltage=0.,xcent=-d5_x_ap,condid="next")
ypwall=YPlane(y0=0,ysign=1,voltage=0.,ycent= d5_y_ap,condid="next")
ymwall=YPlane(y0=0,ysign=-1,voltage=0.,ycent=-d5_y_ap,condid="next")
aperture = xpwall+xmwall+ypwall+ymwall

# --- Lattice periodicity  
top.zlatperi  = largepos # periodicity length [m]  
top.zlatstrt  = 0.       # z of lattice start; added to element z's [m] 
                         #   (can use to change lattice phase) 

# Define transverse simulation grid

# --- Symmetries.  Set for increased statistical efficiency.  These should
#     only be used in cases where lattice symmetries and initial beam
#     conditions and loads allow.  For no symmetry, set both options to false.
w3d.l2symtry = false     # 2-fold symmetry
w3d.l4symtry = false     # 4-fold symmetry


if dist_load_type == 0:
    # Target beam (U33) information
    zref = 68.660938
    vzref = 1510458.1230053091
    sp_z_ave = [zref]
    sp_vz_ave = [vzref]
 
elif dist_load_type == 1:
    # Load particle distribution data

    sp_z_ave = []
    sp_vz_ave = []
    top.npmax = 0
    
    fi = PRpickle.PR(slice_dist0)

    allspx  = fi.allspx
    allspy  = fi.allspy
    allspz  = fi.allspz
    allspvx = fi.allspvx
    allspvy = fi.allspvy
    allspvz = fi.allspvz
    allspw  = fi.allspw
    allspsw = fi.allspsw

    for pcnt,ii in enumerate(sort(sp.keys())):
        sp_z_ave.append(average(allspz[pcnt]))
        sp_vz_ave.append(average(allspvz[pcnt]))
    fi.close()


    fi = PRpickle.PR(slice_dist1)

    allspx2  = fi.allspx
    allspy2  = fi.allspy
    allspz2  = fi.allspz
    allspvx2 = fi.allspvx
    allspvy2 = fi.allspvy
    allspvz2 = fi.allspvz
    allspw2  = fi.allspw
    allspsw2 = fi.allspsw
    fi.close()

    ddspx = (array(allspvx2) + array(allspvx))/2.0
    ddspy = (array(allspvy2) + array(allspvy))/2.0
    ddspz = (array(allspvz2) + array(allspvz))/2.0
    ddspvx = array(allspvx2) - array(allspvx)
    ddspvy = array(allspvy2) - array(allspvy)
    ddspvz = array(allspvz2) - array(allspvz)
    
    vzref = allspvz[12]


if fsflag:
    w3d.nx = 4
    w3d.ny = 4
    w3d.nz = 9
else :
    w3d.nx = 40
    w3d.ny = 40
    w3d.nz = 9


l_grid_x = d5_x_ap*2.0 + 0.02*cm # to be an even nx
l_grid_y = d5_y_ap*2.0 #+ 0.08*cm
l_diag_x = l_grid_x/2.0
l_diag_y = l_grid_y/2.0


w3d.xmmax =  l_grid_x/2.0
w3d.xmmin = -l_grid_x/2.0
w3d.ymmax =  l_grid_y/2.0
w3d.ymmin = -l_grid_y/2.0

dx = l_grid_x/float(w3d.nx) # dx = 0.0004 [m]
dy = l_grid_y/float(w3d.ny) # dy = 0.0004 [m]

z_launch = average(sp_z_ave)

top.vbeam = average(vzref)#sp['U33'].vbeam
d5sim_end = d5_tmp_e + d5_tmp_s - z_launch
all_len = d5_tmp_e + d5_tmp_s - z_launch*2.0
vtarget = top.vbeam
all_time = all_len/vtarget
#top.dt = all_time/2000.0
top.dt = 1.0e-9

zgridlen = d5sim_end - z_launch
w3d.zmmax = d5sim_end + zgridlen
w3d.zmmin = z_launch - zgridlen * 7.0

l_diag_zs = w3d.zmmin
l_diag_ze = w3d.zmmax
l_grid_z = w3d.zmmax - w3d.zmmin

top.fstype = 7
if fsflag:
    top.fstype = -1
    #top.depos = "none"

w3d.boundxy = 0
top.pbound0  = absorb   # bnd condition for particles at z=0
top.pboundnz = absorb
top.pboundxy = absorb
top.ibpush   = 2           # magnetic field particle push, 
                           #   0 - off, 1 - fast, 2 - accurate 

if dist_load_type == 1:
    zmonitor = d5sim_end - 0.05

    zpwall=ZPlane(z0=0,zsign=1,voltage=0.0,zcent=zmonitor,condid="next")
    scraper = ParticleScraper(zpwall)

    top.lsavelostpart = true
    sp['U32'].npmaxlost = 30000
    sp['U33'].npmaxlost = 30000
    sp['U34'].npmaxlost = 30000


if not(fsflag):
    # Add child grid
    solver = MRBlock3D()
    registersolver(solver)

    child1 = solver.addchild(
                    mins=[0.25*w3d.xmmin,w3d.ymmin,z_launch-5.0*cm],
                    maxs=[0.25*w3d.xmmax,w3d.ymmax,d5sim_end],
                    refinement=[4,1,150])

  
# Set user injection function

if dist_load_type == 0:
    add_per_step = 1
    def uinjectall():
        ii = 'U33'
        pnum = 1
        cc = random.randint(0,pnum,add_per_step)
        cp = random.rand(add_per_step)
        gi = ones(add_per_step)
        sp[ii].addparticles(
                z = average(zref),
                vz = average(vzref),
                gi = 1.0, w = 1.0, lallindomain=1 )              
        sp[ii].pid[-add_per_step:,sw0pid] = sp[ii].w[-add_per_step:]
        sp[ii].pid[-add_per_step:,uzp0pid] = sp[ii].uzp[-add_per_step:]
    installparticleloader(uinjectall)
    
elif dist_load_type == 1:
    # Set weight of species
    add_per_step = 10
    for pcnt,ii in enumerate(sort(sp.keys())):
        pnum = len(allspx[pcnt])
        vpart = average(allspvz[pcnt])
        zpart = average(allspz[pcnt])
        sp[ii].sw = allspsw[pcnt]*float(pnum)/float(add_per_step)\
                    *vpart*top.dt # / 1 meter
        sp[ii].vbeam = average(allspvz[pcnt])
        top.npmax += add_per_step

    def uinjectall():
        for pcnt,ii in enumerate(sort(sp.keys())):
            pnum = len(allspx[pcnt])
            cc = random.randint(0,pnum,add_per_step)
            cp = random.rand(add_per_step)
            gi = ones(add_per_step)
            sp[ii].addparticles(
                    x = allspx[pcnt][cc] + cp*ddspx[pcnt][cc]*top.dt,
                    y = allspy[pcnt][cc] + cp*ddspy[pcnt][cc]*top.dt,
                    z = allspz[pcnt][cc] + cp*ddspz[pcnt][cc]*top.dt,
                    vx = allspvx[pcnt][cc] + cp*ddspvx[pcnt][cc],
                    vy = allspvy[pcnt][cc] + cp*ddspvy[pcnt][cc],
                    vz = allspvz[pcnt][cc] + cp*ddspvz[pcnt][cc],
                    gi = gi, w = gi*wmlti, lallindomain=1 )              
            sp[ii].pid[-add_per_step:,sw0pid] = sp[ii].w[-add_per_step:]
            sp[ii].pid[-add_per_step:,uzp0pid] = sp[ii].uzp[-add_per_step:]
    installuserinjection(uinjectall)
                            



# Setup field solver using 2d multigrid field solver. 


################################
# Particle simulation
################################

# Generate the xy PIC code.  In the generate, particles are allocated and
# loaded consistent with initial conditions and load parameters
# set previously.  Particles are advanced with the step() command latepr
# after various diagnostics are setup.

package("w3d")

generate()

# Install conducting aperture on mesh 
installconductors(aperture,dfill=largepos)

# Set ideal bending dipole strength from the target specie spec
if d5p1_typ == "lin": top.dipoby = sp['U33'].mass / sp['U33'].sq * sp['U33'].vbeam / d5_tmp_rc

# Check that inputs are consistent with symmetries (errorcheck package function)
checksymmetry()



# Advance simulation specified steps 

if dist_load_type == 0:

    zstep = top.vbeam*top.dt
    n_step = nint((d5sim_end-z_launch)/zstep) -5
    top.nhist = 1
    step(n_step)
    
    if sp['U33'].getn() == 1:
        savetxt("tmpxvx.lst",transpose((1000.0*sp['U33'].hxbar[0][-1],sp['U33'].hvxbar[0][-1])))

        
elif dist_load_type == 1:
    step(3000)
    execfile( sfld + "outparticle2.py")
    execfile( sfld + "out_ecfield.py")
    
    
    
    lzmnt = 1    # Flag for beam position monitors
    if lzmnt :
        zmps = arange(68.68,zmonitor,2.0*cm)
        zmnt = [0]*len(zmps)
        nnzm = 0
        for ii in zmps :
            zmnt[nnzm] = ZCrossingParticles(zz=ii,laccumulate=1,lsavefields=1)
            nnzm += 1

    step(200)
    execfile( sfld + 'out_mnt.py')

    execfile( sfld + "outparticle2.py")
    execfile( sfld + "outparticle2lost.py")
    execfile( sfld + "out_ecfield.py") 

    step(200)
    execfile( scriptfolder + 'out_mnt.py')


    # Print out timing statistics of run 
    printtimers() 

    # Make sure that last plot is flushed from buffer
    fma() 

