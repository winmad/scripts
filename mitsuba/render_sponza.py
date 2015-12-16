import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"
args = " -o sponza\\sponza_lightcuts.pfm sponza\\sponza.xml"
print cmd + args
os.system(cmd + args)
