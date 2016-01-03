import sys
import os
import numpy as np
import re

'''
Load a PFM file into a Numpy array. Note that it will have
a shape of H x W, not W x H. Returns a tuple containing the
loaded image and the scale factor from the file.
'''
def load_pfm(file):
  color = None
  width = None
  height = None
  scale = None
  endian = None

  header = file.readline().rstrip()
  if header == 'PF':
    color = True    
  elif header == 'Pf':
    color = False
  else:
    raise Exception('Not a PFM file.')

  dim_match = re.match(r'^(\d+)\s(\d+)\s$', file.readline())
  if dim_match:
    width, height = map(int, dim_match.groups())
  else:
    raise Exception('Malformed PFM header.')

  scale = float(file.readline().rstrip())
  if scale < 0: # little-endian
    endian = '<'
    scale = -scale
  else:
    endian = '>' # big-endian

  data = np.fromfile(file, endian + 'f')
  shape = (height, width, 3) if color else (height, width)
  return np.reshape(data, shape)

'''
Save a Numpy array to a PFM file.
'''
def save_pfm(file, image, scale = 1):
  color = None

  if image.dtype.name != 'float32':
    raise Exception('Image dtype must be float32.')

  if len(image.shape) == 3 and image.shape[2] == 3: # color image
    color = True
  elif len(image.shape) == 2 or len(image.shape) == 3 and image.shape[2] == 1: # greyscale
    color = False
  else:
    raise Exception('Image must have H x W x 3, H x W x 1 or H x W dimensions.')

  file.write('PF\n' if color else 'Pf\n')
  file.write('%d %d\n' % (image.shape[1], image.shape[0]))

  endian = image.dtype.byteorder

  if endian == '<' or endian == '=' and sys.byteorder == 'little':
    scale = -scale

  file.write('%f\n' % scale)

  image.tofile(file)

#==============================================================
def calc_grad(LdA, L, L_ref):
    #intensity = np.zeros((3))
    #grad = np.zeros((3))
    #cnt = 0.0
    diff = L - L_ref
    intensity = np.mean(np.mean(diff, axis=0), axis=0)
    grad = np.mean(np.mean(LdA, axis=0), axis=0)
    """
    for i in range(LdA.shape[0]):
        for j in range(LdA.shape[1]):
            # only use volume part
            if (LdA[i][j][0] < 0.001):
                continue

            cnt += 1.0
            for c in range(3):
                intensity[c] += (L[i][j][c] - L_ref[i][j][c])
                grad[c] += LdA[i][j][c]
    """
    res = np.zeros((3))
    for c in range(3):
        #intensity[c] /= cnt
        #grad[c] /= cnt
        res[c] = 2 * intensity[c] * grad[c]
    return res

cmd = "mitsuba -s servers.txt"
#cmd = "mitsuba"

scales = [2]
sample_count = 64
max_iter = 30
max_views = 2
lights = ['basis_sh_0.exr', 'basis_sh_1.exr', 'basis_sh_2.exr', 'basis_sh_3.exr']
fov = 1
num_clusters = 2

b = 20.0
step_a = np.zeros((num_clusters, 3))
step_a[0][0] = 0.4; step_a[0][1] = 40; step_a[0][2] = 200
step_a[1][0] = 0.4; step_a[1][1] = 40; step_a[1][2] = 20000

rgb_init = np.zeros((num_clusters, 3))
rgb_init[0][0] = 1; rgb_init[0][1]= 1; rgb_init[0][2] = 1
rgb_init[1][0] = 1; rgb_init[1][1] = 1; rgb_init[1][2] = 1

rgb = np.zeros((num_clusters, 3))
for i in range(num_clusters):
  for j in range(3):
    rgb[i][j] = rgb_init[i][j]


