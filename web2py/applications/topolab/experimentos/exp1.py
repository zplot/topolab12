# -*- coding: utf-8 -*-

try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx



'''

G = nx.path_graph(8)
E = nx.path_graph(30)

# two separate graphs
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
nx.draw(G, ax=ax1)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
nx.draw(G, ax=ax2)

plt.show()

'''



'''
G = nx.path_graph(21)
fig1 = plt.figure()
nx.draw(G)
plt.show()
'''

G = nx.path_graph(21)
# fig1 = plt.figure()
nx.draw(G)
plt.show()