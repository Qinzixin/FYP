from vertex import Vertex
import math
import copy


import functools


class Graph:
    def __init__(self):
        self.verList = {}  # v-id -> vertex object
        self.edgeList = {}  # e-id -> edge object
        self.numVertices = 0
        self.numEdges = 0
        self.edge_repl = {}
        self.vertex_repl = {}
        self.boundary = []

    def get_edge_set(self):
        return self.edgeList

    # 调用的 edgeList
    def replace_by_edge(self, v_id, e_id,change):
        def generate_rpl_edge():
            for edge in self.edgeList.values():  # edge is the object
                self.edge_repl[edge.fro, edge.id] = edge.to
        if change == True:
            generate_rpl_edge()  # the dictionary for all edge's linkage relationship
        return self.edge_repl.get((v_id, e_id), "None")

    # 图变化后需要重新生成
    def the_clockwise_edge(self, e_id, transition_id):
        def get_angle(edge):
            return edge.angle

        begin_edge = self.edgeList[e_id]
        # print("\nstarting edge ", e_id)
        trans_vertex = self.verList.get(transition_id)
        # print("transition point ",  transition_id)
        list = copy.copy(trans_vertex.edges)
        # print("the list is")

        cardinality = len(list)
        for j in range(cardinality):
            if list[j].to == self.edgeList[e_id].fro:
                list.pop(j)
                break
            elif (len(list) == cardinality):
                j += 1

        for edge in list:
            vec1_x = self.verList[begin_edge.fro].x - self.verList[begin_edge.to].x
            vec1_y = self.verList[begin_edge.fro].y - self.verList[begin_edge.to].y
            vec2_x = self.verList[edge.to].x - self.verList[edge.fro].x
            vec2_y = self.verList[edge.to].y - self.verList[edge.fro].y
            dot = vec1_x * vec2_y - vec2_x * vec1_y
            modulus_1 = math.sqrt(math.pow(vec1_x, 2) + math.pow(vec1_y, 2))
            modulus_2 = math.sqrt(math.pow(vec2_x, 2) + math.pow(vec2_y, 2))
            if not modulus_1*modulus_2==0:
                inner = (vec1_x * vec2_x + vec1_y * vec2_y)
                result = inner / (modulus_1 * modulus_2)

                if dot > 0:
                    cos_theta = result  # big bug!!! avoid using arc cos!!!
                else:
                    cos_theta = -2 - result
            else:
                cos_theta = -5
            # print("edge candidate:",edge.id )#,vec1_x, vec1_y , vec2_x , vec2_y ,cos_theta)
            edge.angle = cos_theta
        sorted_edges = sorted(list, key=get_angle)
        # for edge in sorted_edges:
        # print("angle = %s" % edge.angle)
        # print(self.verList[edge.fro].x,self.verList[edge.fro].y,self.verList[edge.to].x,self.verList[edge.to].y)

        if sorted_edges and trans_vertex:
            next_edge = sorted_edges[0]
            # print("next edge:")
            # print(next_edge.id)
            return next_edge.id
        else:
            return None

    # 图变化后需要重新生成
    def replace_by_vertex(self, e_id, transition_id, change):
        def generate_rpl_vertex():
            self.vertex_repl.clear()
            for edge in self.edgeList.values():
                vertex = edge.to  # vertex is an id
                self.vertex_repl[edge.id, vertex] = self.the_clockwise_edge(edge.id, vertex)  # 连接的最近的边的id

        if change == True:
            generate_rpl_vertex()
        return self.vertex_repl.get((e_id, transition_id), "None")

    def get_vertex_set(self):
        return self.verList

    def get_numVertx(self):
        return self.numVertices

    def get_numEdge(self):
        return self.numEdges

    def addVertex(self, key, x, y):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key, x, y)
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
        cost = edge.length
        # 检查顶点的序号是否合法
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

            self.numEdges = self.numEdges + 1
            # new_edge = Edge(self.numEdges,cost, f, t)

            self.edge_repl[f, edge.id] = t

            self.edgeList[edge.id] = edge

    def get_anti_edge(self,eid):
        return eid + 1;

    @property
    def get_boundary_edges(self):
        boundary = []
        arrow_cnt = self.numEdges;

        for edge in self.edgeList.values():
            vertex = edge.to  # vertex is an id
            self.vertex_repl[edge.id, vertex] = self.the_clockwise_edge(edge.id, vertex)  # 连接的最近的边的id

        def three_edge_trial(e):
            t1 = self.replace_by_vertex(e, self.edgeList[e].to,False)
            t2 = self.replace_by_vertex(t1, self.edgeList[t1].to,False)
            t3 = self.replace_by_vertex(t2, self.edgeList[t2].to,False)
            #print(e)
            #print(e == t3)
            if e == t3:
                return True  # this is a inner edge candidate
            return False

        for k in range(0, arrow_cnt, 2):
            anti_k = self.get_anti_edge(k)
            if not (three_edge_trial(k) and three_edge_trial(anti_k)):
                boundary.append(k)
                boundary.append(anti_k)
                self.edgeList[k].is_boundary = True
                self.edgeList[anti_k].is_boundary = True

        print(boundary)
        return boundary

    def get_boundary_vertex(self, boundary):
        bd_nodes = []
        for node in self.verList:
            self.verList[node].bd = False
            for bd in boundary:
                if self.edgeList[bd].fro == node or self.edgeList[bd].to == node:
                    self.verList[node].bd = True
                    bd_nodes.append(node)
                    break
        return bd_nodes


    def sort_egdes(self, edge_list):
        def cmp(x, y):
            if x.length == y.length:
                if x.id < y.id:
                    return -1
                else:
                    return 1
            else:
                if x.length < y.length:
                    return 1
                else:
                    return -1
        bd_edges = []
        for edge_id in edge_list:
            bd_edges.append(self.edgeList[edge_id])
        bd_edges = sorted(bd_edges, key=functools.cmp_to_key(cmp))
        bd_edges_index = []
        for edge in bd_edges:
            bd_edges_index.append(edge.id)
        return bd_edges_index

    def edge_elimination(self, edge_queue, l, bd):
        def get_anti_edge(eid):
            return eid + 1;

       # return the reveal point
        def reveal(edge_id):
            reveal = -1
            edge = self.edgeList[edge_id]
            reveal_edge_0 = self.replace_by_vertex(self.edgeList[edge_id].anti, edge.fro,True)

            reveal_edge_1 = self.replace_by_vertex(edge_id, edge.to,False)
            inner_vertex = self.replace_by_edge(edge.to, reveal_edge_1,False)

            reveal_edge_2 = self.replace_by_vertex(reveal_edge_1, inner_vertex,False)
            out_vertex = self.replace_by_edge(inner_vertex, reveal_edge_2,False)

            reveal_edge_3 = self.replace_by_vertex(reveal_edge_2, out_vertex,False)

            if reveal_edge_3 == edge_id:
                reveal = reveal_edge_1
            else:
                reveal = reveal_edge_0

            return reveal

        # only to be used in regular judgement
        def reveal2(edge_id):
            reveal = -1
            edge = self.edgeList[edge_id]
            reveal_edge_0 = self.replace_by_vertex(get_anti_edge(edge_id), edge.fro,True)

            reveal_edge_1 = self.replace_by_vertex(edge_id, edge.to,False)
            inner_vertex = self.replace_by_edge(edge.to, reveal_edge_1,False)

            reveal_edge_2 = self.replace_by_vertex(reveal_edge_1, inner_vertex,False)
            out_vertex = self.replace_by_edge(inner_vertex, reveal_edge_2,False)

            reveal_edge_3 = self.replace_by_vertex(reveal_edge_2, out_vertex,False)

            if reveal_edge_3 == edge_id:
                #reveal = reveal_edge_1
                vertex = inner_vertex
            else:
                #reveal = reveal_edge_0
                anti_edge =self.edgeList[self.edgeList[edge_id].anti]
                r2_id = self.replace_by_vertex(anti_edge.id,anti_edge.to,True)
                r2 = self.edgeList[r2_id]
                vertex = r2.to
            return vertex


        def regular(edge_id):
            v = reveal2(edge_id)
            vertex = self.verList[v]
            if vertex.bd == False:
                return True
            else:
                return False

        print("Remain elements in queue:", end=' ')
        while not edge_queue.empty():
            print(edge_queue.qsize(), " ", end='')
            e = edge_queue.get()
            e2 = edge_queue.get()
            if regular(e) and self.edgeList[e].length>l:
                dart_1 = e
                dart_2 = self.edgeList[e].anti
                r1 = reveal(dart_1)
                self.edgeList[r1].is_boundary = True
                vertex_r = self.edgeList[r1].to
                self.verList[vertex_r].bd = True
                r2 = self.vertex_repl[r1,vertex_r]
                self.edgeList[r2].is_boundary = True
                # remove edge from vertex's incident edges
                start = self.edgeList[dart_1].fro
                to = self.edgeList[dart_1].to
                v_start = self.verList[start]
                v_to = self.verList[to]
                v_start.edges.remove(self.edgeList[e])
                anti_e_id = self.edgeList[e].anti
                v_to.edges.remove(self.edgeList[anti_e_id])
                # remove edge from queue and delete the edge from the graph
                self.edgeList.pop(dart_1)
                self.edgeList.pop(dart_2)
                # add reveal edge to the list
                edge_queue.put(r1)
                edge_queue.put(self.edgeList[r1].anti)
                edge_queue.put(r2)
                edge_queue.put(self.edgeList[r2].anti)

