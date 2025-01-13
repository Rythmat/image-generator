import sys

#parameters to indicate png size
width = int(1280)
height = int(1280)

#list of tuples containing the square number and its maximum x and y corner
sqList = []
sqMax = []
sqCol = []
q1 = []
q1Col = []
div = 16
printList = []

colorKey = {
        0: '255 255 255\t',
        1: '0 0 0\t',
        2: '76 153 0\t',
        3: '153 76 0\t'
}
xLen = int(width/div)
yLen = int(height/div)
blacks = [103,118,88,69,55,100,54,84,35,24,114,18,19,34,22,82]
whites = [120,72,117,86,39,99,52,53,68,7,97,1,3,33,81,6]
reds = [104,87,101,70,56,115,36,37,83,8,98,4,5,50,66,2]
greens = [119,102,71,85,116,40,51,67,38,23,113,20,21,49,65,17]
#Generates list of squares with corner and number determined by the number of divisions.
def genSquares():
        numSquares = 256
        for i in range(1, numSquares+1):
            #If the square is in the last column: special casing
            if(i%div==0):
                xco = (div-1)*xLen 
                if (i/div) > (div/2):
                    yco = -1*(yLen)
                else:
                    yco = 0
                yco += (int)(i/div)*(yLen)
                ymax = (int)(i/div)*(yLen)
                xmax = width
            #If the square is not in the last column
            else:
                xco=xmax = (i%div)*xLen
                yco = ((int)(i/div))*yLen
                if (i/div) < (div/2):
                    yco += yLen
                if (i%div) > (div/2):
                    xco += -1*(xLen)
                ymax = ((int)(i/div)+1)*(yLen)
            #Centering around a coordinate rather than propogating from a corner 
            yco += -1*yLen*(div/2)
            xco += -1*xLen*(div/2)
            yco *= -1
            sqMax.append((i, xmax, ymax))
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

def printGrid():
    orig_stdout = sys.stdout
    f = open('grid.ppm','w')
    sys.stdout = f
    start = 0
    print('P3')
    print(width,height)
    print('255')
    while(start<255):
        colors = []
        for i in range(start, start+div):
            colors.append(sqCol[i][0])
        for row in range(int(height/div)):
            for c in colors:
                for col in range(int(width/div)):
                    print(colorKey[c],end='')
            print('')
        start += div

    
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


def findInd(num,list):
    for ind,i in enumerate(list):
        if int(i[0])==int(num):
            return ind

genSquares()
mirrorColors()
printGrid()
