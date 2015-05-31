#!/usr/bin/python
# -*- coding: latin-1 -*-
import random
from ngvoc import *

class Strategy(object):
	def __new__(cls,strat):
		_strattype=strat["strattype"]
		if "M" in strat.keys():
			M=strat["M"]
		if _strattype=="naive":
			tempstrat=object.__new__(StratNaive)
			tempstrat._strattype=_strattype
			return tempstrat
		if _strattype=="naivereal":
			tempstrat=object.__new__(StratNaiveReal)
			tempstrat._strattype=_strattype
			return tempstrat
		elif _strattype=="naivedestructive":
			tempstrat=object.__new__(StratNaiveDestructive)
			tempstrat._strattype=_strattype
			return tempstrat
		elif _strattype=="delaunay":
			tempstrat=object.__new__(StratDelaunay)
			tempstrat.threshold_explo=0.9
			tempstrat._strattype=_strattype
			return tempstrat
		elif _strattype=="delaunayreal":
			tempstrat=object.__new__(StratDelaunayReal)
			tempstrat.threshold_explo=0.9
			tempstrat._strattype=_strattype
			return tempstrat
		elif _strattype[:13]=="delaunaymodif":
			tempstrat=object.__new__(StratDelaunay)
			tempstrat.threshold_explo=float(_strattype[13:])
			tempstrat._strattype=_strattype
			return tempstrat
		elif _strattype=="decisionvector":
			tempstrat=object.__new__(StratDecisionVector)
			tempstrat.decision_vector=strat["decvec"]
			tempstrat._strattype=_strattype
			return tempstrat
		elif _strattype=="decisionvectorreal":
			tempstrat=object.__new__(StratDecisionVectorReal)
			tempstrat.decision_vector=strat["decvec"]
			tempstrat._strattype=_strattype
			return tempstrat
		elif _strattype=="dichotomie":
			tempstrat=object.__new__(StratDecisionVector)
			tempdecvec=np.zeros(M+1)
			tempdecvec[0]=1
			temp_param=2
			for i in range(1,int(np.log(M)/np.log(temp_param))+1):
				tempdecvec[-1-M/(temp_param**i)]=1
			tempstrat.decision_vector=tempdecvec
			tempstrat._strattype=_strattype
			return tempstrat
		elif _strattype[:17]=="dichotomierapport":
			tempstrat=object.__new__(StratDecisionVector)
			tempdecvec=np.zeros(M+1)
			tempdecvec[0]=1
			temp_param=float(_strattype[17:])
			for i in range(1,int(np.log(M)/np.log(temp_param))+1):
				tempdecvec[-1-int(M/(temp_param**i))]=1
			tempstrat.decision_vector=tempdecvec
			tempstrat._strattype=_strattype
			return tempstrat
		elif _strattype=="lastresult":
			tempstrat=object.__new__(StratLastResult)
			tempstrat._strattype=_strattype
			return tempstrat
		elif _strattype=="lastresultreal":
			tempstrat=object.__new__(StratLastResultReal)
			tempstrat._strattype=_strattype
			return tempstrat
		else:
			print "type de strategie non existant"	

	def get_strattype(self):
		return self._strattype

	def visual(self,voc,mem={},vtype=None,iter=100):
		if vtype=="pick_mw":
			tempmat=np.matrix(np.zeros((voc._M,voc._W)))
			for i in range(0,iter):
				lst=self.pick_mw(voc,mem)
				j=lst[0]
				k=lst[1]
				tempmat[j,k]+=1
			plt.title("pick_mw")
			plt.pcolor(np.array(tempmat),vmin=0)


##################################### STRATEGIE NAIVE DESTRUCTIVE################################
class StratNaiveDestructive(Strategy):

	def guess_m(self,w,voc,mem):
		if w in voc.get_known_words():
			tempindexm=random.randint(0,len(voc.get_known_meanings(w))-1)
			m=voc.get_known_meanings(w)[tempindexm]
		else:
			m=random.randint(0,voc.get_M()-1)
		return m

	def pick_w(self,m,voc,mem):
		if m in voc.get_known_meanings():
			tempindexw=random.randint(0,len(voc.get_known_words(m))-1)
			w=voc.get_known_words(m)[tempindexw]
		else:
			w=random.randint(0,voc.get_W()-1)
		return w


	def pick_mw(self,voc,mem):
		m=random.randint(0,voc.get_M()-1)
		w=self.pick_w(m,voc,mem)
		return([m,w])

	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def init_memory(self,voc):
		return {}

		##################################### STRATEGIE NAIVE########################################
