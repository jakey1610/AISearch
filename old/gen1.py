# This will be the genetic algorithm for solving the TSP problem
import readFile
import itertools
import random
import math

# change for roulette selection gives more probability for fitter individuals
# These parameters shouldn't (I don't think) but do produce the best results.
mutationProb = 1
breedProb = 0.9
generations = 1000
initialPop = 25


# `Andrew` : Why do we pass size into this function, we don't even use it?
# `Andrew` city is a shit name, we're talking about graphs here mate.
def getDist(tours, city, size):
    dist = []
    for t in tours:
                # `Andrew` would it be worth refractoring the loop body into a separate function, the smaller the functions the better!
        length = 0
        for x in range(len(t) - 1):
            length += int(city[t[x]][t[x + 1]])
        # `Andrew` - Be careful! You forget the sum the distance from the endpoint of t back to the start (It's a cycle rememebr!)
        dist.append(length)
    return dist

# ------------------- `Andrew` Version genDist
# Notice how all my functions are nice and small
# Would be easy to maintain and understand what they do
# No ambiguity!

def _tourLength(tour, graph):
        # Start Distance + Distances inbetween
    return graph[tour[0]][tour[len(tour) - 1]] \
        + sum(graph[x][x + 1] for x in range(len(tour) - 1))


def _genDist(tours, graph):
    return [_tourLength(tour, graph) for tour in tours]

# ------------------- Back to Jakes Wilderness


# `Andrew` - So this function is quite a common problem, find the k largest elements based on some function that maps a tour to a integer in this case length.
def getNFittest(tours, city, size, n):  # Shit paramter name city once again.
    distances = getDist(tours, city, size)  # `Andrew` - Good name well done
    # `Andrew` - Shit name, it's not an array of distances, it's an array of tours. How the fuck would we know that when it's called `distances`
    distances = [x for _, x in sorted(zip(distances, tours))]
    return distances[0:n]


def _genNFittest(tours, graph, size, n):
    # My own version of the function.
    # the sorted function let's you specify how it sorts items.
    return sorted(tours, key=lambda tour: _tourLength(tour, graph))[0:n]


# Didn't look at this trainwreck, why u using the set things? Oh fuck knows.
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


def crossoverOX(t1, t2, size):  # `Andrew` - BREAK THIS FUNCTION INTO SMALLER FUNCTIONS YOU FUCK
        # `Andrew` - Fuck we got 4 lists for, we're generating 2 children right?
    # `Andrew` - why size-1, no comment to the reader makes this really fucking unclear
        # ` Andrew` - declare variables when you need then, not in advanced! <---- Quite Important in programming
    t1comp = [-1] * (size - 1)
    # `Andrew` - maybe you use this for comparisons on whether something has already been visited? Only guessedthat from below lines
    t2comp = [-1] * (size - 1)
    # `Andrew` i guess this is our new child1, don't be afraid to call it
    t1c = t1[:]
    t2c = t2[:]  # `Andrew` - just looks at the return values, WHY THE FUCK DOES t2c not stand for t2 child like why is comp which is commonly comparisons actually the child
    # why do we suddenly delete random shit, why not just splice the original list to not include the values
    del t1c[0]
    del t1c[-1]
    del t2c[0]
    del t2c[-1]
    sizeNew = size - 1
    # `Andrew` - why use the list, do we really need the additional cost of the list. Can we just use 2 variables? like leftSliceIndex, rightSliceIndex?
    randomIndices = [0, 0]
    # Find the two random cut points # `Andrew` - blessed be this commnet else i would have no fucking clue.
    # `Andrew` - second condition not necessary, just swap the 2 randomly generated numbers if they are the wrong way around?
    while randomIndices[0] == randomIndices[1] or randomIndices[0] > randomIndices[1]:
        randomIndices = [random.randint(
            0, sizeNew - 1), random.randint(0, sizeNew - 1)]
    # Swap the middle sections of each list.
    t1comp[randomIndices[0]:randomIndices[1] +  # `Andrew` - Since you used a fucking list, you can't add additional meaning to hepl the user understand the point of the values contained within the list
           1] = t2c[randomIndices[0]:randomIndices[1] + 1]
    t2comp[randomIndices[0]:randomIndices[1] +
           1] = t1c[randomIndices[0]:randomIndices[1] + 1]
    # iterate through list from randomIndices[1]+1
    order1 = []  # order, order of fucking what
    order2 = []
    # i'm not even going to try and understand this loop, just loads of random variables and modulus
    # why modulus, also don't be afraid to split up one for loop into mulitple if u want to, smaller loop bodies are nice!
    for i in range(0, sizeNew):
        if t1c[(randomIndices[1] + 1 + i) % (sizeNew)] not in t1comp:
            order1.append(t1c[(randomIndices[1] + 1 + i) % (sizeNew)])
        if t2c[(randomIndices[1] + 1 + i) % (sizeNew)] not in t2comp:
            order2.append(t2c[(randomIndices[1] + 1 + i) % (sizeNew)])
    count = randomIndices[1] + 1
    for x1 in order1:
        t1comp[count % (sizeNew)] = x1
        count += 1
    count = randomIndices[1] + 1
    for x2 in order2:
        t2comp[count % (sizeNew)] = x2
        count += 1

    t1comp.insert(0, 0)  # `Andrew` - fuck these for
    t2comp.insert(0, 0)  # magic numbers much
    t1comp.append(0)
    t2comp.append(0)
    # Finally return the new children

    return t1comp, t2comp  # `Andrew`


