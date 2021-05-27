import cv2
import numpy as np
import math


class Point:
    def __init__(self, position, parent, orientation, distance, move=None, parent_distance=None, reverse=False):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.parent = parent
        self.orientation = orientation
        if parent_distance:
            self.distance = parent_distance + distance
        else:
            self.distance = distance
        self.heuristics = self.calculate_heuristics() + self.distance
        self.pixels_per_m = 10
        self.move = move
        self.angle_step = 15
        self.reverse = reverse

    def __str__(self):
        return f'Class Point:\nPosition: {self.position}\nParent: {self.parent}\n' \
               f'Orientation: {self.orientation}\nHeuristics: {self.heuristics}\nDistance: {self.distance}'

    def calculate_heuristics(self):
        return math.sqrt(abs(self.position[0] - 360) * abs(self.position[0] - 360) + abs(self.position[1] - 30) *
                         abs(self.position[1] - 30))

    @staticmethod
    def do_rotate(angle, x, y):
        rad = np.radians(angle)
        x_prim = x * np.cos(-rad) - y * np.sin(-rad)
        y_prim = x * np.sin(-rad) + y * np.cos(-rad)
        return x_prim, y_prim

    def get_state_lattice(self):
        sl_points = []
        for jump in range(7):
            # if abs(jump - self.move) <=1:
            if jump == 3:
                orient = self.orientation
                x = 2.5 * self.pixels_per_m
                y = 0
                x, y = self.do_rotate(self.orientation, x, y)
                sl_points.append(Point((int(x) + self.x, int(y) + self.y), self.position, orient, 25, jump, self.distance, False))
            else:
                orient = self.orientation + (self.angle_step * jump - 3 * self.angle_step)
                x = 5 * self.pixels_per_m
                radius = x / np.sin(abs(jump - 3) * np.radians(self.angle_step))
                y = -(jump - 3) / abs(jump - 3) * (radius - np.cos(abs(jump - 3) * np.radians(self.angle_step)) * radius)
                x, y = self.do_rotate(self.orientation, x, y)
                sl_points.append(Point((int(x) + self.x, int(y) + self.y), self.position, orient,
                                       abs(jump - 3) * 20 + 4, jump, self.distance, False))
            if jump == 3:
                orient = self.orientation
                x = -1.5 * self.pixels_per_m
                y = 0
                x, y = self.do_rotate(self.orientation, x, y)
                x = int(x) + self.x
                y = int(y) + self.y
                sl_points.append(Point((x, y), self.position, orient, 30, jump, self.distance, True))
            else:
                orient = self.orientation - (self.angle_step * (jump - 3))
                x = 5 * self.pixels_per_m
                radius = x / np.sin(abs(jump - 3) * np.radians(self.angle_step))
                y = -(jump - 3) / abs(jump - 3) * (
                            radius - np.cos(abs(jump - 3) * np.radians(self.angle_step)) * radius)
                x, y = self.do_rotate(self.orientation, -x, y)
                x = int(x) + self.x
                y = int(y) + self.y
                sl_points.append(Point((x, y), self.position, orient,
                                       abs(jump - 3) * 60 + 12, jump, self.distance, True))

        return sl_points

    def return_path(self):
        if self.parent:
            if not self.reverse:
                path_points = [(self.parent[0], self.parent[1])]
                if self.move == 3:
                    xs = np.linspace(self.x, self.parent[0], 26, dtype=np.uint32)
                    ys = np.linspace(self.y, self.parent[1], 26, dtype=np.uint32)
                    for xy in range(26):
                        path_point = (xs[xy], ys[xy])
                        path_points.append(path_point)
                else:
                    for i in range(1, 71):
                        jump = self.move
                        orient = self.orientation - (self.angle_step * jump - 3 * self.angle_step)
                        rad = i / 70 * abs(jump - 3) * np.radians(self.angle_step)
                        radius = 5 / np.sin(abs(jump - 3) * np.radians(self.angle_step))
                        x = (np.sin(rad) * radius) * self.pixels_per_m
                        y = -(jump - 3) / abs(jump - 3) * (radius - np.cos(rad) * radius) * self.pixels_per_m
                        x, y = self.do_rotate(orient, x, y)
                        path_point = (int(x)+self.parent[0], int(y)+self.parent[1])
                        if not path_points[0] == path_point:
                            path_points.append(path_point)
                return path_points
            else:
                path_points = [(self.parent[0], self.parent[1])]
                if self.move == 3:
                    xs = np.linspace(self.x, self.parent[0], 26, dtype=np.uint32)
                    ys = np.linspace(self.y, self.parent[1], 26, dtype=np.uint32)
                    for xy in range(26):
                        path_point = (xs[xy], ys[xy])
                        path_points.append(path_point)
                else:
                    for i in range(1, 71):
                        jump = self.move
                        orient = self.orientation + (self.angle_step * jump - 3 * self.angle_step)
                        rad = i / 70 * abs(jump - 3) * np.radians(self.angle_step)
                        radius = 5 / np.sin(abs(jump - 3) * np.radians(self.angle_step))
                        x = (np.sin(rad) * radius) * self.pixels_per_m
                        y = -(jump - 3) / abs(jump - 3) * (radius - np.cos(rad) * radius) * self.pixels_per_m
                        x, y = self.do_rotate(orient, -x, y)
                        path_point = (int(x) + self.parent[0], int(y) + self.parent[1])
                        if not path_points[0] == path_point:
                            path_points.append(path_point)
                return path_points


