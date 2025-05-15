import sys, math, random, os, time, copy
from PIL import Image, ImageDraw, UnidentifiedImageError

width = int(1024)
height = int(1024)

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, other):
    x = self.x + other.x
    y = self.y + other.y
    return Point(x,y)
  
  def __sub__(self, other):
    x = self.x - other.x
    y = self.y - other.y
    return Point(x,y)
  
  def __rmul__(self,num):
    return Point(self.x*num,self.y*num)
  
  def __mul__(self,num):
    return Point(self.x*num,self.y*num)
  
  def __truediv__(self,num):
    return Point(self.x/num, self.y/num)


class Region:
  def __init__(self, vertices):
    self.vertices = vertices
    if(len(vertices)==3):
      self.type = 'tri'
      self.tip = vertices[0]
      self.edge = [vertices[1],vertices[2]]
    else:
      self.type = 'rect'
    

  def corners(self):
    corn = []
    for vert in self.vertices:
      corn.append((vert.x,vert.y))
    return corn
  
  def xMirrored(self):
    corn = []
    for vert in self.vertices:
      corn.append((width-vert.x,vert.y))
    return corn
  
  def yMirrored(self):
    corn = []
    for vert in self.vertices:
      corn.append((vert.x, height-vert.y))
    return corn
  
  def flipped(self):
    corn = []
    for vert in self.vertices:
      corn.append((width-vert.x, height-vert.y))
    return corn

  # returns the boundaries of the rectangle as the minimums, the maximums, and then the center
  def rectBounds(self):
    xmin = width
    xmax = -1
    ymin = height
    ymax = -1
    for vert in self.vertices:
      if vert.x>xmax:
        xmax = vert.x
      if vert.y>ymax:
        ymax = vert.y
      if vert.x<xmin:
        xmin=vert.x
      if vert.y<ymin:
        ymin = vert.y
    xcent = xmin+(xmax-xmin)/2
    ycent = ymin+(ymax-ymin)/2
    return [Point(xmin,ymin), Point(xmax,ymax),Point(xcent,ycent)]

  # quadrisects a rectangle into 4 triangles by drawing lines between each corner opposite eachother  
  def firstRectSect(self):
    center = self.rectBounds()[2]
    verts1 = [center,self.vertices[0],self.vertices[1]]
    verts2 = [center,self.vertices[1],self.vertices[2]]
    verts3 = [center,self.vertices[2],self.vertices[3]]
    verts4 = [center,self.vertices[3],self.vertices[0]]
    return [Region(verts1),Region(verts2),Region(verts3),Region(verts4)]

  # quadrisects a rectangle into 4 rectangles dividing the x component into 4 lengths
  def secondRectSect(self):
    bounds = self.rectBounds()
    xmin = bounds[0].x
    xmax = bounds[1].x
    xStep = Point((xmax-xmin)/4,0)
    botCorn = Point(bounds[0].x,bounds[1].y)
    topCorn = Point(bounds[0].x,bounds[0].y)
    verts1 = [topCorn, topCorn+xStep, botCorn+xStep,botCorn]
    verts2 = [topCorn+xStep, topCorn+2*xStep, botCorn+2*xStep,botCorn+xStep]
    verts3 = [topCorn+2*xStep, topCorn+3*xStep, botCorn+3*xStep,botCorn+2*xStep]
    verts4 = [topCorn+3*xStep, topCorn+4*xStep, botCorn+4*xStep,botCorn+3*xStep]
    return [Region(verts1),Region(verts2),Region(verts3),Region(verts4)]
  
  # quadrisects a rectangle into 4 rectangles dividing the y component into 4 lengths
  def thirdRectSect(self):
    bounds = self.rectBounds()
    ymin = bounds[0].y
    ymax = bounds[1].y
    yStep = Point(0,(ymax-ymin)/4)
    leftCorn = Point(bounds[0].x,bounds[0].y)
    rightCorn = Point(bounds[1].x,bounds[0].y)
    verts1 = [leftCorn, rightCorn, rightCorn+yStep,leftCorn+yStep]
    verts2 = [leftCorn+yStep, rightCorn+yStep, rightCorn+2*yStep, leftCorn+2*yStep]
    verts3 = [leftCorn+2*yStep,rightCorn+2*yStep , rightCorn+3*yStep, leftCorn+3*yStep]
    verts4 = [leftCorn+3*yStep,rightCorn+3*yStep, rightCorn+4*yStep, leftCorn+4*yStep]
    return [Region(verts1),Region(verts2),Region(verts3),Region(verts4)]
  
  # quadrisect a rectangle into 4 rectangles by drawing lines between the midpoints of opposite side lengths
  def fourthRectSect(self):
    bounds = self.rectBounds()
    cent = bounds[2]
    topMid = Point(bounds[2].x,bounds[0].y)
    rightMid = Point(bounds[1].x,bounds[2].y)
    botMid = Point(bounds[2].x,bounds[1].y)
    leftMid = Point(bounds[0].x,bounds[2].y)
    verts1 = [self.vertices[0], topMid, cent, leftMid]
    verts2 = [topMid, self.vertices[1], rightMid, cent]
    verts3 = [cent, rightMid, self.vertices[2], botMid]
    verts4 = [leftMid, cent, botMid, self.vertices[3]]
    return [Region(verts1),Region(verts2),Region(verts3),Region(verts4)]
  
  # quadrisects a triangle into 4 triangles with the same tip and a quarter of the base edge
  def oneTriSect(self):
    tip = self.tip
    edge = self.edge
    start = edge[0]
    edgeStep = (edge[1]-start)/4
    verts1 = [tip, start, start+edgeStep ]
    verts2 = [tip, start+edgeStep, start+edgeStep*2]
    verts3 = [tip, start+edgeStep*2, start+edgeStep*3]
    verts4 = [tip, start+edgeStep*3, start+edgeStep*4]
    return[Region(verts1),Region(verts2),Region(verts3),Region(verts4)]



  def quadrisect(self, instance):
    if self.type=='rect':
      if(instance==0):
        functs = [ self.secondRectSect, self.thirdRectSect, self.fourthRectSect]
      else:
        functs = [self.firstRectSect, self.secondRectSect, self.thirdRectSect, self.fourthRectSect]
      random.shuffle(functs)
      return functs[0]()
    if self.type=='tri':
      return self.oneTriSect()
    
  def lastSect(self):
    if self.type=='rect':
      functs = [self.firstRectSect, self.secondRectSect, self.thirdRectSect, self.fourthRectSect]
      random.shuffle(functs)
      print(f'calling {functs[0]}')
      return functs[0]()
    if self.type=='tri':
      return self.oneTriSect()


