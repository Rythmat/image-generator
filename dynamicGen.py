import sys

#parameters to indicate ppm size
width = int(1280)
height = int(1280)

#The number of squares on the side of an image
div = 16
numSquares = div*div

#The pixel lengths of a square in the image 
xLen = int(width/div)
yLen = int(height/div)

#list of tuples containing the square number, the x coordinate of the starting corner, and the y coordinate of the starting corner
sqList = []
#list of tuples containing the specified color, the x coordinate of the starting corner, and the y coordinate of the starting corner 
sqCol = []
#list of tuples containing the square number, and its specified color
q1 = []

#list of tuples containing the square number, the x coordinate of the starting corner, and the y coordinate of the starting corner if the top corner was indexed as (0,0)
# sqMax = []


#A function to dynamically change the color of the next square/pixel
rVal = 100
gVal = 100
bVal = 100
def generateColor():
    global rVal, gVal, bVal
    rVal += 5
    if(rVal>220):
        rVal = 50
        bVal += 5
    if(bVal>220):
        bVal = 50
        gVal += 5
    if(gVal>220):
        gVal = 50

    

#Generates list of squares with corner and number determined by the number of divisions.
def genSquares():
        for i in range(1, numSquares+1):
            #If the square is in the last column: special casing
            if(i%div==0):
                xco = (div-1)*xLen 
                if (i/div) > (div/2):
                    yco = -1*(yLen)
                else:
                    yco = 0
                yco += (int)(i/div)*(yLen)
                # ymax = (int)(i/div)*(yLen)
                # xmax = width
            #If the square is not in the last column
            else:
                xco = (i%div)*xLen
                # xmax=xco
                yco = ((int)(i/div))*yLen
                if (i/div) < (div/2):
                    yco += yLen
                if (i%div) > (div/2):
                    xco += -1*(xLen)
                # ymax = ((int)(i/div)+1)*(yLen)
            #Centering around a coordinate rather than propogating from a corner 
            yco += -1*yLen*(div/2)
            xco += -1*xLen*(div/2)
            yco *= -1
            # sqMax.append((i, xmax, ymax))
            sqList.append((i, xco, yco))
            # Filling color value for the first quadrant
            if( (i%div<=(div/2)) and (int(i/div)<(div/2))):
                q1.append((i,f"{rVal} {gVal} {bVal}\t"))
                generateColor()
        for i in sqList:
            sqCol.append(i)





#Returns the index of the specified square number in the provided list
def findInd(num,list):
    for ind,i in enumerate(list):
        if int(i[0])==int(num):
            return ind

#Repeats the color pattern from the first quadrant in a mirrored fashion across the quadrants
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

        


def printGrid():
    file = open('grid.ppm','w')
    sys.stdout = file
    start = 0
    print('P3')
    print(width,height)
    print('255')
    while(start<(numSquares-1)):
        colors = []
        for i in range(start, start+div):
            colors.append(sqCol[i][0])
        for row in range(int(height/div)):
            for c in colors:
                for col in range(int(width/div)):
                    print(c,end='')
            print('')
        start += div

def printFun():
    #Sets file output of ppm file
    file = open('art.ppm','w')
    sys.stdout = file


    #Prints header for PPM file
    print('P3')
    print(width,height)
    print('255')

    #Initialize start index
    for row in range(int(height)):
        for col in range(int(width)):
            print(f"{rVal} {gVal} {bVal}\t",end='')
            generateColor()
    


# genSquares()
# mirrorColors()
# printGrid()
printFun()
