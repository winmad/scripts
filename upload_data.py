import os, sys

cmd = "tar zcvf %s %s" % (sys.argv[1], sys.argv[2])
print cmd
os.system(cmd)

cmd = "s3cmd put %s s3://mitsuba/" % (sys.argv[1])
print cmd
os.system(cmd)