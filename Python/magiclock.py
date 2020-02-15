import sys

import traceFileReader

class LockDependency(object):
    def __init__(self, threadName, lockObjectName, currentlyOwnedLockObjectNames):
        self.threadName = threadName
        self.lockObjectName = lockObjectName
        self.currentlyOwnedLockObjectNames = currentlyOwnedLockObjectNames

    def clone(self):
        lst = []
        for x in self.currentlyOwnedLockObjectNames:
            lst.append(x)
        return LockDependency(self.threadName, self.lockObjectName, lst)

def get_OwnedLockObjects(threadName, ownedLockObjectsByThread):
    if threadName not in ownedLockObjectsByThread:
        ownedLockObjectsByThread[threadName] = []
    return ownedLockObjectsByThread[threadName]

def remove_From_List(x, lst):
    if x in lst:
        lst.remove(x)

def create_LockDependencyRelation(lockActions):
    lockDependencyRelation = []
    ownedLockObjectsByThread = {}
    for lockAction in lockActions:
        ownedLockObjects = get_OwnedLockObjects(lockAction.threadName, ownedLockObjectsByThread)
        if lockAction.actionType == traceFileReader.LockActionType.LOCK:
            lockDependencyRelation.append(LockDependency(lockAction.threadName, lockAction.lockObjectName, ownedLockObjects.copy()))
            ownedLockObjects.append(lockAction.lockObjectName)
        elif lockAction.actionType == traceFileReader.LockActionType.UNLOCK:
            remove_From_List(lockAction.lockObjectName, ownedLockObjects)
    return lockDependencyRelation

traceFilename = sys.argv[1]
lockActions = traceFileReader.read_Trace_File_Lines(traceFilename)
lockDependencyRelation = create_LockDependencyRelation(lockActions)

for d in lockDependencyRelation:
    print("(", end="")
    print(str(d.threadName) + "," + str(d.lockObjectName) + ",{", end="")
    for x in d.currentlyOwnedLockObjectNames:
        print(str(x) + ",", end="")
    print("}), ", end="")
print("")