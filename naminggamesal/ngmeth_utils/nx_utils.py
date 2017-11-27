import networkx as nx
import numpy as np

#from ..ngmeth import tempentropy

import additional.custom_func as custom_func
import additional.custom_graph as custom_graph
############################################################################
#NETWORKX TOOLS

def build_nx_graph(agent_list):
	if not hasattr(pop._agentlist[0]._vocabulary,'_content'):
		raise ValueError('this measure is not implemented for this type of vocabulary')
	G = nx.Graph()
	for ag in agent_list:
		tempm = np.sum(ag._vocabulary.get_content())
		G.add_node(ag._id,size=1.-(tempentropy(ag._vocabulary.get_M()-tempm, ag._vocabulary.get_W()-tempm)/tempentropy(ag._vocabulary.get_M(), ag._vocabulary.get_W())))
	list_length = len(agent_list)
	for i in range(list_length):
		agent1 = agent_list[i]
		for j in range(i+1,list_length):
			agent2 = agent_list[j]
			tempmat = np.multiply(agent1._vocabulary.get_content(), agent2._vocabulary.get_content())
			tempm = np.sum(tempmat)
			weight = 1.-(tempentropy(agent1._vocabulary.get_M()-tempm, agent1._vocabulary.get_W()-tempm)/tempentropy(agent1._vocabulary.get_M(), agent1._vocabulary.get_W()))
			if weight != 0:
				G.add_edge(agent1._id,agent2._id,weight=weight)
	return G

def degree_distrib(pop,**kwargs):
	G = build_nx_graph(pop._agentlist)
	return custom_graph.CustomGraph(nx.degree_histogram(G))

def edgevalue_distrib(pop,**kwargs):
	G = build_nx_graph(pop._agentlist)
	dict_XY = {}
	for ed in G.edges:
		weight = ed['weight']
		if weight in list(dict_XY.keys()):
			dict_XY[weight] += 1
		else:
			dict_XY[weight] = 1
	for key, value in list(dict_XY.items()):
		X.append(key)
		Y.append(value)
	return custom_graph.CustomGraph(X=X,Y=Y)


