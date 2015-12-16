import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mtsutil splitGridVolume"

scales = [1, 2, 4]

for i in range(len(scales)):
	scale = scales[i]
	density_filename = "gabardine\\density_" + str(scale) + "x.vol"
	s1_filename = "gabardine\\stddev_0.05\\s1_" + str(scale) + "x.vol"
	s2_filename = "gabardine\\stddev_0.05\\s2_" + str(scale) + "x.vol"
	density_output_filename = "gabardine\\density_splitted\\density_" + str(scale) + "x"
	s1_output_filename = "gabardine\\sggx_0.05_splitted\\s1_" + str(scale) + "x"
	s2_output_filename = "gabardine\\sggx_0.05_splitted\\s2_" + str(scale) + "x"
	args = " " + s2_filename + " " + s2_output_filename
	os.system(cmd + args)