import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mtsutil"

#args = " microflake2SGGX 0 1 2 10 0.3"

# args = " microflake2SGGX 1 gabardine\\gabardine_dir_supertile.vol 0.05 "
# args += "gabardine\\stddev_0.05\\s1_1x.vol gabardine\\stddev_0.05\\s2_1x.vol"

# args = " microflake2SGGX 2 scarf\\data\\volume_description.vol 0.3 "
# args += "scarf\\data\\volume_ -orientation.vol -s1.vol -s2.vol"

args = " microflake2SGGX 1 bunny_10k\\phase\\bunny10k_thin_dir.vol 0.3 "
args += "bunny_10k\\phase\\s1_1x.vol bunny_10k\\phase\\s2_1x.vol"

print cmd + args
os.system(cmd + args)
