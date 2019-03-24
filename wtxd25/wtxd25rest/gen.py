# This will be the genetic algorithm for solving the TSP problem
import readFile
import itertools
import random
import math


mutationProb = 0.2
breedProb = 0.8
generations = 1000
initialPop = 100

def _tourLength(tour, graph):
    return graph[tour[0]][tour[-1]] \
        + sum(graph[tour[x]][tour[x + 1]] for x in range(len(tour) - 1))


def getDist(tours, graph):
    return [_tourLength(tour, graph) for tour in tours]


def getNFittest(tours, graph, size, n):
    return sorted(tours, key=lambda tour: _tourLength(tour, graph))[0:n]

def crossover(t1, t2, size):
    t1comp = t1[:int(size / 2) + 1] + t2[int(size / 2) + 1:]
    t2comp = t2[:int(size / 2) + 1] + t1[int(size / 2) + 1:]
    duplicatest1 = set([x for x in t1comp if t1comp.count(x) > 1 and x != 0])
    duplicatest2 = set([x for x in t2comp if t2comp.count(x) > 1 and x != 0])
    dupIndices1, dupIndices2 = [], []
    for d in duplicatest1:
        dupIndices1.append(t1comp.index(d))
    for d in duplicatest2:
        dupIndices2.append(t2comp.index(d))
    notIncluded1 = list(set(t1) - set(t1comp))
    notIncluded2 = list(set(t2) - set(t2comp))
    count = 0
    for nc1 in notIncluded1:
        t1comp[dupIndices1[count]] = nc1
        count += 1
    count = 0
    for nc2 in notIncluded2:
        t2comp[dupIndices2[count]] = nc2
        count += 1
    return t1comp, t2comp

def _generateTwoRandomDistinctIntegers(maxValue):
    random1 = random.randint(0, maxValue)
    random2 = random.randint(0, maxValue)
    while random1 == random2:
        random2 = random.randint(0, maxValue)
    return min(random1, random2), max(random1, random2)

def crossoverOX(parent1, parent2, size):
    offspring1, offspring2 = [-1] * (size), [-1] * (size)
    # We split after the index which is why the min value is 0, because that means we split between 0 and 1 so 0 won't be in the splice.
    leftSplitIndex, rightSplitIndex = _generateTwoRandomDistinctIntegers(size)

    # Left Region = [0, leftSplitIndex+1),
    # Center Region = [leftSplitIndex+1, rightSplitIndex),
    # Right Region = [rightSplitIndex, size)

    # Copy the center region.
    offspring1[leftSplitIndex:rightSplitIndex] = parent2[leftSplitIndex:rightSplitIndex]
    offspring2[leftSplitIndex:rightSplitIndex] = parent1[leftSplitIndex:rightSplitIndex]
    if rightSplitIndex == size:
        offspring1, offspring2 = offspring1[0:], offspring2[0:]
    #print(parent1,parent2)
    remaining1 = list(set(parent1)-set(offspring2))
    remaining2 = list(set(parent2)-set(offspring1))
    # Copy right region into new offspring from parents
    placeToFill1, placeToFill2 = (rightSplitIndex)%size, (rightSplitIndex)%size
    #print(offspring1,remaining2, offspring2, remaining1)
    
    for i in range(0, len(remaining1)):
        #print(placeToFill2, remaining1[i], offspring2)
        offspring2[placeToFill2] = remaining1[i]
        placeToFill2 = (placeToFill2+1)%(size)
    for i in range(0, len(remaining2)):
        offspring1[placeToFill1] = remaining2[i]
        placeToFill1 = (placeToFill1+1)%(size)
    #print(offspring1, remaining2, offspring2, remaining1)
    offspring1.append(offspring1[0])
    offspring2.append(offspring2[0])

    return offspring1, offspring2

def mutate(t1, size):
    indicesSwap = [0, 0]
    while indicesSwap[0] == indicesSwap[1]:
        indicesSwap = [random.randint(1, size - 1), random.randint(1, size - 1)]
    temp = t1[indicesSwap[0]]
    t1[indicesSwap[0]] = t1[indicesSwap[1]]
    t1[indicesSwap[1]] = temp
    return t1

def _initialTours(initTour):
    tours = [initTour]
    for i in range(initialPop - 1):
        tours.append(sorted(initTour[:-1], key=lambda k: random.random()))
        tours[i + 1].append(tours[i+1][0])
    return tours

def _getCouples(breeders, numBreedingPairs):
    couples = []
    for breeder in range(0, int(numBreedingPairs), 2):
        couple = []
        couple.append(breeders[breeder])
        couple.append(breeders[breeder+1])
        couples.append(couple)
    return couples

def geneticSolve(file):
    name, city, size = readFile.readF(file)
    name = name.strip("\n")
    initTour = []
    for i in range(0, size):
        initTour.append(i)
    initTour.append(initTour[0])
    tours = _initialTours(initTour)
    
    perGen = []
    for g in range(generations):
        print(g)
        # Now we calculate the fitness of the population.
        dist = getDist(tours, city)
        # Find the probabilities of selection for breeding.
        numBreedingPairs = math.floor(breedProb * initialPop * 2 / 4.) * 2
        breeders = getNFittest(tours, city, size, numBreedingPairs)
        couples = _getCouples(breeders, numBreedingPairs)
        children = []
        for c in couples:
            #elitism
            #if random.uniform(0, 10) < 6:
            if int(getDist([c[0]], city)[0]) >= int(getDist([c[1]], city)[0]):
                children.append(c[1])
            else:
                children.append(c[0])
            child = list(crossoverOX(c[0], c[1], size))
            # mutate a child
            index = random.randint(0, 1)
            chance = random.uniform(0, 10)
            if chance < (mutationProb * 10):
                child[index] = mutate(child[index], size)

            #local optimisation
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

            if int(getDist([child[0]], city)[0]) >= int(getDist([child[1]], city)[0]):
                children.append(child[1])
            else:
                children.append(child[0])

        tours = getNFittest(list(tours + children[:]), city, size, initialPop)
        #perGen.append(getDist(getNFittest(list(tours+children[:]), city, size, 1), city))
    # perGen if set up by removing comments shows a definite downward trend but not very quickly.
    #print(perGen)
    finalDistances = getDist(children[-initialPop:], city)
    # textFilename = name.split(",")[0].split("= ")[1]
    # if textFilename[0] != "N":
    #     textFilename = "NEW" + textFilename
    # tfA = open("wtxd25/TourfileA/tour" + textFilename + ".txt", "w+")
    # presentTour = str([x+1 for x in children[finalDistances.index(min(finalDistances))]][:-1]).strip("[]").replace(" ", "")
    # tfA.write(name + "\nTOURSIZE = " + str(size) + ",\nLENGTH = " + str(min(finalDistances)) + ",\n" + presentTour)
    # tfA.close()
    return min(finalDistances), children[finalDistances.index(min(finalDistances))], name, size
print(geneticSolve("NEWAISearchfile026.txt"))
