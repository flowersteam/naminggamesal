#!/usr/bin/python

from . import Topology
import random
import numpy as np
import networkx as nx

##########
class FullGraph(Topology):
	def __init__(self,pop):
		self.graph = nx.Graph()
		for ag in pop._agentlist:
			self.graph.add_node(ag._id)
		list_length = len(pop._agentlist)
		for i in range(list_length):
			agent1 = pop._agentlist[i]
			for j in range(i+1,list_length):
				agent2 = pop._agentlist[j]
				self.graph.add_edge(agent1._id,agent2._id)

	def get_neighbor(self,speaker,pop):
		speaker_id = speaker.get_id()
		hearer_id = random.choice(self.graph.neighbors(speaker_id))
		return pop._agentlist[pop.get_index_from_id(hearer_id)]

	def add_agent(self, agent, pop):
		self.graph.add_node(agent._id)
		list_length = len(pop._agentlist)
		for j in range(list_length-1):
			agent2 = pop._agentlist[j]
			self.graph.add_edge(agent._id,agent2._id)

	def rm_agent(self, agent, pop):
		self.graph.remove_node(agent._id)
