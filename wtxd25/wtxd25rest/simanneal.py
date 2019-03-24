import math
import random
import readFile
def getDist(tour,city,size):
	length = 0
	for x in range(len(tour)-2):
		length+=int(city[tour[x]][tour[x+1]])
	length+=int(city[tour[-2]][0])
	return length

def simulatedAnnealingQMC(file):
	#Check message from Andrew on messenger
	name, city, size = readFile.readF(file)
	temperature = 1000000000000
	iterations = 12000
	scalealpha = 2
	initTour = []
	initTour.append(0)
	for i in range(1,size):
		initTour.append(i) 
	initTour.append(0)
	#Neighbour is two cities flipped
	for count in range(iterations):
		tourInner = initTour[:]
		del tourInner[0]
		del tourInner[-1]
		tK = temperature/(1+scalealpha*(count**2))
		#tK = temperature/(1+math.log(1+count))
		#acceptingThreshold = tK*getDist(initTour, city, size)
		#Find the indices to signify the three subsections.
		randomIndices = [0,0]
		randomIndices[0] = (random.randint(1,size-1))
		randomIndices[1] = (random.randint(1,size-1))
		while randomIndices[0] == randomIndices[1]:
			randomIndices[1] = random.randint(1,size-1)
		neighbour = tourInner[:]
		#Reversal with wraparound
		if randomIndices[0] < randomIndices[1]:
			neighbour[randomIndices[0]:randomIndices[1]] = neighbour[randomIndices[0]:randomIndices[1]][::-1]
		else:
			before = neighbour[randomIndices[0]:][::-1]
			after = neighbour[:randomIndices[1]][::-1]
			changed = after + before
			#getting all indices to fill
			ind = []
			for i in range(randomIndices[0], len(neighbour)):
				ind.append(i)
			for i in range(0, randomIndices[1]):
				ind.append(i)
			for x in range(len(ind)):
				neighbour[ind[x]] = changed[x]
		neighbour.insert(0,0)
		neighbour.append(0)
		results = [getDist(initTour, city, size), getDist(neighbour, city, size)]
		if results[1] < results[0]:
			initTour = neighbour
		elif math.exp((results[0]-results[1])/tK) > 1:
			initTour = neighbour

	return getDist(initTour, city, size), initTour

def simulatedAnnealing(file):
	#Change to exponential decrease of temp
	name, city, size = readFile.readF(file)
	temperature = 100000000
	iterations = 120000
	initTour = []
	initTour.append(0)
	for i in range(1,size):
		initTour.append(i) 
	initTour.append(0)
	
	#Neighbour is two cities flipped
	fstar = 0
	for count in range(iterations):
		#non-monotonic adaptive cooling experimentation
		if count > 0:
			tK = tK*(1+((fsi-fstar)/fsi))
		else:
			tK = temperature
		#tK = temperature/(1+math.log(1+count))
		#acceptingThreshold = tK*getDist(initTour, city, size)
		randomIndices = [0,0]
		randomIndices[0] = random.randint(1,size-1)
		randomIndices[1] = random.randint(1,size-1)
		while randomIndices[0] == randomIndices[1]:
			randomIndices[1] = random.randint(1,size-1)
		neighbour = initTour[:]
		temp = neighbour[randomIndices[0]]
		neighbour[randomIndices[0]] = neighbour[randomIndices[1]]
		neighbour[randomIndices[1]] = temp
		results = [getDist(initTour, city, size), getDist(neighbour, city, size)]
		if results[1] < results[0]:
			initTour = neighbour
			fstar = results[1]
		elif math.exp((results[0]-results[1])/tK) > 1:
			initTour = neighbour
			fstar = results[0]
		if count == 0 and fstar == 0:
			fstar = results[0]
		fsi = results[1]
	# textFilename = name.split(",")[0].split("= ")[1]
	# if textFilename[0] != "N":
	#     textFilename = "NEW" + textFilename
	# tfA = open("wtxd25/TourfileB/tour" + textFilename + ".txt", "w+")
	# presentTour = str([x+1 for x in initTour[:-1]]).strip("[]").replace(" ", "")
	# tfA.write(name + "\nTOURSIZE = " + str(size) + ",\nLENGTH = " + str(getDist(initTour, city, size)) + ",\n" + presentTour)
	# tfA.close()
	return getDist(initTour, city, size), initTour, name, size
print(simulatedAnnealing("NEWAISearchfile026.txt"))



# randomIndices[0] = random.randint(1,size-3)
# randomIndices[1] = random.randint(1,size-2)
# randomIndices[2] = random.randint(1,size-1)
# while len(list(set(randomIndices))) < len(randomIndices):
# 	randomIndices[0] = random.randint(1,size-3)
# 	randomIndices[1] = random.randint(1,size-2)
# 	randomIndices[2] = random.randint(1,size-1)

# cx, cy, cz = random.randint(1,4), random.randint(1,4), random.randint(1,4)
# while len(list(set([cx,cy,cz]))) < len([cx,cy,cz]):
# 	cx, cy, cz = random.randint(1,4), random.randint(1,4), random.randint(1,4)
# neighbour = initTour[:]
# if cx == 1:
# 	neighbour[:randomIndices[0]] = neighbour[:randomIndices[0]][::-1]
# elif cx == 2:
# 	neighbour[randomIndices[0]:randomIndices[1]] = neighbour[randomIndices[0]:randomIndices[1]][::-1]
# elif cx == 3:
# 	neighbour[randomIndices[1]:randomIndices[2]] = neighbour[randomIndices[1]:randomIndices[2]][::-1]
# elif cx == 4:
# 	neighbour[randomIndices[2]:] = neighbour[randomIndices[2]:][::-1]

# if cy == 1:
# 	neighbour[:randomIndices[0]] = neighbour[:randomIndices[0]][::-1]
# elif cy == 2:
# 	neighbour[randomIndices[0]:randomIndices[1]] = neighbour[randomIndices[0]:randomIndices[1]][::-1]
# elif cy == 3:
# 	neighbour[randomIndices[1]:randomIndices[2]] = neighbour[randomIndices[1]:randomIndices[2]][::-1]
# elif cy == 4:
# 	neighbour[randomIndices[2]:] = neighbour[randomIndices[2]:][::-1]

# if cz == 1:
# 	neighbour[:randomIndices[0]] = neighbour[:randomIndices[0]][::-1]
# elif cz == 2:
# 	neighbour[randomIndices[0]:randomIndices[1]] = neighbour[randomIndices[0]:randomIndices[1]][::-1]
# elif cz == 3:
# 	neighbour[randomIndices[1]:randomIndices[2]] = neighbour[randomIndices[1]:randomIndices[2]][::-1]
# elif cz == 4:
# 	neighbour[randomIndices[2]:] = neighbour[randomIndices[2]:][::-1]