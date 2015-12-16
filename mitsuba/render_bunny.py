import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"

scales = [2, 4] #[2, 4]
sample_count = 256

for i in range(len(scales)):
	scale_density = scales[i]
	scale_phase = scales[i]
	args_density = " -Ddensity=bunny\\density\\density_" + str(scale_density) + "x.vol"
	args_s1 = " -Ds1vol=bunny\\phase\\s1_1x.vol"
	args_s2 = " -Ds2vol=bunny\\phase\\s2_1x.vol"
	args_sample_count = " -DsampleCount=" + str(sample_count)
	args = args_density + args_s1 + args_s2 + args_sample_count
	args += " -p 11 -o "
	filename = "bunny\\bunny_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x.pfm"
	args += filename
	args += " bunny\\bunny.xml"
	print cmd + args
	os.system(cmd + args)