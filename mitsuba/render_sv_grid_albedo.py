import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"

fovs = [1] #[15, 8, 4, 2, 1, 0.4]
scales = [1, 2, 4] #[2, 4]
#parts = [0, 1, 2, 3]
sample_count = 16
max_iter = 1

for i in range(len(fovs)): #[15, 8, 4, 2, 1, 0.4]:
	for j in range(len(scales)):
		fov = fovs[i]
		scale_phase = scales[j]
		scale_density = scales[j]
		ref_filename = "gabardine\\albedo_sv_search\\ref_albedo_by_orientation\\fov_" + str(fovs[i]) + "_spp_" + str(sample_count) + "_scale_" + str(scale_phase) + "x_albedo_1x.pfm"
		args_sample_count = " -DsampleCount=" + str(sample_count)
		args_scale_phase = " -Ds1vol=gabardine\\stddev_0.05\\s1_" + str(scale_phase) + "x.vol"
		args_scale_phase += " -Ds2vol=gabardine\\stddev_0.05\\s2_" + str(scale_phase) + "x.vol"
		args_scale_density = " -Ddensity=gabardine\\density_" + str(scale_density) + "x.vol"
		args_1x_density = " -Ddensity=gabardine\\density_1x.vol"
		#args_scale_albedo = " -Dalbedo=gabardine\\albedo_sv\\albedo_fov_" + str(fovs[i]) + "_scale_" + str(scale_phase) + "x.vol"
		
		args_fov = " -Dfov=" + str(fov)
		
		for iter in range(max_iter):
			#r = (r_l + r_r) * 0.5
			#g = (g_l + g_r) * 0.5
			#b = (b_l + b_r) * 0.5
			r = 0.95; g = 0.1; b = 0.1;
			if (iter == 0):
				"""
				if (scales[j] == 1):
					continue
				args_scale_albedo = " -Dalbedo=gabardine\\albedo_by_orientation\\albedo_1x.vol"
				args = args_sample_count + args_scale_phase + args_scale_density + args_scale_albedo + args_fov
				args += " -p 11 -o "
				args += ref_filename
				args += " gabardine\\gabardine_tiled_albedo_sv_grid.xml"
				print cmd + args
				os.system(cmd + args)
			else:
				"""
				args_albedo = " -Dalbedo=gabardine\\albedo_sv_original\\albedo_" + str(scale_phase) + "x.vol"
				args_albedo_scale = " -Dsr=1 -Dsg=1 -Dsb=1"
				"""
				if scales[j] == 2:
					args_albedo_scale = " -Dsr=1.00247 -Dsg=0.989 -Dsb=1.008888"
				else:
					args_albedo_scale = " -Dsr=0.9784 -Dsg=0.95336 -Dsb=0.98881"
				"""
				args = args_sample_count + args_scale_density + args_albedo + args_albedo_scale + args_fov
				#args = args_sample_count + args_1x_density + args_scale_albedo + args_fov
				args += " -p 11 -o "
				ref_filename = "gabardine\\albedo_sv_search\\ref_albedo_original\\fov_" + str(fovs[i]) + "_spp_" + str(sample_count) + "_scale_" + str(scale_phase) + "x_iso_phase.pfm"
				args += ref_filename
				args += " gabardine\\gabardine_tiled_scale_sv_albedo_iso_phase.xml"
				print cmd + args
				os.system(cmd + args)