# --------------------------------- Andrew version of crossoverOX
def _generateTwoRandomDistinctIntegers(maxValue):
    random1 = random.randint(0, maxValue)
    random2 = random.randint(0, maxValue)
    while random1 == random2:
        random2 = random.randint(0, maxValue)
    return min(random1, random2), max(random1, random2)

# Haven't actually tested this function lol!
def _crossoverOX(parent1, parent2, size):  # why call it t1, t2 the're parents!
    offspring1, offspring2 = [-1] * size, [-1] * size
    # We split after the index which is why the min value is 0, because that means we split between 0 and 1 so 0 won't be in the splice.
    leftSplitIndex, rightSplitIndex = _generateTwoRandomDistinctIntegers(size)

    # Left Region = [0, leftSplitIndex+1),
    # Center Region = [leftSplitIndex+1, rightSplitIndex),
    # Right Region = [rightSplitIndex, size)

    # Copy the center region.
    for i in range(leftSplitIndex + 1, rightSplitIndex):
        offspring1[i] = parent1[i]
        offspring2[i] = parent2[i]

    # Copy right region into new offspring from parents
    placeToFill1, placeToFill2 = rightSplitIndex, rightSplitIndex
    def tryCopyLetter(i):
        if parent1[i] not in offspring2:
            offspring2[placeToFill2] = parent1[i]
        if parent2[i] not in offspring1:
            offspring1[placeToFill1] = parent2[i]

    # See, there's nothing wrong with 2 for loops and just no modulus!
    for i in range(rightSplitIndex, size):
        tryCopyLetter(i)
    for i in range(0, leftSplitIndex+1):
        tryCopyLetter(i)

    return offspring1, offspring2

# `Andrew` - didn't look at.
def mutate(t1, size):
    indicesSwap = [0, 0]
    while indicesSwap[0] == indicesSwap[1] or indicesSwap[0] == 0 or indicesSwap[1] == 0:
        indicesSwap = [random.randint(
            0, size - 1), random.randint(0, size - 1)]
    temp = t1[indicesSwap[0]]
    t1[indicesSwap[0]] = t1[indicesSwap[1]]
    t1[indicesSwap[1]] = temp
    return t1

# `Andrew` - didn't look at.
def geneticSolve(file):
    name, city, size = readFile.readF(file)
    tours = []
    initTour = []
    initTour.append(0)
    for i in range(1, size):
        initTour.append(i)
    initTour.append(0)
    tours.append(initTour)
    for i in range(initialPop - 1):
        tours.append(sorted(initTour, key=lambda k: random.random()))
        tours[i + 1].remove(0)
        tours[i + 1].remove(0)
        tours[i + 1].append(0)
        tours[i + 1].insert(0, 0)
    perGen = []
    for g in range(generations):
        print(g)
        # Now we calculate the fitness of the population.
        dist = getDist(tours, city, size)
        # Find the probabilities of selection for breeding.
        breedingPairs = math.ceil(breedProb * initialPop * 2 / 4.) * 2
        indicesBreeding = []
        distances = dist[:]
        for b in range(0, int(breedingPairs)):
            indicesBreeding.append(dist.index(min(distances)))
            del distances[distances.index(min(distances))]
        couples = []
        for t in range(0, int(breedingPairs), 2):
            couple = []
            couple.append(tours[indicesBreeding[t]])
            couple.append(tours[indicesBreeding[t + 1]])
            couples.append(couple)
        # Mutate pairs(somehow...)
        children = []
        for c in couples:
            if random.uniform(0, 10) < 1:
                if int(getDist([c[0]], city, size)[0]) > int(getDist([c[1]], city, size)[0]):
                    children.append(c[1])
                else:
                    children.append(c[0])
            child = list(crossoverOX(c[0], c[1], size))
            # mutate?
            index = random.randint(0, 1)
            chance = random.uniform(0, 10)
            if chance < (mutationProb * 10):
                child[index] = mutate(child[index], size)
            children.append(child[1])
            children.append(child[0])

        tours = getNFittest(list(tours + children[:]), city, size, initialPop)
        # perGen.append(getDist(getNFittest(list(tours+children[:]), city, size, 1), city, size))
    # perGen if set up by removing comments shows a definite downward trend but not very quickly.
    # print(perGen)
    finalDistances = getDist(children[-initialPop:], city, size)
    return min(finalDistances), children[finalDistances.index(min(finalDistances))]


print(geneticSolve("NEWAISearchfile012.txt"))
