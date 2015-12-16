import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"

scales = [1] #[2, 4]
sample_count = 16

for i in range(len(scales)):
	scale_density = scales[i]
	scale_phase = scales[i]
	args_density = " -Ddensity=bunny_10k\\density\\density_" + str(scale_density) + "x.vol"
	args_s1 = " -Ds1vol=bunny_10k\\phase\\s1_1x.vol"
	args_s2 = " -Ds2vol=bunny_10k\\phase\\s2_1x.vol"
	args_sample_count = " -DsampleCount=" + str(sample_count)
	args = args_density + args_s1 + args_s2 + args_sample_count
	args += " -p 11 -o "
	filename = "bunny_10k\\bunny_10k_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x.pfm"
	args += filename
	args += " bunny_10k\\bunny_10k.xml"
	print cmd + args
	os.system(cmd + args)