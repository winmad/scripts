import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"

scales = [1, 2, 4] #[2, 4]
sample_count = 1024

for i in range(len(scales)):
	scale_density = scales[i]
	scale_phase = scales[i]
	args_density = " -Ddensity=bunny\\density\\density_" + str(scale_density) + "x.vol"
	args_s1 = " -Ds1vol=bunny\\phase\\s1_" + str(scale_phase) + "x.vol"
	args_s2 = " -Ds2vol=bunny\\phase\\s2_" + str(scale_phase) + "x.vol"
	args_sample_count = " -DsampleCount=" + str(sample_count)
	args_albedo = " -Dr=0.95 -Dg=0.64 -Db=0.37"
	#args_albedo = " -Dr=0.943154 -Dg=0.590921 -Db=0.297113"
	#args_albedo = " -Dr=0.936426 -Dg=0.534421 -Db=0.210386"
	args = args_density + args_s1 + args_s2 + args_sample_count + args_albedo
	args += " -p 11 -o "
	filename = "bunny\\bunny_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_original_albedo.pfm"
	args += filename
	args += " bunny\\bunny_search_albedo_env_light.xml"
	print cmd + args
	os.system(cmd + args)