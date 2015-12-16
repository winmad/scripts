import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"
args = " -o scarf\\scarf_SGGX_S_4x.pfm scarf\\scarf.xml"
print cmd + args
os.system(cmd + args)
