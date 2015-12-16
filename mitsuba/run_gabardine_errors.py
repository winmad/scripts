import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mtsutil cmp"

for fov in [0.4, 1, 2, 4, 8, 15]:
	for scale in [1, 2, 4]:
		for sample_count in [1, 4, 16]:
			args_result = " gabardine\\glossy_0.05_area_light_better\\fov_" + str(fov) + "_spp_" + str(sample_count) + "_" + str(scale) + "x.pfm"
			args_reference = " gabardine\\glossy_0.05_area_light_better\\fov_" + str(fov) + "_spp_64_1x.pfm"
			args = args_result + args_reference + " 0"
			#print cmd + args
			#print "fov_" + str(fov) + "_spp_" + str(sample_count) + "_" + str(scale) + "x"
			os.system(cmd + args)

