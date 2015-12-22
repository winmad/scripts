import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"

scales = [2, 4] #[2, 4]
sample_count = 1024

for i in range(len(scales)):
	scale_density = scales[i]
	scale_phase = scales[i]
	args_density = " -Ddensity=bunny\\density\\density_" + str(scale_density) + "x.vol"
	args_s1 = " -Ds1vol=bunny\\phase\\s1_" + str(scale_phase) + "x.vol"
	args_s2 = " -Ds2vol=bunny\\phase\\s2_" + str(scale_phase) + "x.vol"
	args_sample_count = " -DsampleCount=" + str(sample_count)
	#args_albedo = " -Dr=0.95 -Dg=0.64 -Db=0.37"
	"""
	if scales[i] == 2:
		args_albedo = " -Dr=0.943154 -Dg=0.590921 -Db=0.297113"
	else:
		args_albedo = " -Dr=0.936426 -Dg=0.534421 -Db=0.210386"
	"""
	if scales[i] == 2:
		args_albedo = " -Dr=0.943150 -Dg=0.591066 -Db=0.297563"
	else:
		args_albedo = " -Dr=0.936523 -Dg=0.535132 -Db=0.211719"
	args_light = " -Dlight=lights\\campus.exr"
	args = args_density + args_s1 + args_s2 + args_sample_count + args_albedo + args_light
	args += " -p 11 -o "
	filename = "bunny\\bunny_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x.pfm"
	args += filename
	args += " bunny\\bunny_search_albedo_env_light.xml"
	print cmd + args
	os.system(cmd + args)