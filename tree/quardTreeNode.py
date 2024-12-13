from .points import Point

class QuardTreeNode(object):
    def __init__(self, representative, boundary):
        self.boundary = boundary
        self.representative = representative
        self.children = []
        
    def _cal_representative(self):
        if not self.is_leaf() and self.children:
            for ii in range(len(self.children)):
                if  isinstance(self.children[ii].representative, Point):
                    return self.children[ii].representative  
        return None
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def remove_point(self, point):
        if self.representative == point:
            self.representative = None
