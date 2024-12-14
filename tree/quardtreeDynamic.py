from .quardTree import QuardTree

class QuardTreeDynamic(object):
    def __init__(self):
        self.levels = []
    def _ensure_levels(self, k):
        while len(self.levels) <= k:
            self.levels.append(None)

    def insert(self, point):
        carry = [point]
        i = 0
        while True:
            self._ensure_levels(i)
            if self.levels[i] is None:
                qt = QuardTree()
                qt.build(carry)
                self.levels[i] = qt

                for j in range(i):
                    self.levels[j] = None
                break
            else:
                old_points = self.levels[i].points
                carry = old_points + carry
                self.levels[i] = None
                i += 1

    def searchANN(self, query_pt, epsilon):
        best_point = None
        best_dist = float('inf')

        for qt in self.levels:
            if qt is not None:
                candidate = qt.searchANN(query_pt, epsilon)
                dist = query_pt.cal_distance(candidate)
                if dist < best_dist:
                    best_dist = dist
                    best_point = candidate
        return best_point

    def get_all_points(self):
        all_points = []
        for qt in self.levels:
            if qt is not None:
                all_points.extend(qt.points)
        return all_points

    
