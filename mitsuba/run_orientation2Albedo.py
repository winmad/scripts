import sys
import os

cmd = "D:\\Lifan\\mitsuba\\dist\\mtsutil orientation2Albedo 0"

scale = 1
density_filename = "gabardine\\albedo_by_orientation\\gabardine_dir_supertile_" + str(scale) + "x.vol"
albedo_filename = "gabardine\\albedo_by_orientation\\albedo_by_orientation_" + str(scale) + "x.vol"
args = " " + density_filename + " " + albedo_filename
os.system(cmd + args)