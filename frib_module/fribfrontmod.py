"""
Python module and input script for a Warp simulation (2D/3D) of
the FRIB front end. For help and/or additional information contact:

    Kei Fukushima       k.fksm.ryv@gmail.com

For documentation see the Warp web-site:

     https://warp.lbl.gov

All code inputs are mks with the exception of particle kinetic energy (eV).   

"""

# Load Warp package
from warp import *

# Set informational labels included on all output cgm plots.   
top.pline2   = "xy Slice Simulation: FRIB Front End" 
top.pline1   = " "   # Add more info, if desired.

# Invoke setup routine for graphics and output files (THIS IS MANDATORY)
setup()

# Set runmaker - included in informational labels on output plots
top.runmaker = "KFukushima"

class BeamSpec:
    """
    Beam Specification Informations 
    type            : particle species
    charge_state    : charge state of the particle
    current         : current of the beam [A]
    group           : group of the beam
    """
    def __init__(self, type, charge_state, current):
        self.type = type
        self.charge_state = charge_state
        self.current = current

class Beams(BeamSpec):
    """
    Loading Beam Handling
    new             : add new beam
    set             : set initial statistic of the beam
    setall          : set initial statistic of the beam for all beams
    """
    def __init__(self):
        pass
        
    def new(self):
        pass
        
    def set(self):
        pass
        
    def setall(self):
        pass

"""        
# Input example      
mr = 0.001    # milli radian
mA = 0.001    # milli ampere
        
Beams.new(type=Uranium, charge_state=33, current=0.210*mA, group='target')
Beams.new(type=Uranium, charge_state=34, current=0.205*mA, group='target')

Beams.new(type=Uranium, charge_state=25, current=0.051*mA, group='others')
Beams.new(type=Uranium, charge_state=26, current=0.068*mA, group='others')
Beams.new(type=Uranium, charge_state=27, current=0.088*mA, group='others')
Beams.new(type=Uranium, charge_state=28, current=0.115*mA, group='others')
.
.
.

Beams.setall(alpha_x = 0.0, alpha_y = 0.0,
             beta_x = 12.9*cm, beta_y = 12.9*cm,
             emitn_edge = 0.4*mm*mr, Et_therm = 3.0,
             SourceBias = 35.0*keV)
"""
             
class LatticeElem:
    """
    Set up Lattice Elements
    solenoid            : 
    accel_gap           : 
    ecr_field           :
    bend                :
    """
    def __init__(self):
        pass
        
    def solenoid(self):
        pass
        
    def accel_gap(self):
        pass
        
    def ecr_field(self):
        pass
        
    def bend(self):
        pass
             
             
class PICspec:
    """
    Set up PIC code Specification
    - grid size etc.
    
    """
    def __init__(self):
             
             
             
             
             
             
             
             
             
             
             
