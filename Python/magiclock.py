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
        print(str(self.threadName) + "," + str(self.lockObjectName) + ",{", end="")
        for x in self.currentlyOwnedLockObjectNames:
            print(str(x), end="")
            if x != self.currentlyOwnedLockObjectNames[-1]:
                print(",", end="")
        print("})", end="")


class LockDependencyRelation(object):
    def __init__(self):
        self.locks = set()
        self.threads = []
        self.lockDependencies = []

    def add(self, lockDependency):
        self.lockDependencies.append(lockDependency)
        self.locks.add(lockDependency.lockObjectName)
        if lockDependency.threadName not in self.threads:
            self.threads.append(lockDependency.threadName)

    def print(self):
        print("\nLockDependencyRelation:")
        for d in self.lockDependencies:
            d.print()
            if d != self.lockDependencies[-1]:
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
        ownedLockObjects = get_OwnedLockObjects(lockAction.threadName, ownedLockObjectsByThread)
        if lockAction.actionType == traceFileReader.LockActionType.LOCK:
            lockDependencyRelation.add(LockDependency(lockAction.threadName, lockAction.lockObjectName, ownedLockObjects.copy()))
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

    projectedD = get_LockDependencyRelation_For(
        D, lockClassification.cyclicSet)
    if projectedD.lockDependencies != D.lockDependencies:
        return lock_Reduction(projectedD, initClassification)

    return lockClassification, projectedD


def get_LockDependencyRelation_For(D, cyclicSet):
    lockDependencyRelation = LockDependencyRelation()

    for d in D.lockDependencies:
        if d.lockObjectName in cyclicSet:
            lockDependencyRelation.add(d)

    return lockDependencyRelation


def visit_Edges_From(cyclicSet, edgesFromTo, visited, m, dc):
    if visited[m] == False:
        if m not in dc:
            dc.append(m)
        visited[m] = True
        for n in cyclicSet:
            if edgesFromTo[m][n] != 0:
                visit_Edges_From(cyclicSet, edgesFromTo, visited, n, dc)


def disjoint_Components_Finder(cyclicSet, edgesFromTo):
    dcs = set()
    dc = []
    visited = {}

    for m in cyclicSet:
        visited[m] = False

    for m in cyclicSet:
        if visited[m] == False:
            visit_Edges_From(cyclicSet, edgesFromTo, visited, m, dc)
            dcs.add(tuple(dc))
            dc = []

    return dcs


def find_Equal_Dependency_Group(Group, D, d):
    for di in D:
        if di == d:
            return Group[di]
    return []


def is_Lock_Dependency_Chain(d):
    if len(d) <= 1:
        return False

    for i in range(len(d) - 1):
        if d[i].lockObjectName not in d[i + 1].currentlyOwnedLockObjectNames:
            return False
        for j in range(len(d)):
            if d[i].threadName == d[j].threadName:
                continue
            if list(set(d[i].currentlyOwnedLockObjectNames) & set(d[j].currentlyOwnedLockObjectNames)):
                return False
    
    return True


def lock_Dependency_Chain_Is_Cyclic_Lock_Dependency_Chain(d):
    if d[-1].lockObjectName in d[0].currentlyOwnedLockObjectNames:
        return True
    return False


def reportCycle(o, size, equCycle, Group):
    if size == len(o):
        potentialDeadlocks.append(equCycle.copy())
    else:
        for d in Group[o[size]]:
            equCycle.append(d)
            reportCycle(o, size + 1, equCycle, Group)
            equCycle.remove(d)


def DFS_Traverse(i, s, d, k, isTraversed, Di, Group):
    s.append(d)
    for j in k[k.index(i) + 1:]:
        if isTraversed[j] == True:
            continue
        for di in Di[j]:
            o = s.copy()
            o.append(di)
            if is_Lock_Dependency_Chain(o):
                if lock_Dependency_Chain_Is_Cyclic_Lock_Dependency_Chain(o):
                    equCycle = []
                    reportCycle(o, 0, equCycle, Group)
                else:
                    isTraversed[j] = True
                    DFS_Traverse(i, s, di, k, isTraversed, Di, Group)
                    isTraversed[j] = False


def cycle_detection(dc, D):
    Group = {}
    isTraversed = {}
    Di = {}

    for t in D.threads:
        isTraversed[t] = False
        Di[t] = []

    for d in D.lockDependencies:
        if d.lockObjectName in dc and d.currentlyOwnedLockObjectNames:
            g = find_Equal_Dependency_Group(Group, Di[d.threadName], d)
            if g:
                g.add(d)
            else:
                Di[d.threadName].append(d)
                Group[d] = []
                Group[d].append(d)

    s = []
    for t in D.threads:
        for d in Di[t]:
            isTraversed[t] = True
            DFS_Traverse(t, s, d, D.threads, isTraversed, Di, Group)


traceFilename = sys.argv[1]
lockActions = traceFileReader.read_Trace_File_Lines(traceFilename)

lockDependencyRelation = create_LockDependencyRelation(lockActions)
lockDependencyRelation.print()

initClassification = init_Classification(lockDependencyRelation)
initClassification.print()

lockClassification, lockDependencyRelation = lock_Reduction(
    lockDependencyRelation, initClassification)
print("\nLock reduction Result:")
print("Cyclic-set:")
print(lockClassification.cyclicSet)
lockDependencyRelation.print()

disjointComponents = disjoint_Components_Finder(
    lockClassification.cyclicSet, initClassification.edgesFromTo)
print("\nDisjoint Components:")
print(disjointComponents)

potentialDeadlocks = []
for dc in disjointComponents:
    cycle_detection(dc, lockDependencyRelation)

print("\nPotential Deadlocks:")
for potentialDeadlock in potentialDeadlocks:
    for d in potentialDeadlock:
        d.print()
        print(end=" ")
    print()
