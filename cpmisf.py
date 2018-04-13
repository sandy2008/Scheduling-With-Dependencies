from random import randint
from sys import argv
PEnum = 4

class Task:
	def __init__(self, task, CP):
		self.task= task
		self.CP = CP

def LoadSample(fname):
	f = open(fname,'r')
	head = f.readline().split()
	n = int(head[0])
	taskpre = [[] for i in range(n+1)]
	tasktime = []
	f.readline()
	for l in f:
		l = l.split()
		tasktime.append(int(l[1]))
		i = 3
		while i < len(l):
			taskpre[int(l[0])-1].append(int(l[i]))
			i += 1
	return (tasktime,taskpre)

def CPMISF(inst):
	undonetask= list(range(1,len(inst[0])))
	readytask = []
	finishtask = [0]
	starttime = [0]*(len(inst[0])-1)
	endtime = [0]*(len(inst[0])-1)
	parents = [[]for i in range((len(inst[0]))-1)]
	petime = [0]*PEnum
	CP = FindCP(inst)
	result = [] #First Digit is Task, 2nd is Machine
	
	
	for i in range ((len(inst[0]))-1):
		parents[i] = inst[1][i]
	
	while len(undonetask) > 0:
		for j in undonetask:
			if set(inst[1][j-1]).issubset(set(finishtask)) and j not in finishtask:
				readytask.append(j)
				readytask = list(set(readytask))
				if len(readytask) > 0:
					readytask.sort(key = lambda s:CP[s-1],reverse=True)
		pemin = petime.index(min(petime))
		if parents[readytask[0]-1] != []:
			for p in parents[readytask[0]-1]:
				starttime[readytask[0]-1] = max(starttime[readytask[0]-1],endtime[p-1], petime[pemin])
		else:
			starttime[readytask[0]-1] = petime[pemin]
		endtime[readytask[0]-1] = starttime[readytask[0]-1] + inst[0][readytask[0]-1]
		petime[pemin] = endtime[readytask[0]-1]
		result.append([pemin + 1,readytask[0]])
		undonetask.remove(readytask[0])
		finishtask.append(readytask[0])
		readytask.remove(readytask[0])
	print(max(CalcFit(inst,result)))


def CalcFit(inst, gene):
	petime = [0]*PEnum
	starttime = [0]*(len(inst[0])-1)
	endtime = [0]*(len(inst[0])-1)
	parents = [[]for i in range((len(inst[0]))-1)]
	for i in range ((len(inst[0]))-1):
		parents[i] = inst[1][i]
	
	
	genelist = []
	now = 0
	for s in range(len(gene)):
		genelist.append(gene[s][1])	
		
	for t in genelist:
		for p in parents[t-1]:
			if p!= 0:
				starttime[t-1] = max(starttime[t-1],endtime[p-1], petime[gene[now][0]-1])
			else:
				starttime[t-1] = petime[gene[now][0]-1]
		endtime[t-1] = starttime[t-1] + inst[0][t-1]
		petime[gene[now][0]-1] = endtime[t-1]
		now += 1
	return(petime)

def FindCP(inst):
	CP = [0]*len(inst[0])
	TaskNext =  [[] for i in range(len(inst[0]))]
	for t in range(len(inst[0])):
		for k in inst[1][t]:
			if k != 0 and t != 0:
				TaskNext[k-1].append(t)
				
	CPboolean = [False]*(len(inst[0])-1)
	CPboolean.append(True)
	
	while CPboolean != [True]*len(inst[0]):
		for t in range(len(inst[0])-1):
			if (sum(CPboolean[g] for g in TaskNext[t]) == len(TaskNext[t])):
				if TaskNext[t] != []:
					CP[t] = max(CP[g] for g in TaskNext[t]) + inst[0][t]
				else:
					CP[t] = inst[0][t]
				CPboolean[t] = True
	print (max(CP))
	return CP
				
					
	




inst = LoadSample(argv[-1])

CPMISF(inst)