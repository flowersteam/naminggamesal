#!/usr/bin/python
import random
import numpy as np
from importlib import import_module
import copy

#####Classe de base
vu_class={
	'imitation':'imitation.Imitation',
	'imitation_permutation':'imitation.ImitationPermutation',

	'minimal':'minimal.Minimal',
	'minimal_keeppreference':'minimal.MinimalKeepPreference',
	'minimalsynonly':'minimal.MinimalSynOnly',
	'minimalsynonly_membased':'minimal.MinimalSynOnlyMemBased',
	'minimalhomreduc':'minimal.MinimalHomonymyReduc',
	'minimalpone':'minimal.MinimalPOne',
	'minimalpone2':'minimal.MinimalPOne2',
	'minimalcatnew':'minimal.MinimalCatNew',
	'minimalbeta':'minimal.MinimalBeta',

	'BLIS':'lateral_inhib.BasicLateralInhibition',
	'BLISsynonly':'lateral_inhib.BLISSynOnly',
	'BLIS_epirob':'lateral_inhib.BLISEpirob',
	'BLIS_heareronly':'lateral_inhib.BasicLateralInhibitionHearerOnly',
	'BLIS_heareronlyfailure':'lateral_inhib.BasicLateralInhibitionHearerOnlyFailure',
	'ILIS':'lateral_inhib.InterpolatedLateralInhibition',

	'frequency':'frequency.Frequency',

	'acceptance':'acceptance.AcceptancePolicy',
	'acceptance_beta':'acceptance.AcceptanceBeta',
	'acceptance_betadecrease':'acceptance.AcceptanceBetaDecrease',
	'acceptance_tsmax':'acceptance.AcceptanceTSMax',
	'acceptance_tsmax_new':'acceptance.AcceptanceTSMaxNew',
	'acceptance_tsmax_new_membasedchoices':'acceptance.AcceptanceTSMaxNewMemBasedChoices',
	'acceptance_entropy':'acceptance.AcceptanceEntropy',
	'acceptance_entropybeta':'acceptance.AcceptanceEntropyBeta',
	'acceptance_vocrelatedentropy':'acceptance.AcceptanceVocRelatedEntropy',
	'acceptance_vocrelatedentropybeta':'acceptance.AcceptanceVocRelatedEntropyBeta',
}

def get_voc_update(vu_type='imitation', **vu_cfg2):
	tempstr = vu_type
	if tempstr in list(vu_class.keys()):
		tempstr = vu_class[tempstr]
	templist = tempstr.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	return getattr(_tempmod,tempclass)(**vu_cfg2)

class VocUpdate(object):
	def __init__(self,memory_policies=[],mem_policy=None,broadcasting=False):
		self.memory_policies = copy.deepcopy(memory_policies)
		if mem_policy is not None:
			self.memory_policies.append(mem_policy)
		self.broadcasting = broadcasting

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.finish_update()

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.finish_update()
