import sys, psutil, time, subprocess

process = subprocess.Popen(['prl','-r', sys.argv[1]])

psutilProcess = psutil.Process(process.pid)
maxMemory = 0
while process.poll() == None:
  memory = psutilProcess.memory_info()[0] / 1024
  if memory > maxMemory:
    maxMemory = memory
  time.sleep(.1)

process.wait()
print("Process used "+str(maxMemory)+" Kb.")