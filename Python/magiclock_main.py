import sys

import magiclockLib.magiclock as magiclock


class PotentialDeadlockNode(object):
    def __init__(self, name):
        self.name = name


class PotentialDeadlockEdge(object):
    def __init__(self, fromNode, toNode):
        self.fromNode = fromNode
        self.toNode = toNode


class PotentialDeadlockGraph(object):
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges


def get_potential_Deadlock_Nodes():
    nodes = []
    edges = set()
    graph = PotentialDeadlockGraph(nodes, edges)

    for potentialDeadlock in potentialDeadlocks:
        for d in potentialDeadlock:
            node = PotentialDeadlockNode(d.threadName)
            if node not in nodes:
                nodes.append(PotentialDeadlockNode(d.threadName))

        for i in range(len(potentialDeadlock) - 1):
            edges.add(PotentialDeadlockEdge(nodes[i], nodes[i + 1]))
        edges.add(PotentialDeadlockEdge(nodes[-1], nodes[0]))

    return graph

potentialDeadlocks = magiclock.find_potential_Deadlocks(sys.argv[1])
