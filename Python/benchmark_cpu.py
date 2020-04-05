import sys
import time
import subprocess

times = 0
for x in range(1, 4):
    timeStarted = time.time()
    process = subprocess.check_call(['prl', '-r', sys.argv[1]])
    timeEnd = time.time()

    times += timeEnd - timeStarted
print("Finished process in " + str(times / 3) + " seconds.")