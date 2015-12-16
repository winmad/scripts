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

#=====================================================
cmd = "D:\\Lifan\\mitsuba\\dist\\mitsuba"

fovs = [15]
scales = [2, 4] #[2, 4]
sample_count = 64
max_iter = 20

albedo_r = np.zeros((len(fovs), len(scales)))
albedo_g = np.zeros((len(fovs), len(scales)))
albedo_b = np.zeros((len(fovs), len(scales)))

for i in range(len(scales)): #[15, 8, 4, 2, 1, 0.4]:
	ref_filename = "bunny\\ref\\bunny_spp_256_scale_1x.pfm"
	img0 = load_pfm(open(ref_filename, "rb"))
	r_l = 0.0; r_r = 1.0; g_l = 0.0; g_r = 1.0; b_l = 0.0; b_r = 1.0
	scale_phase = scales[i]
	scale_density = scales[i]
	args_sample_count = " -DsampleCount=" + str(sample_count)
	args_scale_phase = " -Ds1vol=bunny\\phase\\s1_" + str(scale_phase) + "x.vol"
	args_scale_phase += " -Ds2vol=bunny\\phase\\s2_" + str(scale_phase) + "x.vol"
	args_scale_density = " -Ddensity=bunny\\density\\density_" + str(scale_density) + "x.vol"
		
	for iter in range(max_iter):
		r = (r_l + r_r) * 0.5
		g = (g_l + g_r) * 0.5
		b = (b_l + b_r) * 0.5

		args = args_sample_count + args_scale_density + args_scale_phase
		args_albedo_scale = " -Dr=" + str(r) + " -Dg=" + str(g) + " -Db=" + str(b)
		args += args_albedo_scale

		args += " -p 11 -o "
		filename = "bunny\\bunny"
		filename += "_spp_" + str(sample_count) + "_scale_" + str(scale_density) + "x.pfm"
		args += filename
		args += " bunny\\bunny_search_albedo.xml"
		print cmd + args
		os.system(cmd + args)
			
		print "finish iteration " + str(iter) + "... change albedo..."
		img1 = load_pfm(open(filename, "rb"))
		diff = np.subtract(img1, img0)
		#rel_diff = np.divide(np.abs(diff), img0 + 0.0001)
		avg = np.mean(np.mean(diff, axis=0), axis=0)
			
		if (np.abs(avg[0]) < 1e-6 and np.abs(avg[1]) < 1e-6 and np.abs(avg[2]) < 1e-6):
			break

		if (avg[0] > 0):
			r_r = r
		else:
			r_l = r
		if (avg[1] > 0):
			g_r = g
		else:
			g_l = g
		if (avg[2] > 0):
			b_r = b
		else:
			b_l = b

	albedo_r[0][i] = (r_l + r_r) * 0.5
	albedo_g[0][i] = (g_l + g_r) * 0.5
	albedo_b[0][i] = (b_l + b_r) * 0.5
		
	outfile = open("bunny\\bunny_albedo_values.txt", "a")
	st = "scale: " + str(scale_phase) + "\n"
	outfile.write(st)
	st = "r: " + str(albedo_r[0][i]) + " g: " + str(albedo_g[0][i]) + " b: " + str(albedo_b[0][i]) + "\n"
	outfile.write(st)
	st = "error: " + str(avg[0]) + " " + str(avg[1]) + " " + str(avg[2]) + "\n"
	outfile.write(st)
	outfile.write("=======================\n")
	outfile.close()

