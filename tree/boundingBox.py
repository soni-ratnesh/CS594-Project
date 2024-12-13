import math
import matplotlib.pyplot as plt


class BoundingBox(object):
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min, self.y_min, self.x_max, self.y_max = x_min, y_min, x_max, y_max
    
    def diameter(self):
        return math.sqrt((self.x_max-self.x_min)**2 + (self.y_max - self.y_min)**2)
    
    def contains_point(self, point):
        return self.x_min <= point.x <= self.x_max and self.y_min <= point.y <= self.y_max
    
    def draw(self, ax):
        rect = plt.Rectangle((self.x_min, self.y_min), self.x_max - self.x_min, self.y_max - self.y_min,
                             edgecolor='black', facecolor='none')
        ax.add_patch(rect)
    
