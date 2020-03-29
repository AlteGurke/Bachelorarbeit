import sys
import time
import subprocess

timeStarted = time.time()
process = subprocess.check_call(['prl', '-r', sys.argv[1]])
timeEnd = time.time()

timeDelta = timeEnd - timeStarted
print("Finished process in " + str(timeDelta) + " seconds.")