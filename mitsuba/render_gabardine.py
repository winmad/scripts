import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"

for fov in [0.4, 1, 2, 4, 8, 15]:
	for scale_phase in [2, 4]:#[1, 2, 4]:
		#for scale_density in [1]:#[1, 2, 4]:
			for sample_count in [256]:#[1, 4, 16]:
				scale_density = scale_phase
				args_sample_count = " -DsampleCount=" + str(sample_count)
				args_scale_phase = " -Ds1vol=gabardine\\stddev_0.05\\s1_" + str(scale_phase) + "x.vol"
				args_scale_phase += " -Ds2vol=gabardine\\stddev_0.05\\s2_" + str(scale_phase) + "x.vol"
				args_scale_density = " -Ddensity=gabardine\\density_" + str(scale_density) + "x.vol"
				args_fov = " -Dfov=" + str(fov)
				args = args_sample_count + args_scale_phase + args_scale_density + args_fov
				args += " -p 11 -o gabardine\\glossy_0.05_area_light_scaled_phase_density\\fov_" + str(fov)
				args += "_spp_" + str(sample_count) + "_phase_" + str(scale_phase) + "x_density_" + str(scale_density) + "x.pfm"
				args += " gabardine\\gabardine_tiled_params.xml"
				print cmd + args
				os.system(cmd + args)

