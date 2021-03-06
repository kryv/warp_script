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
random.seed(100)  
#from runcounters import *               # Counter for parametric runs 

#import sys
#vvv = float(sys.argv[2])
#www = float(sys.argv[4])
#vvv = 1.33905666e-06
#www = 5.00001000e-01
tmpload = loadtxt('tmp.dat')
vvv = tmpload[0]
www = tmpload[1]
qqq = tmpload[2]
ppp = tmpload[3]


#sim_area = 0 # straight section
#sim_area = 1 # bend section
sim_area = 2 # 3d bend section

pkldatafolder = '/home/k/wfrib/test/'
#pkldatafolder = '/home/Fukushima/wfrib/test_beam24/'
scriptfolder = '/home/k/local_database/lwfrib/'
#scriptfolder = '/home/Fukushima/wwfrib/'

# Set informational labels included on all output cgm plots.   
top.pline2   = "xy Slice Simulation: FRIB Front End" 
top.pline1   = " "   # Add more info, if desired.  

# Invoke setup routine for graphics and output files (THIS IS MANDATORY)
setup()

# Set runmaker - included in informational labels on output plots
top.runmaker = "SMLund"

#out_plt_lst_x = []
#out_plt_lst_y = []

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

# --- Set species properties for injection 
#        The beam kinetic energy (ekin) and axial velocity (vbeam) should not both
#        be set unless done so consistently.  If one is zero the code sets from
#        the other on generation:
#           vbeam = 0    => set vbeam from ekin
#           ekin  = 0    => set ekin  from vbeam
#

# --- --- unneutralized electric currents ... array elements corresponding to charge state arrays  
mA = 1.e-3
U_ibeam = array([0.210,0.205,0.035,0.051,0.068,0.088,0.115,0.150,0.175,0.192,0.178,0.142,0.110,0.072,0.043,0.031])*mA 
O_ibeam = array([0.300,0.300,0.300,0.200])*mA 

# --- --- kinetic energy 

SourceBias = 35.*keV  # source voltage: set for Q_ref*SourceBias/A =>  4.9264706 keV/u for U 
"""
U_ekin = array(U_charge_states)*SourceBias
O_ekin = array(O_charge_states)*SourceBias 

# --- --- ion temp
#  Guilliaume:  ions likely 2-3 eV and electrons few - 100s of keV.  Ions not equilibrated with electrons.   

# --- --- beam size via edge reference emittance and Twiss parameters:

alpha_x = 0.
beta_x  = 12.9*cm
gamma_x = (1. + alpha_x**2)/beta_x 

alpha_y = 0.
beta_y  = 12.9*cm
gamma_y = (1. + alpha_y**2)/beta_y

mr = 0.001
emitn_edge = 0.4*mm*mr 

v_z_ref   = sqrt(2.*jperev*Q_ref*SourceBias/m_ref)
gamma_ref = 1./sqrt(1.-(v_z_ref/clight)**2)  
emit_edge = emitn_edge/(gamma_ref*v_z_ref/clight) 

top.lrelativ   = 1                # turn on relativity 

r_x  = sqrt(emit_edge*beta_x)
r_y  = sqrt(emit_edge*beta_y) 
rp_x = -sqrt(emit_edge/beta_x)*alpha_x 
rp_y = -sqrt(emit_edge/beta_y)*alpha_y 

# --- thermal velocity and energy (eV) of ref particle from emittance 
vt = v_z_ref*emit_edge/(2.*r_x) 
Et = 0.5*m_ref*vt**2/jperev 

# --- intrinsic thermal emittance scale 
Et_therm = 3.   # Guilliaume's estimated ion temp scale (eV) 
vt_therm = sqrt(2.*(jperev*Et_therm)/m_ref)
emit_therm  = 2.*r_x*vt_therm/v_z_ref
emitn_therm = (gamma_ref*v_z_ref/clight)*emit_therm


# Ratio of thermal to edge emittance suggests value of P_theta contributing to effective emittance 
# emit_therm/emit_edge = 0.10  => most beam PS area from P_theta  

for i in range(U_ns):
  Usp = U_species[i]
  Usp.ekin   = U_ekin[i]           # kinetic energy of beam particle [eV]
  Usp.vbeam  = 0.                  # beam axial velocity [m/sec] (set from ekin if 0) 
  Usp.ibeam  = U_ibeam[i]          # beam current [amps] 
  Usp.emitnx = emitn_therm         # beam x-emittance, rms edge [m-rad] 
  Usp.emitny = emitn_therm         # beam y-emittance, rms edge [m-rad]
  #Usp.emitnx = emitn_edge          
  #Usp.emitny = emitn_edge          
  Usp.vthz   = 0.                  # axial velocity spread [m/sec] 

for i in range(O_ns):
  Osp = O_species[i]
  Osp.ekin   = O_ekin[i] 
  Osp.vbeam  = 0.
  Osp.ibeam  = O_ibeam[i]
  Osp.emitnx = emitn_therm
  Osp.emitny = emitn_therm
  #Osp.emitnx = emitn_edge 
  #Osp.emitny = emitn_edge 
  Osp.vthz   = 0.

# Calculate vbeam and other species quantities 
#derivqty()


U_r_x = zeros(U_ns)
U_r_y = zeros(U_ns)
U_rp_x = zeros(U_ns)
U_rp_y = zeros(U_ns)
O_r_x = zeros(O_ns)
O_r_y = zeros(O_ns)
O_rp_x = zeros(O_ns)
O_rp_y = zeros(O_ns)
for ii in range(U_ns):
 s = U_species[ii]
 tmp_beta_x = beta_x * ((sp['U33'].charge/s.charge)*(s.ekin/sp['U33'].ekin)*(sp['U33'].vbeam/s.vbeam))
 tmp_beta_y = tmp_beta_x
 s.beta_x = tmp_beta_x
 tmp_emit_edge = r_x*r_x / tmp_beta_x
 s.edge_emit = tmp_emit_edge
 #tmp_emit_edge = emit_edge
 U_r_x[ii] = sqrt(tmp_emit_edge*tmp_beta_x)
 U_r_y[ii] = sqrt(tmp_emit_edge*tmp_beta_y)
 U_rp_x[ii] = -sqrt(tmp_emit_edge/tmp_beta_x)
 U_rp_y[ii] = -sqrt(tmp_emit_edge/tmp_beta_y)
 print("    Species: " +str(s.js)+" emit_edge = %s"%tmp_emit_edge)

for ii in range(O_ns):
 s = O_species[ii]
 tmp_beta_x = beta_x * ((sp['U33'].charge/s.charge)*(s.ekin/sp['U33'].ekin)*(sp['U33'].vbeam/s.vbeam))
 tmp_beta_y = tmp_beta_x
 s.beta_x = tmp_beta_x
 tmp_emit_edge = r_x*r_x / tmp_beta_x
 s.edge_emit = tmp_emit_edge
 #tmp_emit_edge = emit_edge
 O_r_x[ii] = sqrt(tmp_emit_edge*tmp_beta_x)
 O_r_y[ii] = sqrt(tmp_emit_edge*tmp_beta_y)
 O_rp_x[ii] = -sqrt(tmp_emit_edge/tmp_beta_x)
 O_rp_y[ii] = -sqrt(tmp_emit_edge/tmp_beta_y)
 

# ---  Calculate and printout Q/M by species and store in a dictionary 
sp_qovm = {}
print("Species Charge to Mass Ratios:")
for ii in sort(sp.keys()):
  s = sp[ii]
  qovm = (s.charge/echarge)/(s.mass/amu)
  sp_qovm.update({ii:qovm})
  print("   Species: "+ii+" Q/A = %s"%qovm)

# ---  Calculate and printout rigidity by species and store in a dictionary 
sp_brho = {}
print("Species Rigidity:")
for ii in sort(sp.keys()):
  s = sp[ii]
  gamma = 1./sqrt(1.-(s.vbeam/clight)**2)
  brho  = gamma*s.mass*s.vbeam/s.charge
  sp_brho.update({ii:brho})
  print("   Species: "+ii+" [B rho] = %s T-m"%brho)


#print("---- Betafunctions ----")
#for ii in sort(sp.keys()):
#  s = sp[ii]
# #tmp_beta = s.beta_x
#  print("   Species: "+ii+" beta_x = %s"%s.beta_x)



# --- Diagnostic plot of [B rho] vs Q/A for species 
def plt_diag_bro(label=None):
  if label == None: label = " "
  brho_min = largepos 
  brho_max = 0.  
  for ii in sp.keys():
    s = sp[ii]
    js = s.js 
    #
    weight = sum(s.sw*s.w) 
    #
    vbeam = sum( (s.sw*s.w)*s.getvz() )/weight
    gammabeam = 1./sqrt(1.-(vbeam/clight)**2)      
    brho  = s.mass*gammabeam*vbeam/s.charge
    #
    brho_min = min(brho,brho_min) 
    brho_max = max(brho,brho_max) 
    #
    plt(ii,sp_qovm[ii],brho,tosys=1,color=s.color) 
    #
  [qovm_min,qovm_max] = [minnd(sp_qovm.values()),maxnd(sp_qovm.values())]
  qovm_pad = 0.1*(qovm_max - qovm_min)
  brho_pad = 0.1*(brho_max - brho_min)
  #
  limits(qovm_min-qovm_pad,qovm_max+qovm_pad,brho_min-brho_pad,brho_max+brho_pad) 
  ptitles(label,"Q/A","[B rho] [Tesla-m]",)
  fma()


#
# Beam centroid and rms envelope initial conditions at s=0      
#    
#   x0:   initial x-centroid xc = <x> [m]
#   y0:   initial y-centroid yc = <y> [m]
#   xp0:  initial x-centroid angle xc' = <x'> = d<x>/ds [rad]
#   yp0:  initial y-centroid angle yc' = <y'> = d<y>/ds [rad]
#
#   a0:   initial x-envelope edge a = 2*sqrt(<(x-xc)^2>) [m]
#   b0:   initial y-envelope edge b = 2*sqrt(<(y-yc)^2>) [m]
#   ap0:  initial x-envelope angle ap = a' = d a/ds [rad]
#   bp0:  initial y-envelope angle bp = b' = d b/ds [rad]

for i in range(U_ns):
  Usp = U_species[i]
  # --- centroid 
  Usp.x0  = 0.
  Usp.y0  = 0.
  Usp.xp0 = 0.
  Usp.yp0 = 0.
  # --- envelope 
  Usp.a0   = U_r_x[i]
  Usp.b0   = U_r_y[i]
  Usp.ap0  = U_rp_x[i]
  Usp.bp0  = U_rp_y[i]

for i in range(O_ns):
  Osp = O_species[i]
  # --- centroid 
  Osp.x0  = 0.   
  Osp.y0  = 0.   
  Osp.xp0 = 0.   
  Osp.yp0 = 0.   
  # --- envelope 
  Osp.a0   = O_r_x[i]              
  Osp.b0   = O_r_y[i]          
  Osp.ap0  = O_rp_x[i]
  Osp.bp0  = O_rp_y[i]  
"""
  
#
# Setup Lattice  
#

ekin_per_u = 12.*keV                             # target kinetic energy/u for LEBT 
StandBias = A_ref*ekin_per_u/Q_ref - SourceBias  # Bias of Injector Column  

Bias = StandBias + SourceBias

#dspall = 69.2
dspall = 0.0

# --- Venus ECR Source 
#     Comment: Must have same z-grids for linear and nonlinear forms.  Minimal error checking to enforce this. 

# --- --- element specification 

ecr_shift  = 11.*cm                 # shift of ecr from lattice file spec to make room for s4p1 
ecr_z_extr = 66.650938 - ecr_shift -dspall # z-location of beam extraction aperture in simulation coordinates     
ecr_sc     = 1.0                    # scale factor to muliply field data by 
ecr_typ    = "lin"                  # type: "lin" = linear optics fields or "nl" = nonlinear r-z field  

# --- --- linear element data  
fi = PRpickle.PR( pkldatafolder + "lat_ecr_venus.lin.20150813.pkl")
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

s4p1_zc  = 66.956900  -dspall # S4 1: z-center  
s4p1_str = 0.6 # 0.754 # S4 1: peak on-axis B_z field strength [Tesla]
s4p1_typ = "lin"        # S4 1: type: "lin" = linear optics fields or "nl" = nonlinear r-z field  

s4p2_zc  = 68.306900   # S4 2: z-center 
s4p2_str = 0.5 # 0.617 # s4 2: peak on-axis B_z field strength [Tesla]
s4p2_typ = "lin"        # S4 1: type: "lin" = linear optics fields or "nl" = nonlinear r-z field  

