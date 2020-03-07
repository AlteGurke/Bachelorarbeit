import networkx as nx
import matplotlib.pyplot as plt

import magiclock_main as magiclock


deadlockGraph = magiclock.get_potential_Deadlock_Nodes()

DG = nx.DiGraph()
for e in deadlockGraph.edges:
    DG.add_edge(e.fromNode, e.toNode)

plt.subplot(121)
nx.draw(DG, with_labels=True, font_weight='bold')

plt.show()