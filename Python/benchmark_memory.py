import sys
import psutil
import time
import subprocess
import os

maxMemoryUsed = 0
for x in range(1, 4):
    process = subprocess.Popen(['prl', '-r', sys.argv[1]])

    maxMemory = 0
    while process.poll() == None:
        parent = psutil.Process(os.getpid())
        memory = parent.memory_info().rss / 1024 / 1024

        for child in parent.children(recursive=True):
            memory += child.memory_info().rss / 1024 / 1024

        if memory > maxMemory:
            maxMemory = memory
        time.sleep(.01)

    process.wait()
    maxMemoryUsed += maxMemory
print("Process used " + str(maxMemoryUsed / 3) + " MB.")
