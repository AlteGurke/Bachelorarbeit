import sys, time, subprocess

timeStarted = time.time() 
process = subprocess.check_call(['prl','-r', sys.argv[1]])
timeEnded = time.time() 

timeDelta = time.time() - timeStarted 
print("Finished process in "+str(timeDelta)+" seconds.")