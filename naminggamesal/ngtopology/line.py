#!/usr/bin/python

from .full_graph import FullGraph
import random
import numpy as np
import networkx as nx

##########
class Line(FullGraph):
	def __init__(self,pop):
		agent_list = pop._agentlist
		self.graph = nx.Graph()
		for ag in agent_list:
			self.graph.add_node(ag._id)
		list_length = len(pop._agentlist)
		for i in range(list_length-1):
			agent1 = agent_list[i]
			agent2 = agent_list[i+1]
			self.graph.add_edge(agent1._id,agent2._id)


	def add_agent(self, agent, pop):
		self.graph.add_node(agent._id)
		ind = pop.get_index_from_id(agent._id)
		id2 = pop._agentlist[id-1]._id
		self.graph.add_edge(agent._id,id2)

class Circle(Line):
	def __init__(self,pop):
		Line.__init__(self,pop)
		agent_list = pop._agentlist
		agent1 = agent_list[0]
		agent2 = agent_list[-1]
		self.graph.add_edge(agent1._id,agent2._id)

	def add_agent(self, agent, pop):
		self.graph.add_node(agent._id)
		ind = pop.get_index_from_id(agent._id)
		id2 = pop._agentlist[id-1]._id
		id3 = pop._agentlist[(id+1)%len(pop._agentlist)]._id
		self.graph.add_edge(agent._id,id2)
		self.graph.add_edge(agent._id,id3)
