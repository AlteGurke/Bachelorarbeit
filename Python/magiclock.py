import sys
from collections import defaultdict

import traceFileReader


class InitClassification(object):
    def __init__(self):
        self.indegree = {}
        self.outdegree = {}
        self.mode = {}
        self.edgesFromTo = defaultdict(lambda: defaultdict(int))
        self.locks = set()

    def print(self):
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
        print("Locks:")
        print(self.locks)


class LockClassification(object):
    def __init__(self):
        self.independentSet = []
        self.intermediateSet = []
        self.innerSet = []
        self.cyclicSet = []

    def print(self):
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
        ownedLockObjects = get_OwnedLockObjects(
            lockAction.threadName, ownedLockObjectsByThread)
        if lockAction.actionType == traceFileReader.LockActionType.LOCK:
            lockDependencyRelation.append(LockDependency(
                lockAction.threadName, lockAction.lockObjectName, ownedLockObjects.copy()))
            ownedLockObjects.append(lockAction.lockObjectName)
        elif lockAction.actionType == traceFileReader.LockActionType.UNLOCK:
            remove_From_List(lockAction.lockObjectName, ownedLockObjects)
    return lockDependencyRelation


def mode(m, D):
    thread = None
    for d in D:
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
    for m in D:
        initClassification.locks.add(m.lockObjectName)
    for m in initClassification.locks:
        initClassification.indegree[m] = 0
        initClassification.outdegree[m] = 0
        initClassification.mode[m] = 0
    for d in D:
        if mode(d.lockObjectName, D) != d.threadName:
            initClassification.mode[d.lockObjectName] = -1
        else:
            initClassification.mode[d.lockObjectName] = d.threadName
        for n in d.currentlyOwnedLockObjectNames:
            initClassification.indegree[d.lockObjectName] += 1
            initClassification.outdegree[n] += 1
            initClassification.edgesFromTo[n][d.lockObjectName] += 1
    return initClassification


def lock_Classification(initClassification):
    lockClassification = LockClassification()
    s = []
    for m in initClassification.locks:
        if initClassification.indegree[m] == 0 and initClassification.outdegree[m] == 0:
            lockClassification.independentSet.append(m)
        else:
            if initClassification.indegree[m] == 0 or initClassification.outdegree[m] == 0:
                lockClassification.intermediateSet.append(m)
                s.append(m)

    while s:
        m = s.pop()
        if initClassification.indegree[m] == 0:
            for n in initClassification.locks:
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
            for n in initClassification.locks:
                if n == m:
                    continue
                if initClassification.outdegree[n] != 0:                        
                    initClassification.outdegree[n] -= initClassification.edgesFromTo[n][m]
                    if initClassification.outdegree[n] == 0:
                        s.append(n)
                        lockClassification.innerSet.append(n)
                initClassification.indegree[m] -= initClassification.edgesFromTo[n][m]
                initClassification.edgesFromTo[n][m] = 0

    for m in initClassification.locks:
        if (m not in lockClassification.independentSet and
            m not in lockClassification.intermediateSet and
                m not in lockClassification.innerSet):
            lockClassification.cyclicSet.append(m)

    return lockClassification

def print_LockDependencyRelation(lockDependencyRelation):
    print("LockDependencyRelation:")
    for d in lockDependencyRelation:
        d.print()
        print(", ", end="")
    print("\n")

def print_InitClassification(initClassification):
    print("Init Classification:")
    initClassification.print()
    print("")

def print_LockClassification(lockClassification):
    print("Lock Classification")
    lockClassification.print()

traceFilename = sys.argv[1]
lockActions = traceFileReader.read_Trace_File_Lines(traceFilename)

lockDependencyRelation = create_LockDependencyRelation(lockActions)
print_LockDependencyRelation(lockDependencyRelation)

initClassification = init_Classification(lockDependencyRelation)
print_InitClassification(initClassification)

lockClassification = lock_Classification(initClassification)
print_LockClassification(lockClassification)