for i in range(len(scales)):
    scale_phase = scales[i]
    scale_density = scales[i]
    scale_albedo = scales[i]
    args_sample_count = " -DsampleCount=" + str(sample_count)
    args_scale_phase = " -Ds1vol=phase/s1_" + str(scale_phase) + "x.vol"
    args_scale_phase += " -Ds2vol=phase/s2_" + str(scale_phase) + "x.vol"
    args_scale_density = " -Ddensity=density/density_" + str(scale_density) + "x.vol"

    args_albedo = " -Dalbedo=albedo/albedo_" + str(scale_albedo) + "x.vol"
    args_segmentation = " -Dsegmentation=albedo/segment_" + str(scale_albedo) + "x.vol"
    args_fov = " -Dfov=" + str(fov)
    args_clusters = " -DnumClusters=2"

    for iter in range(max_iter):
        step = step_a / (iter + b)
        tot_avg_err = np.zeros((3))
        tot_grad = np.zeros((num_clusters, 3))

        for j in range(max_views):
            for k in range(len(lights)):
                args_albedo_scale = ""
                for c in range(num_clusters):
                  args_albedo_scale += " -Dsr" + str(c) + "=" + str(rgb[c][0]) + " -Dsg" + str(c) + "=" + str(rgb[c][1]) + " -Dsb" + str(c) + "=" + str(rgb[c][2])
                args_light = " -Dlight=" + lights[k]
                
                # render
                args = args_sample_count + args_scale_phase + args_scale_density + args_fov + args_light
                args += args_albedo + args_segmentation + args_clusters + args_albedo_scale
                L_filename = "results/hetero_fov_" + str(fov) + "_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_view_" + str(j) + "_sh_" + str(k) + ".pfm"
                args += " -o " + L_filename
                args += " -b 20"
                scene_filename = "hetero_iso_view_" + str(j) + ".xml"
                args += " " + scene_filename
                print cmd + args
                os.system(cmd + args)

                # collect derivative image blocks
                print "*** collecting results ***"
                collect_cmd = "./collect_results.sh /mnt/gabardine_hetero/ 24"
                os.system(collect_cmd)
                collect_cmd = "mv *.pfm tmp/"
                os.system(collect_cmd)
                print "*** collection done ***"

                # render
                args = args_sample_count + args_scale_phase + args_scale_density + args_fov + args_light
                args += args_albedo + args_segmentation + args_clusters + args_albedo_scale
                L_filename = "results/hetero_fov_" + str(fov) + "_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_view_" + str(j) + "_sh_" + str(k) + ".pfm"
                args += " -o " + L_filename
                args += " -b 20"
                scene_filename = "hetero_iso_view_" + str(j) + ".xml"
                args += " " + scene_filename
                print cmd + args
                os.system(cmd + args)

                # combine image blocks
                LdA_s00_filename = "results/LdA_s00_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_view_" + str(j) + "_sh_" + str(k) + ".pfm"
                LdA_s01_filename = "results/LdA_s01_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_view_" + str(j) + "_sh_" + str(k) + ".pfm"
                combine_cmd = "python combine_scale_diff_results.py " + LdA_s00_filename + " " + LdA_s01_filename
                print "*** combining results ***"
                os.system(combine_cmd)
                print "*** combination done ***"

                # clean image blocks
                print "*** cleaning results ***"
                clean_cmd = "./clean_results.sh /mnt/gabardine_hetero/ 24"
                os.system(clean_cmd)
                print "*** clean done ***"

                L_ref_filename = "results/ref/hetero_fov_" + str(fov) + "_spp_1024_scale_1x_view_" + str(j) + "_sh_" + str(k) + ".pfm"
                L_ref = load_pfm(open(L_ref_filename, "rb"))

                L = load_pfm(open(L_filename, "rb"))
                LdA_s00 = load_pfm(open(LdA_s00_filename, "rb"))
                LdA_s01 = load_pfm(open(LdA_s01_filename, "rb"))
                LdA = [LdA_s00, LdA_s01]
                
                print "*** calculating gradients ***"
                for c in range(num_clusters):
                  grad = calc_grad(LdA[c], L, L_ref)
                  tot_grad[c] += grad
                print "*** done ***"
        
                diff = np.subtract(L, L_ref)
                avg = np.mean(np.mean(diff, axis=0), axis=0)
                tot_avg_err += avg
        
        outfile = open("results/hetero_albedo_grads.txt", "a")
        st = "finish iteration " + str(iter) + "... change albedo...\n"
        outfile.write(st)
        st = "sr0: " + str(rgb[0][0]) + " sg0: " + str(rgb[0][1]) + " sb0: " + str(rgb[0][2]) + "\n"
        outfile.write(st)
        st = "grad_sr0: " + str(tot_grad[0][0]) + " grad_sg0: " + str(tot_grad[0][1]) + " grad_sb0: " + str(tot_grad[0][2]) + "\n"
        outfile.write(st)
        st = "sr1: " + str(rgb[1][0]) + " sg1: " + str(rgb[1][1]) + " sb1: " + str(rgb[1][2]) + "\n"
        outfile.write(st)
        st = "grad_sr1: " + str(tot_grad[1][0]) + " grad_sg1: " + str(tot_grad[1][1]) + " grad_sb1: " + str(tot_grad[1][2]) + "\n"
        outfile.write(st)
        st = "error: " + str(tot_avg_err[0]) + " " + str(tot_avg_err[1]) + " " + str(tot_avg_err[2]) + "\n"
        outfile.write(st)
        outfile.write("======================\n")
        outfile.close()

        for c in range(num_clusters):
          rgb[c] -= np.multiply(tot_grad[c], step[c])

