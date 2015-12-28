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
    res = np.zeros((3))
    cnt = 0.0
    for i in range(LdA.shape[0]):
        for j in range(LdA.shape[1]):
            # only use volume part
            #if (LdA[i][j][0] < 0.5):
            #    continue

            cnt += 1.0
            for c in range(3):
                res[c] += 2.0 * (L[i][j][c] - L_ref[i][j][c]) * LdA[i][j][c]
    res /= cnt
    return res

cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"

scales = [2]
sample_count = 64
max_iter = 50
lights = ['lights/campus.exr']

step = 0.02
rgb_init = np.zeros((3))
rgb_init[0] = 0.95; rgb_init[1]= 0.64; rgb_init[2] = 0.37
rgb = np.zeros((3))
rgb[0] = rgb_init[0]; rgb[1] = rgb_init[1]; rgb[2] = rgb_init[2]

L_ref_filename = "bunny_spp_4096_scale_1x_a0.pfm"
L_ref = load_pfm(open(L_ref_filename, "rb"))

for i in range(len(scales)):
    scale_phase = scales[i]
    scale_density = scales[i]
    args_sample_count = " -DsampleCount=" + str(sample_count)
    args_scale_phase = " -Ds1vol=phase/s1_" + str(scale_phase) + "x.vol"
    args_scale_phase += " -Ds2vol=phase/s2_" + str(scale_phase) + "x.vol"
    args_scale_density = " -Ddensity=density/density_" + str(scale_density) + "x.vol"

    for iter in range(max_iter):
        if (iter > 40):
            step = 0.005
        elif (iter > 20):
            step = 0.01
        tot_avg_err = np.zeros((3))
        
        args_albedo = " -Dr=" + str(rgb[0]) + " -Dg=" + str(rgb[1]) + " -Db=" + str(rgb[2])
        args_light = " -Dlight=" + lights[0]
        args = args_sample_count + args_scale_phase + args_scale_density
        args += args_albedo + args_light
        L_filename = "gd_results/bunny_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x.pfm"
        args += " -o " + L_filename
        args += " -p 11 -b 40"
        scene_filename = "bunny_diff_env_light.xml"
        args += " " + scene_filename
        print cmd + args
        os.system(cmd + args)
        
        LdA_filename = "gd_results/LdA_spp_" + str(sample_count) + "_scale_" + str(scales[i]) + "x.pfm"
        combine_cmd = "python ../combine_diff_results.py " + LdA_filename
        os.system(combine_cmd)
        L = load_pfm(open(L_filename, "rb"))
        LdA = load_pfm(open(LdA_filename, "rb"))
        
        grad = calc_grad(LdA, L, L_ref)
        rgb -= grad * step
        
        diff = np.subtract(L, L_ref)
        avg = np.mean(np.mean(diff, axis=0), axis=0)
        tot_avg_err = avg
        
        outfile = open("gd_results/bunny_albedo_grads.txt", "a")
        st = "finish iteration " + str(iter) + "... change albedo...\n"
        outfile.write(st)
        st = "r: " + str(rgb[0]) + " g: " + str(rgb[1]) + " b: " + str(rgb[2]) + "\n"
        outfile.write(st)
        st = "error: " + str(tot_avg_err[0]) + " " + str(tot_avg_err[1]) + " " + str(tot_avg_err[2]) + "\n"
        outfile.write(st)
        st = "grad_r: " + str(grad[0]) + " grad_g: " + str(grad[1]) + " grad_b: " + str(grad[2]) + "\n"
        outfile.write(st)
        outfile.write("======================\n")
        outfile.close()

    outfile = open("gd_results/bunny_albedo_values.txt", "a")
    st = "scale: " + str(scale_phase) + "\n"
    outfile.write(st)
    st = "r: " + str(rgb[0]) + " g: " + str(rgb[1]) + " b: " + str(rgb[2]) + "\n"
    outfile.write(st)
    st = "error: " + str(tot_avg_err[0]) + " " + str(tot_avg_err[1]) + " " + str(tot_avg_err[2]) + "\n"
    outfile.write(st)
    outfile.write("=======================\n")
    outfile.close()