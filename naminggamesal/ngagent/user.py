from . import Agent


color_fail = "\x1b[31m" #'\033[93m'
color_success = "\x1b[32m" #'\033[92m'
color_normal = "\x1b[0m"

class UserAgent(Agent):
	def update_hearer(self,ms,w,mh,bool_succ,context=[]):
		print 'your role was: HEARER'
		if bool_succ:
			color = color_success
		else:
			color = color_fail
		print color,'MEANING:',ms,',WORD:',w,'SUCCESS:',bool_succ,color_normal
		Agent.update_hearer(self,ms=ms,w=w,mh=mh,bool_succ=bool_succ,context=context)


	def update_speaker(self,ms,w,mh,bool_succ,context=[]):
		print 'your role was: SPEAKER'
		if bool_succ:
			color = color_success
		else:
			color = color_fail
		print color,'MEANING:',ms,',WORD:',w,'SUCCESS:',bool_succ,color_normal
		Agent.update_speaker(self,ms=ms,w=w,mh=mh,bool_succ=bool_succ,context=context)

	def warn(self,role):
		print ''
		print 'New interaction:'
		if role == 'speaker':
			print 'You have been chosen as SPEAKER for this interaction'
		elif role == 'hearer':
			print 'You have been chosen as HEARER for this interaction'