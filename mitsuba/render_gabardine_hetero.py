import sys, os

cmd = "mitsuba -s servers9.txt"

scales = [1]
sample_count = 128
fov = 4

for i in range(len(scales)):
    scale_density = scales[i]
    scale_phase = scales[i]
    scale_albedo = scales[i]
    args_fov = " -Dfov=" + str(fov)
    args_density = " -Ddensity=density/density_" + str(scale_density) + "x.vol"
    args_s1 = " -Ds1vol=phase/s1_" + str(scale_phase) + "x.vol"
    args_s2 = " -Ds2vol=phase/s2_" + str(scale_phase) + "x.vol"
    args_sample_count = " -DsampleCount=" + str(sample_count)
    args_albedo = " -Dalbedo=albedo/albedo_" + str(scale_albedo) + "x_zero.vol"
    args = args_fov + args_density + args_s1 + args_s2 + args_sample_count + args_albedo
    args += " -o "
    filename = "results/hetero_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x.pfm"
    args += filename
    scene_filename = "hetero_iso_phase.xml"
    args += " " + scene_filename
    print cmd + args
    os.system(cmd + args)

