import sys

import traceFileReader

from magiclockLib import magiclockTypes
from magiclockLib import lockReduction
from magiclockLib import cycleDetection

def get_OwnedLockObjects(threadName, ownedLockObjectsByThread):
    if threadName not in ownedLockObjectsByThread:
        ownedLockObjectsByThread[threadName] = []
    return ownedLockObjectsByThread[threadName]


def remove_From_List(x, lst):
    if x in lst:
        lst.remove(x)


def create_LockDependencyRelation(lockActions):
    lockDependencyRelation = magiclockTypes.LockDependencyRelation()
    ownedLockObjectsByThread = {}
    for lockAction in lockActions:
        ownedLockObjects = get_OwnedLockObjects(lockAction.threadName, ownedLockObjectsByThread)
        if lockAction.actionType == traceFileReader.LockActionType.LOCK:
            lockDependencyRelation.add(magiclockTypes.LockDependency(lockAction.threadName, lockAction.lockObjectName, ownedLockObjects.copy()))
            ownedLockObjects.append(lockAction.lockObjectName)
        elif lockAction.actionType == traceFileReader.LockActionType.UNLOCK:
            remove_From_List(lockAction.lockObjectName, ownedLockObjects)
    return lockDependencyRelation

traceFilename = sys.argv[1]
lockActions = traceFileReader.read_Trace_File_Lines(traceFilename)

lockDependencyRelation = create_LockDependencyRelation(lockActions)
lockDependencyRelation.print()

initClassification = lockReduction.init_Classification(lockDependencyRelation)
initClassification.print()

lockClassification, lockDependencyRelation = lockReduction.lock_Reduction(lockDependencyRelation, initClassification)
print("\nLock reduction Result:")
print("Cyclic-set:")
print(lockClassification.cyclicSet)
lockDependencyRelation.print()

disjointComponents = cycleDetection.disjoint_Components_Finder(lockClassification.cyclicSet, initClassification.edgesFromTo)
print("\nDisjoint Components:")
print(disjointComponents)

potentialDeadlocks = []
for dc in disjointComponents:
    cycleDetection.cycle_detection(potentialDeadlocks, dc, lockDependencyRelation)

print("\nPotential Deadlocks:")
for potentialDeadlock in potentialDeadlocks:
    for d in potentialDeadlock:
        d.print()
        print(end=" ")
    print()