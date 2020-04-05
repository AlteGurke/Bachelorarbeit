import magiclockLib.magiclockTypes as magiclockTypes

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
    initClassification = magiclockTypes.InitClassification()
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
    lockClassification = magiclockTypes.LockClassification()
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


def get_LockDependencyRelation_For(D, cyclicSet):
    lockDependencyRelation = magiclockTypes.LockDependencyRelation()

    for d in D.lockDependencies:
        if d.lockObjectName in cyclicSet:
            lockDependencyRelation.add(d)

    return lockDependencyRelation


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

    return lockClassification, projectedD