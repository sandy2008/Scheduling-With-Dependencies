from random import randint, random, seed, shuffle
from sys import argv

#Parameters
SEED = 0
PS = 1000
IT = 50
CP = 1.0
MP = 0.05

PEnum = 3

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
		i = PEnum
		while i < len(l):
			taskpre[int(l[0])-1].append(int(l[i]))
			i += 1
	print(taskpre)
	return (tasktime,taskpre)

def Genetic(inst, ps):
	population =  []
	time = 100000
	for k in range (ps):
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
		population.append(gene)
		time = min(CalcFit(inst, gene),time)
	print (time)
	

def CalcFit(inst, gene):
	petime = [0]*PEnum
	starttime = [0]*(len(inst[0])-1)
	endtime = [0]*(len(inst[0])-1)
	parents = [[]for i in range((len(inst[0]))-1)]
	
	for i in range ((len(inst[0]))-1):
		parents[i] = inst[1][i]
		
	for t in range ((len(inst[0]))-1):
		for p in parents[t]:
			starttime[t] = max(endtime[p-1], petime[gene[t][0]-1])
		endtime[t] = starttime[t] + inst[0][t]
		petime[gene[t][0]-1] = endtime[t]
		
	return(max(petime))


	

	
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