class StratNaive(Strategy):

	def guess_m(self,w,voc,mem):
		if w in voc.get_known_words():
			tempindexm=random.randint(0,len(voc.get_known_meanings(w))-1)
			m=voc.get_known_meanings(w)[tempindexm]
		else:
			if len(voc.get_known_meanings())<voc._M:
				m=voc.get_new_unknown_m()
			else:
				m=random.randint(0,voc.get_M()-1)
		return m

	def pick_w(self,m,voc,mem):
		if m in voc.get_known_meanings():
			w=voc.get_random_known_w(m)
		else:
			w=voc.get_new_unknown_w()
		return w


	def pick_mw(self,voc,mem):
		m=random.randint(0,voc.get_M()-1)
		w=self.pick_w(m,voc,mem)
		return([m,w])

	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def init_memory(self,voc):
		return {}

		##################################### STRATEGIE NAIVE REELLE########################################
class StratNaiveReal(Strategy):

	def guess_m(self,w,voc,mem):
		if w in voc.get_known_words():
			tempindexm=random.randint(0,len(voc.get_known_meanings(w))-1)
			m=voc.get_known_meanings(w)[tempindexm]
		else:
			if len(voc.get_known_meanings())<voc._M:
				m=voc.get_new_unknown_m()
			else:
				m=random.randint(0,voc.get_M()-1)
		return m

	def pick_w(self,m,voc,mem):
		if m in voc.get_known_meanings():
			w=voc.get_random_known_w(m)
		else:
			w=voc.get_new_unknown_w()
		return w


	def pick_mw(self,voc,mem):
		m=random.randint(0,voc.get_M()-1)
		w=self.pick_w(m,voc,mem)
		return([m,w])

	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
		
	def init_memory(self,voc):
		return {}

##################################### STRATEGIE DELAUNAY########################################
class StratDelaunay(StratNaive):

	def pick_mw(self,voc,mem):
		test1=self.get_success_rate_over_known_meanings(voc,mem)>self.threshold_explo
		test2=len(voc.get_known_meanings())==voc._M
		test3=len(voc.get_known_meanings())==0
		if (test1 or test3) and (not test2):
			m=voc.get_new_unknown_m()
			w=voc.get_new_unknown_w()
		else:
			m=voc.get_random_known_m()
			w=self.pick_w(m,voc,mem)
		return([m,w])


	def update_hearer(self,ms,w,mh,voc,mem):
		if ms==mh:
			mem["success_m"][mh]+=1
		else:
			mem["fail_m"][mh]+=1
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		if ms==mh:
			mem["success_m"][ms]+=1
		else:
			mem["fail_m"][ms]+=1
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def init_memory(self,voc):
		mem={}
		mem["success_m"]=[0]*voc._M
		mem["fail_m"]=[0]*voc._M
		return mem

	def get_success_rate_over_known_meanings(self,voc,mem):
		succ_sum=0
		fail_sum=0
		for m in voc.get_known_meanings():
			succ_sum+=mem["success_m"][m]
			fail_sum+=mem["fail_m"][m]
		if succ_sum==0:
			return 0
		else:
			return succ_sum/float(fail_sum+succ_sum)




