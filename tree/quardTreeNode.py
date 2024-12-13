class QuardTreeNode(object):
    def __init__(self, points, boundary):
        self.boundary = boundary
        self.points = points
        self.representative = self._cal_representative()
        self.children = []
        
    def _cal_representative(self):
        if self.points:
            return self.points[0]
        return None
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def remove_point(self, point):
        if point in self.points:
            self.points.remove(point)
        self.representative = self._cal_representative()
