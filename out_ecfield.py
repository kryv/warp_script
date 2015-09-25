from warp import *

fo = PWpickle.PW("ecfield_"+str(top.it)+".pkl")

fo.xi = 0.25*w3d.xmmin
fo.xf = 0.25*w3d.xmmax
fo.yi = w3d.ymmin
fo.yf = w3d.ymmax
fo.zi = z_launch-5.0*cm
fo.zf = w3d.zmmax

fo.ex = child1.getselfe()[0]
fo.ey = child1.getselfe()[1]
fo.ez = child1.getselfe()[2]
 
fo.close()