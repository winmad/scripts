import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"
args = " -o gabardine\\glossy_fov_0_4_S_1x.pfm gabardine\\gabardine_tiled.xml"
#args = " -o gabardine\\aniso_full_SGGX_S_1x.pfm gabardine\\gabardine.xml"
#args = " -o gabardine\\aniso_SGGX.pfm gabardine\\gabardine_1block_ref.xml"
print cmd + args
os.system(cmd + args)
