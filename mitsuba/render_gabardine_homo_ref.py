import sys, os

#cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"
cmd = "mitsuba -s servers.txt"

scales = [1]
sample_count = 2048
fovs = [4, 1]
lights = ["basis_sh_0.exr", "basis_sh_1.exr", "basis_sh_2.exr", "basis_sh_3.exr"]
max_views = 2

for i in range(len(scales)):
    scale_density = scales[i]
    scale_phase = scales[i]
    scale_albedo = scales[i]
    
    args_density = " -Ddensity=density/density_" + str(scale_density) + "x.vol"
    args_s1 = " -Ds1vol=phase/s1_" + str(scale_phase) + "x.vol"
    args_s2 = " -Ds2vol=phase/s2_" + str(scale_phase) + "x.vol"
    args_sample_count = " -DsampleCount=" + str(sample_count)
    args_albedo = " -Dr=0.95 -Dg=0.1 -Db=0.1"
    
    for fov in fovs:
        args_fov = " -Dfov=" + str(fov)
        for j in range(max_views):
            for k in range(len(lights)):
                light = lights[k]
                args_light = " -Dlight=" + light
                args = args_fov + args_density + args_s1 + args_s2 + args_sample_count + args_albedo + args_light
                args += " -o "
                filename = "results/ref/homo_fov_" + str(fov) + "_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_view_" + str(j) + "_sh_" + str(k) + ".pfm"
                args += filename
                scene_filename = "homo_sggx_view_" + str(j) + ".xml"
                args += " " + scene_filename
                print cmd + args
                os.system(cmd + args)

