import cv2
import numpy as np
import math


class Point:
    def __init__(self, position, parent, orientation, parent_distance=None):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.parent = parent
        self.orientation = orientation
        self.distance = self.calculate_distance(parent_distance)
        self.heuristics = self.calculate_heuristics()
        self.step = 5

    def __str__(self):
        return f'Class Point:\nPosition: {self.position}\nParent: {self.parent}\n' \
               f'Orientation: {self.orientation}\nHeuristics: {self.heuristics}\nDistance: {self.distance}'

    def calculate_distance(self, parent_distance):
        if self.parent:
            if self.orientation == 'N' or self.orientation == 'E' or self.orientation == 'S' or self.orientation == 'W':
                return parent_distance + 1
            else:
                return parent_distance + 1.41
        else:
            return 0

    def calculate_heuristics(self):
        return math.sqrt(abs(self.position[0] - 360) * abs(self.position[0] - 360) + abs(self.position[1] - 30) *
                         abs(self.position[1] - 30))

    def get_state_lattice(self):
        N = Point((self.x, self.y - self.step), self.position, 'N', self.distance)
        NE = Point((self.x + self.step, self.y - self.step), self.position, 'NE', self.distance)
        E = Point((self.x + self.step, self.y), self.position, 'E', self.distance)
        SE = Point((self.x + self.step, self.y + self.step), self.position, 'SE', self.distance)
        S = Point((self.x, self.y + self.step), self.position, 'S', self.distance)
        SW = Point((self.x - self.step, self.y + self.step), self.position, 'SW', self.distance)
        W = Point((self.x - self.step, self.y), self.position, 'W', self.distance)
        NW = Point((self.x - self.step, self.y - self.step), self.position, 'NW', self.distance)
        if self.orientation == 'N':
            return [N, NW, NE]
        if self.orientation == 'NE':
            return [N, E, NE]
        if self.orientation == 'E':
            return [E, NE, SE]
        if self.orientation == 'SE':
            return [S, E, SE]
        if self.orientation == 'S':
            return [S, SE, SW]
        if self.orientation == 'SW':
            return [S, W, SW]
        if self.orientation == 'W':
            return [W, SW, NW]
        if self.orientation == 'NW':
            return [N, W, NE]

    def return_path(self):
        if self.parent:
            path_points = []
            if self.parent[0] == self.x:
                for y in range(self.step):
                    path_point = (self.x, int(self.y + y * ((self.parent[1] - self.y) / abs(self.parent[1] - self.y))))
                    path_points.append(path_point)
            elif self.parent[1] == self.y:
                for x in range(self.step):
                    path_point = (int(self.x + x * ((self.parent[0] - self.x) / abs(self.parent[0] - self.x))), self.y)
                    path_points.append(path_point)
            else:
                for xy in range(self.step):
                    path_point = (int(self.x + xy * ((self.parent[0] - self.x) / abs(self.parent[0] - self.x))),
                                  int(self.y + xy * ((self.parent[1] - self.y) / abs(self.parent[1] - self.y))))
                    path_points.append(path_point)
            return path_points


map = cv2.imread("mapa3.png")

width = np.shape(map)[1]
height = np.shape(map)[0]

start = Point((20, 20), None, 'E')
points = [start]
queue = [start]
while queue:
    point = queue.pop(0)
    new_points = point.get_state_lattice()
    for new_point in new_points:
        is_new = True
        if 0 > new_point.x > width and 0 > new_point.y > height:
            is_new = False
        if map[new_point.x, new_point.y, 0] == 0 and map[new_point.x, new_point.y, 1] == 0 and \
                map[new_point.x, new_point.y, 2] == 0:
            is_new = False
        for i in range(5):
            if map[new_point.x + i, new_point.y + 4, 0] == 0 or map[new_point.x - i, new_point.y + 4, 0] == 0 or \
                    map[new_point.x + i, new_point.y - 4, 0] == 0 or map[new_point.x - i, new_point.y - 4, 0] == 0 or \
                    map[new_point.x + 4, new_point.y + i, 0] == 0 or map[new_point.x + 4, new_point.y + i, 0] == 0 or \
                    map[new_point.x - 4, new_point.y - i, 0] == 0 or map[new_point.x - 4, new_point.y - i, 0] == 0:
                is_new = False
        for point in points:
            if point.position == new_point.position and point.orientation == new_point.orientation:
                is_new = False
                break
        if is_new:
            points.append(new_point)
            queue.append(new_point)

for point2 in points:
    path = point2.return_path()
    if path:
        for point in path:
            print(point)
            map[point[0], point[1]] = [255, 0, 0]

points = sorted(points, key=lambda e: e.distance)
path = []
for point in points:
    if point.y == 360 and point.x == 30:
        path.append(point)
        break
while True:
    print(len(path))
    if path[-1].distance == 0:
        break
    for point in points:
        if point.x == path[-1].parent[0] and point.y == path[-1].parent[1]:
            path.append(point)
            break

for point2 in path:
    path_from_point = point2.return_path()
    if path_from_point:
        for point in path_from_point:
            print(point)
            map[point[0], point[1]] = [0, 0, 255]

map = cv2.resize(map, (1200,900), interpolation=cv2.INTER_AREA)
cv2.imshow('map', map)
cv2.waitKey(0)
cv2.destroyAllWindows()
