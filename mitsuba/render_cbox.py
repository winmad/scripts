import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"
args = " -o cbox\\cbox_lightcuts.pfm cbox\\cbox.xml"
print cmd + args
os.system(cmd + args)
