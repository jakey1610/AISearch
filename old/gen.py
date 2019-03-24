#This will be the genetic algorithm for solving the TSP problem
import readFile
import itertools
import random
import math
#change for roulette selection gives more probability for fitter individuals
#These parameters shouldn't (I don't think) but do produce the best results. Look into elitism
mutationProb = 1
breedProb = 0.9
generations = 1000
initialPop = 50
def getDist(tours,city,size):
	dist = []
	for t in tours:
		length = 0
		for x in range(len(t)-1):
			length+=int(city[t[x]][t[x+1]])
		dist.append(length)
	return dist

def getNFittest(tours,city,size,n):
	distances = getDist(tours,city,size)
	distances = [x for _,x in sorted(zip(distances,tours))]
	return distances[0:n]

def crossover(t1, t2, size):
	t1comp = t1[:int(size/2)+1] + t2[int(size/2)+1:]
	t2comp = t2[:int(size/2)+1] + t1[int(size/2)+1:]
	duplicatest1 = set([x for x in t1comp if t1comp.count(x) > 1 and x != 0])
	duplicatest2 = set([x for x in t2comp if t2comp.count(x) > 1 and x != 0])
	dupIndices1,dupIndices2 = [],[]
	for d in duplicatest1:
		dupIndices1.append(t1comp.index(d))
	for d in duplicatest2:
		dupIndices2.append(t2comp.index(d))
	notIncluded1 = list(set(t1) - set(t1comp))
	notIncluded2 = list(set(t2) - set(t2comp))
	count = 0
	for nc1 in notIncluded1:
		t1comp[dupIndices1[count]] = nc1
		count +=1
	count = 0
	for nc2 in notIncluded2:
		t2comp[dupIndices2[count]] = nc2
		count +=1
	return t1comp, t2comp

def crossoverOX(t1,t2,size):
	t1comp = [-1]*(size-1)
	t2comp = [-1]*(size-1)
	t1c = t1[:]
	t2c = t2[:]
	del t1c[0]
	del t1c[-1]
	del t2c[0]
	del t2c[-1]
	sizeNew = size-1
	randomIndices =[0,0]
	#Find the two random cut points
	while randomIndices[0] == randomIndices[1] or randomIndices[0]>randomIndices[1]:
		randomIndices = [random.randint(0,sizeNew-1), random.randint(0,sizeNew-1)]
	#Swap the middle sections of each list.
	t1comp[randomIndices[0]:randomIndices[1]+1] = t2c[randomIndices[0]:randomIndices[1]+1]
	t2comp[randomIndices[0]:randomIndices[1]+1] = t1c[randomIndices[0]:randomIndices[1]+1]
	#iterate through list from randomIndices[1]+1
	order1 = []
	order2 = []
	for i in range(0,sizeNew):
		if t1c[(randomIndices[1]+1+i)%(sizeNew)] not in t1comp:
			order1.append(t1c[(randomIndices[1]+1+i)%(sizeNew)])
		if t2c[(randomIndices[1]+1+i)%(sizeNew)] not in t2comp:
			order2.append(t2c[(randomIndices[1]+1+i)%(sizeNew)])
	count = randomIndices[1]+1
	for x1 in order1:
		t1comp[count%(sizeNew)] = x1
		count +=1
	count = randomIndices[1]+1
	for x2 in order2:
		t2comp[count%(sizeNew)] = x2
		count +=1

	t1comp.insert(0,0)
	t2comp.insert(0,0)
	t1comp.append(0)
	t2comp.append(0)
	#Finally return the new children
	return t1comp, t2comp

