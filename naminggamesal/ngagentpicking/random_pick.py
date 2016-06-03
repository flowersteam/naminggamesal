#!/usr/bin/python

from . import AgentPick
import random
import numpy as np

##########
class RandomPick(AgentPick):
	def pick_speaker(self, pop):
		return random.choice(pop._agentlist)

	def pick_hearer(self, speaker, pop):
		speaker_id = speaker.get_id()
		j = random.randint(0,len(pop._agentlist)-2)
		if pop.get_index_from_id(speaker_id) <= j:
			j += 1
		return pop._agentlist[j]
