import os, sys

cmd = "s3cmd get s3://mitsuba/%s ./" % (sys.argv[1])
print cmd
os.system(cmd)

#cmd = "tar zxvf %s" % (sys.argv[1])
#print cmd
#os.system(cmd)





