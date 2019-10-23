import numpy
from pylab import *
from queue import PriorityQueue
import copy

# 定义一个含有障碍物的20×20的栅格地图
# 10表示可通行点
# 0表示障碍物

MapSize = 20
map_grid = numpy.full((21, 21), int(10), dtype=numpy.int8)
map_grid[0, 0:21] = 0
map_grid[0:21, 0] = 0
map_grid[20, 0:21] = 0
map_grid[0:21, 20] = 0
map_grid[3, 3:8] = 0
map_grid[3:10, 7] = 0
map_grid[10, 3:8] = 0
map_grid[17, 13:17] = 0
map_grid[10:17, 13] = 0
map_grid[10, 13:17] = 0

'''
MapSize = 5

map_grid = numpy.full((MapSize+2, MapSize+2), int(10), dtype=numpy.int8)
map_grid[0, 0:MapSize+2] = 0
map_grid[0:MapSize+2, 0] = 0
map_grid[MapSize+1, 0:MapSize+2] = 0
map_grid[0:MapSize+2, MapSize+1] = 0

map_grid[3, 2:5] = 0

'''

class AStar(object):
    def drawMap(self, a):
        map_direction = copy.deepcopy(map_grid)
        
        for i in set(a.open):
            #print(i)
            map_direction[i] = 8

        for i in a.path:
            #print(i)
            map_direction[i] = 6

        map_direction[a.start] = 4
        map_direction[a.goal] = 3

        plt.imshow(map_direction, cmap=plt.cm.hot, interpolation='nearest', vmin=0, vmax=10)
        # plt.colorbar()
        xlim(-1, MapSize+1)  # 设置x轴范围
        ylim(-1, MapSize+1)  # 设置y轴范围
        my_x_ticks = numpy.arange(1, MapSize+2, 1)
        my_y_ticks = numpy.arange(1, MapSize+2, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        plt.grid(True)

    def calc(self, a, b):
        #return 10 * max(abs(a[0] - b[0]), abs(a[1] - b[1]))
        return numpy.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def __init__(self):
        self.start = (5, 2)  # 起点坐标
        self.goal = (15, 15)  # 终点坐标
        '''
        self.start = (1, 3)  # 起点坐标
        self.goal = (5, 3)  # 终点坐标
        '''
        self.f = {}
        self.prec = {}
        for i in range(0, MapSize+2):
            for j in range(0, MapSize+2):
                self.f[i, j] = 233333333   # Inf
                self.prec[i, j] = (i, j)
        
        self.f[self.start] = 0
        self.dx =   [ 0, 1, 1, 1, 0,-1,-1,-1]
        self.dy =   [ 1, 1, 0,-1,-1,-1, 0, 1]
        self.dDis = [self.calc((0, 0), (self.dx[i], self.dy[i])) for i in range(8)]
        self.open = []
        self.path = []

    def getPath(self, curPos):
        self.path.append(curPos)
        #print(curPos)
        if self.prec[curPos] == curPos:
            return
        self.getPath(self.prec[curPos])

    def main(self):
        q = PriorityQueue()

        q.put((self.calc(self.start, self.goal), self.start))
        
        plt.figure()
        ax1 = plt.subplot(111)
        plt.sca(ax1)
        plt.show()

        while not q.empty():
            curDis, curPos = q.get()
            
            plt.figure()
            ax1 = plt.subplot(111)
            plt.sca(ax1)
            self.drawMap(self)

            self.open.append(curPos)

            if curPos == self.goal:
                print('success')
                break

            for i in range(8):
                newPos = (curPos[0] + self.dx[i], curPos[1] + self.dy[i])
                newDis = self.f[curPos] + self.dDis[i]

                if map_grid[newPos] != 0 and newDis < self.f[newPos]:
                    self.f[newPos] = newDis
                    self.prec[newPos] = curPos
                    q.put((newDis + self.calc(newPos, self.goal), newPos))
        
        self.getPath(self.goal)

if __name__ == '__main__':

    a1 = AStar()
    a1.main()
