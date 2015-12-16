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

fovs = [1] #[15, 8, 4, 2, 1, 0.4]
scales = [2, 4] #[2, 4]
sample_count = 16
max_iter = 16

albedo_r = np.zeros((len(fovs), len(scales)))
albedo_g = np.zeros((len(fovs), len(scales)))
albedo_b = np.zeros((len(fovs), len(scales)))

for i in range(len(fovs)): #[15, 8, 4, 2, 1, 0.4]:
	for j in range(len(scales)): #[2, 4]:
		ref_filename = "gabardine\\albedo_sv_search\\ref_albedo_by_orientation\\fov_" + str(fovs[i]) + "_spp_256_scale_1x_iso_phase.pfm"
		img0 = load_pfm(open(ref_filename, "rb"))
		r_l = 0.9; r_r = 1.1; g_l = 0.9; g_r = 1.1; b_l = 0.9; b_r = 1.1
		fov = fovs[i]
		scale_phase = scales[j]
		scale_density = scales[j]
		args_sample_count = " -DsampleCount=" + str(sample_count)
		#args_scale_phase = " -Ds1vol=gabardine\\sggx_0.05_splitted\\s1_" + str(scale_phase) + "x_" + str(split_part) + ".vol"
		#args_scale_phase += " -Ds2vol=gabardine\\sggx_0.05_splitted\\s2_" + str(scale_phase) + "x_" + str(split_part) + ".vol"
		args_scale_density = " -Ddensity=gabardine\\density_" + str(scale_density) + "x.vol"
		args_fov = " -Dfov=" + str(fov)
		
		for iter in range(max_iter):
			r = (r_l + r_r) * 0.5
			g = (g_l + g_r) * 0.5
			b = (b_l + b_r) * 0.5

			args = args_sample_count + args_scale_density + args_fov
			args_albedo = " -Dalbedo=gabardine\\albedo_by_orientation\\albedo_" + str(scales[j]) + "x.vol"
			args_albedo_scale = " -Dsr=" + str(r) + " -Dsg=" + str(g) + " -Dsb=" + str(b)
			args += args_albedo + args_albedo_scale

			args += " -p 11 -o "
			filename = "gabardine\\albedo_sv_search\\fov_" + str(fov)
			filename += "_spp_" + str(sample_count) + "_scale_" + str(scale_density) + "x_iso_phase.pfm"
			args += filename
			args += " gabardine\\gabardine_tiled_scale_sv_albedo_iso_phase.xml"
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

		albedo_r[i][j] = (r_l + r_r) * 0.5
		albedo_g[i][j] = (g_l + g_r) * 0.5
		albedo_b[i][j] = (b_l + b_r) * 0.5
		
		outfile = open("gabardine\\albedo_sv_search\\albedo_sv_scale_values.txt", "a")
		st = "fov: " + str(fov) + "  scale: " + str(scale_phase) + "\n"
		outfile.write(st)
		st = "r: " + str(albedo_r[i][j]) + " g: " + str(albedo_g[i][j]) + " b: " + str(albedo_b[i][j]) + "\n"
		outfile.write(st)
		st = "error: " + str(avg[0]) + " " + str(avg[1]) + " " + str(avg[2]) + "\n"
		outfile.write(st)
		outfile.write("=======================\n")
		outfile.close()


