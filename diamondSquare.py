import sys
import math
import random
import graphics
import argparse
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pygame
from pygame.locals import *
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

def genDefaultMap(size, var):
    map = [[0]*size for i in range(size)]
    return map

def genHeight(twoDMap, heightVariance):
    width = len(twoDMap)-1
    while width > 1:
        subSquare = width//2
        for i in range(0, len(twoDMap)-1, width):
            for j in range(0, len(twoDMap)-1, width):
                ave = (twoDMap[i][j]+twoDMap[i+width][j]+twoDMap[i][j+width]+twoDMap[i][j+width])/4
                rand = random.uniform(-heightVariance, heightVariance)
                twoDMap[i+subSquare][j+subSquare] = ave+rand

        for i in range(0, len(twoDMap), subSquare):
            for j in range((i+subSquare)%width, len(twoDMap), width):
                count = 0
                sum  = 0

                sum += twoDMap[i-subSquare][j] if i-subSquare>=0 else 0
                count += 1 if i-subSquare >= 0 else 0
                
                sum += twoDMap[i+subSquare][j] if i+subSquare < len(twoDMap) else 0
                count += 1 if i+subSquare < len(twoDMap) else 0
                
                sum += twoDMap[i][j-subSquare] if j-subSquare>=0 else 0
                count += 1 if j-subSquare >= 0 else 0
                
                sum += twoDMap[i][j+subSquare] if j+subSquare<len(twoDMap) else 0
                count += 1 if j+subSquare<len(twoDMap) else 0
                
                ave = sum/count
                # ave=sum/4
                rand = random.uniform(-heightVariance,heightVariance)
                twoDMap[i][j] = ave+rand

        heightVariance/=2
        width//=2

def drawHeightMap(twoDMap):
    win = graphics.GraphWin('Map',1000,1000, False)
    diff = round(800/len(twoDMap))
    maxH = np.amax(twoDMap)
    minH = np.amin(twoDMap)
    for i in range(0,len(twoDMap)):
        for j in range(0,len(twoDMap)):
            drawcolor = round(255*(twoDMap[i][j])/maxH)
            # drawcolor = round(255*(twoDMap[i][j]-min)/(max-min))
            colorString = '#{0:06x}'.format(drawcolor*256**2+drawcolor*256+drawcolor) if(drawcolor>=0) else 'blue'#'#{0:06x}'.format(255-drawcolor)
            point = graphics.Rectangle(graphics.Point(diff*i,diff*j),graphics.Point(diff*(i+1),diff*(j+1)))
            point.setFill(colorString)
            point.draw(win)
    win.flush()
    win.getMouse()
    win.close()
def draw3DMapMPL(twoDMap):
    z = np.array(twoDMap)
    x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))
    water = [[0]*len(x) for i in range(len(y))]
    # w = np.array(water)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x,y,z)
    # ax.plot_surface(x,y,w)
    plt.title('3d map')
    plt.show(block=False)
    input("Press any key to stop")
    plt.close('all')

