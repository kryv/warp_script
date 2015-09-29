# warp_script


|**Directories** | |
|:-----------|:-------------|
| frib\_module                  | Developing scripts for the Warp FRIB front end simulations.  |
| matplotlib\_anim\_wrapper     | Scripts for making movies by matplotlib packages.  |
| movies                        | Sample movie and script of the FRIB front end (bending section). | 
| output\_script                | Scripts for taking output data from the Warp simulation script.  |
| previous\_versions            | Previous version of the Warp simulation script.  |



## Files

- anm_plot.py
  - Movie making script for the Warp simulation in the straight section of the FRIB front end
(Not rely on matplotlib_anim_wrapper type)

- anm_plot_bnd.py  
  - Movie making script for the Warp simulation in the bending section of the FRIB front end 
(Not rely on matplotlib_anim_wrapper type)

- b2-meth.py
  - Root finding script by the Warp simulation result and Broyden method

- frib-front-3d.py
  - 3D Warp simulation script (grid data of the lattice elements and initial particle distributions are required)

- frib-front-xy_to3d.py
  - 2D Warp simulation script (grid data of the lattice elements is required)
