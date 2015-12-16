import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mtsutil"
# args = " downSampleVolume 0 gabardine\\gabardine_s2_supertile.vol 2 2 2 gabardine\\gabardine_s2_supertile_2x.vol"

# args = " downSampleVolume 0 gabardine\\density_1x.vol 4 4 4 gabardine\\density_4x.vol"

# args = " downSampleVolume 0 gabardine\\albedo_by_orientation\\albedo_1x.vol 2 2 2 gabardine\\albedo_by_orientation\\albedo_2x.vol"

# args = " downSampleVolume 1 scarf\\data\\volume_description.vol 4 4 4 "
# args += "scarf\\data\\volume_ -s1.vol -s1_4x.vol"

# args = " downSampleVolume 1 scarf\\data\\volume_description.vol 4 4 4 "
# args += "scarf\\data\\volume_ -s2.vol -s2_4x.vol"

# args = " downSampleVolume 0 bunny\\density\\density_1x.vol 4 4 4 bunny\\density\\density_4x.vol"
# args = " downSampleVolume 0 bunny_10k\\density\\density_1x.vol 4 4 4 bunny_10k\\density\\density_4x.vol"

args = " downSampleVolume 0 gabardine\\albedo_sv_original\\albedo_1x.vol 4 4 4 gabardine\\albedo_sv_original\\albedo_4x.vol"

print cmd + args
os.system(cmd + args)
