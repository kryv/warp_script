from warp import *

filename = "frib-rms.dat"
fout = open(filename, "w")
fout.write(" zbeam_pos       all_xrms        all_yrms        U33_xrms        U33_yrms        U34_xrms        U34_yrms\n")
for index in range(0,top.jhist+1):
 fout.write("%15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e\n" %\
           (top.hzbeam[index], top.hxrms[0,index,-1],           top.hyrms[0,index,-1],\
                               top.hxrms[0,index,sp['U33'].js], top.hyrms[0,index,sp['U33'].js],\
                               top.hxrms[0,index,sp['U34'].js], top.hyrms[0,index,sp['U34'].js]))
fout.close()

filename = "frib-remt.dat"
fout = open(filename, "w")
fout.write(" zbeam_pos       all_nremt       U33_nremt       U34_nremt       all_rrms        U33_rrms        U34_rrms\n")
for index in range(0,top.jhist+1):
 fout.write("%15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e\n" %\
           (top.hzbeam[index], top.hepsnr[0,index,-1], top.hepsnr[0,index,sp['U33'].js], top.hepsnr[0,index,sp['U34'].js],\
                               top.hrrms[0,index,-1],  top.hrrms[0,index,sp['U33'].js],  top.hrrms[0,index,sp['U34'].js]))
fout.close()

filename = "frib-ncam.dat"
fout = open(filename, "w")
fout.write(" zbeam_pos       all_ncam        U33_ncam        U34_ncam        all_Lra         U33_Lra         U34_Lra\n")
for index in range(0,top.jhist+1):
 fout.write("%15.8e %15.8e %15.8e %15.8e %15.8e %15.8e %15.8e\n" %\
           (top.hzbeam[index], sum(hl_pthn_bar[index,:]), hl_pthn_bar[index,sp['U33'].js], hl_pthn_bar[index,sp['U34'].js],\
                               average(hl_lang[index,:]), hl_lang[index,sp['U33'].js],     hl_lang[index,sp['U34'].js]))
fout.close()
