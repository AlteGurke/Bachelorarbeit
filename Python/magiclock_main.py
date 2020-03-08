import sys

import magiclockLib.magiclock as magiclock


class PotentialDeadlockEdge(object):
    def __init__(self, fromNode, toNode, text):
        self.fromNode = fromNode
        self.toNode = toNode
        self.text = text

    def print(self):
        print("From: " + self.fromNode)
        print("To: " + self.toNode)
        print("Text: " + self.text)


class PotentialDeadlockGraph(object):
    def __init__(self, edges):
        self.edges = edges

    def print(self):
        print("Edges:")
        for e in self.edges:
            e.print()


def get_potential_Deadlock_Nodes(traceFilename):
    edges = []
    graph = PotentialDeadlockGraph(edges)

    potentialDeadlocks = magiclock.find_potential_Deadlocks(traceFilename)

    for potentialDeadlock in potentialDeadlocks:
        for i in range(len(potentialDeadlock) - 1):
            edges.append(PotentialDeadlockEdge(potentialDeadlock[i].lockObjectName, potentialDeadlock[i + 1].lockObjectName, potentialDeadlock[i + 1].threadName))
        edges.append(PotentialDeadlockEdge(potentialDeadlock[-1].lockObjectName, potentialDeadlock[0].lockObjectName, potentialDeadlock[0].threadName))

    return graph

if __name__ == '__main__':
    magiclock.find_potential_Deadlocks(sys.argv[1])
