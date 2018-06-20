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
		self.stdvec = [0 for _ in range(len(Y))]
		self.minvec = [np.nan for _ in range(len(Y))]
		self.maxvec = [np.nan for _ in range(len(Y))]

		if X is None:
			self._X = [list(range(len(Y)))]
		else:
			self._X = [X]


		self.extensions=["eps","png","pdf"]

		for key,value in kwargs.items():
			setattr(self,key,value)

		self.stdvec=[self.stdvec]
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
		if len(path)!=0:
			out_path=path[0]
		else:
			out_path=""

		self.save(out_path)
		self.draw()
		for extension in self.extensions:
			plt.savefig(out_path+self.filename+"."+extension,format=extension,bbox_inches='tight')
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
		current_palette = sns.color_palette()
		for i in range(0,len(self._Y)):

			Xtemp = copy.deepcopy(self._X[i])
			Ytemp = copy.deepcopy(self._Y[i])
			stdtemp = copy.deepcopy(self.stdvec[i])
			mintemp = copy.deepcopy(self.minvec[i])
			maxtemp = copy.deepcopy(self.maxvec[i])
			if self.sort: # WARNING!!!!! No X value should appear 2 times -> bug to solve
				tempdic = {}
				for j in range(0,len(Xtemp)):
					tempdic[Xtemp[j]]=[Ytemp[j],stdtemp[j]]
				temptup=sorted(tempdic.items())
				for j in range(0,len(temptup)):
					Xtemp[j]=temptup[j][0]
					Ytemp[j]=temptup[j][1][0]
					stdtemp[j]=temptup[j][1][1]
			base_line = plt.plot(Xtemp,Ytemp,**self.Yoptions[i])[0]
			if self.loglog:
				plt.xscale('symlog',basex=self.loglog_basex)
				plt.yscale('symlog',basex=self.loglog_basey)
			elif self.semilog:
				plt.xscale('symlog',basex=self.loglog_basex)
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
				if 'color' in list(self.Yoptions[i].keys()):
					plt.fill_between(Xtemp,Ytempmin,Ytempmax, alpha=self.alpha,**self.Yoptions[i])
				else:
					plt.fill_between(Xtemp,Ytempmin,Ytempmax, alpha=self.alpha, facecolor=base_line.get_color(), **self.Yoptions[i])

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
			handles, labels = plt.gca().get_legend_handles_labels()
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
			if ax.get_xlim()[1]-ax.get_xlim()[0] > 1000:
				mkfunc = lambda x, pos: '%1.fM' % (x * 1e-6) if x >= 1e6 else '%1.fK' % (x * 1e-3) if x >= 1e3 else '%1.f' % x
				mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
				ax.xaxis.set_major_formatter(mkformatter)

		if hasattr(self,'yticker') and self.yticker:
			ax = matplotlib.pyplot.gca()
			if ax.get_ylim()[1]-ax.get_ylim()[0] > 1000:
				mkfunc = lambda x, pos: '%1.fM' % (x * 1e-6) if x >= 1e6 else '%1.fK' % (x * 1e-3) if x >= 1e3 else '%1.f' % x
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
		self.__dict__.update(in_dict)

	def add_graph(self,other_graph):
		self._X = self._X + copy.deepcopy(other_graph._X)
		self._Y = self._Y + copy.deepcopy(other_graph._Y)
		self.Yoptions = self.Yoptions + copy.deepcopy(other_graph.Yoptions)
		self.stdvec = self.stdvec + copy.deepcopy(other_graph.stdvec)
		self.minvec = self.minvec + copy.deepcopy(other_graph.minvec)
		self.maxvec = self.maxvec + copy.deepcopy(other_graph.maxvec)
		
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

	def complete_with(self,other_graph, mix=True, remove_duplicates=False):
		for i in range(0,len(self._X)):
			if mix and not self._X[-1]<other_graph._X[0]:
				X = copy.deepcopy(self._X[i])
				Y = copy.deepcopy(self._Y[i])
				stdvec = copy.deepcopy(self.stdvec[i])
				minvec = copy.deepcopy(self.minvec[i])
				maxvec = copy.deepcopy(self.maxvec[i])
				Xind = 0
				oXind = 0
				self._X[i] = []
				self._Y[i] = []
				self.stdvec[i] = []
				self.minvec[i] = []
				self.maxvec[i] = []
				while Xind < len(X) and oXind < len(other_graph._X[i]):
					if X[Xind] < other_graph._X[i][oXind]:
						self._X[i].append(X[Xind])
						self._Y[i].append(Y[Xind])
						self.stdvec[i].append(stdvec[Xind])
						self.minvec[i].append(minvec[Xind])
						self.maxvec[i].append(maxvec[Xind])
						Xind += 1
					elif X[Xind] > other_graph._X[i][oXind]:
						self._X[i].append(other_graph._X[i][oXind])
						self._Y[i].append(other_graph._Y[i][oXind])
						self.stdvec[i].append(other_graph.stdvec[i][oXind])
						self.minvec[i].append(other_graph.minvec[i][oXind])
						self.maxvec[i].append(other_graph.maxvec[i][oXind])
						oXind += 1
					else:
						self._X[i].append(X[Xind])
						self._Y[i].append(Y[Xind])
						self.stdvec[i].append(stdvec[Xind])
						self.minvec[i].append(minvec[Xind])
						self.maxvec[i].append(maxvec[Xind])
						Xind += 1
						oXind += 1
			else:
				self._X[i]=list(copy.deepcopy(self._X[i]))+list(copy.deepcopy(other_graph._X[i]))
				self._Y[i]=list(copy.deepcopy(self._Y[i]))+list(copy.deepcopy(other_graph._Y[i]))
				self.stdvec[i]=list(copy.deepcopy(self.stdvec[i]))+list(copy.deepcopy(other_graph.stdvec[i]))
				self.minvec[i]=list(copy.deepcopy(self.minvec[i]))+list(copy.deepcopy(other_graph.minvec[i]))
				self.maxvec[i]=list(copy.deepcopy(self.maxvec[i]))+list(copy.deepcopy(other_graph.maxvec[i]))
			if remove_duplicates:
				X = copy.deepcopy(self._X[i])
				Y = copy.deepcopy(self._Y[i])
				stdvec = copy.deepcopy(self.stdvec[i])
				minvec = copy.deepcopy(self.minvec[i])
				maxvec = copy.deepcopy(self.maxvec[i])
				self._X[i] = []
				self._Y[i] = []
				self.stdvec[i] = []
				self.minvec[i] = []
				self.maxvec[i] = []
				for j in range(len(X)):
					if X[j] not in self._X[i]:
						self._X[i].append(X[j])
						self._Y[i].append(Y[j])
						self.stdvec[i].append(stdvec[j])
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

	def merge(self):
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
		#Xtemp = []
		self.Yoptions=[self.Yoptions[0]]
		self.std=1
		Ydict = {}
		for j in range(len(self._Y)):
			for i in range(len(self._Y[j])):
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


		#max_length = max([len(self._Y[j]) for j in range(len(self._Y))])
		#for i in range(max_length):
		#	Ylist = [Ycopy[j][i] for j in range(len(Ycopy)) if len(Ycopy[j])>i]
		#	Ytemp.append(np.mean(Ylist))
		#	stdtemp.append(np.std(Ylist))
		#	#Ytemp.append(np.mean(list(Yarray[:,i])))
		#	#stdtemp.append(np.std(list(Yarray[:,i])))
		self._Y = [Ytemp]
		self.stdvec = [stdtemp]
		self.minvec = [mintemp]
		self.maxvec = [maxtemp]
		self._X = [Xlist]
		self.modif_time = time.strftime("%Y%m%d%H%M%S", time.localtime())



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
		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())


	def func_of(self,graph2):
		newgraph=copy.deepcopy(self)
		for i in range(0,len(newgraph._X)):
			newgraph._X[i]=graph2._Y[i]
			newgraph.xlabel=graph2.title[6:]
			newgraph.title=self.title+"_func_of_"+newgraph.xlabel
		return newgraph