# --- --- linear element data  
#fi = PRpickle.PR("lat_s4.lin.20140603.pkl")
fi = PRpickle.PR( pkldatafolder + "lat_s4.lin.20141031.pkl")
s4_dz  = fi.s4_dz 
s4_nz  = fi.s4_nz  
s4_z_m = fi.s4_z_m 
s4_bz0_m   = fi.s4_bz0_m
s4_bz0p_m  = fi.s4_bz0p_m
fi.close() 

s4_zlen = s4_z_m.max() - s4_z_m.min() 
s4_lin_id = addnewmmltdataset(zlen=s4_zlen,ms=s4_bz0_m,msp=s4_bz0p_m,nn=0,vv=0)

# --- --- nonlinear element field data 
#fi = PRpickle.PR('lat_s4.rz.20140603.pkl') 
fi = PRpickle.PR( pkldatafolder + 'lat_s4.rz.20141031.pkl') 
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
#fi = PRpickle.PR('lat_s4.at.20140603.pkl') 
fi = PRpickle.PR( pkldatafolder + 'lat_s4.at.20141031.pkl') 
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

# Define vector potential function for both linear and nonlinear solenoid magnetic fields  
def getatheta(r):
  # --- gather vector potential 
  n = len(r) 
  at = zeros(n)
  at_scratch = zeros(n) 
  z  = top.zbeam*ones(n)
  if   top.zbeam >= ecr_zmmin and top.zbeam <= ecr_zmmax:
    # --- contribution in venus 
    if ecr_typ == "lin":
      getgrid1d(n,z,at_scratch,ecr_nz,ecr_sc*ecr_bz0_m,ecr_zmmin,ecr_zmmax)
      at_scratch = at_scratch*r/2.
    elif ecr_typ == "nl":
       raise Exception("Vector Potential: ECR Nonlinear not defined")  
    else:
       raise Exception("Vector Potential: ECR not defined") 
    at += at_scratch
  if top.zbeam >= s4p1_zc-s4_zlen/2. and top.zbeam <= s4p1_zc+s4_zlen/2.:
    # --- contribution from 1st s4 
    if s4p1_typ == "lin": 
      getgrid1d(n,z,at_scratch,s4_nz,s4p1_str*s4_bz0_m,s4p1_zc-s4_zlen/2.,s4p1_zc+s4_zlen/2.)
      at_scratch = at_scratch*r/2.
    elif s4p1_typ == "nl":
      getgrid2d(n,r,z,at_scratch,s4_nr,s4_nz,s4p1_str*s4_at_m,s4_r_m.min(),s4_r_m.max(), 
                s4p1_zc-s4_zlen/2.,s4p1_zc+s4_zlen/2.)
    else:
      raise Exception("Vector Potential: S4.1 not defined")
    at += at_scratch
  if top.zbeam >= s4p2_zc-s4_zlen/2. and top.zbeam <= s4p2_zc+s4_zlen/2.:
    # --- contribution from 2nd s4
    if s4p2_typ == "lin": 
      getgrid1d(n,z,at_scratch,s4_nz,s4p2_str*s4_bz0_m,s4p2_zc-s4_zlen/2.,s4p2_zc+s4_zlen/2.)
      at_scratch = at_scratch*r/2.
    elif s4p2_typ == "nl": 
      getgrid2d(n,r,z,at_scratch,s4_nr,s4_nz,s4p2_str*s4_at_m,s4_r_m.min(),s4_r_m.max(), 
                s4p2_zc-s4_zlen/2.,s4p2_zc+s4_zlen/2.)
    else:
      raise Exception("Vector Potential: S4.2 not defined")
    at += at_scratch
  return at 


# --- Grated Acceleration Gap
#   Note: for ideal zero-length gap:  top.lacclzl=true for zero length gap.  Accel given given by acclez*(accelze-acclzs) 
#   see dave grote email on caution on setting top.acclsw for gaps.   
#   Comment: Linear and nonlinear forms must have same axial grid.  Miminal error checking only for this.  

# --- --- element specification 
gag_zc  = 67.811564 -dspall # Grated Accel Gap: z-center  
gag_typ = "nl"       # Grated Accel Gap: type: "ideal" = Short gap kick, "lin" = linear r-z field imported, "nl" = nonlinear r-z field imported   

# --- --- linear element data  
# fi = PRpickle.PR("lat_gag.lin.20140624.pkl")  # Original Warp model with simplified geometry  
fi = PRpickle.PR( pkldatafolder + "lat_gag.lin.20141029.pkl")    # Poisson model with high detail 
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
fi = PRpickle.PR( pkldatafolder + 'lat_gag.rz.20141029.pkl')   # Poisson model with high detail 
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

d5p1_str = 0.6015157305571277 + www #*(1.0+((float(www)-500.0)/100.0/1000.0)) # D5 1: Input field scale factor
#d5p1_str = 0.17780642034475383
#d5p1_str = 0.17780754936945101
d5p1_typ = "nl"        # D5 1: type: "lin" = linear optics fields or "3d" = 3d field  

# --- --- nonlinear element data 
#Bend magnet section info
d5_cond_in = 43.0*cm
d5_cond_out = 84.0*cm
d5_x_ap = (d5_cond_out - d5_cond_in)/2.0
d5_y_ap = 5.0*cm
d5_tmp_rc = (d5_cond_out + d5_cond_in)/2.0
d5_tmp_s = 69.2                                    -dspall
d5_tmp_e = d5_tmp_s + (d5_tmp_rc*2.0*pi)*0.25

#bgrd data info
d5sim_frng_l = 50.0*cm
d5sim_zlen = d5sim_frng_l*2.0 + d5_tmp_e - d5_tmp_s 
d5sim_str = d5_tmp_s - d5sim_frng_l
d5sim_end = d5sim_str+d5sim_zlen

d5a_nx = 150
d5a_ny = 20
d5a_nz = 300

d5a_xw = (75.0)*cm
d5a_yw = 10.0*cm
d5a_zlen = (150.0)*cm 
#d5a_zlen = (d5_tmp_rc*2.0*pi)*0.25

d5a_cen = (d5_tmp_s + d5_tmp_e)/2.0
d5a_s = d5a_cen - d5a_zlen/2.0
d5a_e = d5a_cen + d5a_zlen/2.0
d5a_xs = -d5_tmp_rc +15.0*cm  + vvv #+ ((float(vvv)-500.0)/10.0)*mm

d5a_dx = d5a_xw/float(d5a_nx)
d5a_dy = d5a_yw/float(d5a_ny)
d5a_dz = d5a_zlen/float(d5a_nz)

d5a_oy = qqq
d5a_ph = ppp


if d5p1_typ == "nl" :
 print "--- loading bend bgrid"
 
 if False :
  data = getdatafromtextfile(scriptfolder+"bend_tri.table",dims=[3,None],)
  if len(data[0]) != (d5a_nx+1)*(d5a_ny+1)*(d5a_nz+1): raise Exception("bend grid data is invalid.")
  d5a_bx = data[0].copy()
  d5a_by = data[1].copy()
  d5a_bz = data[2].copy()

  d5a_bx.resize((d5a_nx+1,d5a_ny+1,d5a_nz+1))
  d5a_by.resize((d5a_nx+1,d5a_ny+1,d5a_nz+1))
  d5a_bz.resize((d5a_nx+1,d5a_ny+1,d5a_nz+1)) 
  
 if True :
  fi = PRpickle.PR( pkldatafolder + 'lat_d5.3d.20140527.pkl') 
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
  #d5p2 = addnewbgrd(dx=d5_3d_dx, dy=d5_3d_dy, xs=d5_3d_x_m.min(), ys=d5_3d_y_m.min(),
  #  zs=d5p1_zc-d5_3d_zlen/2., ze=d5p1_zc+d5_3d_zlen/2., id=d5_3d_id, sc=d5p1_str)
  d5p2 = addnewbgrd(dx=d5a_dx, dy=d5a_dy, xs=d5a_xs, ys=-0.5*d5a_yw,
    zs=d5a_s, ze=d5a_e, id=d5a_3d_id, sc=d5p1_str, he=0, lb=1, oy = d5a_oy, op = d5a_ph,ph = d5a_ph)
  #should be ot = -pi*0.25
else:
  print("Warning: No D5 1st Dipole Applied Fields Defined") 
  d5p1 = None


# --- Neutralization specifications 
#     Break points z1 and z2 correspond to z values where neutralization is turned off and then back on so the beam is 
#     unneutralized in the grated acceleration gap.  

neut_z1 = gag_zc - 20.90*cm    # z of neutralization stop post injector before grated gap: set via 1% of gap E_z field reached  
neut_z2 = gag_zc + 22.28*cm  


neut_f1 = 0.75                 # corresponding electron neutralization factors 
neut_f2 = 0.75  
"""
# --- Aperture specfications 
#     load scraper after generation of pic code  
if sim_area == 0:
 r_p_up   = 8.00*cm 
 r_p_down = 7.62*cm  

 r_ap   = [r_p_up,gag_rp,r_p_down]
 v_ap   = [SourceBias+StandBias,StandBias/2.,0.] 
 z_ap_l = [ecr_z_extr,  gag_col_zs, gag_col_ze]
 z_ap_u = [gag_col_zs,  gag_col_ze, 69.2   ]

 r_p = max(r_ap)   # Max aperture in simulations 
 
 aperture = [] 
 for i in range(len(r_ap)):
   rp = r_ap[i] 
   v  = v_ap[i] 
   zl = z_ap_l[i] 
   zu = z_ap_u[i]
   
   aperture.append( ZCylinderOut(radius=rp,zlower=zl,zupper=zu,condid="next") )
   top.prwall = r_p

if sim_area == 1 or sim_area == 2 :
 r_p = 8.0*cm
 
 xpwall=XPlane(x0=0,xsign=1,voltage=0.,xcent= d5_x_ap,condid="next")
 xmwall=XPlane(x0=0,xsign=-1,voltage=0.,xcent=-d5_x_ap,condid="next")
 ypwall=YPlane(y0=0,ysign=1,voltage=0.,ycent= d5_y_ap,condid="next")
 ymwall=YPlane(y0=0,ysign=-1,voltage=0.,ycent=-d5_y_ap,condid="next")
 aperture = xpwall+xmwall+ypwall+ymwall
"""

  
# --- Add a circular aperture particle scraper at pipe radius aperture. 
#       Could also use ParticleScraper(conductors=aperture) but 
#       setting prwall is faster for a simple cylinder. 
#top.prwall = r_p    # reset this later consistent with actual aperture in range simulated in advances 

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

# -- Grid increments
#      First choose number grid cells without symmetry and reset 
#      consistent with symmetry options

if sim_area == 0:
 n_grid = 400 # 200 previous # number grid cells (no symmetries)  
 
 sym_x = 1.
 sym_y = 1.
 if w3d.l4symtry:
   sym_x = 0.5
   sym_y = 0.5
 elif w3d.l2symtry:
   sym_x = 0.5
 
 w3d.nx = int(sym_x*n_grid) 
 w3d.ny = int(sym_y*n_grid)

 # ---- Grid bounds 
 #      Some bounds will be reset to zero by code on generation
 #      if symmetry options are set.
 l_grid = 2.*r_p               # length edge of simulation grid [m]      
 w3d.xmmax =  l_grid/2.        # x-grid max limit [m] 
 w3d.xmmin = -l_grid/2.        # x-grid min limit [m] 
 w3d.ymmax =  l_grid/2.        # y-grid max limit [m] 
 w3d.ymmin = -l_grid/2.        # y-grid min limit [m] 
 
 # --- grid increments to use before code generation in setup
 dx = l_grid/float(n_grid)


 # Particle loading
 #
 # Set simulation macro-particle number (top.npmax) by specifying the
 #  number of macro-particles to load per xy grid cell (nppg) using an
 # rms equivalent uniform density beam measure.  This number is (re)set
 # consistently with the symmetry options.  
 #   sp['name'].np = particle #
 #   top.nplive = total number live particles = len(sp)*top.npmax at time of load 
 # 
 
 #nppg = 100.    # number of particles per grid cell
 nppg = 100.
 top.npmax = int(nppg*pi*(r_x*r_y)/dx**2*sym_x*sym_y) # max initial particles loaded (each species) 
 
 z_launch  = ecr_z_extr + 10.*cm 

# Distribution loads type 
#  Comment: 
#     See stptcl routine for how loading works.   
#     At present, all species are loaded with the same value of distrbtn.   zbeam can be 
#     set before the generate for the beam location. 

