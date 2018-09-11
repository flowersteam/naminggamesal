#!/usr/bin/python

from . import AgentPick
import random
import numpy as np

##########
class RandomPick(AgentPick):
	def pick_speaker(self, pop):
		speaker = random.choice(pop._agentlist)
		#speaker.warn(role='speaker')
		return speaker

	def pick_hearer(self, speaker, pop):
		ind = random.choice(range(len(pop._agentlist)-1))
		hearer = pop._agentlist[ind]
		if hearer == speaker:
			hearer = pop._agentlist[-1]
		return hearer
