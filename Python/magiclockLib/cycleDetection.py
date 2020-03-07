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


def reportCycle(potentialDeadlocks, o, size, equCycle, Group):
    if size == len(o):
        potentialDeadlocks.append(equCycle.copy())
    else:
        for d in Group[o[size]]:
            equCycle.append(d)
            reportCycle(potentialDeadlocks, o, size + 1, equCycle, Group)
            equCycle.remove(d)


def DFS_Traverse(potentialDeadlocks, i, s, d, k, isTraversed, Di, Group):
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
                    reportCycle(potentialDeadlocks, o, 0, equCycle, Group)
                else:
                    isTraversed[j] = True
                    DFS_Traverse(potentialDeadlocks, i, s, di, k, isTraversed, Di, Group)
                    isTraversed[j] = False


def cycle_detection(potentialDeadlocks, dc, D):
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
            DFS_Traverse(potentialDeadlocks, t, s, d, D.threads, isTraversed, Di, Group)
