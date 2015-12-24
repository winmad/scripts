import sys
import os

cmd = "mitsuba -c node001"

scales = [1] #[2, 4]
sample_count = 64

for i in range(len(scales)):
	scale_density = scales[i]
	scale_phase = scales[i]
	args_density = " -Ddensity=density/density_" + str(scale_density) + "x.vol"
	args_s1 = " -Ds1vol=phase/s1_" + str(scale_phase) + "x.vol"
	args_s2 = " -Ds2vol=phase/s2_" + str(scale_phase) + "x.vol"
	args_sample_count = " -DsampleCount=" + str(sample_count)
	args_light = " -Dlight=campus.exr"
	args_albedo = " -Dr=0.95 -Dg=0.64 -Db=0.37"
	#args_albedo = " -Dr=0.96 -Dg=0.65 -Db=0.38"
	#args_albedo = " -Dr=0.943154 -Dg=0.590921 -Db=0.297113"
	#args_albedo = " -Dr=0.936426 -Dg=0.534421 -Db=0.210386"
	args = args_density + args_s1 + args_s2 + args_sample_count + args_albedo + args_light
	args += " -b 40 -o "
	filename = "bunny_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_a0.pfm"
	args += filename
	args += " bunny_diff_env_light.xml"
	print cmd + args
	os.system(cmd + args)
