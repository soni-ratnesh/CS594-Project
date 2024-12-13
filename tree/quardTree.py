from .quardTreeNode import QuardTreeNode
from .boundingBox import BoundingBox



class QuardTree(object):
    def __init__(self):
        self.root = None
    
    def build(self, points):

        x_coords = [point.x for point in points]
        y_coords = [point.y for point in points]

        boundary = BoundingBox(
                x_min=min(x_coords),
                y_min=min(y_coords),
                x_max=max(x_coords),
                y_max=max(y_coords)
            )
        
        self.root = QuardTreeNode(points=points, boundary=boundary)
        self._subdivide(self.root)
    
    def _subdivide(self, node):
        if node is None:
            return ValueError("Build QuardTree it first")
        
        x_mid = (node.boundary.x_max - node.boundary.x_min)/2 + node.boundary.x_min
        y_mid = (node.boundary.y_max - node.boundary.y_min)/2 + node.boundary.y_min

        quards = [
            BoundingBox(node.boundary.x_min, node.boundary.y_min, x_mid, y_mid),
            BoundingBox(x_mid, node.boundary.y_min, node.boundary.x_max, y_mid),
            BoundingBox(node.boundary.x_min, y_mid, x_mid, node.boundary.y_max),
            BoundingBox(x_mid, y_mid, node.boundary.x_max, node.boundary.y_max)
        ]

        quard_points = {quard : [] for quard in quards}

        for point in node.points:
            for quard in quards:
                if quard.contains_point(point):
                    quard_points[quard].append(point)
                    break

        for quard, points in quard_points.items():
            if points:
                child = QuardTreeNode(boundary=quard, points=points)
                node.children.append(child)
                if len(points) > 1:
                    self._subdivide(child) 
    
    def searchANN(self, query_pt, epsilon):
        S = [self.root]

        curr_point = self.root.representative
        curr_distance = query_pt.cal_distance(curr_point)

        while S:
            node = S.pop(0)
            node_distance = query_pt.cal_distance(node.representative)
            
            if node_distance < curr_distance:
                curr_distance = node_distance
                curr_point = node.representative

            if (node_distance - node.boundary.diameter()) < ((1 - epsilon / 2) * curr_distance):
                S.extend([child for child in node.children])

        return curr_point
