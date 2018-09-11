import networkx as nx
import math
import numpy as np

def balanced_tree_N(r,N):
	h = math.ceil( np.log(r*N-N+1)/np.log(r) -1 )
	Nbis = int((r**(h+1)-1)/(r-1))
	G = nx.balanced_tree(r,h)
	for n in range(N,Nbis):
		G.remove_node(n)
	return G
