import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mtsutil fillEmptyVoxels 0"

scale = 1
old_albedo_filename = "gabardine\\albedo_by_orientation\\albedo_" + str(scale) + "x_zero.vol"
albedo_filename = "gabardine\\albedo_by_orientation\\albedo_" + str(scale) + "x.vol"
args = " " + old_albedo_filename + " " + albedo_filename
os.system(cmd + args)