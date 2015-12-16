import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mtsutil clampVolume 0"

for thr in [0.05, 0.1, 0.3, 0.5]:
	for scale in [2, 4]:
		input_file = "gabardine\\density\\density_" + str(scale) + "x_" + str(0) + ".vol"
		output_file = "gabardine\\density\\density_" + str(scale) + "x_" + str(thr) + ".vol"
		args = " " + input_file + " " + str(thr) + " " + output_file
		print cmd + args
		os.system(cmd + args)