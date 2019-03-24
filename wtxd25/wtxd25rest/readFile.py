import re
city = []

def readF(file):
	f = open("cityfiles/"+file, "r")
	name = f.readline()
	size = int(f.readline().split("=")[1].split(",")[0])
	for i in range(size+2):
		city.append([])
	count = 0
	while count <= size:
		line = f.readline()
		if line != "\n":
			line = line.split(",")
			if "" in line:
				line.remove("")
			if line != []:
				if line[-1] == "\n":
					del line[-1]
			city[count] = line
			count +=1

	#Make it so that each line has the correct amount of connections
	countNum = size-1
	c = 0
	while countNum != 0:
		if len(city[c])<countNum:
			city[c] = city[c] + city[c+1]
			del city[c+1]
		countNum-=1
		c+=1
	for c in range(len(city)):
		city[c] = [0]*(size - len(city[c])-1) + city[c]
	for y in range(size-1):
		for x in range(len(city[y])):
			try:
				city[y][x] = int(city[y][x])
			except ValueError:
				city[y][x] = int(re.sub("[^0-9]", "", city[y][x]))
	for x in range(size-1):
		city[size-1][x] = (city[x][-1])
	for y in range(size):
		city[y].insert(y, 0)
	for y in range(size-1):
		for x in range(len(city[y])):
			try:
				city[x][y] = int(city[y][x])
			except ValueError:
				city[x][y] = int(re.sub("[^0-9]", "", city[y][x]))
	if city[-1] == []:
		del city[-1]
	f.close()
	return name, city, size
#print(readF("NEWAISearchfile012.txt"))