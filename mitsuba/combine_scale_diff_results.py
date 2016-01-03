import sys
import os
import numpy as np
import re
import array

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

width = 480
height = 360
crop_width = 20
crop_height = 20
num_width = width / crop_width
num_height = height / crop_height
num_images = num_width * num_height

img = np.zeros((height, width, 3), np.float32)

def combine_image_blocks(prefix, out_filename):
  for i in range(num_width):
	  for j in range(num_height):
		  block_offset_x = crop_width * i
		  block_offset_y = crop_height * j

		  filename = "tmp/" + prefix + "_%03d_%03d.pfm" % (block_offset_x, block_offset_y)
		  #print filename

 		  pfmimg = load_pfm(open(filename, 'rb'))
		  for x in range(crop_width):
			  for y in range(crop_height):
				  offset_y = crop_height * (num_height - j - 1) + y
				  offset_x = block_offset_x + x

				  img[offset_y][offset_x][0] = pfmimg[y][x][0]
				  img[offset_y][offset_x][1] = pfmimg[y][x][1]
				  img[offset_y][offset_x][2] = pfmimg[y][x][2]

		  cmd = "rm " + filename
		  os.system(cmd)
  
  outfile = open(out_filename, 'wb')
  save_pfm(outfile, img)


combine_image_blocks("LdA_s00", sys.argv[1])
combine_image_blocks("LdA_s01", sys.argv[2])
#combine_image_blocks("image_seg", "image_seg.pfm")