if sim_area == 1 or sim_area == 2 :

 if False:
  fi = PRpickle.PR(scriptfolder +'/match_depos/ideal_bend/allpart1275.pkl')
  #fi = PRpickle.PR('allpart1275.pkl')
  pcnt = 0
  sp_z_ave = []
  sp_vz_ave = []
  top.npmax = 0

  allspx  = fi.allspx
  allspy  = fi.allspy
  allspz  = fi.allspz
  allspvx = fi.allspvx
  allspvy = fi.allspvy
  allspvz = fi.allspvz
  allspw  = fi.allspw
  allspsw = fi.allspsw

  for ii in sort(sp.keys()):
   sp_z_ave.append(average(allspz[pcnt]))
   sp_vz_ave.append(average(allspvz[pcnt]))
   pcnt += 1
  fi.close()

 sym_x = 1.
 sym_y = 1.
 if sim_area == 1:
  w3d.nx = 1026  
  w3d.ny = 250
 if sim_area == 2:
  w3d.nx = 4
  w3d.ny = 4
  w3d.nz = 8

 #l_diag = 2.0 * 8.0*cm #use for distribution plot
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

 z_launch = d5sim_str
 
 if sim_area == 2 :
  w3d.zmmax = d5sim_end + 2.0*cm
  w3d.zmmin = z_launch - 3.5
  l_diag_zs = w3d.zmmin
  l_diag_ze = w3d.zmmax
  l_grid_z = w3d.zmmax - w3d.zmmin
  #dz = l_grid_z/float(w3d.nz)
  
#w3d.xmmin = -1.
#w3d.xmmax =  1.
#w3d.ymmin = -2.
#w3d.ymmax =  2.
#w3d.zmmin = -1.5
#w3d.zmmax = +5.
  
  
# rms equivalent beam loaded with the specified distribution form 
#     KV => KV Distribution 
#
#     SG => semi-Gaussian distribution 
#             (KV density and local Gaussian angle spread about KV flutter) 
#
#     TE => Pseudoequilibrium with Thermal  Equilibrium form 
#     WB => Pseudoequilibrium with Waterbag Equilibrium form
#             The Pseudoequilibrium distributions use continuous focused 
#             equilibrium forms which are canoically transformed to AG 
#             symmetry of the lattice. 
#
#     For more info on loads, see review paper:
#       Lund, Kikuchi, and Davidson, PRSTAB 12, 114801 (2009) 

if sim_area == 0:
 #w3d.distrbtn = "KV"          # initial KV distribution
 #w3d.distrbtn = "TE"          # initial thermal distribution
 w3d.distrbtn = "WB"          # initial waterbag distribution
 #w3d.distrbtn = "SG"          # initial semi-Gaussian distribution 
 
elif sim_area == 1 :
 w3d.distrbtn = "none"
 def injectall():
  pcnt = 0
  for ii in sort(sp.keys()):
   gi = ones(len(allspx[pcnt]))
   sp[ii].addparticles(x=allspx[pcnt],   y=allspy[pcnt],   z=allspz[pcnt],\
                  vx=allspvx[pcnt], vy=allspvy[pcnt], vz=allspvz[pcnt],\
                      gi = gi, w = allspw[pcnt], lallindomain=1)
   sp[ii].sw = allspsw[pcnt]
   sp[ii].vbeam = average(allspvz[pcnt])
   top.npmax += sp[ii].getn()
   pcnt += 1
 #installparticleloader(injectall)

"""
elif sim_area == 2 :
 w3d.distrbtn = "none"
 def uinjectall():
  add_per_step = 100
  pcnt = 0
  for ii in sort(sp.keys()):
   pnum = len(allspx[pcnt])
   vpart = average(allspvz[pcnt])
   zpart = average(allspz[pcnt])
   dspz = (random.rand(add_per_step))*vpart*top.dt
   cc = random.randint(0,pnum,add_per_step)
   gi = ones(add_per_step)
   sp[ii].addparticles(x=allspx[pcnt][cc],   y=allspy[pcnt][cc],   z=allspz[pcnt][cc]+dspz,\
                       vx=allspvx[pcnt][cc], vy=allspvy[pcnt][cc], vz=allspvz[pcnt][cc],\
                       gi = gi, w = allspw[pcnt][cc], lallindomain=1)
   sp[ii].sw = allspsw[pcnt]#*float(pnum)/float(add_per_step)#/(vpart*top.dt)
   #if top.it ==1 : sp[ii].vbeam = vpart    
   top.npmax += add_per_step
   pcnt += 1
installparticleloader(uinjectall)
 #installbeforestep(injectall)
installuserinjection(uinjectall)
"""

def testadd():
 sp['U33'].addparticles(z=z_launch,vz=1510321.7243528133, gi=1)

#installuserinjection(testadd)
installparticleloader(testadd)
sp['U33'].vbeam = 1510321.7243528133
top.vbeam = 1510321.7243528133

if False:
 def reset():
  top.zbeam = 0.0
 installbeforestep(reset)

# --- random number options to use in loading 
w3d.xrandom  = "pseudo" # "digitrev"    # load x,y,z  with digitreverse random numbers #
w3d.vtrandom = "pseudo" # "digitrev"    # load vx, vy with digitreverse random numbers
w3d.vzrandom = "pseudo" # "digitrev"    # load vz     with digitreverse random numbers 
w3d.cylinder = true          # load a cylinder


# Particle moving
#
"""
z_adv = 69.2   # Axial position in lattice to advance to 

top.lrelativ   =  false    # turn off relativistic kinematics
top.relativity = 0         # turn off relativistic self-field correction
                           #   to account for approx diamagnetic B-field of beam

if sim_area == 0 or sim_area == 1 :
 wxy.ds = 2.*mm             # ds for part adv [m] 
 wxy.lvzchang = true        # Use iterative stepping, which is needed if
                            # the vz of the particles changes.
                            #  ... must change even in linear lattice 
                            #          for high-order energy conservation 
"""

alltime = 1.9974556675147568/1510321.7243528133

if sim_area == 2 :
 #top.dt = 1.0e-9
 top.dt = alltime/2000.0
 #top.pbound0   = absorb   # bnd condition for particles at z=0
 #top.pboundnz  = absorb
 #top.pboundxy = absorb
                            
#top.ibpush   = 2           # magnetic field particle push, 
                           #   0 - off, 1 - fast, 2 - accurate 


# Setup field solver using 2d multigrid field solver. 

if sim_area == 0 or sim_area == 1:
 w3d.boundxy = 0              # Neuman boundary conditions on edge of grid.
 w3d.solvergeom = w3d.XYgeom  # fieldsolve type to 2d multigrid 

elif sim_area == 2:
 w3d.boundxy = 0
 top.fstype = -1


# --- Uncomment to turn off space-charge deposition for simulation of particles 
#     moving in applied field  
top.depos = "none"


# Turn on x-window plots, if desired; use winkill() to close interactively.  
#winon()

"""
# Potential profile diagnostic primarily for initial beam 
def diag_plt_phi_ax(xmax=None,label=None):
  if xmax == None: xmax = min(w3d.xmesh.max(),w3d.ymesh.max())
  ixmax = sum(where(w3d.xmesh < xmax, 1, 0))
  iymax = sum(where(w3d.ymesh < xmax, 1, 0)) 
  if label == None: label = "Beam Potential at y,x = 0 b,r"
  #
  ix_cen = sum(where(w3d.xmesh < 0., 1, 0))
  iy_cen = sum(where(w3d.ymesh < 0., 1, 0))
  if sim_area == 0 or sim_area ==1 :
   phix = getphi(iy=iy_cen)
   phiy = getphi(ix=ix_cen)
  elif sim_area == 2:
   phix = getphi(iy=iy_cen, iz = top.zbar[0,-1])
   phiy = getphi(ix=ix_cen, iz = top.zbar[0,-1])
   
   
  phimin = min(phix[ixmax],phiy[iymax]) 
  #
  plg(phix,w3d.xmesh/mm)
  plg(phiy,w3d.ymesh/mm,color="red") 
  ptitles(label,"x,y [mm]","phi [V]", )
  limits(-xmax/mm,xmax/mm,0.0,'e') 
"""
  
################################
# Particle simulation
################################

#top.vbeam = 0.0#1510321.7243528133
#top.zbeam = average(sp_z_ave)


# Generate the xy PIC code.  In the generate, particles are allocated and
# loaded consistent with initial conditions and load parameters
# set previously.  Particles are advanced with the step() command latepr
# after various diagnostics are setup.
if sim_area == 0 or sim_area == 1 :
 package("wxy")
 if sim_area == 1 : top.zbeam = z_launch
elif sim_area == 2:
 package("w3d")


generate()

# Read in diagnostics for applied lattice fields 
#execfile( pkldatafolder + "diag_lattice.py") 

# Install conducting aperture on mesh 
#installconductors(aperture,dfill=largepos)

if d5p1_typ == "lin": top.dipoby =d5p1_str #array([ 0.17780642])
#if d5p1_typ == "lin": top.dipoby = array([ 0.0])
#top.dipoby = array([ 0.18817846])
#raise Exception("to here")

# Check that inputs are consistent with symmetries (errorcheck package function)
#checksymmetry()

top.nhist = 1

zstep = top.vbeam*top.dt
n_step = nint((d5sim_end-z_launch)/zstep) -10  # add two extra steps in case of roundoff accumulation 
step(n_step)

zzh = sp['U33'].hzbar[0]
xxh = sp['U33'].hxbar[0]
vxh = sp['U33'].hvxbar[0]
yyh = sp['U33'].hybar[0]
vyh = sp['U33'].hvybar[0]

#savetxt("zx.lst3",transpose((zzh,xxh)))
#savetxt("zvx.lst3",transpose((zzh,vxh)))
savetxt("zxyvpp.lst",transpose((zzh,xxh,vxh,yyh,vyh)))
if sp['U33'].getn() == 1  :
 savetxt("zxyv.lst",transpose((1000.0*xxh[-2],vxh[-2],1000.0*yyh[-2],vyh[-2])))

meshplot = 0
if meshplot :
 nz = 1000
 nx = 50
 ny = 1

 zmesh=[]
 xmesh=[]
 ymesh=[]

 for zz in linspace(69.1,70.50,nz)-dspall:
  for xx in linspace(0.0,0.0,1):
   for yy in linspace(0,0,ny):
    zmesh.append(zz)
    xmesh.append(xx)
    ymesh.append(0.0)


 (ex_mesh,ey_mesh,ez_mesh,bx_mesh,by_mesh,bz_mesh) = getappliedfields(x=xmesh,y= ymesh,z=zmesh)

 savetxt("xzb1.dat",transpose((xmesh,zmesh,by_mesh*10000)))


# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------

raise Exception("to here")

if sim_area == 0:
 # Carry out an initial unneutralized field solve with conducting pipe after generate 
 for s in sp.values():       
  s.w   = 1.      # Need full charge: set relative weight to unity 

 loadrho() 
 fieldsolve() 

 # Make plot of initial unneutralized beam potential profile 
         
 diag_plt_phi_ax(label="Initial Unneutralized Beam Potential at y,x = 0 b,r") 
 fma()

 diag_plt_phi_ax(label="Initial Unneutralized Beam Potential at y,x = 0 b,r",xmax=1.5*r_x)
 fma()


# Setup variable weight species needs for neutralization and acceleration 

# --- set initial weight factors consistent with neutralization factor 
#       w0 = initial weight (same for all particles in species) 
#       species.w = array of variable weight factors 
if sim_area == 0 :
 for s in sp.values(): 
  s.w0  = 1.-neut_f1
  #s.w   = 1.-neut_f1
  s.sw0    = s.sw       # save initial sw    (in case later changed)  
  s.vbeam0 = s.vbeam    # save initial vbeam (in case later changed)
 top.pgroup.pid[:,uzp0pid] = top.pgroup.uzp  
elif sim_area == 1 :
 for s in sp.values(): 
  s.pid[:,sw0pid]  = s.w
  #s.w   = 1.-neut_f1
  s.sw0    = s.sw       # save initial sw    (in case later changed)  
  s.vbeam0 = s.vbeam    # save initial vbeam (in case later changed)
 #top.pgroup.pid[:,uzp0pid] = top.pgroup.uzp
elif sim_area == 2 :
 for s in sp.values(): 
  s.pid[:,sw0pid]  = s.w
  s.pid[:,uzp0pid] = s.uzp
  #s.w   = 1.-neut_f1
  s.sw0    = s.sw       # save initial sw    (in case later changed)  
  s.vbeam0 = s.vbeam    # save initial vbeam (in case later changed)
