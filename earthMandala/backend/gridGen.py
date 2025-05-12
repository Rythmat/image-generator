import sys, math, random, os, time
from PIL import Image, UnidentifiedImageError

#parameters to indicate png size
width = int(512)
height = int(512)

def makeColorKey():
    # red = [random.randint(180,255),random.randint(0, 60), random.randint(0, 60) ]
    # green = [random.randint(0, 80), random.randint(160, 255), random.randint(0, 80)]
    # dark = [random.randint(80, 120), random.randint(50, 90), random.randint(30, 60)]
    # light = [random.randint(220, 255), random.randint(220, 255), random.randint(220, 255)]
    red = [random.randint(0,255),random.randint(0, 255), random.randint(0, 255) ]
    green = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    dark = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    light = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    return {0: '255 255 255\t', 1:f'{dark[0]} {dark[1]} {dark[2]}\t', 2:f'{green[0]} {green[1]} {green[2]}\t', 3:f'{red[0]} {red[1]} {red[2]}\t' }


def genColors(div, colored):
    for i in range(int(div*div/16)):
        base = 2*i + int(1.5*div*math.floor(i*4/div))
        bases = [base+1, base+2, base+div+1, base+div+2]
        random.shuffle(bases)
        colored["whites"].append(bases[0])
        colored["blacks"].append(bases[1])
        colored["greens"].append(bases[2])
        colored["reds"].append(bases[3])


#Generates list of squares with corner and number determined by the number of divisions.
def genSquares(div, xLen, yLen, sqList, sqCol, q1, colored):
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
                if ((i%div) > (div/2)) or (i%div==0):
                    xco -= xLen
            #Centering around a coordinate rather than propogating from a corner 
            yco += -1*yLen*(div/2)
            xco += -1*xLen*(div/2)
            yco *= -1
            sqList.append((i, xco, yco))
            if( (i%div<=int(div/2)) and (int(i/div)<int(div/2))):
                if i in colored["blacks"]:
                    q1.append((i,1))
                    continue
                if i in colored["whites"]:
                    q1.append((i,0))
                    continue
                if i in colored["reds"]:
                    q1.append((i,3))
                    continue
                if i in colored["greens"]:
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
def mirrorColors(div,  sqList, sqCol, q1):
    for pos in q1:
        sq1 = pos[0]
        sq2 = pos[0] + div - 2 * (pos[0]%div) + 1
        sq3 = div*div - div*(math.floor(pos[0]/div)+1) + pos[0]%div
        sq4 = div*div - div*(math.floor(pos[0]/div)+1) + pos[0]%div + div - 2 * (pos[0]%div) + 1
        sqCol[sq1-1] = (pos[1], sqList[findInd(sq1,sqList)][1],sqList[findInd(sq1,sqList)][2])
        sqCol[sq2-1] = (pos[1], sqList[findInd(sq2,sqList)][1],sqList[findInd(sq2,sqList)][2])
        sqCol[sq3-1] = (pos[1], sqList[findInd(sq3,sqList)][1],sqList[findInd(sq3,sqList)][2])
        sqCol[sq4-1] = (pos[1], sqList[findInd(sq4,sqList)][1],sqList[findInd(sq4,sqList)][2])

#Populates a file with the completed grid of RGB values
def printGrid(div, colorKey, sqCol, output="grid.png"):
    ppm = output.replace(".png", "ppm")
    with open(ppm, 'w') as outFile:
        outFile.write('P3\n')
        outFile.write(f'{width} {height}\n')
        outFile.write('255\n')

        start = 0
        while start < div*div-1:
            colors = [sqCol[i][0] for i in range(start, start + div)]
            for _ in range(height // div):
                line = ''
                for c in colors:
                    line += colorKey[c] * (width // div)
                outFile.write(line + '\n')
            start += div

        outFile.flush()
        os.fsync(outFile.fileno())
    for _ in range(20):
        try:
            with Image.open(ppm) as img:
                img.load()
                img.save(output)
            break
        except (UnidentifiedImageError, ValueError, OSError):
            time.sleep(0.1)
    os.remove(ppm)


#Runs everything necessary to produce a new unique grid image file 
def runGridGen(output="grid.png"):
    sqList = []
    sqCol = []
    q1 = []
    colored = {
        'whites': [],
        'blacks': [],
        'greens': [],
        'reds': []
    }
    divs = [8,16,32]
    random.shuffle(divs)
    div = divs[0]
    xLen = int(width/div)
    yLen = int(height/div)
    colors = makeColorKey()
    genColors(div, colored)
    genSquares(div, xLen, yLen, sqList, sqCol, q1, colored)
    mirrorColors(div, sqList, sqCol, q1)
    for tup in sqCol:
        if(tup[0]>3):
            print(tup)
    printGrid(div, colors, sqCol, output)


if __name__ == "__main__":
    runGridGen()