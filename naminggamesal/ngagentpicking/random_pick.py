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
		speaker_id = speaker.get_id()
		j = random.randint(0,len(pop._agentlist)-2)
		if pop.get_index_from_id(speaker_id) <= j:
			j += 1
		hearer = pop._agentlist[j]
		#hearer.warn(role='hearer')
		return hearer