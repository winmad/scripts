import os, sys

#cmd = "sudo cp -r %s %s" % (sys.argv[1], sys.argv[2])
#print cmd
#os.system(cmd)

cmd = "sudo tar zxvf %s -C %s" % (sys.argv[1], sys.argv[2])
print cmd
os.system(cmd)

