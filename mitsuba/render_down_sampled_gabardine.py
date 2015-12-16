import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"

for fov in [2]: #[15, 8, 4, 2, 1, 0.4]:
	for scale_phase in [2]: #[2, 4]:
		for clamp_thr in [0.5]: #[0.05, 0.1, 0.3, 0.5]:
			for sample_count in [256]:#[1, 4, 16]:
				scale_density = scale_phase
				args_sample_count = " -DsampleCount=" + str(sample_count)
				args_scale_phase = " -Ds1vol=gabardine\\stddev_0.05\\s1_" + str(scale_phase) + "x.vol"
				args_scale_phase += " -Ds2vol=gabardine\\stddev_0.05\\s2_" + str(scale_phase) + "x.vol"
				args_scale_density = " -Ddensity=gabardine\\density\\density_" + str(scale_density) + "x_" + str(clamp_thr) + ".vol"
				args_fov = " -Dfov=" + str(fov)
				args = args_sample_count + args_scale_phase + args_scale_density + args_fov
				args += " -p 11 -o gabardine\\clamped_results\\fov_" + str(fov)
				args += "_spp_" + str(sample_count) + "_scale_" + str(scale_density) + "x_clamp_" + str(clamp_thr) + ".pfm"
				args += " gabardine\\gabardine_tiled_params.xml"
				print cmd + args
				os.system(cmd + args)

