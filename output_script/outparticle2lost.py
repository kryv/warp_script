from warp import *


fo = PWpickle.PW("lostpart2_"+str(top.it)+".pkl")

fo.tlos = [0.0]*3

fo.xlos = [0.0]*3
fo.uxlos = [0.0]*3

fo.ylos = [0.0]*3
fo.uylos = [0.0]*3

fo.zlos = [0.0]*3
fo.uzlos = [0.0]*3

fo.exlos = [0.0]*3
fo.eylos = [0.0]*3
fo.ezlos = [0.0]*3

for ncn,ii in enumerate(['U32','U33','U34']):
 if len(sp[ii].xplost) != 0:
  fo.tlos[ncn] = sp[ii].tplost
  fo.xlos[ncn] = sp[ii].xplost
  fo.uxlos[ncn] = sp[ii].uxplost
  fo.ylos[ncn] = sp[ii].yplost
  fo.uylos[ncn] = sp[ii].uyplost
  fo.zlos[ncn] = sp[ii].zplost
  fo.uzlos[ncn] = sp[ii].uzplost
  fo.exlos[ncn] = sp[ii].exlost
  fo.eylos[ncn] = sp[ii].eylost
  fo.ezlos[ncn] = sp[ii].ezlost 
 
fo.close()