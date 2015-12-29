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
    intensity = np.zeros((3))
    grad = np.zeros((3))
    cnt = 0.0
    for i in range(LdA.shape[0]):
        for j in range(LdA.shape[1]):
            # only use volume part
            if (LdA[i][j][0] < 0.001):
                continue

            cnt += 1.0
            for c in range(3):
                intensity[c] += (L[i][j][c] - L_ref[i][j][c])
                grad[c] += LdA[i][j][c]

    res = np.zeros((3))
    for c in range(3):
        intensity[c] /= cnt
        grad[c] /= cnt
        res[c] = 2 * intensity[c] * grad[c]
    return res

cmd = "mitsuba -s servers.txt"

scales = [2, 4]
sample_count = 128
max_iter = 50
max_views = 6
lights = ['basis_sh_0.exr', 'basis_sh_1.exr', 'basis_sh_2.exr', 'basis_sh_3.exr']

step_a = np.zeros((3))
step_a[0] = 0.01; step_a[1] = 1; step_a[2] = 6
rgb_init = np.zeros((3))
rgb_init[0] = 0.95; rgb_init[1]= 0.64; rgb_init[2] = 0.37
rgb = np.zeros((3))
rgb[0] = rgb_init[0]; rgb[1] = rgb_init[1]; rgb[2] = rgb_init[2]


for i in range(len(scales)):
    scale_phase = scales[i]
    scale_density = scales[i]
    args_sample_count = " -DsampleCount=" + str(sample_count)
    args_scale_phase = " -Ds1vol=phase/s1_" + str(scale_phase) + "x.vol"
    args_scale_phase += " -Ds2vol=phase/s2_" + str(scale_phase) + "x.vol"
    args_scale_density = " -Ddensity=density/density_" + str(scale_density) + "x.vol"

    for iter in range(max_iter):
        step = step_a / (iter + 1.0)
        tot_avg_err = np.zeros((3))
        tot_grad = np.zeros((3))

        for j in range(max_views):
            for k in range(len(lights)):
                args_albedo = " -Dr=" + str(rgb[0]) + " -Dg=" + str(rgb[1]) + " -Db=" + str(rgb[2])
                args_light = " -Dlight=" + lights[k]
                args = args_sample_count + args_scale_phase + args_scale_density
                args += args_albedo + args_light
                L_filename = "results/bunny_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_view_" + str(j) + "_sh_" + str(k) + ".pfm"
                args += " -o " + L_filename
                args += " -b 40"
                scene_filename = "bunny_diff_view_" + str(j) + ".xml"
                args += " " + scene_filename
                print cmd + args
                os.system(cmd + args)

                L_ref_filename = "results/ref/bunny_spp_1024_scale_1x_view_" + str(j) + "_sh_" + str(k) + ".pfm"
                L_ref = load_pfm(open(L_ref_filename, "rb"))

                collect_cmd = "./collect_results.sh /mnt/bunny/ 19"
                os.system(collect_cmd)
                LdA_filename = "results/LdA_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x_view_" + str(j) + "_sh_" + str(k) + ".pfm"
                combine_cmd = "python combine_diff_results.py " + LdA_filename
                os.system(combine_cmd)
                L = load_pfm(open(L_filename, "rb"))
                LdA = load_pfm(open(LdA_filename, "rb"))
        
                grad = calc_grad(LdA, L, L_ref)
                tot_grad += grad
        
                diff = np.subtract(L, L_ref)
                avg = np.mean(np.mean(diff, axis=0), axis=0)
                tot_avg_err += avg
        
        outfile = open("results/bunny_albedo_grads.txt", "a")
        st = "finish iteration " + str(iter) + "... change albedo...\n"
        outfile.write(st)
        st = "r: " + str(rgb[0]) + " g: " + str(rgb[1]) + " b: " + str(rgb[2]) + "\n"
        outfile.write(st)
        st = "error: " + str(tot_avg_err[0]) + " " + str(tot_avg_err[1]) + " " + str(tot_avg_err[2]) + "\n"
        outfile.write(st)
        st = "grad_r: " + str(tot_grad[0]) + " grad_g: " + str(tot_grad[1]) + " grad_b: " + str(tot_grad[2]) + "\n"
        outfile.write(st)
        outfile.write("======================\n")
        outfile.close()

        rgb -= np.multiply(tot_grad, step)

    outfile = open("results/bunny_albedo_values.txt", "a")
    st = "scale: " + str(scale_phase) + "\n"
    outfile.write(st)
    st = "r: " + str(rgb[0]) + " g: " + str(rgb[1]) + " b: " + str(rgb[2]) + "\n"
    outfile.write(st)
    st = "error: " + str(tot_avg_err[0]) + " " + str(tot_avg_err[1]) + " " + str(tot_avg_err[2]) + "\n"
    outfile.write(st)
    outfile.write("=======================\n")
    outfile.close()
