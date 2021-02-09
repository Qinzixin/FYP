from vertex import Vertex
import math
import copy


class Graph:
    def __init__(self):
        self.verList = {} # v-id -> vertex object
        self.edgeList = {} # e-id -> edge object
        self.numVertices = 0
        self.numEdges = 0
        self.edge_repl = {}
        self.vertex_repl = {}

    def get_edge_set(self):
        return self.edgeList

    def replace_by_edge(self,v_id,e_id):
        def generate_rpl_edge():
            for edge in self.edgeList.values(): # edge is the object
                self.edge_repl[edge.fro,edge.id] = edge.to
        generate_rpl_edge() # the dictionary for all edge's linkage relationship
        return self.edge_repl.get((v_id,e_id),"None")

    def the_clockwise_edge(self,e_id, transition_id):
        def get_angle(edge):
            return edge.angle
        begin_edge = self.edgeList[e_id]
        print("\nstarting edge ", e_id)
        trans_vertex = self.verList.get(transition_id)
        print("transition point ",  transition_id)
        list = copy.copy(trans_vertex.edges)
        print("the list is")

        cardinality = len(list)
        for j in range(cardinality):
            if list[j].to == self.edgeList[e_id].fro:
                list.pop(j)
                break
            elif (len(list)== cardinality):
                j += 1

        for edge in list:
            vec1_x = self.verList[begin_edge.fro].x - self.verList[begin_edge.to].x
            vec1_y = self.verList[begin_edge.fro].y - self.verList[begin_edge.to].y
            vec2_x = self.verList[edge.to].x - self.verList[edge.fro].x
            vec2_y = self.verList[edge.to].y - self.verList[edge.fro].y
            dot = vec1_x * vec2_y - vec2_x* vec1_y
            modulus_1 = math.sqrt(math.pow(vec1_x,2) + math.pow(vec1_y,2))
            modulus_2 = math.sqrt(math.pow(vec2_x, 2) + math.pow(vec2_y, 2))
            inner = (vec1_x * vec2_x + vec1_y * vec2_y)
            result = inner / (modulus_1 * modulus_2)

            if dot > 0:
                cos_theta = result # big bug!!! avoid using arc cos!!!
            else :
                cos_theta = -2 - result

            print("edge candidate:",edge.id )#,vec1_x, vec1_y , vec2_x , vec2_y ,cos_theta)
            edge.angle = cos_theta
        sorted_edges = sorted(list, key = get_angle)
        #for edge in sorted_edges:
            #print("angle = %s" % edge.angle)
            #print(self.verList[edge.fro].x,self.verList[edge.fro].y,self.verList[edge.to].x,self.verList[edge.to].y)

        if sorted_edges and trans_vertex:
            next_edge = sorted_edges[0]
            print("next edge:")
            print(next_edge.id)
            return next_edge.id
        else:
            return None

    def replace_by_vertex(self,e_id,transition_id):
        def generate_rpl_vertex():
            for edge in self.edgeList.values():
                vertex = edge.to # vertex is an id
                self.vertex_repl[edge.id,vertex] = self.the_clockwise_edge(edge.id,vertex) #连接的最近的边的id
        generate_rpl_vertex()
        return self.vertex_repl.get((e_id,transition_id),"None")


    def get_vertex_set(self):
        return self.verList

    def get_numVertx(self):
        return self.numVertices

    def get_numEdge(self):
        return self.numEdges

    def addVertex(self, key,x,y):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key,x,y)
        self.verList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.verList:
            return self.verList[n]
        else:
            return None

    def __contains__(self, item):
        return item in self.verList or item in self.edgeList

    def print(self):
        for v in self.verList:
            print(v)
        for e in self.edgeList.values():
            e.print()

    def check_edge(self, f, t):
        for edge in self.edgeList.values():
            if edge.check_edge_exist(f, t):
                return True
        return False

    def addEdge(self, edge):
        id = edge.id
        f = edge.fro
        t = edge.to
        cost = edge.weight
        #检查顶点的序号是否合法
        if f not in self.verList:
            nv = self.addVertex(f)
        if t not in self.verList:
            nv = self.addVertex(t)
        # f and t are indices
        if self.check_edge(f, t) == False:
            # set vertex f's (which is a object in the verlist ) neighbour
            self.verList[f].addNeighbor(self.verList[t], cost)
            # update connectedTo dictionary for a vertex
            self.verList[f].addConnection(edge)
            # update edge set for a vertex

            self.numEdges = self.numEdges +1
            # new_edge = Edge(self.numEdges,cost, f, t)

            self.edge_repl[f,edge.id] = t

            self.edgeList[edge.id]= edge