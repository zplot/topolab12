# -*- coding: utf-8 -*-


from matplotlib.figure import Figure
import networkx as nx

fig = Figure()
ax = fig.add_axes()
G = nx.house_graph()
nx.draw(G, ax=ax)

