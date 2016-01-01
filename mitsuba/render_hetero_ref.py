import sys
import os

#cmd = "mitsuba -s servers.txt"
cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"

scales = [1] #[2, 4]
sample_count = 1024
fov = 1

for i in range(len(scales)):
    for j in range(2):
        for k in range(4):
            view = j
            light = k
            scale_density = scales[i]
            scale_phase = scales[i]
            args_density = " -Ddensity=density/density_" + str(scale_density) + "x.vol"
            args_s1 = " -Ds1vol=phase/s1_" + str(scale_phase) + "x.vol"
            args_s2 = " -Ds2vol=phase/s2_" + str(scale_phase) + "x.vol"
            args_sample_count = " -DsampleCount=" + str(sample_count)
            args_light = " -Dlight=basis_sh_" + str(light) + ".exr"
            args_albedo = " -Dalbedo=albedo/albedo_" + str(scales[i]) + "x.vol"
            args_segmentation = " -Dsegmentation=albedo/segment_" + str(scales[i]) + "x.vol"
            args_fov = " -Dfov=" + str(fov)

            args_clusters = " -DnumClusters=2"
            args_albedo_scale = ""
            for c in range(2):
                args_albedo_scale += " -Dsr" + str(c) + "=1.0 -Dsg" + str(c) + "=1.0 -Dsb" + str(c) + "=1.0"

            args = args_density + args_s1 + args_s2 + args_sample_count + args_light + args_fov
            args += args_albedo_scale + args_clusters + args_albedo + args_segmentation
            args += " -b 20"
            args += " -o "
            filename = "results/ref/hetero_fov_" + str(fov) + "_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_view_" + str(view) + "_sh_" + str(light) + ".pfm"
            args += filename
            args += " hetero_iso_view_" + str(view) + "_ref.xml"
            print cmd + args
            os.system(cmd + args)