def crossoverCX(t1,t2,size):
	t1comp = [-1]*(size-1)
	t2comp = [-1]*(size-1)
	t1c = t1[:]
	t1left = t1[:]
	t2c = t2[:]
	t2left = t2[:]
	del t1c[0]
	del t1c[-1]
	del t2c[0]
	del t2c[-1]
	del t1left[0]
	del t1left[-1]
	del t2left[0]
	del t2left[-1]
	sizeNew = size-1
	t1comp[0]=t1c[0]
	t2left.remove(t1c[0])
	i = t1c.index(t2c[0])
	#Complete one cycle
	while t1comp[i] != t1c[0] and t2c[i] in t2left:
		t1comp[i] = t2c[i]
		t2left.remove(t2c[i])
		i = t1c.index(t2c[i])
	#Once cycle complete
	for x in range(sizeNew):
		if t1comp[x]==-1:
			count = 0
			while t2left[(x+count)%(len(t2left))] in t1comp:
				count+=1
			t1comp[x] = t2left[(x+count)%(len(t2left))]
			t2left.remove(t2left[(x+count)%(len(t2left))])

	t2comp[0]=t2c[0]
	t1left.remove(t2c[0])
	i = t2c.index(t1c[1])
	#Change for the second child
	while t2comp[i] != t2c[0] and t1c[i] in t1left:
		t2comp[i] = t1c[i]
		t1left.remove(t1c[i])
		i = t2c.index(t1c[i])
	#Once cycle complete
	for x in range(sizeNew):
		if t2comp[x]==-1:
			count = 0
			while t1left[(x+count)%(len(t1left))] in t2comp:
				count+=1
			t2comp[x] = t1left[(x+count)%(len(t1left))]
			t1left.remove(t1left[(x+count)%(len(t1left))])
	t1comp.insert(0,0)
	t2comp.insert(0,0)
	t1comp.append(0)
	t2comp.append(0)
	return t1comp,t2comp

def mutate(t1, size):
	indicesSwap = [0,0]
	while indicesSwap[0] == indicesSwap[1] or indicesSwap[0] == 0 or indicesSwap[1] == 0:
		indicesSwap = [random.randint(0,size-1), random.randint(0,size-1)]
	temp = t1[indicesSwap[0]]
	t1[indicesSwap[0]] = t1[indicesSwap[1]]
	t1[indicesSwap[1]] = temp
	return t1

def geneticSolve(file):
	name, city, size = readFile.readF(file)
	tours = []
	initTour = []
	initTour.append(0)
	for i in range(1,size):
		initTour.append(i)
	initTour.append(0)
	tours.append(initTour)
	for i in range(initialPop-1):
		tours.append(sorted(initTour, key=lambda k: random.random()))
		tours[i+1].remove(0)
		tours[i+1].remove(0)
		tours[i+1].append(0)
		tours[i+1].insert(0,0)
	perGen = []
	for g in range(generations):
		print(g)
		dist = getDist(tours,city,size)
		#Find the probabilities of selection for breeding.
		breedingPairs = math.ceil(breedProb*initialPop*2 / 4.) * 2
		indicesBreeding = []
		distances = dist[:]
		for b in range(0,int(breedingPairs)):
			indicesBreeding.append(dist.index(min(distances)))
			del distances[distances.index(min(distances))]
		couples = []
		for t in range(0,int(breedingPairs),2):
			couple = []
			couple.append(tours[indicesBreeding[t]])
			couple.append(tours[indicesBreeding[t+1]])
			couples.append(couple)
		#Mutate pairs(somehow...)
		children = []
		for c in couples:
			#On some random occasions add in the fittest parent.
			#print(c[0], c[1])
			if random.uniform(0,10)<1:
				if int(getDist([c[0]],city,size)[0]) > int(getDist([c[1]],city,size)[0]):
					children.append(c[1])
				else:
					children.append(c[0])
			child = list(crossoverOX(c[0], c[1], size))
			#mutate?
			index = random.randint(0,1)
			chance = random.uniform(0,10)
			if chance < (mutationProb*10):
				child[index] = mutate(child[index], size)

			#do some local optimization
			consecutive = 1
			sindex = 0
			for ch in range(2):
				for citycount in range(1,len(child[ch])):
					if child[ch][citycount]+1 == child[ch][citycount-1]:
						if consecutive == 1:
							sindex = citycount
						consecutive+=1
					else:
						if consecutive >= 4:
							child[ch][sindex+1:(sindex-1)+consecutive] = child[ch][sindex:(sindex-1)+consecutive][::-1]
						consecutive=1


			#append both children to the child list.
			children.append(child[1])
			children.append(child[0])
			
		tours = getNFittest(list(tours + children[:]), city, size, initialPop)
		#perGen.append(getDist(getNFittest(list(children[:]), city, size, 1), city, size))
	#perGen if set up by removing comments shows a definite downward trend but not very quickly.
	#print(perGen)
	finalDistances = getDist(children[-initialPop:],city,size)
	return min(finalDistances), children[finalDistances.index(min(finalDistances))]
print(geneticSolve("NEWAISearchfile535.txt"))