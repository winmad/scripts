import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"

fovs = [4] #[15, 8, 4, 2, 1, 0.4]
scales = [1] #[2, 4]
parts = [0, 1, 2, 3]
sample_count = 256
max_iter = 1

for i in range(len(fovs)): #[15, 8, 4, 2, 1, 0.4]:
	
	#ref_filename = "gabardine\\ref_constant\\fov_" + str(fovs[i]) + "_1x.pfm"
	for j in range(len(parts)):
		fov = fovs[i]
		split_part = parts[j]
		scale_phase = 1
		scale_density = 1
		ref_filename = "gabardine\\albedo_sv_search\\ref_area\\fov_" + str(fovs[i]) + "_spp_256_scale_1x_" + str(split_part) + ".pfm"
		args_sample_count = " -DsampleCount=" + str(sample_count)
		args_scale_phase = " -Ds1vol=gabardine\\sggx_0.05_splitted\\s1_" + str(scale_phase) + "x_" + str(split_part) + ".vol"
		args_scale_phase += " -Ds2vol=gabardine\\sggx_0.05_splitted\\s2_" + str(scale_phase) + "x_" + str(split_part) + ".vol"
		args_scale_density = " -Ddensity=gabardine\\density_splitted\\density_" + str(scale_density) + "x_" + str(split_part) + ".vol"
		args_fov = " -Dfov=" + str(fov)
		
		for iter in range(max_iter):
			#r = (r_l + r_r) * 0.5
			#g = (g_l + g_r) * 0.5
			#b = (b_l + b_r) * 0.5
			r = 0.95; g = 0.1; b = 0.1;
			args = args_sample_count + args_scale_phase + args_scale_density + args_fov
			args_albedo = " -Dr=" + str(r) + " -Dg=" + str(g) + " -Db=" + str(b)
			args += args_albedo

			args += " -p 11 -o "
			filename = "gabardine\\albedo_sv_search\\fov_" + str(fov)
			filename += "_spp_" + str(sample_count) + "_scale_" + str(scale_density) + "x_" + str(split_part) + ".pfm"
			#args += filename
			args += ref_filename
			args += " gabardine\\gabardine_tiled_albedo_sv.xml"
			print cmd + args
			os.system(cmd + args)
		





