from warp import *


fo = PWpickle.PW("allpart"+str(top.it)+".pkl")

fo.allspx = []
fo.allspy = []
fo.allspz = []
fo.allspvx = []
fo.allspvy = []
fo.allspvz = []
fo.allspw = []
fo.allspsw = []
for ii in sort(sp.keys()):
 fo.allspx.append(sp[ii].getx())
 fo.allspy.append(sp[ii].gety())
 fo.allspz.append(sp[ii].getz())
 fo.allspvx.append(sp[ii].getvx())
 fo.allspvy.append(sp[ii].getvy())
 fo.allspvz.append(sp[ii].getvz())
 fo.allspw.append(sp[ii].getw())
 fo.allspsw.append(sp[ii].sw)
fo.close()