def drawImage(fileName, regions):
  img = Image.new("RGB", (width, height), "white")
  draw = ImageDraw.Draw(img)
  colors = [(255,255,255),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255))]
  for region in regions:   
      random.shuffle(colors)
      for i in range(len(region)):
        draw.polygon(region[i].corners(), fill=colors[i])
        draw.polygon(region[i].xMirrored(), fill=colors[i])
        draw.polygon(region[i].yMirrored(), fill=colors[i])
        draw.polygon(region[i].flipped(), fill=colors[i])
  # img.save(fileName,quality=80)
  img.show()

def runGenerate(output="mandala.png"):
    initialRectangle = Region([Point(0,0),Point(width/2,0),Point(width/2,height/2),Point(0,height/2)])
    firstSplit = initialRectangle.fourthRectSect()
    thisSplit = firstSplit
    nextSplit = []
    div = random.randint(1,3)
    for i in range(div):
      if i == 0:
        for ent in thisSplit:
          nextSplit.append(ent.quadrisect(i))
        thisSplit=[copy.deepcopy(region) for region in nextSplit]
      else:
        for list in thisSplit:
          for ent in list:
            nextSplit.append(ent.quadrisect(i))
        thisSplit=[copy.deepcopy(region) for region in nextSplit]
    drawImage(output, thisSplit)



if __name__ == "__main__":
    runGenerate()