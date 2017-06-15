from . import Environment
import random
import networkx as nx
from ..ngmeth import srtheo_local

from additional import networkx_graphs as nx_g

class GraphEnv(Environment):

	def __init__(self, graph_type='complete_graph', graph_args={'n':1},uuid_instance=None, W=None):
		self.core_meanings = [0]
		try:
			self.meaning_graph = getattr(nx,graph_type)(**graph_args)
		except:
			self.meaning_graph = getattr(nx_g,graph_type)(**graph_args)
		self.meaning_graph_pos = nx.spring_layout(self.meaning_graph)
		if W is None:
			W = len(self.meaning_graph.nodes())
		self.W = W
		self.M = len(self.meaning_graph.nodes())


	def update_agent(self,agent,ms,w,mh,context=[]):
		m_list = self.meaning_graph.neighbors(ms)+[ms]
		agent._vocabulary.discover_meanings(m_list=m_list)
		#agent._vocabulary.discover_words(m_list=w_list)
		for mem_key in agent._memory.keys():
			if hasattr(agent._memory[mem_key],'discover_meanings'):
				agent._memory[mem_key].discover_meanings(m_list=m_list)

	def init_agent(self,agent):
		agent._vocabulary.discover_meanings(m_list=self.core_meanings)
		agent._vocabulary.discover_words(w_list=range(self.W))
		for mem_key in agent._memory.keys():
			if hasattr(agent._memory[mem_key],'discover_meanings'):
				agent._memory[mem_key].discover_meanings(m_list=self.core_meanings)
			if hasattr(agent._memory[mem_key],'discover_words'):
				agent._memory[mem_key].discover_words(w_list=range(self.W))


class GraphEnvSuccessExplore(GraphEnv):

	def update_agent(self,agent,ms,w,mh,context=[]):
		if srtheo_local(agent,m=ms) >= 1.:
			GraphEnv.update_agent(self,agent=agent,ms=ms,w=w,mh=mh,context=context)
		else:
			agent._vocabulary.discover_meanings(m_list=[ms])
			for mem_key in agent._memory.keys():
				if hasattr(agent._memory[mem_key],'discover_meanings'):
					agent._memory[mem_key].discover_meanings(m_list=[ms])
