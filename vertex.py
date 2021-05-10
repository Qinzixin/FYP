class Vertex:
    def __init__(self, key,x ,y):
        self.id = key
        self.x = x
        self.y = y
        self.bd = False

        self.connectedTo = {}  # Adjacency list, represented as a dictionary, represents the leading vertex
        # id -> weight

        self.edges = [] # When the node is from, the collection of edges stores the edge object
        # set of edges


    def print(self):
        print(self.key, self.connectedTo)

    # nbr is the ID of the connected node
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
