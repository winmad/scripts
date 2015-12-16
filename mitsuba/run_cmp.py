import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mtsutil "
args = "cmp "
args += "gabardine\\glossy_0.05_area_light_better\\fov_2_spp_4_4x.pfm "
args += "gabardine\\glossy_0.05_area_light_better\\fov_2_spp_64_1x.pfm "
args += "0"

print cmd + args
os.system(cmd + args)