# --- save initial uzp for all species at once 
#top.pgroup.pid[:,uzp0pid] = top.pgroup.uzp


# --- adjust weights  
@callfrombeforeloadrho
def adjustweights():
  for s in sp.values():
    if s.getn() !=0:
     if sim_area == 0:
      s.w[:] = s.w0*s.pid[:,uzp0pid]/s.uzp
     elif sim_area == 1 or sim_area == 2:
      s.w[:] = s.pid[:,sw0pid]*s.pid[:,uzp0pid]/s.uzp


#raise Exception("to here")

# Carry out explicit fieldsolve with adjusted rho consistent with neutralization 
loadrho()
fieldsolve()

#raise Exception("to here")

# Make plot of initial neutralized beam potential profile 
if sim_area == 0 or sim_area == 1:         
 diag_plt_phi_ax(label="Initial f = %s Neutralized Beam Potential at y,x = 0 b,r"%(neut_f1))
 fma()

 diag_plt_phi_ax(label="Initial f = %s Neutralized Beam Potential at y,x = 0 b,r"%(neut_f1),xmax=1.5*r_x)
 fma()

#raise Exception("to here")

# Modify intital distribution loaded on generate to include canonical angular momentum
# 
bz0_extr   = getappliedfields(x=0.,y=0.,z=ecr_z_extr)[5]    # B_z on-axis at ECR extraction plane
bz0_launch = getappliedfields(x=0.,y=0.,z=z_launch)[5]      # B_z on-axis at simulation launch location 

inj_ang_mom = true

if sim_area == 0:
 sp_krot_launch = {}
 sp_krot_v      = {} 
 for ii in sp.keys():
   s = sp[ii]
   # --- rigidity tes
   gamma = 1./sqrt(1.-(s.vbeam/clight)**2)
   brho  = gamma*s.mass*s.vbeam/s.charge
   # --- rms calculation
   rms_launch = sqrt(average( (s.xp)**2 + (s.yp)**2 ))
   rms_extr   = sqrt( (s.a0/2.)**2 + (s.b0/2.)**2 )     # *** Replace with beam size at extraction ! ****
   # --- rot wavenumbers at launch and in vacuum v 
   krot_launch = (bz0_extr*rms_extr**2/rms_launch**2 - bz0_launch)/(2.*brho)
   krot_v      = bz0_extr/(2.*brho)
   # 
   sp_krot_launch.update({ii:krot_launch})
   sp_krot_v.update({ii:krot_v}) 
   #
   if inj_ang_mom: 
     s.uxp -= krot_launch*s.yp*s.uzp
     s.uyp += krot_launch*s.xp*s.uzp

 # --- make plots of initial rotation by species at launch point and if transported in vacuuo    

 def diag_plt_krot_launch(): 
   for ii in sp.keys():
     plt(ii,sp_qovm[ii],sp_krot_launch[ii],tosys=1,color=sp[ii].color) 

   [qovm_min,qovm_max] = [minnd(sp_qovm.values()),maxnd(sp_qovm.values())]
   [krot_launch_min,krot_launch_max] = [minnd(sp_krot_launch.values()),maxnd(sp_krot_launch.values())]
   qovm_pad = 0.1*(qovm_max - qovm_min)
   krot_launch_pad = 0.1*(krot_launch_max - krot_launch_min)

   limits(qovm_min-qovm_pad,qovm_max+qovm_pad,krot_launch_min-krot_launch_pad,krot_launch_max+krot_launch_pad) 
   ptitles("Angular Phase Advance Wavenumber: Beam Launch","Q/A","Wavenumber [Rad/m]",)
   fma() 

 diag_plt_krot_launch() 

 def diag_plt_krot_v():
   for ii in sp.keys():
     plt(ii,sp_qovm[ii],sp_krot_v[ii],tosys=1,color=sp[ii].color)

   [qovm_min,qovm_max] = [minnd(sp_qovm.values()),maxnd(sp_qovm.values())]
   [krot_v_min,krot_v_max] = [minnd(sp_krot_v.values()),maxnd(sp_krot_v.values())]

   krot_v_pad = 0.1*(krot_v_max - krot_v_min)
   qovm_pad = 0.1*(qovm_max - qovm_min)
   limits(qovm_min-qovm_pad,qovm_max+qovm_pad,krot_v_min-krot_v_pad,krot_v_max+krot_v_pad) 
   ptitles("Angular Phase Advance Wavenumber: Beam Launch in Bz=0","Q/A","Wavenumber [Rad/m]",)
   fma()

 diag_plt_krot_v() 


# Make plot of initial Brho by species 
plt_diag_bro(label = "Initial Rigidity by Species") 

#raise exception("to here")


# Setup diagnostics
# Diagnostics are grouped into several classes:
#   - Particle:  Snapshot plots of distribution function projections 
#   - Field:     Snapshot plots of self fields 
#   - History:   History plots on the evolution of moments and particle counts 
#                   accumulated as the simulation advances.   

# --- set max simulation step for diagnostic setup 
max_diag_step = 5.e4

# --- set history diagnostic and moment accumulations 
if sim_area == 0:
 ds_diag = 1.*cm 
 top.nhist = max(1,nint(ds_diag/wxy.ds))

if sim_area == 1:
 top.nhist = 1#max(1,nint(ds_diag/wxy.ds))           # step interval for histories 

top.itmomnts[0:3] = [0,max_diag_step,top.nhist]   # do loop ranges for moments 
                                                  #   and status writes to tty

# Fix intitial history diagnostics to account for species weight changes
top.jhist = top.jhist-1   # needed to be minus 1 to reset save in right postion 
from getzmom import *
zmmnt() 
savehist(0.) 


# ---- local diagnostic history arrays 
hl_lenhist_max = 10000
hl_vbeam    = fzeros([hl_lenhist_max,top.ns])
hl_ekin     = fzeros([hl_lenhist_max,top.ns])  # axial beam kinetic energy 
hl_spnum    = fzeros([hl_lenhist_max,top.ns])  # number simulation particles
hl_spnumt   = fzeros([hl_lenhist_max])         # number simulation particles (all species) 
hl_ibeam_p  = fzeros([hl_lenhist_max,top.ns])  # beam current (particle)   
hl_ibeam_e  = fzeros([hl_lenhist_max,top.ns])  # beam current (electrical) 
hl_ibeam_pt = fzeros([hl_lenhist_max])         # total beam current (particle)   
hl_ibeam_et = fzeros([hl_lenhist_max])         # total beam current (electrical)   
hl_lambda_p = fzeros([hl_lenhist_max,top.ns])  # line charge (particle) 
hl_lambda_e = fzeros([hl_lenhist_max,top.ns])  # line charge (electrical) 
hl_pth_bar  = fzeros([hl_lenhist_max,top.ns])  # canonical angular momentum (tilde{P_theta}) 
hl_pthn_bar = fzeros([hl_lenhist_max,top.ns])  # normalized canonical angular momentum (P_theta/(m*c))  
hl_lz_bar   = fzeros([hl_lenhist_max,top.ns])  # mechanical angular momentum
hl_krot     = fzeros([hl_lenhist_max,top.ns])  # rotation wavenumber  
hl_lang     = fzeros([hl_lenhist_max,top.ns])  # Larmor rotation angle  
hl_epspv    = fzeros([hl_lenhist_max,top.ns])  # rms total phase volume emittance 
hl_epspvn   = fzeros([hl_lenhist_max,top.ns])  # rms normalized total phase volume emittance ** warning save scaled mm-mrad **
#
hl_ave_vbeam =  fzeros([hl_lenhist_max]) 
hl_Rt       = fzeros([hl_lenhist_max])         # rms rad   (all species) 
hl_Qt       = fzeros([hl_lenhist_max])         # Perveance (all species) 
hl_emitt    = fzeros([hl_lenhist_max])         # emittance (all species) 
hl_sovs0    = fzeros([hl_lenhist_max])         # effective SC depression  

hl_dz = top.nhist*wxy.ds

@callfromafterstep
def diag_hist_hl():
  # check step in history accumulation cycle 
  if top.it%top.nhist != 0: return
  # accumulate history diagnostics by species
  vbtmp = []  
  for ii in sp.keys():
    s = sp[ii]
    js = s.js 
    #
    weight = sum(s.sw*s.w) 
    #
    vbeam = sum( (s.sw*s.w)*s.getvz() )/weight
    gammabeam = 1./sqrt(1.-(vbeam/clight)**2)      
    brho  = s.mass*gammabeam*vbeam/s.charge
    #if ii == 'U33' : print "vz "+ str(s.getvz()[1])
    #if ii == 'U33' : print "z  "+ str(s.getz()[1])
    #
    #rsq = (s.getx())**2 + (s.gety())**2 # species radii squared for ptheta calculation
    #r   = sqrt(rsq)
    r   = s.getr() 
    rsq = r*r  
    #
    #avg_xsq = sum( (s.sw*s.w)*(s.xp)**2 )/weight
    #avg_ysq = sum( (s.sw*s.w)*(s.yp)**2 )/weight
    avg_rsq = sum( (s.sw*s.w)*rsq )/weight
    #
    #avg_xyp = sum( (s.sw*s.w)*s.getx()*s.getyp() )/weight
    #avg_yxp = sum( (s.sw*s.w)*s.gety()*s.getxp() )/weight
    #
    avg_xpy = s.mass*sum( (s.sw*s.w)*s.getx()*s.getuy() )/weight
    avg_ypx = s.mass*sum( (s.sw*s.w)*s.gety()*s.getux() )/weight
    #
    bz0  = getappliedfields(x=0.,y=0.,z=top.zbeam)[5]
    #
    hl_vbeam[top.jhist,js] = vbeam
    # --- Axial kinetic energy 
    hl_ekin[top.jhist,js] = s.mass*clight**2*(gammabeam - 1.)/jperev     
    # --- Simulation Particle Number 
    hl_spnum[top.jhist,js] = s.getn()  
    # --- Current, particle (approx here) 
    hl_ibeam_p[top.jhist,js] = s.charge*s.sw*(s.vbeam0/vbeam)*sum( s.getvz() )  # Fix! use weights correctly  ?? 
    # --- Current, electrical  
    hl_ibeam_e[top.jhist,js] = s.charge*sum( (s.sw*s.w)*s.getvz() )             # Fix! use weights correctly  ??
    # --- line charge 
    hl_lambda_p[top.jhist,js] = hl_ibeam_p[top.jhist,js]/vbeam 
    hl_lambda_e[top.jhist,js] = hl_ibeam_e[top.jhist,js]/vbeam 
    # --- Mechanical angular momentum: <x*y'> - <y*x'>  
    #hl_lz_bar[top.jhist,js] = avg_xyp - avg_yxp
    hl_lz_bar[top.jhist,js] = (avg_xpy - avg_ypx)/(s.mass*gammabeam*vbeam)  
    # --- Normalized canonical angular momentum 
    #hl_pthn_bar[top.jhist,js] = gammabeam*(vbeam/clight)*hl_pth_bar[top.jhist,js]
    #hl_pthn_bar[top.jhist,js] = ( avg_xpy - avg_ypx + (s.charge*bz0/2.)*avg_rsq )/(s.mass*clight)  
    hl_pthn_bar[top.jhist,js] = ( avg_xpy - avg_ypx + sum( (s.sw*s.w)*s.charge*r*getatheta(r) )/weight )/(s.mass*clight)
    # --- Canonical angular momentum (scaled by gamma_b*beta_b*m*c) 
    #hl_pth_bar[top.jhist,js] = hl_lz_bar[top.jhist,js] + bz0/(2.*brho)*avg_rsq 
    hl_pth_bar[top.jhist,js] = hl_pthn_bar[top.jhist,js]/(gammabeam*vbeam/clight) 
    # --- rms total phase volume emittance
    hl_epspv[top.jhist,js] = sqrt( (top.hepsr[0,top.jhist,js])**2 + 4.*(hl_pth_bar[top.jhist,js])**2 ) 
    # --- rms normalized total phase volume emittance ** warning norm emittance scaled mm-mrad to keep to Warp pattern ** 
    hl_epspvn[top.jhist,js] = (gammabeam*(vbeam/clight))*hl_epspv[top.jhist,js]*1.e6 
    # --- Rotation wavenumber 
    hl_krot[top.jhist,js] = hl_lz_bar[top.jhist,js]/avg_rsq
    
    vbtmp.append(vbeam)
    
    # --- Larmor Rotation angle: integrate from previous step  
    if top.jhist == 0:
      hl_lang[0,js] = 0.  
    else:
      hl_lang[top.jhist,js] = hl_lang[top.jhist-1,js] + 0.5*hl_dz*(hl_krot[top.jhist-1,js]+hl_krot[top.jhist,js])  
  # --- total number of simulation particles 
  hl_spnumt[top.jhist] = float(sum(hl_spnum[top.jhist,:]))
  # --- total currents 
  hl_ibeam_pt[top.jhist] = sum(hl_ibeam_p[top.jhist,:]) 
  hl_ibeam_et[top.jhist] = sum(hl_ibeam_e[top.jhist,:]) 
  # --- total perveance 
  #hl_Rt[top.jhist] = sqrt(average( getx(jslist=-1)**2 + gety(jslist=-1)))
  hl_ave_vbeam[top.jhist] = average(vbtmp)
 

