#!/usr/bin/python
import sys
try:
	if sys.version_info.major == 2:
		import Tkinter
	else:
		import tkinter
except ImportError:
	import matplotlib
	matplotlib.use('Agg')
	sys.stderr.write('Tkinter not installed, loading matplotlib and pyplot with Agg backend\n')

import matplotlib.pyplot as plt
import time
import numpy as np
import pickle
import copy

import matplotlib
import seaborn as sns
#sns.set(rc={'image.cmap': 'Purples_r'})

sns.set_style('darkgrid')
matplotlib.rcParams['pdf.fonttype'] = 42  #set font type to true type, avoids possible incompatibility while submitting papers
matplotlib.rcParams['ps.fonttype'] = 42

def load_graph(filename):
	with open(filename, 'rb') as fichier:
		mon_depickler=pickle.Unpickler(fichier)
		tempgr=mon_depickler.load()
	return tempgr


class CustomGraph(object):
	def __init__(self,Y=None,X=None,**kwargs):
		self.keepwinopen = 0
		self.sort = 1
		self.filename = "graph"+time.strftime("%Y%m%d%H%M%S", time.localtime())
		if "filename" in list(kwargs.keys()):
			self.filename = kwargs["filename"]
		self.title = self.filename
		self.xlabel = "X"
		self.ylabel = "Y"
		self.alpha = 0.3

		self.Yoptions = [{}]
		self.legendoptions = {}
		self.legend_permut = []

		self.loglog = False
		self.semilog = False
		self.loglog_basex = 10
		self.loglog_basey = 10

		self.xmin = None
		self.xmax = None
		self.ymin = None
		self.ymax = None

		self.std = False
		self.std_mode = 'std'

		self.xticker = True
		self.yticker = True

		if Y is None:
			self._Y = []
		else:
			self._Y = [Y]
		self.stdvec = [np.nan for _ in range(len(Y))]
		self.all_data = [ [] for _ in Y ]
		self.minvec = [np.nan for _ in Y]
		self.maxvec = [np.nan for _ in Y]

		if X is None:
			self._X = [list(range(len(Y)))]
		else:
			self._X = [X]


		self.extensions=["eps","png","pdf"]

		self.symlog = True

		for key,value in kwargs.items():
			setattr(self,key,value)

		self.stdvec=[self.stdvec]
		self.all_data=[self.all_data]
		self.minvec=[self.minvec]
		self.maxvec=[self.maxvec]

		self.init_time=time.strftime("%Y%m%d%H%M%S", time.localtime())
		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())

	def show(self):
		plt.ion()
		#fig = plt.gcf()
		self.draw()
		plt.show()
		#return fig

	def save(self,*path):
		if path:
			out_path=path[0]
		else:
			out_path="graphs/"
		with open(out_path+self.filename+".b", 'wb') as fichier:
			mon_pickler=pickle.Pickler(fichier)
			mon_pickler.dump(self)

	def write_files(self,*path):
		backend = plt.get_backend()
		plt.switch_backend('Agg')
		try:
			if len(path)!=0:
				out_path=path[0]
			else:
				out_path=""
			self.save(out_path)
			self.draw()
			for extension in self.extensions:
				plt.savefig(out_path+self.filename+"."+extension,format=extension,bbox_inches='tight')
		finally:
			plt.switch_backend(backend)

	def savefig(self,*args,**kwargs):
		backend = plt.get_backend()
		plt.switch_backend('Agg')
		try:
			self.draw()
			plt.savefig(*args,**kwargs)
		finally:
			plt.switch_backend(backend)

	def draw(self):

		#colormap=['blue','black','green','red','yellow','cyan','magenta']
		#colormap=['black','green','red','blue','yellow','cyan','magenta']
		#colormap=['blue','red','green','black','yellow','cyan','magenta']
		#colormap=['black','green','blue','red','yellow','cyan','magenta']
		#colormap=['darkolivegreen','green','darkorange','red','yellow','cyan','magenta']


		#plt.figure()
		plt.ion()
		plt.cla()
		plt.clf()
		handles = []
		current_palette = sns.color_palette()
		for i in range(0,len(self._Y)):

			Xtemp = copy.copy(self._X[i])
			Ytemp = copy.copy(self._Y[i])
			stdtemp = copy.copy(self.stdvec[i])
			mintemp = copy.copy(self.minvec[i])
			maxtemp = copy.copy(self.maxvec[i])
			if self.sort: # WARNING!!!!! No X value should appear 2 times -> bug to solve
				tempdic = {}
				for j in range(0,len(Xtemp)):
					tempdic[Xtemp[j]]=[Ytemp[j],stdtemp[j]]
				temptup=sorted(tempdic.items())
				for j in range(0,len(temptup)):
					Xtemp[j]=temptup[j][0]
					Ytemp[j]=temptup[j][1][0]
					stdtemp[j]=temptup[j][1][1]
			if hasattr(self,'plot_style') and self.plot_style == 'scatter':
				base_line = plt.scatter(Xtemp,Ytemp,**self.Yoptions[i])
			else:
				base_line = plt.plot(Xtemp,Ytemp,**self.Yoptions[i])[0]
			handles.append(base_line)
			if not hasattr(self,'symlog') or self.symlog:
				log_str = 'symlog'
			else:
				log_str = 'log'
			if self.loglog:
				plt.xscale(log_str,basex=self.loglog_basex)
				plt.yscale(log_str,basex=self.loglog_basey)
			elif self.semilog:
				plt.xscale(log_str,basex=self.loglog_basex)
			if self.std:
				Ytempmin = [0 for _ in Ytemp]
				Ytempmax = [0 for _ in Ytemp]
				for j in range(0,len(Ytemp)):
					if not hasattr(self,'std_mode') or self.std_mode == 'std':
						Ytempmax[j]=Ytemp[j]+stdtemp[j]
						Ytempmin[j]=Ytemp[j]-stdtemp[j]
					elif self.std_mode == 'minmax':
						Ytempmax[j] = maxtemp[j]
						Ytempmin[j] = mintemp[j]
				if 'alpha' in list(self.Yoptions[i]):
					alpha = self.alpha*self.Yoptions[i]['alpha']
					Yopt = copy.deepcopy(self.Yoptions[i])
					del Yopt['alpha']
				else:
					alpha = self.alpha
					Yopt = copy.deepcopy(self.Yoptions[i])
				for opt in ['marker','linestyle']:
					if opt in Yopt:
						del Yopt[opt]
				try:
					if 'color' in list(self.Yoptions[i].keys()):
						plt.fill_between(Xtemp,Ytempmin,Ytempmax, alpha=alpha,**Yopt)
					else:
						plt.fill_between(Xtemp,Ytempmin,Ytempmax, alpha=alpha, facecolor=base_line.get_color(), **Yopt)
				except:
					pass

		plt.xlabel(self.xlabel)
		if self.ylabel is not None and (len(self.ylabel)<4 or (self.ylabel[:2]=='$\\' and self.ylabel[-1] == '$')):
			plt.ylabel(self.ylabel,rotation=0)
		else:
			plt.ylabel(self.ylabel)
		plt.title(self.title)

		if self.xmin is not None:
			plt.xlim(xmin=self.xmin)
		if self.xmax is not None:
			plt.xlim(xmax=self.xmax)
		if self.ymin is not None:
			plt.ylim(ymin=self.ymin)
		if self.ymax is not None:
			plt.ylim(ymax=self.ymax)


		if self.legend_permut != []:
			labels = self.legendoptions['labels']
			handles2, labels2 = [], []
			for tr in range(len(self.legend_permut)):
				handles2.append(handles[self.legend_permut[tr]])
				#handles2[self.legend_permut[tr]] = handles[tr]
				labels2.append(labels[self.legend_permut[tr]])
				#labels2[self.legend_permut[tr]] = labels[tr]
			if handles2 == []:
				handles2 = handles

			legend_opt = copy.deepcopy(self.legendoptions)
			if 'labels' in list(self.legendoptions.keys()):
				del legend_opt['labels']
			labels3 = [l for l in labels2 if l != '_nolegend_' ]
			handles3 = [h for h,l in zip(handles2,labels2) if l != '_nolegend_' ]
			plt.legend(handles=handles3, labels=labels3, **legend_opt)
		elif self.legendoptions != {}:
			if 'labels' in self.legendoptions.keys():
				#handles, labels = plt.gca().get_legend_handles_labels()
				legend_opt = copy.deepcopy(self.legendoptions)
				labels = self.legendoptions['labels']
				handles2 = [h for h,l,lo in zip(handles,labels,self.legendoptions['labels']) if lo != '_nolegend_' ]
				labels2 = [lo for h,l,lo in zip(handles,labels,self.legendoptions['labels']) if lo != '_nolegend_' ]
				if 'labels' in list(self.legendoptions.keys()):
					del legend_opt['labels']
				plt.legend(handles=handles2, labels=labels2, **legend_opt)
			else:
				plt.legend(**self.legendoptions)

		#plt.legend(bbox_to_anchor=(0,0,0.55,0.8))
		#plt.legend(bbox_to_anchor=(0,0,0.5,1))
		#
		#plt.legend(bbox_to_anchor=(0,0,1,0.7))
		#plt.legend(bbox_to_anchor=(0,0,1,0.54))
		if hasattr(self, 'fontsize'):
			matplotlib.rcParams['font.size'] = self.fontsize
			matplotlib.rcParams['xtick.labelsize'] = self.fontsize
			matplotlib.rcParams['ytick.labelsize'] = self.fontsize
			matplotlib.rcParams['axes.titlesize'] = self.fontsize
			matplotlib.rcParams['axes.labelsize'] = self.fontsize
			matplotlib.rcParams['legend.fontsize'] = self.fontsize
		if hasattr(self, 'rcparams'):
			for key,value in self.rcparams:
				matplotlib.rcParams[key] = value


		if hasattr(self,'xticker') and self.xticker:
			ax = matplotlib.pyplot.gca()
			if self.loglog:
				xticks = [ax.get_xlim()[0]]
				base = self.loglog_basex
				exponent = int(np.log(xticks[0])/np.log(base))
				step = int(xticks[0]/(base**exponent))
				if step*(base**exponent) == xticks[0]:
					step += 1
				while xticks[-1] < ax.get_xlim()[1]:
					if step >= base:
						step = 1
						exponent += 1
					xticks.append(step*base**exponent)
					step += 1
				plt.xticks(xticks)
			elif ax.get_xlim()[1]-ax.get_xlim()[0] > 1000:
				mkfunc = lambda x, pos: '%1.fM' % (x * 1e-6) if x >= 1e6 else '%1.fk' % (x * 1e-3) if x >= 1e3 else '%1.f' % x
				mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
				ax.xaxis.set_major_formatter(mkformatter)

		if hasattr(self,'yticker') and self.yticker:
			ax = matplotlib.pyplot.gca()
			if self.loglog:
				yticks = [ax.get_ylim()[0]]
				base = self.loglog_basey
				exponent = int(np.log(yticks[0])/np.log(base))
				step = int(yticks[0]/(base**exponent))
				if step*(base**exponent) == yticks[0]:
					step += 1
				while yticks[-1] < ax.get_ylim()[1]:
					if step >= base:
						step = 1
						exponent += 1
					yticks.append(step*base**exponent)
					step += 1
				plt.yticks(yticks)
			elif ax.get_ylim()[1]-ax.get_ylim()[0] > 1000:
				mkfunc = lambda x, pos: '%1.fM' % (x * 1e-6) if x >= 1e6 else '%1.fk' % (x * 1e-3) if x >= 1e3 else '%1.f' % x
				mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
				ax.yaxis.set_major_formatter(mkformatter)

		plt.draw()

	def add_option(self,idx=None,**options):
		if idx is None:
			for yopt in self.Yoptions:
				yopt.update(**copy.deepcopy(options))
		else:
			self.Yoptions[idx].update(**copy.deepcopy(options))

	def __add__(self,other_graph):
		g = copy.deepcopy(self)
		if other_graph is not None:
			g.add_graph(other_graph)
		return g

	def __setstate__(self, in_dict):
		if not 'minvec' in list(in_dict.keys()):
			in_dict['minvec'] = [[np.nan for _ in X] for X in in_dict['_X']]
		if not 'maxvec' in list(in_dict.keys()):
			in_dict['maxvec'] = [[np.nan for _ in X] for X in in_dict['_X']]
		if not 'all_data' in list(in_dict.keys()):
			in_dict['all_data'] = [[[] for _ in X] for X in in_dict['_X']]
		self.__dict__.update(in_dict)

	def add_graph(self,other_graph):
		self._X = self._X + copy.copy(other_graph._X)
		self._Y = self._Y + copy.copy(other_graph._Y)
		self.Yoptions = self.Yoptions + copy.deepcopy(other_graph.Yoptions)
		self.stdvec = self.stdvec + copy.copy(other_graph.stdvec)
		self.all_data = self.all_data + copy.deepcopy(other_graph.all_data)
		self.minvec = self.minvec + copy.copy(other_graph.minvec)
		self.maxvec = self.maxvec + copy.copy(other_graph.maxvec)

		label_in_1 = 'labels' in self.legendoptions
		label_in_2 = 'labels' in other_graph.legendoptions
		if label_in_1 or label_in_2:
			if not label_in_1:
				self_labels = ['' for _ in self._X]
				other_labels = other_graph.legendoptions['labels']
			elif not label_in_2:
				self_labels = self.legendoptions['labels']
				other_labels = ['' for _ in other_graph._X]
			else:
				self_labels = self.legendoptions['labels']
				other_labels = other_graph.legendoptions['labels']
			self.legendoptions['labels'] = self_labels + copy.deepcopy(other_labels)

		if self.xmin is None or other_graph.xmin is None:
			self.xmin = None
		else:
			self.xmin = min(self.xmin,other_graph.xmin)
		if self.ymin is None or other_graph.ymin is None:
			self.ymin = None
		else:
			self.ymin = min(self.ymin,other_graph.ymin)
		if self.xmax is None or other_graph.xmax is None:
			self.xmax = None
		else:
			self.xmax = max(self.xmax,other_graph.xmax)
		if self.ymax is None or other_graph.ymax is None:
			self.ymax = None
		else:
			self.ymax = max(self.ymax,other_graph.ymax)

	def remove_graph(self,ind=-1):
		for v_a in ['_X','_Y','Yoptions','stdvec','all_data','minvec','maxvec']:
			v = getattr(self,v_a)
			v2 = v[:ind]
			if ind not in [-1,len(v)]:
				v2 += v[ind+1:]
			setattr(self,v_a,v2)

	def complete_with(self,other_graph, mix=True, remove_duplicates=False):
		other_graph = copy.deepcopy(other_graph)
		for i in range(0,len(self._X)):
			if mix and not self._X[-1]<other_graph._X[0]:
				X = copy.copy(self._X[i])
				Y = copy.copy(self._Y[i])
				stdvec = copy.copy(self.stdvec[i])
				all_data = copy.deepcopy(self.all_data[i])
				minvec = copy.copy(self.minvec[i])
				maxvec = copy.copy(self.maxvec[i])
				Xind = 0
				oXind = 0
				self._X[i] = []
				self._Y[i] = []
				self.stdvec[i] = []
				self.all_data[i] = []
				self.minvec[i] = []
				self.maxvec[i] = []
				while Xind < len(X) and oXind < len(other_graph._X[i]):
					if X[Xind] < other_graph._X[i][oXind]:
						self._X[i].append(X[Xind])
						self._Y[i].append(Y[Xind])
						self.stdvec[i].append(stdvec[Xind])
						self.all_data[i].append(all_data[Xind])
						self.minvec[i].append(minvec[Xind])
						self.maxvec[i].append(maxvec[Xind])
						Xind += 1
					elif X[Xind] > other_graph._X[i][oXind]:
						self._X[i].append(other_graph._X[i][oXind])
						self._Y[i].append(other_graph._Y[i][oXind])
						self.stdvec[i].append(other_graph.stdvec[i][oXind])
						self.all_data[i].append(other_graph.all_data[i][oXind])
						self.minvec[i].append(other_graph.minvec[i][oXind])
						self.maxvec[i].append(other_graph.maxvec[i][oXind])
						oXind += 1
					else:
						self._X[i].append(X[Xind])
						self._Y[i].append(Y[Xind])
						self.stdvec[i].append(stdvec[Xind])
						self.all_data[i].append(all_data[Xind])
						self.minvec[i].append(minvec[Xind])
						self.maxvec[i].append(maxvec[Xind])
						Xind += 1
						oXind += 1
			else:
				self._X[i]=list(copy.copy(self._X[i]))+list(copy.copy(other_graph._X[i]))
				self._Y[i]=list(copy.copy(self._Y[i]))+list(copy.copy(other_graph._Y[i]))
				self.stdvec[i]=list(copy.copy(self.stdvec[i]))+list(copy.deepcopy(other_graph.stdvec[i]))
				self.all_data[i]=list(copy.deepcopy(self.all_data[i]))+list(copy.deepcopy(other_graph.all_data[i]))
				self.minvec[i]=list(copy.copy(self.minvec[i]))+list(copy.copy(other_graph.minvec[i]))
				self.maxvec[i]=list(copy.copy(self.maxvec[i]))+list(copy.copy(other_graph.maxvec[i]))
			if remove_duplicates:
				X = copy.copy(self._X[i])
				Y = copy.copy(self._Y[i])
				stdvec = copy.copy(self.stdvec[i])
				all_data = copy.deepcopy(self.all_data[i])
				minvec = copy.copy(self.minvec[i])
				maxvec = copy.copy(self.maxvec[i])
				self._X[i] = []
				self._Y[i] = []
				self.stdvec[i] = []
				self.all_data[i] = []
				self.minvec[i] = []
				self.maxvec[i] = []
				for j in range(len(X)):
					if X[j] not in self._X[i]:
						self._X[i].append(X[j])
						self._Y[i].append(Y[j])
						self.stdvec[i].append(stdvec[j])
						self.all_data[i].append(all_data[j])
						self.minvec[i].append(minvec[j])
						self.maxvec[i].append(maxvec[j])
		if self.xmin is None or other_graph.xmin is None:
			self.xmin = None
		else:
			self.xmin = min(self.xmin,other_graph.xmin)
		if self.ymin is None or other_graph.ymin is None:
			self.ymin = None
		else:
			self.ymin = min(self.ymin,other_graph.ymin)
		if self.xmax is None or other_graph.xmax is None:
			self.xmax = None
		else:
			self.xmax = max(self.xmax,other_graph.xmax)
		if self.ymax is None or other_graph.ymax is None:
			self.ymax = None
		else:
			self.ymax = max(self.ymax,other_graph.ymax)
		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())

