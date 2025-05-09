import sys, math, random

#parameters to indicate png size
width = int(1280)
height = int(1280)
# Number of square per row and per column
div = 16
# The pixel lengths of a square in the final image
xLen = int(width/div)
yLen = int(height/div)

#list of tuples containing the square number, the x coordinate of the starting corner, and the y coordinate of the starting corner
sqList = []
#list of tuples containing the specified color, the x coordinate of the starting corner, and the y coordinate of the starting corner 
sqCol = []
#list of tuples containing the square number, and its specified color
q1 = []


# A color key with the RBG values where 0 is white, 1 is black/brown, 2 is green, and 3 is red
colorKey = {
        0: '255 255 255\t',
        1: '98 73 45\t',
        2: '47 75 38\t',
        3: '107 5 4\t'
}

# The squares in the first quadrant specified to be a certain color
whites = []
blacks = []
greens = []
reds = []
# Default Standard
# whites = [120,72,117,86,39,99,52,53,68,7,97,1,3,33,81,6]
# blacks = [103,118,88,69,55,100,54,84,35,24,114,18,19,34,22,82]
# greens = [119,102,71,85,116,40,51,67,38,23,113,20,21,49,65,17]
# reds = [104,87,101,70,56,115,36,37,83,8,98,4,5,50,66,2]

def genColors():
    whites.clear()
    blacks.clear()
    greens.clear()
    reds.clear()
    for i in range(16):
        base = 2*i + 24*math.floor(i/4)
        bases = [base+1, base+2, base+17, base+18]
        random.shuffle(bases)
        whites.append(bases[0])
        blacks.append(bases[1])
        greens.append(bases[2])
        reds.append(bases[3])


#Generates list of squares with corner and number determined by the number of divisions.
def genSquares():
        sqCol.clear()
        q1.clear()
        sqList.clear()
        numSquares = div*div
        for i in range(1, numSquares+1):
            #If the square is in the last column: special casing
            if(i%div==0):
                xco = (div-1)*xLen 
                if (i/div) > (div/2):
                    yco = -1*(yLen)
                else:
                    yco = 0
                yco += (int)(i/div)*(yLen)
            #If the square is not in the last column
            else:
                xco = (i%div)*xLen
                yco = ((int)(i/div))*yLen
                if (i/div) < (div/2):
                    yco += yLen
                if (i%div) > (div/2):
                    xco += -1*(xLen)
            #Centering around a coordinate rather than propogating from a corner 
            yco += -1*yLen*(div/2)
            xco += -1*xLen*(div/2)
            yco *= -1
            sqList.append((i, xco, yco))
            if( (i%div<=8) and (int(i/div)<8)):
                if i in blacks:
                    q1.append((i,1))
                    continue
                if i in whites:
                    q1.append((i,0))
                    continue
                if i in reds:
                    q1.append((i,3))
                    continue
                if i in greens:
                    q1.append((i,2))
                    continue
        for i in sqList:
            sqCol.append(i)

#Returns the index of the specified square number in the provided list
def findInd(squareNum,list):
    for index,square in enumerate(list):
        if int(square[0])==int(squareNum):
            return index


#Populates the color pattern from the first quadrant in a mirrored fashion across the quadrants
def mirrorColors():
    for pos in q1:
        for i,sq in enumerate(sqList):
            xco = sqList[findInd(pos[0],sqList)][1]
            yco = sqList[findInd(pos[0],sqList)][2]
            if((abs(sq[1]))==(abs(xco)) and (abs(sq[2]))==(abs(yco))):
                temp = list(sq)
                temp[0] = pos[1]
                sqCol[i] = tuple(temp)
                continue


#Populates a file with the completed grid of RGB values
def printGrid():
    with open('grid.ppm', 'w') as outFile:
        outFile.write('P3\n')
        outFile.write(f'{width} {height}\n')
        outFile.write('255\n')

        start = 0
        while start < 255:
            colors = [sqCol[i][0] for i in range(start, start + div)]
            for _ in range(height // div):
                line = ''
                for c in colors:
                    line += colorKey[c] * (width // div)
                outFile.write(line + '\n')
            start += div


#Runs everything necessary to produce a new unique grid image file 
def runGridGen():
    genColors()
    genSquares()
    mirrorColors()
    printGrid()

if __name__ == "__main__":
    runGridGen()