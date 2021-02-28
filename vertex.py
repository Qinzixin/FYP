class Vertex:
    def __init__(self, key,x ,y):
        self.id = key
        self.x = x
        self.y = y
        self.bd = False

        self.connectedTo = {}  # 领结列表，表示为字典，表示领居顶点
        # id -> weight

        self.edges = [] # 表示节点为from的情况下，边的集合，存的是edge的对象
        # set of edges


    def print(self):
        print(self.key, self.connectedTo)

    # nbr是连接的node的id
    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def addConnection(self,edge):
        self.edges.append(edge)

    def __str__(self):
        return str(self.id) + "is connected to: " \
               + str(x.id for x in self.connectedTo)

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def get_coordinate(self):
        return [self.x,self.y]

    def get_edges(self):
        return self.edges
