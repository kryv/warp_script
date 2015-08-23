from warp import *

for ls in sp_target :
 filename = ls+"_bnd.dat"
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

 
#------- output xbar ------- 
filename = "xbar.dat"
fout = open(filename, "a") 
fout.write(" zbeam_pos       ")
for i in sort(sp.keys()):
 if len(i) == 2:
  fout.write(i+"              ")
 if len(i) == 3:
  fout.write(i+"             ")
fout.write("\n")

for index in range(0,top.jhist+1):
 fout.write("%15.8e "%(top.hzbeam[index]))
 for i in sort(sp.keys()):
  fout.write("%15.8e "%(sp[i].hxbar[0,index]))
 fout.write("\n") 
fout.close()
 
#------- output xrms -------
filename = "xrms.dat"
fout = open(filename, "a") 
fout.write(" zbeam_pos       ")
for i in sort(sp.keys()):
 if len(i) == 2:
  fout.write(i+"              ")
 if len(i) == 3:
  fout.write(i+"             ")
fout.write("\n")

for index in range(0,top.jhist+1):
 fout.write("%15.8e "%(top.hzbeam[index]))
 for i in sort(sp.keys()):
  fout.write("%15.8e "%(sp[i].hxrms[0,index]))
 fout.write("\n")  
fout.close()
 
#------- output yrms -------
filename = "yrms.dat"
fout = open(filename, "a") 
fout.write(" zbeam_pos       ")
for i in sort(sp.keys()):
 if len(i) == 2:
  fout.write(i+"              ")
 if len(i) == 3:
  fout.write(i+"             ")
fout.write("\n")

for index in range(0,top.jhist+1):
 fout.write("%15.8e "%(top.hzbeam[index]))
 for i in sort(sp.keys()):
  fout.write("%15.8e "%(sp[i].hyrms[0,index]))
 fout.write("\n")  
fout.close()
 
#------- output rrms -------
filename = "rrms.dat"
fout = open(filename, "a") 
fout.write(" zbeam_pos       ")
for i in sort(sp.keys()):
 if len(i) == 2:
  fout.write(i+"              ")
 if len(i) == 3:
  fout.write(i+"             ")
fout.write("\n")

for index in range(0,top.jhist+1):
 fout.write("%15.8e "%(top.hzbeam[index]))
 for i in sort(sp.keys()):
  fout.write("%15.8e "%(sp[i].hrrms[0,index]))
 fout.write("\n")  
fout.close()
 
 
#------- output xemt -------
filename = "xemt.dat"
fout = open(filename, "a") 
fout.write(" zbeam_pos       ")
for i in sort(sp.keys()):
 if len(i) == 2:
  fout.write(i+"              ")
 if len(i) == 3:
  fout.write(i+"             ")
fout.write("\n")

for index in range(0,top.jhist+1):
 fout.write("%15.8e "%(top.hzbeam[index]))
 for i in sort(sp.keys()):
  fout.write("%15.8e "%(sp[i].hepsx[0,index]))
 fout.write("\n")  
fout.close()
 
#------- output yemt -------
filename = "yemt.dat"
fout = open(filename, "a") 
fout.write(" zbeam_pos       ")
for i in sort(sp.keys()):
 if len(i) == 2:
  fout.write(i+"              ")
 if len(i) == 3:
  fout.write(i+"             ")
fout.write("\n")

for index in range(0,top.jhist+1):
 fout.write("%15.8e "%(top.hzbeam[index]))
 for i in sort(sp.keys()):
  fout.write("%15.8e "%(sp[i].hepsy[0,index]))
 fout.write("\n")  
fout.close()

#------- output nremt -------
filename = "nremt.dat"
fout = open(filename, "a") 
fout.write(" zbeam_pos       ")
for i in sort(sp.keys()):
 if len(i) == 2:
  fout.write(i+"              ")
 if len(i) == 3:
  fout.write(i+"             ")
fout.write("\n")

for index in range(0,top.jhist+1):
 fout.write("%15.8e "%(top.hzbeam[index]))
 for i in sort(sp.keys()):
  fout.write("%15.8e "%(sp[i].hepsnr[0,index]))
 fout.write("\n")  
fout.close()
 
