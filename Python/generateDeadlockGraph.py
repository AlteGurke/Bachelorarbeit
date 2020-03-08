import sys
import networkx as nx
import matplotlib.pyplot as plt
import ntpath

import magiclock_main as magiclock

traceFilename = sys.argv[1]
deadlockGraph = magiclock.get_potential_Deadlock_Nodes(traceFilename)

DG = nx.DiGraph()
for e in deadlockGraph.edges:
    DG.add_edge(e.fromNode, e.toNode, label=e.text)

plt.subplot(121)
plt.title("Potential Deadlocks found in: " + ntpath.basename(traceFilename))

pos = nx.spring_layout(DG)
nx.draw(DG, pos, with_labels=True, font_weight='bold', connectionstyle='arc3, rad = 0.1', node_size=1000)

edge_labels = nx.get_edge_attributes(DG,'label')
nx.draw_networkx_edge_labels(DG, pos, edge_labels, label_pos=0.3)

plt.show()