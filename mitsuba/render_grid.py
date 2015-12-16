import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"
args = " -o grid\\grid.pfm grid\\grid.xml"
print cmd + args
os.system(cmd + args)
