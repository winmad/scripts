import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mtsutil createGridVolume"

fov = 4
scale = 4
original_filename = "gabardine\\albedo_by_orientation\\albedo_" + str(scale) + "x.vol"
albedo_filename = "gabardine\\albedo_by_orientation\\albedo_" + str(scale) + "x_smaller.vol"
args = " " + original_filename + " " + albedo_filename
os.system(cmd + args)