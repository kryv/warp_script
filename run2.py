import os
import sys

for i in range(50,96,5):
 fname = "result-WB-s4nl-neut0"+str(i)
 os.system("python frib-front-xy_l1.py -l " + str(i) + " > log")
 os.system("python frib-front-xy_b2.py -l " + str(i) + " > log")
 os.system("mkdir "+ fname)
 os.system("mv *.pkl *.dat *cgm* *.mp4 "+ fname)
 