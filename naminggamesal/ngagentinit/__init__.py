#!/usr/bin/python
import random
import numpy as np
from importlib import import_module


agent_init_class={
	'agent_init':'agent_init.AgentInit',
	'own_words':'own_conventions.OwnWordsInit',
	'converged':'converged.Converged',
	'converged_halfline':'converged.ConvergedHalfLine',
	'oneuser':'oneuser.OneUser',
	'onedifferent':'oneuser.OneDifferent',
	'oneuser_noninteractive':'oneuser.OneUserNonInteractive',
	'mixed_pop':'mixed_pop.MixedPop',
	'mixed_pop_proba':'mixed_pop.MixedPopProba',
}

def get_agent_init(agent_init_type='agent_init', **agent_init_cfg2):
	tempap = agent_init_type
	if tempap in list(agent_init_class.keys()):
		tempap = agent_init_class[tempap]
	templist = tempap.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	tempap = getattr(_tempmod,tempclass)(**agent_init_cfg2)
	return tempap