diag_hist_hl()   # make sure initial diagnostic saved before any steps 


# --- Plot limits for particle phase space plots. If lframe = true (default
#     false) diagnostics such as ppxxp for x-x' particle phase space will
#     use these ranges.  
#      max/min x,y   plot coordinates (m) 
#      max/min x',y' plot coordinates (rad)
if sim_area == 0:
 l_diag = r_p
 top.xplmax =  l_diag  
 top.xplmin = -l_diag
 top.yplmax =  l_diag
 top.yplmin = -l_diag    

if sim_area == 1 or sim_area == 2:
 top.xplmax =  l_diag_x  
 top.xplmin = -l_diag_x
 top.yplmax =  l_diag_y
 top.yplmin = -l_diag_y       

top.xpplmax = 75.*mr
top.xpplmin = -top.xpplmax    
top.ypplmax =  top.xpplmax 
top.ypplmin = -top.xpplmax

if sim_area == 2:
 top.zplmax =  l_diag_ze
 top.zplmin =  l_diag_zs
 

# --- Color palette for phase-space plots (comment for default)
#     Search for .gp suffix files in the Warp scripts directory for possible
#     choices.  Some useful ones include:
#       earth.gp   (default)        heat.gp     (heat) 
#       gray.gp    (gray scale)     rainbow.gp  (rainbow) 
#palette("heat.gp")

# --- Set a chop factor for particle phase space plots to avoid plotting
#     too many particles (large storage and features will obscure).  Set
#     for approx 10 K particles per species plotted.  
#chop_fraction = 10.e3/float(top.npmax) 
chop_fraction = 10.e3/float(30000)

# --- Particle phase space diagnostics.
#     The list diag_step_part contains all steps where diagnostics in
#     diag_part() are made.  The list can contain repeated elements
#     and need not be ordered

if sim_area == 0: 
 diag_part_z = array([
   z_launch,
   s4p1_zc,
   s4p1_zc-20.*cm,
   s4p1_zc+20.*cm, 
   s4p2_zc,
   s4p2_zc-20.*cm,
   s4p2_zc+20.*cm, 
   gag_zc, 
   #gag_col_zs,
   #gag_col_zs-5.*cm,
   #gag_col_ze,
   gag_col_ze+5.*cm,
   z_adv,
   (s4p1_zc+gag_zc)/2.,
   (s4p2_zc+z_adv)/2. ]) 

 diag_part_z_name = [ 
   "Initial Launch", 
   "S4 Solenoid #1: z-Center", 
   "S4 Solenoid #1: z-Center - 20 cm", 
   "S4 Solenoid #1: z-Center + 20 cm",
   "S4 Solenoid #2: z-Center", 
   "S4 Solenoid #2: z-Center - 20 cm", 
   "S4 Solenoid #2: z-Center + 20 cm",
   "Grated Gap: z-Center",
   #"Grated Gap: z-Start", 
   #"Grated Gap: z-Center - 5 cm", 
   #"Grated Gap: z-End",
   "Grated Gap: z-End + 5 cm", 
   "Final: Before D2 Dipole",
   "Between S4 Solenoid #1 and Grated Gap",
   "Between S4 Solenoid #2 and Final (Before D2 Dipole)" 
                    ]
                    
 diag_field_z = array([
   z_launch,
   s4p1_zc,gag_zc,
   s4p2_zc,
   z_adv 
                     ]) 

 diag_field_z_name = [ 
   "Initial Launch", 
   "S4 Solenoid #1: z-Center", 
   "Grated Gap: z-Center",
   "S4 Solenoid #1: z-Center", 
   "Final: Before D2 Dipole"
                      ]

 diag_hist_z    = array([z_adv]) #array([gag_col_zs,z_adv])

 diag_part_step = nint((diag_part_z-z_launch)/wxy.ds)
 diag_part_z_names = {diag_part_step[i]:diag_part_z_name[i] for i in range(len(diag_part_step))}
 diag_field_step = nint((diag_field_z-z_launch)/wxy.ds)
 diag_field_z_names = {diag_field_step[i]:diag_field_z_name[i] for i in range(len(diag_field_step))}
 diag_hist_step = nint((diag_hist_z-z_launch)/wxy.ds)

if sim_area == 1 or sim_area == 2:
 diag_part_step = arange(5,4001,5)
 diag_part_z_names = [str(i) for i in diag_part_step] 
 diag_field_step = arange(5,4001,5)
 diag_field_z_names = [str(i) for i in diag_field_step] 
 diag_hist_step = arange(250,4001,250)

def diag_part(plt_xy=False,plt_xxp=False,plt_yyp=False,plt_xpyp=False,
              plt_zx=False,plt_zvz=False,
              plt_trace=False, plt_denxy=False, plt_denr=False):
  print "Making particle diagnostic plots"
  #
  try:  
    z_label = diag_part_z_names[top.it]
  except:
    z_label = ""
  #
  # --- x-y projection
  if plt_xy:
    # --- All Species 
    #  Caution:  js=-1 with density plot will just overlay species contour plots 
    #ppxy(js=-1,lframe=true,chopped=chop_fraction,color='density',ncolor=25,
    #     titles=false,yscale=1./mm,xscale=1./mm)
    ppxy(js=-1,lframe=true,chopped=chop_fraction,titles=false,yscale=1./mm,xscale=1./mm)
    ptitles("x-y Phase Space: All Species, z = %5.2f m"%(top.zbeam),
            "x [mm]","y [mm]",z_label)
    fma()
    # --- Target Species 
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      co = s.color
      lab+= ii + "("+co+"), "
      s.ppxy(lframe=true,chopped=chop_fraction,titles=false,yscale=1./mm,xscale=1./mm)
    ptitles("x-y Phase Space: "+lab+" z = %5.2f m"%(top.zbeam),"x [mm]","y [mm]",z_label)
    fma()
  # --- x-x' projection
  if plt_xxp: 
    # --- All Species
    #   Caution:  js = -1 with density plot will overlay species contour plots  
    #ppxxp(js = -1,lframe=true,chopped=chop_fraction,slope='auto',color='density',ncolor=25,
    #      titles=false,yscale=1./mr,xscale=1./mm)
    ppxxp(js = -1,lframe=true,chopped=chop_fraction,slope='auto',titles=false,yscale=1./mr,xscale=1./mm)
    ptitles("x-x' Phase Space: All Species, z = %5.2f m"%(top.zbeam),"x [mm]","x' [mrad]",z_label)
    fma()
    # --- Target Species 
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      co = s.color
      lab+= ii + "("+co+"), "
      s.ppxxp(lframe=true,chopped=chop_fraction,slope='auto',titles=false,yscale=1./mr,xscale=1./mm)
    ptitles("x-x' Phase Space: "+lab+" z = %5.2f m"%(top.zbeam),"x [mm]","x' [mrad]",z_label)
    fma()
  # --- y-y' projection
  if plt_yyp:
    # --- All Species 
    #   Caution: js=-1 with denisty plot will overlay species contour plots 
    #ppyyp(js=-1,lframe=true,chopped=chop_fraction,slope='auto',color='density',ncolor=25,
    #      titles=false,yscale=1./mr,xscale=1./mm)
    ppyyp(js=-1,lframe=true,chopped=chop_fraction,slope='auto',ncolor=25,
          titles=false,yscale=1./mr,xscale=1./mm)
    ptitles("y-y' Phase Space: All Species, z = %5.2f m"%(top.zbeam),
            "y [mm]","y' [mrad]",z_label)
    fma()
    # --- Target Species 
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      co = s.color
      lab+= ii + "("+co+"), "
      s.ppyyp(lframe=true,chopped=chop_fraction,slope='auto',titles=false,yscale=1./mr,xscale=1./mm)
    ptitles("y-y' Phase Space: "+lab+" z = %5.2f m"%(top.zbeam),"y [mm]","y' [mrad]",z_label)
    fma()
  # --- x'-y' projection
  if plt_xpyp:
    # --- All Species 
    #   Caution:  js=-1 with density plot will overlay species countours 
    #ppxpyp(js=-1,lframe=true,chopped=chop_fraction,slope='auto',color='density',ncolor=25,
    #       titles=false,yscale=1./mr,xscale=1./mr)
    ppxpyp(js=-1,lframe=true,chopped=chop_fraction,slope='auto',titles=false,yscale=1./mr,xscale=1./mr)
    ptitles("x'-y' Phase Space: All Species, z = %5.2f m"%(top.zbeam),"x' [mrad]","y' [mrad]",z_label)
    fma()
    # --- Target Species 
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      co = s.color
      lab+= ii + "("+co+"), "
      s.ppxpyp(lframe=true,chopped=chop_fraction,slope='auto',titles=false,yscale=1./mr,xscale=1./mm)
    ptitles("x'-y' Phase Space: "+lab+" z = %5.2f m"%(top.zbeam),"x' [mrad]","y' [mrad]",z_label)
    fma()
  # --- x-y, x-x', y-y', x'-y' projections, 4 to a page (trace-space)
  if plt_trace:
    # --- All Species 
    pptrace(lframe=true,chopped=chop_fraction,slope='auto',color='density',ncolor=25)
    fma()
  # --- x-z projection
  if plt_zx:
    # --- All Species 
    #  Caution:  js=-1 with density plot will just overlay species contour plots 
    #ppxy(js=-1,lframe=true,chopped=chop_fraction,color='density',ncolor=25,
    #     titles=false,yscale=1./mm,xscale=1./mm)
    ppzx(js=-1,lframe=true,chopped=chop_fraction,titles=false,yscale=1./mm,xscale=1./mm)
    ptitles("z-x Phase Space: All Species",
            "z [mm]","x [mm]",z_label)
    fma()
    # --- Target Species 
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      co = s.color
      lab+= ii + "("+co+"), "
      s.ppzx(lframe=true,chopped=chop_fraction,titles=false,yscale=1./mm,xscale=1./mm)
    ptitles("z-x Phase Space: "+lab,"z [mm]","x [mm]",z_label)
    fma()
  # --- x-x' projection
  if plt_zvz: 
    # --- All Species
    #   Caution:  js = -1 with density plot will overlay species contour plots  
    #ppxxp(js = -1,lframe=true,chopped=chop_fraction,slope='auto',color='density',ncolor=25,
    #      titles=false,yscale=1./mr,xscale=1./mm)
    ppzvz(js = -1,lframe=true,titles=false,yscale=1.,xscale=1./mm)
    ptitles("z-vz Phase Space: All Species","z [mm]","vz [m/s]",z_label)
    fma()
    # --- Target Species 
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      co = s.color
      lab+= ii + "("+co+"), "
      s.ppzvz(lframe=true,titles=false,yscale=1.,xscale=1./mm)
    ptitles("z-vz Phase Space: "+lab,"z [mm]","vz [m/s]",z_label)
    fma()
    
  # --- charge density on x and y axes
  if plt_denxy:
    rho_sc = 1.
    ix_cen = sum(where(w3d.xmesh < 0.,1,0))
    iy_cen = sum(where(w3d.ymesh < 0.,1,0))
    # --- All Species 
    rho_x = getrho(iy=iy_cen)
    rho_y = getrho(ix=ix_cen) 
    # 
    plg(rho_x/rho_sc,w3d.xmesh/mm)
    if w3d.l4symtry: plg(rho_x/rho_sc,-w3d.xmesh/mm) 
    plg(rho_y/rho_sc,w3d.ymesh/mm,color="red")
    if w3d.l4symtry or w3d.l2symtry: 
      plg(rho_y/rho_sc,-w3d.ymesh/mm,color="red")
    ptitles("Charge Density: All Species, on x[b], y[r] Axes: z = %5.2f m"%(top.zbeam),
            "x,y [mm]","Density [arb units]",z_label)
    fma()
    
    # --- Target Species: species.get_density() returns density     
    for ii in sp_target:
      s = sp[ii]
      co = s.color
      den = s.get_density()/cm**3
      plg(den[:,iy_cen],w3d.xmesh/mm)
      if w3d.l4symtry: plg(den[:,iy_cen],-w3d.xmesh/mm) 
      plg(den[ix_cen,:],w3d.ymesh/mm,color="red")
      if w3d.l4symtry or w3d.l2symtry: plg(den[ix_cen,:],-w3d.ymesh/mm,color="red")
      ptitles("Density: "+ii+" on x[b], y[r] Axes: z = %5.2f m"%(top.zbeam),
              "x,y [mm]","Density [#/cm^3]",z_label)
      fma()
      
    for ii in sp_target:
      s = sp[ii]
      co = s.color
      den = s.get_density()/cm**2
      denx = [sum(den[jj]) for jj in range(len(den))]
      plg(denx,w3d.xmesh/mm,color=co)
    ptitles("Density: "+ii+" on x projection, Axes: z = %5.2f m"%(top.zbeam),
              "x [mm]","Density [#/cm^2]",z_label)
    fma()
   # --- charge density on radial shme
  if plt_denr:
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
    # --- for all species on mesh 
    for ii in sp.keys():
       s  = sp[ii]
       #
       np = s.getn() 
       rp = s.getr() 
       wp = s.getweights()
       #
       deposgrid1d(1,np,rp,wp,nr,weightr,count,0.,rmax)
    #
    den[1:nr+1] = weightr[1:nr+1]/(2.*pi*dr*rmesh[1:nr+1])
    den[0]      = den[1]   # set origin by next grid up to remove distraction
    #
    #
    plg(den/cm**3, rmesh/mm)
    plg(den/cm**3,-rmesh/mm) 
    ptitles("Radial Number Density: All Species, z = %5.2f m"%(top.zbeam),"radius r [mm]","rho [particles/cm**3]",z_label)
    ir = min(nr,sum(where(den>0,1,0)))      # index farthest radial extent of rho in radial mesh assuming no halo  
    rmmax = max(1.2*rmesh[ir],0.01) # set curoff to contain radial density  
    rmmax = cm*nint(rmmax/cm + 0.5) # round up to nearest cm to contain plot 
    denmax = 1.2*maxnd(den) 
    limits(-rmmax/mm,rmmax/mm,0.,denmax/cm**3)
    fma() 
    # --- for target species on mesh 
    for ii in sp_target:
       s  = sp[ii]
       co = s.color 
       lab = ii + "("+co+"), "
       #
       np = s.getn() 
       rp = s.getr() 
       wp = s.getweights()
       #
       weightr = zeros(nr+1)   # reset for clean accumulation/count with itask = 1 
       count   = zeros(nr+1)   
       deposgrid1d(1,np,rp,wp,nr,weightr,count,0.,rmax)
       # 
       den[1:nr+1] = weightr[1:nr+1]/(2.*pi*dr*rmesh[1:nr+1])
       den[0]      = den[1]   # set origin by next grid up to remove distraction
       #
       #
       plg(den/cm**3, rmesh/mm,color=co)
       plg(den/cm**3,-rmesh/mm,color=co) 
       ptitles("Radial Number Density: "+lab+" z = %5.2f m"%(top.zbeam),"radius r [mm]","rho [particles/cm**3]",z_label)
       ir = sum(where(den>0,1,0))      # index farthest radial extent of rho in radial mesh assuming no halo  
       rmmax = max(1.2*rmesh[ir],0.01) # set curoff to contain radial density  
       rmmax = cm*nint(rmmax/cm + 0.5) # round up to nearest cm to contain plot 
       denmax = 1.2*maxnd(den) 
       limits(-rmmax/mm,rmmax/mm,0.,denmax/cm**3)
       fma()
 
    