#	def complete_with(self,other_graph):
#		for i in range(0,len(self._X)):
#			self._X[i]=range(0, len(self._X[i])+len(other_graph._X[i]))
#			self._Y[i]=list(copy.deepcopy(self._Y[i]))+list(copy.deepcopy(other_graph._Y[i]))
#			self.stdvec[i]=list(copy.deepcopy(self.stdvec[i]))+list(copy.deepcopy(other_graph.stdvec[i]))
#		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())

	def get_alldata_graph(self,lim_m=None):
		ans = copy.deepcopy(self)
		ans._Y[0] = [self.all_data[0][i][0] for i in range(len(self.all_data[0]))]
		ans.stdvec=[[0 for _ in range(len(self._X[0]))]]
		if lim_m is None:
			lim_m = len(self.all_data[0][0])
		else:
			lim_m = min(len(self.all_data[0][0]),lim_m)
		for m in range(1,lim_m):
		    g1 = copy.deepcopy(self)
		    g1._Y[0] = [self.all_data[0][i][m] for i in range(len(self.all_data[0]))]
		    g1.stdvec=[[0 for _ in range(len(self._X[0]))]]
		    ans.add_graph(g1)
		return ans

	def merge(self,keep_all_data=True):
		#Yarray=np.array(self._Y)
		#stdarray=np.array(self.stdvec)
		Xcopy = copy.deepcopy(self._X)
		Ycopy = copy.deepcopy(self._Y)
		stdcopy = copy.deepcopy(self.stdvec)
		mincopy = copy.deepcopy(self.minvec)
		maxcopy = copy.deepcopy(self.maxvec)
		stdtemp = []
		mintemp = []
		maxtemp = []
		Ytemp = []
		alldatatemp = []
		#Xtemp = []
		self.Yoptions=[self.Yoptions[0]]
		self.std=1
		Ydict = {}
		for j in range(len(self._Y)):
			for i in range(len(self._Y[j])):
				if self._Y[j][i] is not None:
					if Xcopy[j][i] in list(Ydict.keys()):
						Ydict[Xcopy[j][i]].append(Ycopy[j][i])
					else:
						Ydict[Xcopy[j][i]] = [Ycopy[j][i]]
		Xlist = list(Ydict.keys())
		Xlist.sort()
		for x in Xlist:
			Ylist = Ydict[x]
			Ytemp.append(np.mean(Ylist))
			stdtemp.append(np.std(Ylist))
			mintemp.append(np.min(Ylist))
			maxtemp.append(np.max(Ylist))
			alldatatemp.append(copy.deepcopy(Ylist))


		#max_length = max([len(self._Y[j]) for j in range(len(self._Y))])
		#for i in range(max_length):
		#	Ylist = [Ycopy[j][i] for j in range(len(Ycopy)) if len(Ycopy[j])>i]
		#	Ytemp.append(np.mean(Ylist))
		#	stdtemp.append(np.std(Ylist))
		#	#Ytemp.append(np.mean(list(Yarray[:,i])))
		#	#stdtemp.append(np.std(list(Yarray[:,i])))
		if keep_all_data:
			self.all_data = [alldatatemp]
		#else:
		#	self.all_data = [[[] for _ in X] for X in self._X]
		self._Y = [Ytemp]
		self.stdvec = [stdtemp]
		self.minvec = [mintemp]
		self.maxvec = [maxtemp]
		self._X = [Xlist]
		self.modif_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
		self.regularize()


	def wise_merge(self):
		param_list=[]
		for i in range(len(self.Yoptions)):
			param_list.append(self.Yoptions[i]["label"])
		param_values={}
		for ind,param in enumerate(param_list):
			if param not in list(param_values.keys()):
				param_values[param]=copy.deepcopy(self)
				param_values[param]._X=[self._X[ind]]
				param_values[param]._Y=[self._Y[ind]]
				param_values[param].Yoptions=[self.Yoptions[ind]]
			else:
				tempgraph=copy.deepcopy(self)
				tempgraph._X=[self._X[ind]]
				tempgraph._Y=[self._Y[ind]]
				tempgraph.Yoptions=[self.Yoptions[ind]]
				param_values[param].add_graph(copy.deepcopy(tempgraph))
		tempgraph=copy.deepcopy(self)
		tempgraph._X=[]
		tempgraph._Y=[]
		tempgraph.Yoptions=[]
		tempgraph.stdvec=[]
		tempgraph.minvec=[]
		tempgraph.maxvec=[]
		for key in list(param_values.keys()):
			param_values[key].merge()
			tempgraph.add_graph(param_values[key])
		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())
		return tempgraph

	def empty(self):
		self._Y=[]
		self._X=[]
		self.Yoptions=[]
		self.stdvec=[]
		self.minvec=[]
		self.maxvec=[]
		self.all_data=[]
		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())

	def empty_copy(self):
		ans = copy.deepcopy(self)
		ans.empty()
		return ans

	def regularize(self):
		nb_curves = len(self._Y)
		for attr in ['_X','Yoptions','minvec','stdvec','maxvec','all_data']:
			if len(getattr(self,attr)) >= nb_curves:
				setattr(self,attr,getattr(self,attr)[:nb_curves])
			else:
				val_attr = getattr(self,attr)
				for i in list(range(len(getattr(self,attr)),nb_curves)):
					val_attr.append([])
				setattr(self,attr,val_attr)
		for i in list(range(nb_curves)):
			nb2 = len(self._Y[i])
			for attr in ['_X','Yoptions','minvec','stdvec','maxvec','all_data']:
				if len(getattr(self,attr)[i]) >= nb2:
					attr_val = getattr(self,attr)
					attr_val[i] = getattr(self,attr)[i][:nb2]
					setattr(self,attr,attr_val)
				else:
					if attr == '_X':
						if len(self._X[i]):
							last = self._X[i][-1]
						else:
							last = -1
						self._X[i] += [ 1+last+j for j in list(range(nb2-len(self._X[i])))]
					elif attr == 'Yoptions':
						self.Yoptions[i] =  {}
					elif attr == 'all_data':
						self.all_data[i] += [ [] for j in list(range(nb2-len(self.all_data[i])))]
					else:
						val_attr = getattr(self,attr)
						val_attr[i] += [ np.nan for j in list(range(nb2-len(getattr(self,attr)[i])))]
						setattr(self,attr,val_attr)

	def func_of(self,graph2):
		newgraph=copy.deepcopy(self)
		for i in range(0,len(newgraph._X)):
			newgraph._X[i]=graph2._Y[i]
			newgraph.xlabel=graph2.title[6:]
			newgraph.title=self.title+"_func_of_"+newgraph.xlabel
		return newgraph
