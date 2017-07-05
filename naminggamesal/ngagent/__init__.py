#!/usr/bin/python

from .agent import Agent

import random
import numpy as np
from importlib import import_module


agent_class={
	'agent':'agent.Agent',
	'user':'user.UserAgent',
}



def get_agent(agent_type=None, **agent_cfg2):
	if agent_type is None:
		return Agent(**agent_cfg2)
	tempagent = agent_type
	if tempagent in agent_class.keys():
		tempagent = agent_class[tempagent]
	templist = tempagent.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	tempagent = getattr(_tempmod,tempclass)(**agent_cfg2)
	return tempagent
