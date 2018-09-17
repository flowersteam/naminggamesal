from . import BaseWordChoice

class WordPreference(BaseWordChoice):

	def pick_w(self,m,voc,mem,context=[]):
		if m in voc.get_known_meanings():
			if m in list(mem['prefered words'].keys()):
				w = mem['prefered words'][m]
				if w not in voc.get_known_words(m=m):
					w = voc.get_random_known_w(m=m)
			else:
				w = voc.get_random_known_w(m=m)
		elif voc.get_unknown_words():
			w = voc.get_new_unknown_w()
		else:
			w = voc.get_random_known_w(option='min')
		return w

class PlaySmart(WordPreference):

	def __init__(self, *args, **kwargs):
		WordPreference.__init__(self,memory_policies=[{'mem_type':'wordpreference_smart'}],*args,**kwargs)


class PlayLast(WordPreference):

	def __init__(self, *args, **kwargs):
		WordPreference.__init__(self,memory_policies=[{'mem_type':'wordpreference_last'}],*args,**kwargs)

class PlayFirst(WordPreference):

	def __init__(self, *args, **kwargs):
		WordPreference.__init__(self,memory_policies=[{'mem_type':'wordpreference_first'}],*args,**kwargs)