##################################### STRATEGIE DELAUNAY REELLE########################################
class StratDelaunayReal(StratNaive):

	def pick_mw(self,voc,mem):
		test1=self.get_success_rate_over_known_meanings(voc,mem)>self.threshold_explo
		test2=len(voc.get_known_meanings())==voc._M
		test3=len(voc.get_known_meanings())==0
		if (test1 or test3) and (not test2):
			m=voc.get_new_unknown_m()
			w=voc.get_new_unknown_w()
		else:
			m=voc.get_random_known_m()
			w=self.pick_w(m,voc,mem)
		return([m,w])


	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			mem["success_m"][mh]+=1
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
		else:
			mem["fail_m"][mh]+=1

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			mem["success_m"][ms]+=1
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
		else:
			mem["fail_m"][ms]+=1
		
	def init_memory(self,voc):
		mem={}
		mem["success_m"]=[0]*voc._M
		mem["fail_m"]=[0]*voc._M
		return mem

	def get_success_rate_over_known_meanings(self,voc,mem):
		succ_sum=0
		fail_sum=0
		for m in voc.get_known_meanings():
			succ_sum+=mem["success_m"][m]
			fail_sum+=mem["fail_m"][m]
		if succ_sum==0:
			return 0
		else:
			return succ_sum/float(fail_sum+succ_sum)




################################### STRATEGIE DECISION VECTOR #########################################""

#Ne pas oublier STRATTYPE, NAME et l'initialisation dans la classe strategy

class StratDecisionVector(StratNaive):

	def pick_mw(self,voc,mem):
		Mtemp=len(voc.get_known_meanings())
		tirage=random.random()
		if tirage<self.decision_vector[Mtemp]:
			m=voc.get_new_unknown_m()
		else:
			m=voc.get_random_known_m()
		w=self.pick_w(m,voc,mem)
		return([m,w])


	def init_memory(self,voc):
		return {}
################################### STRATEGIE DECISION VECTOR REELLE#########################################""

#Ne pas oublier STRATTYPE, NAME et l'initialisation dans la classe strategy

class StratDecisionVectorReal(StratNaiveReal):

	def pick_mw(self,voc,mem):
		Mtemp=len(voc.get_known_meanings())
		tirage=random.random()
		if tirage<self.decision_vector[Mtemp]:
			m=voc.get_new_unknown_m()
		else:
			m=voc.get_random_known_m()
		w=self.pick_w(m,voc,mem)
		return([m,w])


	def init_memory(self,voc):
		return {}





##################################### STRATEGIE LAST_RESULT########################################
class StratLastResult(StratNaive):

	def pick_mw(self,voc,mem):
		test2=len(voc.get_known_meanings())==voc._M
		test3=len(voc.get_known_meanings())==0
		#if (mem["result"] or test3) and (not test2):
		if mem["result"]:
			m=voc.get_new_unknown_m()
			w=voc.get_new_unknown_w()
		else:
			m=voc.get_random_known_m()
			w=self.pick_w(m,voc,mem)
		return([m,w])


	def update_hearer(self,ms,w,mh,voc,mem):
		if ms==mh:
			mem["result"]=1
		else:
			mem["result"]=0
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		if ms==mh:
			mem["result"]=1
		else:
			mem["result"]=0
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def init_memory(self,voc):
		mem={}
		mem["result"]=1
		return mem

##################################### STRATEGIE LAST_RESULT REELLE########################################
class StratLastResultReal(StratNaiveReal):

	def pick_mw(self,voc,mem):
		test2=len(voc.get_known_meanings())==voc._M
		test3=len(voc.get_known_meanings())==0
		if (mem["result"] or test3) and (not test2):
			m=voc.get_new_unknown_m()
			w=voc.get_new_unknown_w()
		else:
			m=voc.get_random_known_m()
			w=self.pick_w(m,voc,mem)
		return([m,w])


	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			mem["result"]=1
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
		else:
			mem["result"]=0

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			mem["result"]=1
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
		else:
			mem["result"]=0

	def init_memory(self,voc):
		mem={}
		mem["result"]=1
		return mem

################################### TEMPLATE NEW STRATEGY #########################################""

#Ne pas oublier STRATTYPE, NAME et l'initialisation dans la classe strategy

# class StratNAME(Strategy):

# 	def guess_m(self,w,voc,mem):
# 		return m


# 	def pick_w(self,m,voc,mem):
# 		return w


# 	def pick_mw(self,voc,mem):
# 		return([m,w])


# 	def update_hearer(self,ms,w,mh,voc,mem):


# 	def update_speaker(self,ms,w,mh,voc,mem):


# 	def init_memory(self,voc):
# 		return mem