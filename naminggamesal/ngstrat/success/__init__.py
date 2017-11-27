from .global_success import GlobalSuccess
from .communicative_success import CommunicativeSuccess
from .alignment_success import AlignmentSuccess

from importlib import import_module

#####Classe de base
success_class={
	'global':'global_success.GlobalSuccess',
	'global_norandom':'global_success.GlobalSuccessNoRandom',
	'global_epirob':'global_success.GlobalSuccessEpirob',
	'global_restrictive':'global_success.GlobalSuccessRestrictive',
	'communicative':'communicative_success.CommunicativeSuccess',
	'communicative_max':'communicative_success.CommunicativeSuccessMax',
	'alignment':'alignment_success.AlignmentSuccess',
}

def get_success(success_type='global', **success_cfg2):
	tempint = success_type
	if tempint in list(success_class.keys()):
		tempint = success_class[tempint]
	templist = tempint.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	tempsucc = getattr(_tempmod,tempclass)(**success_cfg2)
	return tempsucc

