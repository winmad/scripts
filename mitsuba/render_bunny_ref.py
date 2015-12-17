import sys
import os

cmd = "mitsuba -s servers.txt"

scales = [1] #[2, 4]
sample_count = 512

for i in range(len(scales)):
	for j in range(6):
		view = j
		scale_density = scales[i]
		scale_phase = scales[i]
		args_density = " -Ddensity=density/density_" + str(scale_density) + "x.vol"
		args_s1 = " -Ds1vol=phase/s1_1x.vol"
		args_s2 = " -Ds2vol=phase/s2_1x.vol"
		args_sample_count = " -DsampleCount=" + str(sample_count)
		args_albedo = " -Dr=0.95 -Dg=0.64 -Db=0.37"
		args = args_density + args_s1 + args_s2 + args_sample_count + args_albedo
		args += " -o "
		filename = "results/ref/bunny_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_view_" + str(view) + ".pfm"
		args += filename
		args += " bunny_view_" + str(view) + ".xml"
		print cmd + args
		os.system(cmd + args)
