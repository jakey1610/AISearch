import gen
import simanneal
import time
def collateGen():
	fileextensions = ["012","017","021","026","042","048","058","175","180","535"]
	files = []
	results = []
	for i in range(0,len(fileextensions)):
		files.append("NEWAISearchfile"+fileextensions[i]+".txt")
	for f in files:
		print(f)
		start = time.time()
		result = gen.geneticSolve(f)
		end = time.time()
		resulttime = end - start
		avgr = result[0]
		for i in range(0,9):
			rtry = gen.geneticSolve(f)
			avgr += rtry[0]
			if result[0]>rtry[0]:
				result = rtry
		avgr /= 10
		results.append([result, avgr, resulttime])
		# name = result[2]
		# size = result[3]
		# textFilename = name.split(",")[0].split("= ")[1]
		# if textFilename[0] != "N":
		# 	textFilename = "NEW" + textFilename
		# tfA = open("wtxd25/TourfileA/tour" + textFilename + ".txt", "w+")
		# presentTour = str([x+1 for x in result[1][:-1]]).strip("[]").replace(" ", "")
		# tfA.write(name + "\nTOURSIZE = " + str(size) + ",\nLENGTH = " + str(result[0]) + ",\n" + presentTour)
		# tfA.close()
	return results

def collateSA():
	fileextensions = ["012","017","021","026","042","048","058","175","180","535"]
	files = []
	results = []
	for i in range(0,len(fileextensions)):
		files.append("NEWAISearchfile"+fileextensions[i]+".txt")
	for f in files:
		print(f)
		start = time.time()
		result = simanneal.simulatedAnnealing(f)
		end = time.time()
		resulttime = end - start
		avgr = result[0]
		for i in range(0,9):
			rtry = simanneal.simulatedAnnealing(f)
			avgr += rtry[0]
			if result[0]>rtry[0]:
				result = rtry
		avgr /= 10
		results.append([result,avgr, resulttime])
		# name = result[2]
		# size = result[3]
		# textFilename = name.split(",")[0].split("= ")[1]
		# if textFilename[0] != "N":
		# 	textFilename = "NEW" + textFilename
		# tfA = open("wtxd25/TourfileB/tour" + textFilename + ".txt", "w+")
		# presentTour = str([x+1 for x in result[1][:-1]]).strip("[]").replace(" ", "")
		# tfA.write(name + "\nTOURSIZE = " + str(size) + ",\nLENGTH = " + str(result[0]) + ",\n" + presentTour)
		# tfA.close()
	return results

print(collateGen())
print(collateSA())