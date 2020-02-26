import os.path, time
import sys
print("last modified: %s" % time.ctime(os.path.getmtime(sys.argv[1])))
print("created: %s" % time.ctime(os.path.getctime(sys.argv[1])))