def heightMap(twoDMap):
    # print(np.amax(twoDMap))
    vertices = []
    edges = []
    rec = []
    length = len(twoDMap)
    minWater = np.amin(twoDMap)
    for x in range(len(twoDMap)):
        for y in range(len(twoDMap)):
            # vertices.append((x,y,twoDMap[x][y])) if twoDMap[x][y] >0 else vertices.append((x,y,0))
            vertices.append((x,y,twoDMap[x][y]))
            # if twoDMap[x][y] < 0:
            #     print(twoDMap[x][y])
    for y in range(length-1, -1, -1):
        for x in range(length-1, -1, -1):
            if y < length-1 and x < length-1:
                rec.append(((x*length)+y,(x*length)+y+1, (x+1)*length+y+1,(x+1)*length+y))
            # if y < length-1:
            #     edges.append((x*length+y,x*length+y+1))
            # if x < length-1:
            #     edges.append((x*length+y,(x+1)*length+y))
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    # glBegin(GL_QUADS)
    # glColor3iv((200,200,200))
    # for square in rec:
    #     for vertex in square:
    #         glVertex3fv(vertices[vertex])
    # glEnd()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glBegin(GL_QUADS)
    
    for i in range(length-1):
        glColor3fv((.5,.5,.5))
        glVertex3fv((0,i,twoDMap[0][i])) if twoDMap[0][i] >=0 else glVertex3fv((0,i,0))
        glVertex3fv((0,i,0))
        glVertex3fv((0,i+1,0))
        glVertex3fv((0,i+1,twoDMap[0][i+1])) if twoDMap[0][i+1] >=0 else glVertex3fv((0,i+1,0))

    
        glVertex3fv((length-1,i,twoDMap[length-1][i])) if twoDMap[length-1][i] >=0 else glVertex3fv((length-1,i,0))
        glVertex3fv((length-1,i,0))
        glVertex3fv((length-1,i+1,0))
        glVertex3fv((length-1,i+1,twoDMap[length-1][i+1])) if twoDMap[length-1][i+1] >=0 else glVertex3fv((length-1,i+1,0))

        glVertex3fv((i,0,twoDMap[i][0])) if twoDMap[i][0] >=0 else glVertex3fv((i,0,0))
        glVertex3fv((i,0,0))
        glVertex3fv((i+1,0,0))
        glVertex3fv((i+1,0,twoDMap[i+1][0]))if twoDMap[i+1][0] >=0 else glVertex3fv((i+1,0,0))

        glVertex3fv((i,length-1,twoDMap[i][length-1])) if twoDMap[i][length-1] >=0 else glVertex3fv((i,length-1,0))
        glVertex3fv((i,length-1,0))
        glVertex3fv((i+1,length-1,0))
        glVertex3fv((i+1,length-1,twoDMap[i+1][length-1])) if twoDMap[i+1][length-1] >=0 else glVertex3fv((i+1,length-1,0))
    for square in rec:
        maxHeight = -1000000
        for vertex in square:
            maxHeight = max(maxHeight, vertices[vertex][2])
        if maxHeight <= -6:
            glColor3fv((0,0,255/255))
        elif maxHeight <= 0:
            glColor3fv((0/255,160/255,255/255))
        elif maxHeight <= 6:
            # glColor3fv((98,89,75))
            glColor3fv((249/255,227/255,190/255))
        elif maxHeight > 150:
            glColor3fv((255/255, 250/255, 250/255))
        else:
            glColor3fv((155/255,118/255,83/255))
        for vertex in square:
            # print(vertices[vertex])
            # if vertices[vertex][2] < 0:
            #     print("test")
            #     vertices[vertex] = (vertices[vertex][0], vertices[vertex][1], 0)
            temp = vertices[vertex] if vertices[vertex][2] > 0 else (vertices[vertex][0],vertices[vertex][1],0)
            glVertex3fv(temp)
            # print(vertices[vertex])

    
    glEnd()

    glDepthFunc(GL_LEQUAL)

    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glBegin(GL_QUADS)
    # glDisable(GL_POLYGON_OFFSET_FILL);
    # glDepthMask(GL_TRUE)
    
    # glDepthFunc(GL_ALWAYS)
    # print(len(rec))
    for square in rec:
        glColor3fv((0,0,0))
        # print(len(square))
        max_height = -1000000
        for vertex in square:
            max_height = max(max_height, vertices[vertex][2])
        if max_height <= -6:
            glColor3fv((0,0,1))
        elif max_height <= 0:
            glColor3fv((0,160/255,1))
        else:
            glColor3fv((0,0,0))
        for vertex in square:
            temp = vertices[vertex] if vertices[vertex][2] > 0 else (vertices[vertex][0],vertices[vertex][1],0)
            glVertex3fv(temp)
    
    glEnd()

    glDepthFunc(GL_LESS)
    
    
    # glBegin(GL_LINES)
    # glColor3iv((0,0,0))
    # for edge in edges:
    #     for vertex in edge:
    #         glVertex3fv(vertices[vertex])
    # glEnd()

def draw3DSelf(twoDMap, x=1000, y=1000):
    pygame.init()
    display = (x,y)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_LINE_SMOOTH)
    glDepthRange(0.0,1.0)
    # glDepthFunc(GL_LEQUAL)
    # glLineWidth(2.0)
    gluPerspective(45, (x/y),.1,5000)
    glTranslate(-len(twoDMap)/2,-len(twoDMap)/2,-(len(twoDMap)*3000/(x+y)))
    glRotate(-50,1,0,0)
    # test = True
    while True:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x1 = len(twoDMap)/2
                    y1 = len(twoDMap)/2
                    glTranslatef(x1,y1,x1*3000/(x+y))
                    glRotatef(10,0,0,1)
                    glTranslatef(-x1,-y1,-x1*3000/(x+y))
                elif event.key == pygame.K_RIGHT:
                    x1 = len(twoDMap)/2
                    y1 = len(twoDMap)/2
                    glTranslatef(x1,y1,x1*3000/(x+y))
                    glRotatef(-10,0,0,1)
                    glTranslatef(-x1,-y1,-x1*3000/(x+y))
            # event to rotate
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        heightMap(twoDMap)
        pygame.display.flip()
        pygame.time.wait(10)
        # test= False
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--size", type=int)
    parser.add_argument("-v", "--variance", type=float)
    parser.add_argument("-s", "--seed", type=int)
    args = parser.parse_args()

    # size = int(sys.argv[1])
    if not args.size or not args.variance:
        print("incorrect parameters use: python diamondSquare.py -n [size] -v [variance] (Optional:) -s [seed]")
        exit()
    size = args.size
    log = math.log2(size-1)
    if math.floor(log) != math.ceil(log):
        print("Invalid Size: must be in the form 2^n+1")
        exit
    # heightVariance = int(sys.argv[2])*(size-1)
    if args.seed:
        random.seed(args.seed)
    heightVariance = args.variance*(size-1)/10
    map = genDefaultMap(size, heightVariance)
    genHeight(map, heightVariance)
    # if map[int((size-1)/2)][int((size-1)/2)]<=0:
    #     for i in map:
    #         for j in i:
    #             j *= -1
    # drawHeightMap(map)
    # draw3DMapMPL(map)
    draw3DSelf(map)
    # for i in range(0,size):
    #     for j in range(0,size):
    #         print("%.2f "%map[i][j], end='')
    #     print("")