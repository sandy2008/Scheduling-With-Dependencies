from random import randint, random, seed, shuffle
from sys import argv

#Parameters
SEED = 0
PS = 200
IT = 50
CP = 1.0
MP = 0.05

PEnum = 8

class Gene:
	def __init__(self, info, time):
		self.info = info
		self.time = time

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

def Genetic(inst, ps):
	population =  []
	time = 100000
	for k in range (ps): #Generate Init. Population
		undonetask= list(range(1,len(inst[0])))
		readytask = []
		finishtask = [0]
		gene = [] #First Digit is Task, 2nd is Machine
		while len(undonetask) > 0:
			for j in undonetask:
				if set(inst[1][j-1]).issubset(set(finishtask)) and j not in finishtask:
					readytask.append(j)
					readytask = list(set(readytask))
					shuffle(readytask)
			gene.append([randint(1,PEnum),readytask[0]])
			undonetask.remove(readytask[0])
			finishtask.append(readytask[0])
			readytask.remove(readytask[0])
		genewithtime = Gene(gene,CalcFit(inst,gene))
		population.append(genewithtime)
	for t in range(ps):
		population.append(Gene(Crossover(inst, population[t].info, population[randint(0,t)].info)[0],CalcFit(inst,Crossover(inst, population[t].info, population[randint(0,t)].info)[0])))
		population.append(Gene(Crossover(inst, population[t].info, population[randint(0,t)].info)[1],CalcFit(inst,Crossover(inst, population[t].info, population[randint(0,t)].info)[1])))
		population.append(Gene(Crossover(inst, population[t].info, population[randint(0,t)].info)[2],CalcFit(inst,Crossover(inst, population[t].info, population[randint(0,t)].info)[2])))
		population.append(Gene(Crossover(inst, population[t].info, population[randint(0,t)].info)[3],CalcFit(inst,Crossover(inst, population[t].info, population[randint(0,t)].info)[3])))
	population.sort(key = lambda x:x.time)
	print(max(population[0].time))
	
	

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

def Crossover(inst, gene1, gene2):
	length = len(inst[0])-1
	t = randint(0,length-1)
	geneson1 = []
	geneson2 = []
	geneson3 = []
	geneson4 = []
	for i in range(length):
		if i<t:
			geneson1.append(gene1[i])
			geneson2.append(gene2[i])
			geneson3.append([gene2[i][0],gene1[i][1]])
			geneson4.append([gene1[i][0],gene2[i][1]])
		elif i>=t:
			geneson3.append(gene1[i])
			geneson4.append(gene2[i])
			geneson1.append([gene2[i][0],gene1[i][1]])
			geneson2.append([gene1[i][0],gene2[i][1]])
	return [geneson1,geneson2,geneson3,geneson4]
	

	
def usage():
    print ('Usage: %s [OPTIONS] <instance-file>' % argv[0])
    print ('Options:')
    print ('  -s <seed>           Random seed. Default: %d' % SEED)
    print ('  -p <population>     Population size. Default: %d' % PS)
    print ('  -i <iterations>     Iterations. Default: %d' % IT)
    print ('  -c <crossover-prob> Crossover probability. Default: %f' % CP)
    print ('  -m <mutation-prob>  Mutation probability. Default: %f' % MP)

if len(argv) < 2:
    usage()
    exit(1)

i = 1
while i < len(argv) - 1:
    if argv[i] == '-s':
        SEED = int(argv[i+1])
    elif argv[i] == '-p':
        PS = int(argv[i+1])
    elif argv[i] == '-i':
        IT = int(argv[i+1])
    elif argv[i] == '-n':
        PEnum = int(argv[i+1])
    elif argv[i] == '-c':
        CP = float(argv[i+1])
    elif argv[i] == '-m':
        MP = float(argv[i+1])
        
    elif argv[i] == '-h':
        usage()
        exit(0)
    else:
        print ('Unknown option: %s' % argv[i])
        usage()
        exit(1)
    i = i + 2

seed(SEED)
inst = LoadSample(argv[-1])

Genetic(inst, PS)
