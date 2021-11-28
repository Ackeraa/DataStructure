from collections import defaultdict
import networkx as nx
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt

G = nx.MultiDiGraph()
width = defaultdict(int)
depth = {}

class Node:

    def __init__(self, text, color="blue"):
        self._text = text
        self.depth = None
        self.width = None
        G.add_node(self, color=color, size=len(text) * 300)

    def connect(self, node, label="", color="black"):
        G.add_edge(self, node, label=label, color=color)

    def __str__(self):
        return self._text

def traverse():
    for node in G.nodes(data=True):
        print(node[1]['color'], node[0])

    for edge in G.edges(data=True):
        print(edge[0], edge[1], edge[2])

def dfs(u, fa, d):
    width[d] += 1
    u.depth = d
    u.width = width[d]
    for v in u.children.values():
        if v != fa:
            dfs(v, u, d + 1)

def draw(root, fname='a'):
    pos = nx.spring_layout(G)
    #pos = nx.planar_layout(G)
    #pos = nx.spiral_layout(G)

    dfs(root, -1, 1)
    pos = {}
    for node in G.nodes(data=True):
        pos[node[0]] = (node[0].width / (width[node[0].depth] + 1) , 1 / node[0].depth)

    plt.figure(1)
    nx.draw(G, pos, with_labels=True, font_weight='bold', connectionstyle='arc3, rad = 0.1',\
            node_color=[x[1]['color'] for x in G.nodes(data=True)],\
            node_size=[x[1]['size'] for x in G.nodes(data=True)],\
            edge_color=[x[2]['color'] for x in G.edges(data=True)])

    edge_labels=dict([((u,v,),d['label'])
                 for u,v,d in G.edges(data=True)])

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3)

    plt.savefig(fname + ".eps", dpi=600, format="eps")

if __name__ == '__main__':
    node = Node('11')
    node1 = Node('2', 'red')
    node.connect(node1, '1->2')
    node1.connect(node, '2->1')
    draw(node)
