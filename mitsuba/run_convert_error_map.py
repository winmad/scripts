import sys
import os

cmd = "D:\\Lifan\\HDRITools-0.3.0\\bin\\batchToneMapper"
args = " -e 0 --srgb -f png D:\\Lifan\\mitsuba\\scenes\\bunny\\albedo_search\\*.pfm"

print cmd + args
os.system(cmd + args)