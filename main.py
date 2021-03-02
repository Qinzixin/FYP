import numpy as np
import matplotlib.pyplot as plt
import math
from vertex import Vertex
from edge import Edge
from graph import Graph

# 在建图时应该尽量用graph层次提供的api

# vertex location, in x,y form
map = [[1,1],[2,2],[3,4],[4,1],[5,3]]

# edge : start node, end node and length
matrix = [[1, 3, 1], [1, 4, 2], [2, 3, 3], [2, 4, 4], [3, 5, 5], [4, 5, 6], [1, 2, 7],[2,5,1]]


def buildGraph(vertices,edges):
    graph = Graph()
    i = 0
    for vertex in vertices:
        i = i+1 # the key that uniquely identifies the vertex
        x = vertex[0] # the x coordinate of the vertex
        y = vertex[1] # the y coordinate
        v = Vertex(i,x,y)
        graph.addVertex(i,x,y)
        # new a vertex, write to graph's vertex list (which is a dictionary)
        # vid -> v object
        # the vertex dictionary adopts a key(id) and add a vertex object to the graph's vertex list
    e = 0
    for edge in edges:
        for i in range(2):
            '''
            deal with vertex
            '''
            weight = edge[2]
            if i == 0:
                fro,to = edge[0],edge[1]
            else:
                to,fro = edge[0],edge[1]
            # check the vertex is valid
            if fro not in graph.verList.keys():
                graph.verList[fro] = Vertex(fro,0,0) # 默认坐标是原点
            if to not in graph.verList.keys():
                graph.verList[to] = Vertex(to,0,0)
            # 根据id找到对应的vertex对象
            start_vertex = graph.verList[fro]
            end_vertex = graph.verList[to]
            # compute the edge's gradient
            gradient = (start_vertex.y - end_vertex.y)/(start_vertex.x - end_vertex.x)
            # compute the edge's length
            length = (1.0 + pow(gradient,2))*abs(start_vertex.x - end_vertex.x)
            '''
              construct edges
            '''
            # generate a edge object
            new_edge = Edge(e,weight, fro, to, gradient,length)
            # append to edge list: id -> edge object
            graph.addEdge(new_edge)
            e= e+1
    return graph


if __name__ == "__main__":
    # map is the set of vertex coordinate
    # matrix is the edge relation
    s = buildGraph(map,matrix)
    #s.print()
    points = np.array(map)
    plt.plot(points[:, 0], points[:, 1], 'o',color="black",markersize=1.5)
    for edge in s.edgeList.values():
        v1 = s.getVertex(edge.fro)
        v2 = s.getVertex(edge.to)
        x1, x2 = v1.x, v2.x
        y1, y2 = v1.y, v2.y
        #print(x1,x2,y1,y2)
        plt.plot([x1,x2],[y1,y2])

    # map an edge to its next edge
    mv1 = s.replace_by_edge(3,8)
    #print("is mapped to " + "% s" % mv1 )

    mv = s.replace_by_vertex(8,5)
    #print("is mapped to " + "% s" % mv )
    #s.get_edge_set()

    bd_e = s.get_boundary_edges
    bd_v = s.get_boundary_vertex(bd_e)
    bd_sorted = s.sort_egdes(bd_e)
    print(bd_sorted)
    s.edge_elimination(bd_sorted,0.0,bd_sorted)

    plt.show()