# --- Field diagnostics.  
#     The list diag_step_field containins all steps where
#     diagnostics in diag_field() are made. The list can contain repeated
#     elements and need not be ordered.   


def diag_field(plt_pa=False,plt_pc_xy=False,plt_pc_xyp=False,plt_pc_zx=False,plt_pc_zxp=False):
  print "Making field diagnostic plots"
  #
  try:  
    z_label = diag_field_z_names[top.it]
  except:
    z_label = ""
  # --- self-field electrostatic potential
  if plt_pc_xy:
    pfxy(cond=true,titles=false,yscale=1./mm,xscale=1./mm,iz = 0)
    ptitles("Self-Field Potential: z = %5.2f"%(top.zbeam),
            "x [mm]","y [mm]",z_label)
    fma()
  # --- self-field electrostatic potential and particles together
  if plt_pc_xyp:
    # --- All particle species included 
    pfxy(cond=true,titles=false,yscale=1./mm,xscale=1./mm)
    #   Caution: js=-1 with density plot will superimpose species contours 
    #ppxy(js=-1,lframe=true,chopped=chop_fraction,color='density',ncolor=25,
    #     titles=false,yscale=1./mm,xscale=1./mm)
    ppxy(js=-1,lframe=true,chopped=chop_fraction,titles=false,yscale=1./mm,xscale=1./mm)
    ptitles("Self-Field Potential: z = %5.2f"%(top.zbeam),
            "x [mm]","y [mm]",z_label)
    fma()
    # --- Target particle species 
    lab = ""
    pfxy(cond=true,titles=false,yscale=1./mm,xscale=1./mm)
    for ii in sp_target:
      s = sp[ii]
      co = s.color
      lab+= ii + "("+co+"), "
      s.ppxy(lframe=true,chopped=chop_fraction,titles=false,yscale=1./mm,xscale=1./mm)
      s.ppxy(lframe=true,chopped=chop_fraction,titles=false,yscale=1./mm,xscale=1./mm)
    ptitles("Self-Field Potential: + "+lab+" Particles, z = %5.2f"%(top.zbeam),"x [mm]","y [mm]",z_label)
    fma()
    # --- self-field electrostatic potential
  if plt_pc_zx:
    pfzx(cond=true,titles=false,yscale=1./mm,xscale=1./mm)
    ptitles("Self-Field Potential z-x",
            "z [mm]","x [mm]",z_label)
    fma()
  # --- self-field electrostatic potential and particles together
  if plt_pc_xyp:
    # --- All particle species included 
    pfzx(cond=true,titles=false,yscale=1./mm,xscale=1./mm)
    #   Caution: js=-1 with density plot will superimpose species contours 
    #ppxy(js=-1,lframe=true,chopped=chop_fraction,color='density',ncolor=25,
    #     titles=false,yscale=1./mm,xscale=1./mm)
    ppzx(js=-1,lframe=true,chopped=chop_fraction,titles=false,yscale=1./mm,xscale=1./mm)
    ptitles("Self-Field Potential z-x",
            "z [mm]","x [mm]",z_label)
    fma()
    # --- Target particle species 
    lab = ""
    pfzx(cond=true,titles=false,yscale=1./mm,xscale=1./mm)
    for ii in sp_target:
      s = sp[ii]
      co = s.color
      lab+= ii + "("+co+"), "
      s.ppzx(lframe=true,chopped=chop_fraction,titles=false,yscale=1./mm,xscale=1./mm)
      s.ppzx(lframe=true,chopped=chop_fraction,titles=false,yscale=1./mm,xscale=1./mm)
    ptitles("Self-Field Potential z-x : + "+lab,"z [mm]","x [mm]",z_label)
    fma()
  # --- Electrostatic potential on principal axes 
  if plt_pa:
    diag_plt_phi_ax(label="Beam Potential along y,x = 0 [b,r] at z = %5.2f"%(top.zbeam))
    fma()
    # 
    xrms = max(top.xrms[0,sp['U33'].js],top.xrms[0,sp['U34'].js]) 
    diag_plt_phi_ax(label="Beam Potential along y,x = 0 [b,r] at z = %5.2f"%(top.zbeam),xmax=2.*xrms) 
    fma() 


# --- History diagnostics.  These can be made at intermediate stages of the
#     run as well as at the end.  The list diag_step_hist contains all
#     steps where diagnostics in diag_hsit() are made. The list can
#     contain repeated elements and need not be ordered.
#     Notes:
#      * Many additional history diagnostics can be added by looking for
#        relevant moments accumulated in the Warp (see the variable group
#        "Hist" in top.v for an extensive list of variables that can be
#         used) and using gist commands to make relevant plots

#diag_hist_z    = array([z_adv]) #array([gag_col_zs,z_adv])
#diag_hist_step = nint((diag_hist_z-z_launch)/wxy.ds)

