import sys
from collections import defaultdict

import traceFileReader


class InitClassification(object):
    def __init__(self):
        self.indegree = {}
        self.outdegree = {}
        self.mode = {}
        self.edgesFromTo = defaultdict(lambda: defaultdict(int))

    def print(self):
        print("\nInit Classification:")
        print("Indegrees:")
        print(self.indegree)
        print("Oudegrees:")
        print(self.outdegree)
        print("Modes:")
        print(self.mode)
        print("edgesFromTo:")
        for (f, t) in self.edgesFromTo.items():
            print(f, end=": ")
            for x in t:
                print(x, end=",")
            print("")


class LockClassification(object):
    def __init__(self):
        self.independentSet = []
        self.intermediateSet = []
        self.innerSet = []
        self.cyclicSet = []

    def print(self):
        print("\nLock Classification:")
        print("IndependentSet:")
        print(self.independentSet)
        print("IntermediateSet:")
        print(self.intermediateSet)
        print("InnerSet:")
        print(self.innerSet)
        print("CyclicSet:")
        print(self.cyclicSet)


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

    def print(self):
        print("(", end="")
        print(str(self.threadName) + "," +
              str(self.lockObjectName) + ",{", end="")
        for x in self.currentlyOwnedLockObjectNames:
            print(str(x) + ",", end="")
        print("})", end="")


class LockDependencyRelation(object):
    def __init__(self):
        self.locks = set()
        self.lockDependencies = []

    def add(self, lockDependency):
        self.lockDependencies.append(lockDependency)
        self.locks.add(lockDependency.lockObjectName)
    
    def print(self):
        print("\nLockDependencyRelation:")
        for d in self.lockDependencies:
            d.print()
            print(", ", end="")
        print("\nLocks:")
        print(self.locks)


def get_OwnedLockObjects(threadName, ownedLockObjectsByThread):
    if threadName not in ownedLockObjectsByThread:
        ownedLockObjectsByThread[threadName] = []
    return ownedLockObjectsByThread[threadName]


def remove_From_List(x, lst):
    if x in lst:
        lst.remove(x)


def create_LockDependencyRelation(lockActions):
    lockDependencyRelation = LockDependencyRelation()
    ownedLockObjectsByThread = {}
    for lockAction in lockActions:
        ownedLockObjects = get_OwnedLockObjects(
            lockAction.threadName, ownedLockObjectsByThread)
        if lockAction.actionType == traceFileReader.LockActionType.LOCK:
            lockDependencyRelation.add(LockDependency(
                lockAction.threadName, lockAction.lockObjectName, ownedLockObjects.copy()))
            ownedLockObjects.append(lockAction.lockObjectName)
        elif lockAction.actionType == traceFileReader.LockActionType.UNLOCK:
            remove_From_List(lockAction.lockObjectName, ownedLockObjects)
    return lockDependencyRelation


def mode(m, D):
    thread = None
    for d in D.lockDependencies:
        if d.lockObjectName != m:
            continue
        if thread == None:
            thread = d.threadName
        elif d.threadName == thread:
            continue
        else:
            return None
    return thread


def init_Classification(D):
    initClassification = InitClassification()
    for m in D.locks:
        initClassification.indegree[m] = 0
        initClassification.outdegree[m] = 0
        initClassification.mode[m] = 0
    for d in D.lockDependencies:
        if mode(d.lockObjectName, D) != d.threadName:
            initClassification.mode[d.lockObjectName] = -1
        else:
            initClassification.mode[d.lockObjectName] = d.threadName
        for n in d.currentlyOwnedLockObjectNames:
            initClassification.indegree[d.lockObjectName] += 1
            initClassification.outdegree[n] += 1
            initClassification.edgesFromTo[n][d.lockObjectName] += 1
    return initClassification


def lock_Classification(D, initClassification):
    lockClassification = LockClassification()
    s = []
    for m in D.locks:
        if initClassification.indegree[m] == 0 and initClassification.outdegree[m] == 0:
            lockClassification.independentSet.append(m)
        else:
            if initClassification.indegree[m] == 0 or initClassification.outdegree[m] == 0:
                lockClassification.intermediateSet.append(m)
                s.append(m)

    while s:
        m = s.pop()
        if initClassification.indegree[m] == 0:
            for n in D.locks:
                if n == m:
                    continue
                if initClassification.indegree[n] != 0:
                    initClassification.indegree[n] -= initClassification.edgesFromTo[m][n]
                    if initClassification.indegree[n] == 0:
                        s.append(n)
                        lockClassification.innerSet.append(n)
                initClassification.outdegree[m] -= initClassification.edgesFromTo[m][n]
                initClassification.edgesFromTo[m][n] = 0
        if initClassification.outdegree[m] == 0:
            for n in D.locks:
                if n == m:
                    continue
                if initClassification.outdegree[n] != 0:                        
                    initClassification.outdegree[n] -= initClassification.edgesFromTo[n][m]
                    if initClassification.outdegree[n] == 0:
                        s.append(n)
                        lockClassification.innerSet.append(n)
                initClassification.indegree[m] -= initClassification.edgesFromTo[n][m]
                initClassification.edgesFromTo[n][m] = 0

    for m in D.locks:
        if (m not in lockClassification.independentSet and
            m not in lockClassification.intermediateSet and
                m not in lockClassification.innerSet):
            lockClassification.cyclicSet.append(m)

    return lockClassification

def lock_Reduction(D, initClassification):
    lockClassification = lock_Classification(D, initClassification)
    lockClassification.print()
    for m in lockClassification.cyclicSet[:]:
        if initClassification.mode[m] != -1:
            lockClassification.cyclicSet.remove(m)
            for n in lockClassification.cyclicSet:
                if initClassification.edgesFromTo[m][n] != 0:
                    initClassification.indegree[n] -= initClassification.edgesFromTo[m][n]
                    initClassification.edgesFromTo[m][n] = 0
            for n in lockClassification.cyclicSet:
                if initClassification.edgesFromTo[n][m] != 0:
                    initClassification.outdegree[n] -= initClassification.edgesFromTo[n][m]
                    initClassification.edgesFromTo[n][m] = 0
    
    projectedD = get_LockDependencyRelation_For(D, lockClassification.cyclicSet)
    if projectedD.lockDependencies != D.lockDependencies:
        return lock_Reduction(projectedD, initClassification)

    return lockClassification

def get_LockDependencyRelation_For(D, cyclicSet):
    lockDependencyRelation = LockDependencyRelation()

    for d in D.lockDependencies:
        if d.lockObjectName in cyclicSet:
            lockDependencyRelation.add(d)

    return lockDependencyRelation


traceFilename = sys.argv[1]
lockActions = traceFileReader.read_Trace_File_Lines(traceFilename)

lockDependencyRelation = create_LockDependencyRelation(lockActions)
lockDependencyRelation.print()

initClassification = init_Classification(lockDependencyRelation)
initClassification.print()

lockClassification = lock_Reduction(lockDependencyRelation, initClassification)
print("\nLock classification Result:")
lockClassification.print()