map_name = "mapa2.png"
map = cv2.imread(map_name)
map = np.transpose(map, (1, 0, 2))
width = np.shape(map)[1]
height = np.shape(map)[0]

start = []
start_pos = (0, 0)
end_pos = (0, 0, 0)

if map_name == "mapa2.png":
    start_pos = (70, 70)
    end_pos = (780, 1380, 90)
    start = Point(start_pos, None, 270, 0, 3)
if map_name == "mapa3.png":
    start_pos = (120, 120)
    end_pos = (100, 1440, 270)
    start = Point(start_pos, None, 270, 0, 3)
if map_name == "mapa6.png":
    start_pos = (20, 20)
    end_pos = (40, 260, 0)
    start = Point(start_pos, None, 180, 0, 3)
if map_name == "mapa7.png":
    start_pos = (60, 60)
    end_pos = (750, 960, 90)
    start = Point(start_pos, None, 270, 0, 3)

points = [start]
queue = [start]
end_found = False
while queue:
    print(len(queue))
    queue = sorted(queue, key=lambda e: e.heuristics)
    point = queue.pop(0)
    new_points = point.get_state_lattice()
    for new_point in new_points:
        is_new = True
        if 0 > new_point.x or new_point.x > height-10 or new_point.y > width-10 or 0 > new_point.y:
            is_new = False
            continue
        for point in points:
            if abs(new_point.x - point.x) < 3 and abs(new_point.y - point.y) < 3 \
                    and abs(new_point.orientation - point.orientation) < 10:
                is_new = False
                continue
        if not new_point.reverse:
            if new_point.move == 3:
                xs = np.linspace(new_point.x, new_point.parent[0], 5, dtype=np.uint32)
                ys = np.linspace(new_point.y, new_point.parent[1], 5, dtype=np.uint32)
                for xy in range(5):
                    middle_point = (xs[xy], ys[xy])
                    x_add, y_add = Point.do_rotate(new_point.orientation, 5, 5)
                    if map[middle_point[0] + int(x_add), middle_point[1] + int(y_add), 0] == 0 or \
                            map[middle_point[0] - int(y_add), middle_point[1] + int(x_add), 0] == 0 or \
                            map[middle_point[0] + int(y_add), middle_point[1] - int(x_add), 0] == 0 or \
                            map[middle_point[0] - int(x_add), middle_point[1] - int(y_add), 0] == 0:
                        is_new = False
                        break
            else:
                for i in range(1, 20):
                    jump = new_point.move
                    orient = new_point.orientation - (new_point.angle_step * jump - 3 * new_point.angle_step)
                    rad = i / 20 * abs(jump - 3) * np.radians(new_point.angle_step)
                    radius = 5 / np.sin(abs(jump - 3) * np.radians(new_point.angle_step))
                    x = (np.sin(rad) * radius) * new_point.pixels_per_m
                    y = -(jump - 3) / abs(jump - 3) * (radius - np.cos(rad) * radius) * new_point.pixels_per_m
                    x, y = new_point.do_rotate(orient, x, y)
                    middle_point = (int(x) + new_point.parent[0], int(y) + new_point.parent[1])
                    x_add, y_add = Point.do_rotate(orient, 5, 5)
                    if map[middle_point[0] + int(x_add), middle_point[1] + int(y_add), 0] == 0 or \
                            map[middle_point[0] - int(y_add), middle_point[1] + int(x_add), 0] == 0 or \
                            map[middle_point[0] + int(y_add), middle_point[1] - int(x_add), 0] == 0 or \
                            map[middle_point[0] - int(x_add), middle_point[1] - int(y_add), 0] == 0:
                        is_new = False
                        break
        else:
            if new_point.move == 3:
                xs = np.linspace(new_point.x, new_point.parent[0], 5, dtype=np.uint32)
                ys = np.linspace(new_point.y, new_point.parent[1], 5, dtype=np.uint32)
                for xy in range(5):
                    middle_point = (xs[xy], ys[xy])
                    x_add, y_add = Point.do_rotate(new_point.orientation, 5, 5)
                    if map[middle_point[0] + int(x_add), middle_point[1] + int(y_add), 0] == 0 or \
                            map[middle_point[0] - int(y_add), middle_point[1] + int(x_add), 0] == 0 or \
                            map[middle_point[0] + int(y_add), middle_point[1] - int(x_add), 0] == 0 or \
                            map[middle_point[0] - int(x_add), middle_point[1] - int(y_add), 0] == 0:
                        is_new = False
                        break
            else:
                for i in range(1, 20):
                    jump = new_point.move
                    orient = new_point.orientation + (new_point.angle_step * jump - 3 * new_point.angle_step)
                    rad = i / 20 * abs(jump - 3) * np.radians(new_point.angle_step)
                    radius = 5 / np.sin(abs(jump - 3) * np.radians(new_point.angle_step))
                    x = (np.sin(rad) * radius) * new_point.pixels_per_m
                    y = -(jump - 3) / abs(jump - 3) * (radius - np.cos(rad) * radius) * new_point.pixels_per_m
                    x, y = new_point.do_rotate(orient, -x, y)
                    middle_point = (int(x) + new_point.parent[0], int(y) + new_point.parent[1])
                    x_add, y_add = Point.do_rotate(orient, 5, 5)
                    if map[middle_point[0] + int(x_add), middle_point[1] + int(y_add), 0] == 0 or \
                            map[middle_point[0] - int(y_add), middle_point[1] + int(x_add), 0] == 0 or \
                            map[middle_point[0] + int(y_add), middle_point[1] - int(x_add), 0] == 0 or \
                            map[middle_point[0] - int(x_add), middle_point[1] - int(y_add), 0] == 0:
                        is_new = False
                        break
        if map[new_point.x, new_point.y, 0] == 0 and map[new_point.x, new_point.y, 1] == 0 and \
                map[new_point.x, new_point.y, 2] == 0:
            is_new = False
            continue
        for jump in range(9):
            if map[new_point.x + jump, new_point.y + 8, 0] == 0 or map[new_point.x - jump, new_point.y + 8, 0] == 0 or \
                    map[new_point.x + jump, new_point.y - 8, 0] == 0 or map[new_point.x - jump, new_point.y - 8, 0] == 0 or \
                    map[new_point.x + 8, new_point.y + jump, 0] == 0 or map[new_point.x + 8, new_point.y + jump, 0] == 0 or \
                    map[new_point.x - 8, new_point.y - jump, 0] == 0 or map[new_point.x - 8, new_point.y - jump, 0] == 0:
                is_new = False
                break
        # for point in points:
        #     if point.position == new_point.position and point.orientation == new_point.orientation:
        #         is_new = False

        if is_new:
            points.append(new_point)
            queue.append(new_point)
            map[new_point.x, new_point.y] = [0, 0, 255]
            # cv2.imshow('map', map)
            # cv2.waitKey(0)

            if abs(new_point.x - end_pos[0]) < 25 and abs(new_point.y - end_pos[1]) < 25 \
                    and abs(new_point.orientation % 360 - end_pos[2]) <= 30:
                end_found = True
                print("end found!")
                break
    # if len(queue) > 25:
    #     break
    if end_found:
        break


for point2 in points:
    path = point2.return_path()
    if path:
        for point in path:
            map[point[0], point[1]] = [255, 0, 0]

points = sorted(points, key=lambda e: e.distance)
if end_found:
    path = []
    for point in points:
        if abs(point.x - end_pos[0]) < 25 and abs(point.y - end_pos[1]) < 25 and abs(point.orientation % 360 - end_pos[2]) <= 45:
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
                map[point[0], point[1]] = [0, 0, 255]

# map = cv2.resize(map, (750,1000), interpolation=cv2.INTER_AREA)
cv2.imshow('map', map)
cv2.waitKey(0)
cv2.destroyAllWindows()