def diag_hist(plt_ekin=False,plt_spnum=False,plt_curr_p=False,plt_curr_e=False,plt_lam_p=False,plt_lam_e=False,
              plt_lz=False,plt_pth=False,plt_pthn=False,plt_krot=False,plt_lang=False,
              plt_cen=False,plt_envrms=False,plt_envmax=False,plt_envrmsp=False, 
              plt_emit=False,plt_emitn=False,plt_emitg=False,plt_emitng=False,plt_emitr=False,plt_emitnr=False,
              plt_emitpv=False,emitpvn=False, 
              plt_temp=False,plt_temp_flow=False):
  print "Making history diagnostic plots"
  #
  # --- kinetic energy 
  if plt_ekin:
    # --- All Species Combined, MeV
    #hpekin(titles=false,yscale=1.,lhzbeam=true)
    #ptitles("History: All Species Kinetic Energy","z [m]","MeV", )
    #fma()
    # --- All Species, in keV/u 
    for ii in sort(sp.keys()):
      s = sp[ii]
      js = s.js
      co = s.color
      A  = s.mass/amu
      plg(hl_ekin[0:top.jhist+1,js]/(A*kV),top.hzbeam[0:top.jhist+1],color=co)        
      #hpekin(js=js,color=co,titles=false,yscale=1./A,lhzbeam=true)    
    ptitles("History: Kinetic Energy","z [m]","KeV/u", )
    fma()
    # --- U species, in MeV/u
    for ii in sort(sp_U.keys()):
      s = sp[ii]
      js = s.js
      co = s.color
      A  = s.mass/amu
      #hpekin(js=js,color=co,titles=false,yscale=1./A,lhzbeam=true)
      plg(hl_ekin[0:top.jhist+1,js]/(A*kV),top.hzbeam[0:top.jhist+1],color=co)        
    ptitles("History: U Species Kinetic Energy","z [m]","KeV/u", )
    fma()
    # --- O species, in MeV/u 
    for ii in sort(sp_O.keys()):
      s = sp[ii]
      js = s.js
      co = s.color
      A  = s.mass/amu
      plg(hl_ekin[0:top.jhist+1,js]/(A*kV),top.hzbeam[0:top.jhist+1],color=co)        
      #hpekin(js=js,color=co,titles=false,yscale=1./A,lhzbeam=true) # Was getting wrong answer !!
    ptitles("History: O Species Kinetic Energy","z [m]","KeV/u", )
    fma()
    # --- By Target Species, in kV/Q
    #     Plot by KV/Q so you can see total potential gain falling through 
    #     full bias to check system tuning  
    zi = top.hzbeam[0]
    zf = top.hzbeam[top.jhist]
    ekin_t = Bias/kV
    lab = ""
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      Q  = s.charge_state
      lab+= ii + "("+co+"), "
      plg(hl_ekin[0:top.jhist+1,js]/(Q*kV),top.hzbeam[0:top.jhist+1],color=co)        
      #hpekin(js=js,color=co,titles=false,yscale=1./Q,lhzbeam=true)
    plg(array([ekin_t,ekin_t]),array([zi,zf]),type="dash") 
    ptitles("History: "+lab+"Kinetic Energy","z [m]","KeV/Q", )
    limits(zi,zf,0.,1.2*ekin_t) 
    fma()
  # --- simulation particle number (to check for lost particles)
  #     Comment: tried using hppnum() but was unclear what was being plotted 
  if plt_spnum:
    # --- All Species Combined  
    plg(hl_spnumt[0:top.jhist+1],top.hzbeam[0:top.jhist+1])    
    ptitles("History: Live Sim Particle Number (all species)", "z [m]","Particle Number (simulation)", )
    fma()
    # --- All Species Individually 
    for ii in sort(sp.keys()):
      s = sp[ii]
      js = s.js
      co = s.color
      plg(hl_spnum[0:top.jhist+1,js],top.hzbeam[0:top.jhist+1],color=co)        
    ptitles("History: Live Sim Particle Number (by species)","z [m]","Particle Number (simulation)", )
    fma() 
    # --- Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(hl_spnum[0:top.jhist+1,js],top.hzbeam[0:top.jhist+1],color=co)        
    ptitles("History: "+lab+" Live Sim Particle Number","z [m]","Particle Number (simulation)", )
    fma()             
  # --- current (particle)  
  if plt_curr_p:
    # --- All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(hl_ibeam_p[0:top.jhist+1,js]*1.e6,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species Particle Current (approx)", "z [m]","Current (microA)", )
    fma() 
    # --- Target Species 
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(hl_ibeam_p[0:top.jhist+1,js]*1.e6,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" Particle Current (approx)","z [m]","Current (microA)", )
    fma() 
    # --- Total
    plg(hl_ibeam_pt[0:top.jhist+1]*1.e3,top.hzbeam[0:top.jhist+1])    
    ptitles("History: Total Particle Current (approx)","z [m]","Current (mA)", )
    fma()             
  # --- current (electrical)  
  if plt_curr_e:
    # --- All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(hl_ibeam_e[0:top.jhist+1,js]*1.e6,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species Electrical Current", "z [m]","Current (microA)", )
    fma()
    # --- Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(hl_ibeam_e[0:top.jhist+1,js]*1.e6,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" Electrical Current","z [m]","Current (microA)", )
    fma()
    # --- Total
    plg(hl_ibeam_et[0:top.jhist+1]*1.e3,top.hzbeam[0:top.jhist+1])    
    ptitles("History: Total Electrical Current","z [m]","Current (mA)", )
    fma()                          
  # --- line charge (particle)  
  if plt_lam_p:
    # --- All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(hl_lambda_p[0:top.jhist+1,js]*10**9,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species Particle Line Charge", "z [m]","Line Charge (nC/m)", )
    fma()
    # --- Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(hl_lambda_p[0:top.jhist+1,js]*10**9,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" Particle Line Charge","z [m]","Line Charge (nC/m)", )
    fma()             
  # --- line charge (electrical)  
  if plt_lam_e:
    # --- All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(hl_lambda_e[0:top.jhist+1,js]*10**9,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species Electrical Line Charge", "z [m]","Line Charge (nC/m)", )
    fma()
    # --- Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(hl_lambda_e[0:top.jhist+1,js]*10**9,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" Electrical Line Charge","z [m]","Line Charge (nC/m)", )
    fma()             
  # --- lz mechanical angular momentum  
  if plt_lz:
    # --- All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(hl_lz_bar[0:top.jhist+1,js]*10**6,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species Mechanical Angular Mom", "z [m]","<xy'>-<yx'>  [mm-mrad]", )
    fma()
    # --- Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(hl_lz_bar[0:top.jhist+1,js]*10**6,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" Mechanical Angular Mom","z [m]","<xy'>-<yx'>  [mm-mrad]", )
    fma()             
  # --- canonical angular momentum  
  if plt_pth:
    # --- All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(hl_pth_bar[0:top.jhist+1,js]*10**6,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species Canonical Angular Mom", "z [m]","Ptheta  [mm-mrad]", )
    fma()
    # --- Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(hl_pth_bar[0:top.jhist+1,js]*10**6,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" Canonical Angular Mom","z [m]","Ptheta  [mm-mrad]", )
    fma()             
  # --- canonical angular momentum (normalized)   
  if plt_pthn:
    # --- All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(hl_pthn_bar[0:top.jhist+1,js]*10**6,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species Norm Canonical Angular Mom", "z [m]","Ptheta  [mm-mrad]", )
    fma()
    # --- Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(hl_pthn_bar[0:top.jhist+1,js]*10**6,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" Norm Canonical Angular Mom","z [m]","Ptheta  [mm-mrad]", )
    fma()             
  # --- effective rotation wavenumber 
  if plt_krot:
    # --- All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(hl_krot[0:top.jhist+1,js],top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species Effective Rot Wavenumber", "z [m]","krot  [rad/m]", )
    fma()
    # --- Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(hl_krot[0:top.jhist+1,js],top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" Effective Rot Wavenumber","z [m]","krot  [rad/m]", )
    fma()             
  # --- larmor rotation angle   
  if plt_lang:
    # --- All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg((180./pi)*hl_lang[0:top.jhist+1,js],top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species Larmor Rot Angle", "z [m]","Rotation [deg]", )
    fma()
    # --- Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg((180./pi)*hl_lang[0:top.jhist+1,js],top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" Larmor Rot Angle","z [m]","Rotation  [deg]", )
    fma()             
  # --- centroid
  if plt_cen:
    # All Species Combined, x- and y-plane 
    hpxbar(titles=false,yscale=1./mm,lhzbeam=true)
    hpybar(titles=false,yscale=1./mm,lhzbeam=true,color="red")
    ptitles("History: All Species x-,y-Centroid: x[b], y[r]","z [m]","<x>, <y> Centroids [mm]", )
    fma()
    # --- By Target Species, x-plane 
    hpxbar(titles=false,yscale=1./(sqrt(2.)*mm),lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpxbar(js=js,color=co,titles=false,yscale=1./(sqrt(2.)*mm),lhzbeam=true)    
    ptitles("History: "+lab+"x-Centroid","z [m]","<x> [mm]", )
    fma()
    #
    lab = ""    
    for ii in sp.keys():
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpxbar(js=js,color=co,titles=false,yscale=1./(sqrt(2.)*mm),lhzbeam=true)    
    ptitles("History: "+lab+"x-Centroid","z [m]","<x> [mm]", )
    fma()
    # --- By Target Species, y-plane 
    hpybar(titles=false,yscale=1./(sqrt(2.)*mm),lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpybar(js=js,color=co,titles=false,yscale=1./(sqrt(2.)*mm),lhzbeam=true)    
    ptitles("History: "+lab+"y-Centroid","z [m]","<y> [mm]", )
    fma()
    #
    lab = ""    
    for ii in sp.keys():
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpybar(js=js,color=co,titles=false,yscale=1./(sqrt(2.)*mm),lhzbeam=true)    
    ptitles("History: "+lab+"y-Centroid","z [m]","<y> [mm]", )
    fma()
  # --- rms envelope width 
  if plt_envrms:
    # --- All Species Combined, x- and y-plane  
    hpenvx(titles=false,yscale=1./(2.*mm),lhzbeam=true)    
    hpenvy(titles=false,yscale=1./(2.*mm),lhzbeam=true,color="red")
    ptitles("History: All Species RMS Envelope: x[b], y[r]","z [m]","RMS Width [mm]", )
    fma()
    # --- Target Species, x-plane 
    hpenvx(titles=false,yscale=1./(2.*mm),lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpenvx(js=js,color=co,titles=false,yscale=1./(2.*mm),lhzbeam=true)    
    ptitles("History: "+lab+"RMS x-Envelope","z [m]","RMS Width [mm]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpenvx(js=js,color=co,titles=false,yscale=1./(2.*mm),lhzbeam=true)    
    ptitles("History: "+lab+"RMS x-Envelope","z [m]","RMS Width [mm]", )
    fma()
    # --- Target Species, y-plane 
    hpenvy(titles=false,yscale=1./(2.*mm),lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpenvy(js=js,color=co,titles=false,yscale=1./(2.*mm),lhzbeam=true)    
    ptitles("History: "+lab+"RMS y-Envelope","z [m]","RMS Width [mm]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpenvy(js=js,color=co,titles=false,yscale=1./(2.*mm),lhzbeam=true)    
    ptitles("History: "+lab+"RMS y-Envelope","z [m]","RMS Width [mm]", )
    fma()
  # --- max particle envelopes 
  if plt_envmax:
    # --- x-plane, All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(top.hxmaxp[0:top.jhist+1,js]/mm,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species max particle x", "z [m]","Max x [mm]", )
    fma()
    # --- x-plane, Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(top.hxmaxp[0:top.jhist+1,js]/mm,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" max particle x","z [m]","Max x [mm]", )
    fma()             
    # --- y-plane, All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(top.hymaxp[0:top.jhist+1,js]/mm,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species max particle y", "z [m]","Max y [mm]", )
    fma()
    # --- y-plane, Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(top.hymaxp[0:top.jhist+1,js]/mm,top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" max particle y","z [m]","Max y [mm]", )
    fma()             
  # --- rms envelope angle  
  if plt_envrmsp:
    # --- Target Species, x-plane 
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(top.hxxpbar[0,0:top.jhist+1,js]/(top.hxrms[0,0:top.jhist+1,js]*mr),top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+"RMS x-Envelope Angle","z [m]","RMS Angle [mr]", )
    fma()
    # --- Target Species, y-plane 
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(top.hyypbar[0,0:top.jhist+1,js]/(top.hyrms[0,0:top.jhist+1,js]*mr),top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+"RMS y-Envelope Angle","z [m]","RMS Angle [mr]", )
    fma()
  # --- emittance, unnormalized 
  if plt_emit:
    # --- All Species Combined, x- and y-plane 
    hpepsx(titles=false,yscale=1./(mm*mr),lhzbeam=true)
    hpepsy(titles=false,yscale=1./(mm*mr),lhzbeam=true,color="red")
    ptitles("History: All Species RMS Edge x-, y-Emittance: x[b],y[r]","z [m]","Emittance [mm-mr]", )
    fma()
    # --- Target Species, x-plane 
    hpepsx(titles=false,yscale=1./(mm*mr),lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsx(js=js,color=co,titles=false,yscale=1./(mm*mr),lhzbeam=true)    
    ptitles("History: "+lab+"RMS Edge x-Emittance","z [m]","Emittanace [mm-mr]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsx(js=js,color=co,titles=false,yscale=1./(mm*mr),lhzbeam=true)    
    ptitles("History: "+lab+"RMS Edge x-Emittance","z [m]","Emittanace [mm-mr]", )
    fma()
    # --- Target Species, y-plane 
    hpepsy(titles=false,yscale=1./(mm*mr),lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsy(js=js,color=co,titles=false,yscale=1./(mm*mr),lhzbeam=true)    
    ptitles("History: "+lab+"RMS Edge y-Emittance","z [m]","Emittance [mm-mr]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsy(js=js,color=co,titles=false,yscale=1./(mm*mr),lhzbeam=true)    
    ptitles("History: "+lab+"RMS Edge y-Emittance","z [m]","Emittance [mm-mr]", )
    fma()
  # --- emittance, normalized ** warning norm emittance scaled mm-mrad by default **
  if plt_emitn:
    # --- All Species Combined, x- and y-plane 
    hpepsnx(titles=false,yscale=1.,lhzbeam=true)
    hpepsny(titles=false,yscale=1.,lhzbeam=true,color="red")
    ptitles("History: All Species Norm RMS Edge x-, y-Emittance: x[b],y[r]","z [m]","Norm Emittance [mm-mr]", )
    fma()
    # --- By Target Species, x-plane 
    hpepsnx(titles=false,yscale=1.,lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsnx(js=js,color=co,titles=false,yscale=1.,lhzbeam=true)    
    ptitles("History: "+lab+"Norm RMS Edge x-Emittance","z [m]","Norm Emittanace [mm-mr]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsnx(js=js,color=co,titles=false,yscale=1.,lhzbeam=true)    
    ptitles("History: "+lab+"Norm RMS Edge x-Emittance","z [m]","Norm Emittanace [mm-mr]", )
    fma()
    # --- By Target Species, y-plane 
    hpepsny(titles=false,yscale=1.,lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsny(js=js,color=co,titles=false,yscale=1.,lhzbeam=true)    
    ptitles("History: "+lab+"Norm RMS Edge y-Emittance","z [m]","Norm Emittance [mm-mr]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsny(js=js,color=co,titles=false,yscale=1.,lhzbeam=true)    
    ptitles("History: "+lab+"Norm RMS Edge y-Emittance","z [m]","Emittance [mm-mr]", )
    fma()
  # --- emittance, generalized unnormalized 
  if plt_emitg:
    # --- All Species Combined, g- and h-plane 
    hpepsg(titles=false,yscale=1./(mm*mr),lhzbeam=true)
    hpepsh(titles=false,yscale=1./(mm*mr),lhzbeam=true,color="red")
    ptitles("History: All Species RMS g-, h-Emittance: g[b],h[r]","z [m]","Emittance [mm-mr]", )
    fma()
    # --- By Target Species, g-plane 
    hpepsg(titles=false,yscale=1./(mm*mr),lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsg(js=js,color=co,titles=false,yscale=1./(mm*mr),lhzbeam=true)    
    ptitles("History: "+lab+"RMS g-Emittance","z [m]","Emittanace [mm-mr]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsg(js=js,color=co,titles=false,yscale=1./(mm*mr),lhzbeam=true)    
    ptitles("History: "+lab+"RMS g-Emittance","z [m]","Emittanace [mm-mr]", )
    fma()
    # --- By Target Species, h-plane 
    hpepsh(titles=false,yscale=1./(mm*mr),lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsh(js=js,color=co,titles=false,yscale=1./(mm*mr),lhzbeam=true)    
    ptitles("History: "+lab+"RMS h-Emittance","z [m]","Emittance [mm-mr]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsh(js=js,color=co,titles=false,yscale=1./(mm*mr),lhzbeam=true)    
    ptitles("History: "+lab+"RMS h-Emittance","z [m]","Emittance [mm-mr]", )
    fma()
  # --- emittance, generalized normalized 
  if plt_emitng:
    # --- All Species Combined, g- and h-plane 
    hpepsng(titles=false,yscale=1.,lhzbeam=true)
    hpepsnh(titles=false,yscale=1.,lhzbeam=true,color="red")
    ptitles("History: All Species RMS Norm g-, h-Emittance: g[b],h[r]","z [m]","Norm Emittance [mm-mr]", )
    fma()
    # --- By Target Species, g-plane  
    hpepsng(titles=false,yscale=1.,lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsng(js=js,color=co,titles=false,yscale=1.,lhzbeam=true)    
    ptitles("History: "+lab+"RMS Norm g-Emittance","z [m]","Norm Emittanace [mm-mr]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsng(js=js,color=co,titles=false,yscale=1.,lhzbeam=true)    
    ptitles("History: "+lab+"RMS Norm g-Emittance","z [m]","Norm Emittanace [mm-mr]", )
    fma()
    # --- By Target Species, h-plane 
    hpepsnh(titles=false,yscale=1.,lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsnh(js=js,color=co,titles=false,yscale=1.,lhzbeam=true)    
    ptitles("History: "+lab+"RMS Norm h-Emittance","z [m]","Norm Emittance [mm-mr]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsnh(js=js,color=co,titles=false,yscale=1.,lhzbeam=true)    
    ptitles("History: "+lab+"RMS Norm h-Emittance","z [m]","Norm Emittance [mm-mr]", )
    fma()
  # --- emittance, generalized radial unnormalized 
  if plt_emitr:
    # --- All Species Combined
    hpepsr(titles=false,yscale=1./(mm*mr),lhzbeam=true)
    ptitles("History: All Species RMS r-Emittance","z [m]","Emittance [mm-mr]", )
    fma()
    # --- By Target Species  
    hpepsr(titles=false,yscale=1./(mm*mr),lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsr(js=js,color=co,titles=false,yscale=1./(mm*mr),lhzbeam=true)    
    ptitles("History: "+lab+"RMS r-Emittance","z [m]","Emittanace [mm-mr]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsr(js=js,color=co,titles=false,yscale=1./(mm*mr),lhzbeam=true)    
    ptitles("History: "+lab+"RMS r-Emittance","z [m]","Emittanace [mm-mr]", )
    fma()
  # --- emittance, generalized radial normalized ** warning norm emittance scaled mm-mrad by default **
  if plt_emitnr:
    # --- All Species Combined
    hpepsnr(titles=false,yscale=1.,lhzbeam=true)
    ptitles("History: All Species Norm RMS r-Emittance","z [m]","Norm Emittance [mm-mr]", )
    fma()
    # --- By Target Species  
    hpepsnr(titles=false,yscale=1.,lhzbeam=true)
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsnr(js=js,color=co,titles=false,yscale=1.,lhzbeam=true)    
    ptitles("History: "+lab+"RMS Norm r-Emittance","z [m]","Norm Emittanace [mm-mr]", )
    fma()
    #
    lab = ""    
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      hpepsnr(js=js,color=co,titles=false,yscale=1.,lhzbeam=true)    
    ptitles("History: "+lab+"RMS Norm r-Emittance","z [m]","Norm Emittanace [mm-mr]", )
    fma()
  # --- emittance, total phase volume, unnormalized 
  if plt_emitpv:
    # --- All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(hl_epspv[0:top.jhist+1,js]/(mm*mr),top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species Total Phase Volume Emittance", "z [m]","Emittance [mm-mrad]", )
    fma()
    # --- Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(hl_epspv[0:top.jhist+1,js]/(mm*mr),top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" Total Phase Volume Emittance","z [m]","Emittance [mm-mrad]", )
    fma()             
  # --- emittance, total phase volume, normalized  ** warning norm emittance scaled mm-mrad by default **
  if plt_emitpv:
    # --- All Species Combined  
    for ii in sort(sp.keys()):
      s = sp[ii]        
      js = s.js
      co = s.color
      plg(hl_epspvn[0:top.jhist+1,js],top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: Species Total Phase Volume Norm Emittance", "z [m]","Norm Emittance [mm-mrad]", )
    fma()
    # --- Target Species
    lab = "" 
    for ii in sp_target:
      s = sp[ii]
      js = s.js
      co = s.color
      lab+= ii + "("+co+"), "
      plg(hl_epspvn[0:top.jhist+1,js],top.hzbeam[0:top.jhist+1],color=co)    
    ptitles("History: "+lab+" Total Phase Volume Norm Emittance","z [m]","Norm Emittance [mm-mrad]", )
    fma()             
  # --- temperature using <x'2> and corelation of x and x' via <x*x'> 
  if plt_temp and top.jhist > 0:
    xrms  = top.hxrms[0,1:top.jhist+1,0]
    emitx = top.hepsx[0,1:top.jhist+1,0]
    plg(beam.mass*top.vbeam**2*emitx**2/(jperev*16.*xrms**2),
        top.hzbeam[1:top.jhist+1] )
    yrms  = top.hyrms[0,1:top.jhist+1,0]
    emity = top.hepsy[0,1:top.jhist+1,0]
    plg(beam.mass*top.vbeam**2*emity**2/(jperev*16.*yrms**2),
        top.hzbeam[1:top.jhist+1],color="red")
    ptitles("History: Spatial Avg Temp: x [b], y [r]",
            "z [m]","Spatial Avg Temp (eV)", )
    fma()

#  -- Install diagnostics at appropriate intervals after steps
#       Add options to generate plots desired 
#  -- Install diagnostics at appropriate intervals after steps
#       Add options to generate plots desired 

# Function to call diagnostics at a timestep in step control lists 
if sim_area == 0 or sim_area == 1 :
 def diag_calls():
  if top.it in diag_part_step:
    diag_part(plt_xy=true,plt_xxp=true,plt_yyp=true,plt_xpyp=true,
              plt_trace=false,plt_denxy=true,plt_denr=true)
  if top.it in diag_field_step: 
    diag_field(plt_pc=true,plt_pc_xy=true,plt_pa=true)
  if top.it in diag_hist_step:
    diag_hist(plt_ekin=true,plt_spnum=true,plt_curr_e=true,plt_curr_p=true,plt_lam_p=true,plt_lam_e=true,
              plt_lz=true,plt_pth=true,plt_pthn=true,plt_krot=true,plt_lang=true, 
              plt_cen=true,plt_envrms=true,plt_envmax=true,plt_envrmsp=true,  
              plt_emit=true,plt_emitn=true,plt_emitg=true,plt_emitng=true,plt_emitr=true,plt_emitnr=true, 
              plt_emitpv=true,emitpvn=true)
elif sim_area == 2 :
 def diag_calls():
  if top.it in diag_part_step:
    diag_part(plt_xy=true,plt_xxp=true,plt_yyp=true,plt_xpyp=true,
              plt_zx=true,plt_zvz=true,
              plt_trace=false,plt_denxy=true,plt_denr=true)
  if top.it in diag_field_step: 
    diag_field(plt_pc_xy=true,plt_pc_xyp=true,plt_pc_zx=true,plt_pc_zxp=true,plt_pa=true)
  if top.it in diag_hist_step:
    diag_hist(plt_ekin=true,plt_spnum=true,plt_curr_e=true,plt_curr_p=true,plt_lam_p=true,plt_lam_e=true,
              plt_lz=true,plt_pth=true,plt_pthn=true,plt_krot=true,plt_lang=true, 
              plt_cen=true,plt_envrms=true,plt_envmax=true,plt_envrmsp=true,  
              plt_emit=true,plt_emitn=true,plt_emitg=true,plt_emitng=true,plt_emitr=true,plt_emitnr=true, 
              plt_emitpv=true,emitpvn=true)

# Install diagnostic calls after simulation step
installafterstep(diag_calls)

# Step 0 diagnostics (if any) of the initial distribution loaded 
diag_calls() 

# Advance simulation specified steps 

#execfile(scriptfolder + "anm_plot_bnd.py")

#raise Exception("to here")

if sim_area == 0:
 # ---- to grated accel gap  
 n_step = nint((neut_z1-z_launch)/wxy.ds) 
 top.prwall = r_p_up    # consistent aperture 
 step(n_step)

 # --- reset species weights to turn off neutralization  
 for s in sp.values():
    s.w0 = 1. 

 loadrho()     # applies adjusted species weights  
 fieldsolve()  # make field consistent with turned off neutralization 

 # --- unneutralized advance in acceleration column  
 n_step = nint((neut_z2-top.zbeam)/wxy.ds)
 top.prwall = gag_rp   # consistent aperture 
 step(n_step)

 # --- reset species weights to turn on post accel gap neutralization  
 for s in sp.values():
    s.w0 = 1.-neut_f2 

 # --- neutralized advance after acceleration column to start of dipole   
 n_step = nint((z_adv-top.zbeam)/wxy.ds) - 5   # add two extra steps in case of roundoff accumulation 
 top.prwall = r_p_down    # consistent aperture 
 step(n_step)
 
 execfile( scriptfolder + "outparticle.py")
 step(7) # add two extra steps in case of roundoff accumulation 
 execfile( scriptfolder + "outputdat2.py")
 execfile( scriptfolder + "outputdat3.py")

if sim_area == 1 or sim_area == 2 :
 if sim_area == 1 :
   n_step = nint((d5a_end-top.zbeam)/wxy.ds) + 2   # add two extra steps in case of roundoff accumulation 
 if sim_area == 2 :
   n_step = nint((d5a_end-top.zbeam)/dz) + 2   # add two extra steps in case of roundoff accumulation 
 step(n_step)

 execfile( scriptfolder + "outputdat3.py")
 step(2)
 
 diag_hist(plt_ekin=true,plt_spnum=true,plt_curr_e=true,plt_curr_p=true,plt_lam_p=true,plt_lam_e=true,
              plt_lz=true,plt_pth=true,plt_pthn=true,plt_krot=true,plt_lang=true, 
              plt_cen=true,plt_envrms=true,plt_envmax=true,plt_envrmsp=true,  
              plt_emit=true,plt_emitn=true,plt_emitg=true,plt_emitng=true,plt_emitr=true,plt_emitnr=true, 
              plt_emitpv=true,emitpvn=true)

# Make additional history plots for final run if not already called 
#if not(top.it >= diag_hist_step.max()):
#  diag_hist()  # Add full arg list 

# Save restart dump of run.  By default the name of the dump file is
# top.runid (or script name if this is not set) with the step number (iii)
# and ".dump" appended to the name:
#       runidiii.pdb 
# To restart:
#   % python
#     >>> from warp import *
#     >>> restart("runidiii.dump") 
#
#dump() 

# Make plot of final Brho by species 
#plt_diag_bro(label = "Final Rigidity by Species") 

# Output data to auxillary file
output_data = false 
output_data_file = "frib-front-xy_data.txt" 

if output_data:
  fout = open(output_data_file,"a")
  #
  #fout.write("Run Number %s :\n"%irun) 
  fout.write(" Solenoid Excitations:\n")
  fout.write("  S41 = %s \n"%s4p1_str)
  fout.write("  S41 = %s \n"%s4p2_str)
  for ii in sp_target:
    s  = sp[ii] 
    js = s.js 
    rmsx    = top.hxrms[0,top.jhist,js]
    drmsxds = top.hxxpbar[0,top.jhist,js]/top.hxrms[0,top.jhist,js]
    # Final rms envelope width and angles 
    fout.write("   "+ii+": \n")
    fout.write("     sqrt(<x^2>) = %s mm, d sqrt(<x^2>)/ds = %s mr \n"%(rmsx/mm,drmsxds/mr))     
  #
  fout.close() 


# Print out timing statistics of run 
printtimers() 

# Make sure that last plot is flushed from buffer
fma() 

