import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def cal_distance(self, point):
        return  math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    