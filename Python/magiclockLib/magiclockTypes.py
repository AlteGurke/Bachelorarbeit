from collections import defaultdict

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