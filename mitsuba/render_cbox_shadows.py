import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"
args = " -o cbox\\cbox_shadows_gi_lightcuts.ppm cbox\\cbox_shadows.xml"
print cmd + args
os.system(cmd + args)
