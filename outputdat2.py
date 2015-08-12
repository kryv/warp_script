from warp import *

for ls in sp_target :
 filename = ls+".dat"
 fout = open(filename, "w")
 fout.write(" zbeam_pos       "+ls+"_vz_ave      "+ls+"_xrms        "+ls+"_yrms        "+ls+"_rrms        "+ls+"_remt        "+ls+"_nremt       "\
                               +ls+"_ncam        "+ls+"_cam         "+ls+"_pvemt       "+ls+"_npvemt      "+ls+"_krot        "\
                               +ls+"_lang\n")
 for index in range(0,top.jhist+1):
  fout.write("%15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e\n" %\
            (top.hzbeam[index], hl_vbeam[index,sp[ls].js], 
             top.hxrms[0,index,sp[ls].js], top.hyrms[0,index,sp[ls].js], top.hrrms[0,index,sp[ls].js],\
             top.hepsr[0,index,sp[ls].js], top.hepsnr[0,index,sp[ls].js],\
             hl_pthn_bar[index,sp[ls].js], hl_pth_bar[index,sp[ls].js],\
             hl_epspv[index,sp[ls].js],    hl_epspvn[index,sp[ls].js],
             hl_krot[index,sp[ls].js],     hl_lang[index,sp[ls].js]))
 fout.close()


ls = "All"
filename = ls+".dat"
fout = open(filename, "w")
fout.write(" zbeam_pos       "+ls+"_vz_ave      "+ls+"_xrms        "+ls+"_yrms        "+ls+"_rrms        "+ls+"_remt        "+ls+"_nremt       "\
                              +ls+"_ncam        "+ls+"_cam         "+ls+"_pvemt       "+ls+"_npvemt      "+ls+"_krot        "\
                              +ls+"_lang\n")
for index in range(0,top.jhist+1):
 tmp_pthn = tmp_pth = tmp_epspv = tmp_epspvn = tmp_krot = tmp_lang = []
 for ls in sp.keys():
  tmp_pthn.append(hl_pthn_bar[index,sp[ls].js])
  tmp_pth.append(hl_pth_bar[index,sp[ls].js])
  tmp_epspv.append(hl_epspv[index,sp[ls].js])
  tmp_epspvn.append(hl_epspvn[index,sp[ls].js])
  tmp_krot.append(hl_krot[index,sp[ls].js])
  tmp_lang.append(hl_lang[index,sp[ls].js])
 fout.write("%15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e\n" %\
            (top.hzbeam[index], hl_ave_vbeam[index], 
             top.hxrms[0,index,-1], top.hyrms[0,index,-1], top.hrrms[0,index,-1],\
             top.hepsr[0,index,-1], top.hepsnr[0,index,-1],\
             average(tmp_pthn),  average(tmp_pth),\
             average(tmp_epspv), average(tmp_epspvn),
             average(tmp_krot),  average(tmp_lang)))
fout.close()
