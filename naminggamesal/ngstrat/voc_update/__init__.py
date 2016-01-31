#!/usr/bin/python
import random
import numpy as np
from importlib import import_module

#####Classe de base
vu_class={
	'imitation':'imitation.Imitation',
	'minimal':'minimal.Minimal',
	'minimalsynonly':'minimal.MinimalSynOnly',
	'minimalpone':'minimal.MinimalPOne',
	'minimalpone2':'minimal.MinimalPOne2',
	'minimalcatnew':'minimal.MinimalCatNew',

	'BLIS':'lateral_inhib.BasicLateralInhibition',
	'BLIS_epirob':'lateral_inhib.BLISEpirob',
	'BLIS_heareronly':'lateral_inhib.BasicLateralInhibitionHearerOnly',
	'BLIS_heareronlyfailure':'lateral_inhib.BasicLateralInhibitionHearerOnlyFailure',
	'ILIS':'lateral_inhib.InterpolatedLateralInhibition',

	'frequency':'frequency.Frequency'
}

def get_voc_update(vu_type='imitation', **vu_cfg2):
	tempstr = vu_type
	if tempstr in vu_class.keys():
		tempstr = vu_class[tempstr]
	templist = tempstr.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	return getattr(_tempmod,tempclass)(**vu_cfg2)

class VocUpdate(object):
	def __init__(self):
		pass

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.finish_update()

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.finish_update()
