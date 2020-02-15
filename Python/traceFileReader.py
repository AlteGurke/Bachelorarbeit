class LockActionType:
    LOCK = 1
    UNLOCK = 2

class LockAction(object):
    def __init__(self, timeStamp, threadName, lockObjectName, actionType):
        self.timeStamp = timeStamp
        self.threadName = threadName
        self.lockObjectName = lockObjectName
        self.actionType = actionType

def lockAction_sort(lockAction):
    return lockAction.timeStamp

def read_Trace_File_Lines(traceFilename):
    file = open(traceFilename, 'r') 
    lines = file.readlines()

    lockActions = []
    for line in lines:
        lineValues = line.strip().split(':')
        threadAndObjectName = lineValues[1][2:-1].split(',')
        if lineValues[1][0] == "l":
            lockActions.append(LockAction(lineValues[0], threadAndObjectName[0], threadAndObjectName[1], LockActionType.LOCK))
        elif lineValues[1][0] == "u":
            lockActions.append(LockAction(lineValues[0], threadAndObjectName[0], threadAndObjectName[1], LockActionType.UNLOCK))
            
    lockActions.sort(key=lockAction_sort)
    return lockActions