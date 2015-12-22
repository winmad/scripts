import sys
import os

cmd = "mitsuba -s servers.txt"

scales = [1] #[2, 4]
sample_count = 1024

for i in range(len(scales)):
	for j in range(6):
		for k in range(4):
			view = j
			light = k
			scale_density = scales[i]
			scale_phase = scales[i]
			args_density = " -Ddensity=density/density_" + str(scale_density) + "x.vol"
			args_s1 = " -Ds1vol=phase/s1_" + str(scale_phase) + "x.vol"
			args_s2 = " -Ds2vol=phase/s2_" + str(scale_phase) + "x.vol"
			args_sample_count = " -DsampleCount=" + str(sample_count)
			args_light = " -Dlight=basis_sh_" + str(light) + ".exr"
			args_albedo = " -Dr=0.95 -Dg=0.64 -Db=0.37"
			args = args_density + args_s1 + args_s2 + args_sample_count + args_albedo + args_light
			args += " -o "
			filename = "results/ref/bunny_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_view_" + str(view) + "_sh_" + str(light) + ".pfm"
			args += filename
			args += " bunny_view_" + str(view) + "_env.xml"
			print cmd + args
			os.system(cmd + args)
