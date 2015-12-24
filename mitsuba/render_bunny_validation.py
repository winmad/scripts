import sys
import os

cmd = "mitsuba -s servers.txt"

scales = [2, 4] #[2, 4]
sample_count = 1024
light = "campus.exr"

for i in range(len(scales)):
	scale_density = scales[i]
	scale_phase = scales[i]
	args_density = " -Ddensity=density/density_" + str(scale_density) + "x.vol"
	args_s1 = " -Ds1vol=phase/s1_" + str(scale_phase) + "x.vol"
	args_s2 = " -Ds2vol=phase/s2_" + str(scale_phase) + "x.vol"
	args_sample_count = " -DsampleCount=" + str(sample_count)
	#args_albedo = " -Dr=0.95 -Dg=0.64 -Db=0.37"
	if scales[i] == 2:
		args_albedo = " -Dr=0.943175 -Dg=0.591277 -Db=0.298049"
	else:
		args_albedo = " -Dr=0.936571 -Dg=0.535716 -Db=0.213255"
	args_light = " -Dlight=" + light
	args = args_density + args_s1 + args_s2 + args_sample_count + args_albedo + args_light
	args += " -o "
	filename = "results/validation/bunny_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x.pfm"
	args += filename
	args += " bunny_search_albedo_env_light.xml"
	print cmd + args
	os.system(cmd + args)

scales = [1, 2, 4]
for i in range(len(scales)):
	scale_density = scales[i]
	scale_phase = scales[i]
	args_density = " -Ddensity=density/density_" + str(scale_density) + "x.vol"
	args_s1 = " -Ds1vol=phase/s1_" + str(scale_phase) + "x.vol"
	args_s2 = " -Ds2vol=phase/s2_" + str(scale_phase) + "x.vol"
	args_sample_count = " -DsampleCount=" + str(sample_count)
	args_albedo = " -Dr=0.95 -Dg=0.64 -Db=0.37"
	"""
	if scales[i] == 2:
		args_albedo = " -Dr=0.943154 -Dg=0.590921 -Db=0.297113"
	else:
		args_albedo = " -Dr=0.936426 -Dg=0.534421 -Db=0.210386"
	
	if scales[i] == 2:
		args_albedo = " -Dr=0.943175 -Dg=0.591277 -Db=0.298049"
	else:
		args_albedo = " -Dr=0.936571 -Dg=0.535716 -Db=0.213255"
	"""
	args_light = " -Dlight=" + light
	args = args_density + args_s1 + args_s2 + args_sample_count + args_albedo + args_light
	args += " -o "
	filename = "results/validation/bunny_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_original_albedo.pfm"
	args += filename
	args += " bunny_search_albedo_env_light.xml"
	print cmd + args
	os.system(cmd + args)
