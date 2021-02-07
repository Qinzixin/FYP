class Edge:
    def __init__(self,key , weight, fro, to, gradient):
        self.id = key;
        self.weight = weight;
        self.fro = fro;
        self.to = to;
        self.gradient = gradient;
        self.is_boundary = False;
        self.angle = 2e10;


    def check_edge_exist(self, f, t):
        if self.fro == f and self.to == t:
            return True
        '''
        if self.fro == t and self.to == f:
            return True
        '''
        return False

    def print(self):
        print(self.weight, self.fro, self.to)
