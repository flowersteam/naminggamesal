from builtins import range
import copy

class HoledRange(object):
	def __init__(self,range_max):
		self.range_obj = range(range_max)
		self.consider = []
		self.discard = []
		self.counter = None

	@classmethod
	def from_range(cls,range_obj):
		assert range_obj.start == 0
		assert range_obj.step == 1
		return cls(range_max=len(range_obj))

	def __len__(self):
		return len(self.range_obj)

	def __contains__(self,elt):
		if elt in self.range_obj:
			if elt in self.discard:
				return False
			else:
				return True
		elif elt in self.consider:
			return True
		else:
			return False

	def __iter__(self):
		self.counter = None
		return self

	def __next__(self):
		if self.counter is None:
			if len(self.range_obj) > 0:
				self.counter = 0
			else:
				raise StopIteration
		elif self.counter == len(self.range_obj)-1:
			self.counter = None
			raise StopIteration
		else:
			self.counter += 1
		if self.counter in self.discard:
			return self.replace(self.counter)
		else:
			return self.counter

	next = __next__  # python2.x compatibility.

	def __delitem__(self, key):
		self.remove(self[key])

	def __getitem__(self, key):
		ans = self.range_obj[key]
		if ans in self.discard:
			return self.replace(ans)
		else:
			return ans

	def __setitem__(self, key, value):
		raise NotImplementedError

	def append(self,elt):
		assert elt not in self
		new_limit = len(self.range_obj)
		if elt > new_limit:
			self.consider.append(elt)
			if new_limit not in self:
				self.discard.append(new_limit)
			else:
				self.consider.remove(new_limit)
		elif elt < new_limit:
			self.discard.remove(elt)
			if new_limit in self:
				self.consider.remove(new_limit)
			else:
				self.discard.append(new_limit)
		self.range_obj = range(len(self.range_obj)+1)

	def remove(self,elt):
		assert elt in self
		new_limit = len(self.range_obj)-1
		if elt > new_limit:
			self.consider.remove(elt)
			if new_limit not in self:
				self.discard.remove(new_limit)
			else:
				self.consider.append(new_limit)
		elif elt < new_limit:
			self.discard.append(elt)
			if new_limit in self:
				self.consider.append(new_limit)
			else:
				self.discard.remove(new_limit)
		self.range_obj = range(len(self.range_obj)-1)



	def replace(self,elt):
		assert elt in self.discard
		for i in range(len(self.discard)):
			if self.discard[i] == elt:
				return self.consider[i]

	def __str__(self):
		return str(self.range_obj)+' , discard: '+str(self.discard)+' , consider: '+str(self.consider)

	def __repr__(self):
		return str(self)

	def extend(self,other):
		for elt in other:
			if elt not in self:
				self.append(elt)

	def __add__(self,other):
		ans = copy.deepcopy(self)
		ans.extend(other)
		return ans

class HoledRangeOld(object):
	def __init__(self,range_max):
		self.range_obj = range(range_max)
		self.replace = {}

	def __len__(self):
		return len(self.range_obj)

	def __contains__(self,elt):
		if elt in range(self.range_max):
			if elt in self.replace.keys():
				return False
			else:
				return True
		elif elt in self.replace.values():
			return True
		else:
			return False

	def __iter__(self):
		return self

	def __next__(self):
		try:
			ans = self.range_obj.__next__()
		except StopIteration:
			raise
		except:
			ans = self.range_obj.next()
		if ans in self.replace.keys():
			return self.replace[ans]
		else:
			return ans

	next = __next__  # python2.x compatibility.

	def __delitem__(self, key):
		self.remove(self[key])

	def __getitem__(self, key):
		ans = self.range_obj[key]
		if ans in self.replace.keys():
			return self.replace[ans]
		else:
			return ans

	def __setitem__(self, key, value):
		raise NotImplementedError

	def append(self,elt):
		assert elt not in self
		if len(self.range_obj) not in self:
			if elt > len(self.range_obj):
				self.replace[len(self.range_obj)] = elt
			elif elt < len(self.range_obj):
				self.replace[len(self.range_obj)] = self.replace[elt]
		else:
			arg = [k for k in self.replace.keys() if self.replace[k] == len(self.range_obj) ][0]
			if elt > len(self.range_obj):
				self.replace[arg] = elt
			elif elt < len(self.range_obj):
				self.replace[arg] = self.replace[elt]
			elif elt == len(self.range_obj):
				del self.replace[arg]
		self.range_obj = range(len(self.range_obj)+1)

	def remove(self,elt):
		if elt in self:
			if elt < len(self.range_obj)-1:
				self.replace[elt] = len(self.range_obj)-1
			elif elt > len(self.range_obj)-1:
				self.replace[elt] = len(self.range_obj)-1
			self.range_obj = range(len(self.range_obj)-1)
		else:
			raise ValueError(str(elt)+' not in holed range.')


