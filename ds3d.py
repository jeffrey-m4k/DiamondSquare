# Todo: Use argparse to get arguments instead of just reading sys.argv

import math, random, numpy as np, datetime, time, sys, matplotlib.pyplot as plt
from PIL import Image
from mayavi import mlab

def avg(*arg):
	return sum(arg)/len(arg)


def main(rows=513, cols=513):

	global noiseMap

	startTime = time.time()

	print("\n")
	sys.stdout.write("\rInitializing heightmap...")

	noiseMap = np.zeros((cols,rows))
	noiseMap[0,0], noiseMap[0,cols-1], noiseMap[rows-1,0], noiseMap[rows-1,cols-1] \
		= (random.sample(list(range(256)), 4))

	stepSize = cols-1
	rCap = 150
	r = lambda: random.randrange(int(-rCap),int(rCap+1),1)

	# Not required for the algorithm, just to give some info to the user

	stepsRequired = str(int(math.log(cols-1, 2)) * 2)
	stepCount = 1

	while stepSize > 1:
		stepFactor = int(((cols-1) // stepSize))
		nOfSquares = stepFactor**2
		sqList = getSquares(cols-1, stepFactor)
		diaList = getDiamonds(cols-1, stepFactor, sqList)

		sys.stdout.flush()
		sys.stdout.write("\rPerforming diamond step [" + str(stepCount) + "/" + stepsRequired + "]")

		for x in range(len(sqList)):
			diaStep(sqList[x][0], sqList[x][1], stepSize, r())

		stepCount += 1
		sys.stdout.flush()
		sys.stdout.write("\rPerforming square step  [" + str(stepCount) + "/" + stepsRequired + "]")

		for x in range(len(diaList)):
			squareStep(diaList[x][0], diaList[x][1], stepSize, r(), cols-1)

		stepCount += 1
		sys.stdout.flush()

		stepSize //= 2
		rCap *= .45

	print((" Done in " + str(round(time.time() - startTime, 3)) + "s\n"))


# - This function causes massive slowdown (8x slower) - do not use

#def showProgress(input, max):
#	percentDone = int(round(input/max, 2) * 100)
#	barString = [" "," "," "," "," "," "," "," "," "," ", \
#				 " "," "," "," "," "," "," "," "," "," ", \
#				 " "," "," "," "," "," "," "," "," "," ", \
#				 " "," "," "]
#	for x in range(percentDone//3):
#		barString[x] = "█"
#	progressBar = "\r | " + "".join(barString) + " | " + str(percentDone) + "%"
#	sys.stdout.write(progressBar)


def getSquares(aSize, div):

	coordList = []

	for n in range(0,div):
		for x in range(0,div):
			coords = [n*(aSize//div), x*(aSize//div)]
			coordList.append(coords)

	return coordList


def getDiamonds(aSize, div, squares):

	squareVList = []
	coordList = []
	coordListFiltered = []

	for x in range(len(squares)):
		squareVList.append([squares[x][0], squares[x][1]])
		squareVList.append([squares[x][0] + (aSize//div), squares[x][1]])
		squareVList.append([squares[x][0], squares[x][1] + (aSize//div)])
		squareVList.append([squares[x][0] + (aSize//div), squares[x][1] + (aSize//div)])

	squareVList = list(map(list,set(map(tuple,squareVList))))
	squareVList.sort()

	for x in range(len(squareVList)):	
		coordList.append([squareVList[x][0] + aSize//(div*2), squareVList[x][1]])		
		coordList.append([squareVList[x][0] - aSize//(div*2), squareVList[x][1]])		
		coordList.append([squareVList[x][0], squareVList[x][1] + aSize//(div*2)])	
		coordList.append([squareVList[x][0], squareVList[x][1] - aSize//(div*2)])

	coordList = list(map(list,set(map(tuple,coordList))))
	for coord in range(len(coordList)):
		if not any(n<0 or n>aSize for n in coordList[coord]):
			coordListFiltered.append(coordList[coord])
	coordListFiltered.sort()

	return coordListFiltered


def diaStep(x, y, stepSize, r):

	avgValue = avg(noiseMap[x,y],noiseMap[x+stepSize,y],noiseMap[x,y+stepSize],noiseMap[x+stepSize,y+stepSize])
	indexToChange = (x+stepSize//2, y+stepSize//2)
	noiseMap[indexToChange] = avgValue + r
	
	if noiseMap[indexToChange] > 255:
		noiseMap[indexToChange] = 255
	elif noiseMap[indexToChange] < 0:
		noiseMap[indexToChange] = 0


def squareStep(x, y, stepSize, r, aSize):

	diaCorners = [[x+stepSize//2,y],[x,y+stepSize//2],[x-stepSize//2,y],[x,y-stepSize//2]]
	diaCornersFiltered = []
	for coord in range(len(diaCorners)):
		if not any(n<0 or n>aSize for n in diaCorners[coord]):
			diaCornersFiltered.append(diaCorners[coord])
	diaCornersFiltered.sort()

	avgTotal = 0
	for coord in range(len(diaCornersFiltered)):
		avgTotal += noiseMap[int(diaCornersFiltered[coord][0]), int(diaCornersFiltered[coord][1])]
	avgValue = avgTotal / len(diaCornersFiltered)

	noiseMap[x,y] = avgValue + r
	if noiseMap[x,y] > 255:
		noiseMap[x,y] = 255
	elif noiseMap[x,y] < 0:
		noiseMap[x,y] = 0


def makeMap(outputName, size):

	global noiseMap

	main(size,size)

	if not "-ns" in sys.argv:
		noiseMapB = noiseMap.astype(np.uint8)
		img = Image.fromarray(noiseMapB)
		img.save(outputName)
		print("Output saved as " + outputName)

	if not "-3donly" in sys.argv and not "-x" in sys.argv:
		plt.imshow(noiseMap, cmap='tab20b', interpolation='nearest')
		plt.show()

	if not "-2donly" in sys.argv and not "-x" in sys.argv:
		mlab.surf(noiseMap, colormap='gist_earth', warp_scale='auto')
		mlab.show()


try:
	size = int(sys.argv[1])
except (IndexError, ValueError):
	print("No width and height specified, defaulting to 513x513.")
	size = 513


outputName = "DS-" + str(size) + "x" + str(size) + "-" + str(datetime.datetime.now()).replace(':', '') + ".png"
makeMap(outputName, size)
	