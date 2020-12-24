import sys
import math
import random
import graphics
import argparse
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

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
    max = 0
    min = 0
    for i in twoDMap:
        for j in i:
            max = j if j > max else max
            min = j if j < min else min
    for i in range(0,len(twoDMap)):
        for j in range(0,len(twoDMap)):
            drawcolor = round(255*(twoDMap[i][j])/max)
            # drawcolor = round(255*(twoDMap[i][j]-min)/(max-min))
            colorString = '#{0:06x}'.format(drawcolor*256**2+drawcolor*256+drawcolor) if(drawcolor>=0) else 'blue'#'#{0:06x}'.format(255-drawcolor)
            point = graphics.Rectangle(graphics.Point(diff*i,diff*j),graphics.Point(diff*(i+1),diff*(j+1)))
            point.setFill(colorString)
            point.draw(win)
    win.flush()
    win.getMouse()
    win.close()
def draw3DMap(twoDMap):
    z = np.array(twoDMap)
    x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))
    water = [[0]*len(x) for i in range(len(y))]
    w = np.array(water)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x,y,z)
    ax.plot_surface(x,y,w)
    plt.title('3d map')
    plt.show(block=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--size", type=int)
    parser.add_argument("-v", "--variance", type=int)
    parser.add_argument("-s", "--seed", type=int)
    args = parser.parse_args()
    size = args.size

    # size = int(sys.argv[1])
    log = math.log2(size-1)
    if math.floor(log) != math.ceil(log):
        print("Invalid Size: must be in the form 2^n+1")
        exit
    # heightVariance = int(sys.argv[2])*(size-1)
    if args.seed:
        random.seed(args.seed)
    heightVariance = args.variance*(size-1)
    map = genDefaultMap(size, heightVariance)
    genHeight(map, heightVariance)
    # if map[int((size-1)/2)][int((size-1)/2)]<=0:
    #     for i in map:
    #         for j in i:
    #             j *= -1
    # drawHeightMap(map)
    draw3DMap(map)
    input("Press any key to stop")
    plt.close('all')
    # for i in range(0,size):
    #     for j in range(0,size):
    #         print("%.2f "%map[i][j], end='')
    #     print("")