import numpy as np
import matplotlib.pyplot as plt
import math
from vertex import Vertex
from edge import Edge
from graph import Graph

from queue import Queue

from scipy.spatial import Delaunay
import numpy as np

# 在建图时应该尽量用graph层次提供的api
points_i = np.array([[1,1]])

def read_points_data():
    global points_i
    node_data = open('data/design1.data', 'r')
    for line in node_data:
        records = line.split()
        x = float(records[0])
        y = float(records[1])
        points_i = np.append(points_i, [[x, y]], axis=0)
    node_data.close()

def triangulate():
    points = points_i
    tri = Delaunay(points)
    for s in tri.simplices:
        print(s)
    edges = []
    for relation in tri.simplices:
        if not ([relation[0],relation[1]] in edges or [relation[1],relation[0]] in edges ):
            edges.append([relation[0],relation[1]])
        if not ([relation[1], relation[2]] in edges or [relation[2], relation[1]] in edges ):
            edges.append([relation[1],relation[2]])
        if not ([relation[2], relation[0]] in edges or [relation[0], relation[2]] in edges ):
            edges.append([relation[0],relation[2]])
    #print(edges)
    edges_match = np.array(edges)
    fro = points[edges_match[:,0]]
    to = points[edges_match[:,1]]

    for i in range(len(fro)):
        x = [fro[i][0], to[i][0]]
        y = [fro[i][1], to[i][1]]
        plt.plot(x,y,color='g')

    plt.plot(points_i[:, 0], points_i[:, 1], 'o',color="black",markersize=0.5)
    plt.show()
    return edges

# vertex location, in x,y form
# map = [[1,1],[2,2],[3,4],[4,1],[5,3]]
# map is okay
read_points_data()
edges = triangulate()
map = points_i.tolist()

# edge : start node, end node and length
matrix = edges
print(matrix[0])
#matrix = [[1, 3, 1], [1, 4, 2], [2, 3, 3], [2, 4, 4], [3, 5, 5], [4, 5, 6], [1, 2, 7],[2,5,1]]
# to be generated

def buildGraph(vertices,edges):
    graph = Graph()
    i = 0
    for vertex in vertices:
        x = vertex[0] # the x coordinate of the vertex
        y = vertex[1] # the y coordinate
        v = Vertex(i,x,y)
        graph.addVertex(i,x,y)
        i = i+1 # the key that uniquely identifies the vertex
        # new a vertex, write to graph's vertex list (which is a dictionary)
        # vid -> v object
        # the vertex dictionary adopts a key(id) and add a vertex object to the graph's vertex list
    e = 0


    for edge in edges:
        for i in range(2):
            '''
            deal with vertex
            '''
            #weight = edge[2]
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
            # compute the edge's length
            if not (math.isclose(start_vertex.x , end_vertex.x, rel_tol=1e-9)):
                gradient = (start_vertex.y - end_vertex.y)/(start_vertex.x - end_vertex.x)
                length = (1.0 + pow(gradient, 2)) * abs(start_vertex.x - end_vertex.x)
            else:
                gradient = float('inf')
                length  = abs(start_vertex.y - end_vertex.y)
            #print(length)
            '''
              construct edges
            '''
            # generate a edge object
            new_edge = Edge(e, fro, to, gradient,length)
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


    #initial plt
    '''
    for edge in s.edgeList.values():
        v1 = s.getVertex(edge.fro)
        v2 = s.getVertex(edge.to)
        x1, x2 = v1.x, v2.x
        y1, y2 = v1.y, v2.y
        #print(x1,x2,y1,y2)
        plt.plot([x1,x2],[y1,y2])
'''
    bd_e = s.get_boundary_edges
    bd_v = s.get_boundary_vertex(bd_e)
    bd_sorted = s.sort_egdes(bd_e)
    print(bd_sorted)
    print("bd sorted")
    q = Queue(maxsize=250000)

    for i in bd_sorted:
        q.put(i)

    print("Start Elimination")
    s.edge_elimination(q,0.0,bd_sorted)

    print("End of elimination")
    for edge in s.edgeList.values():
        v1 = s.getVertex(edge.fro)
        v2 = s.getVertex(edge.to)
        x1, x2 = v1.x, v2.x
        y1, y2 = v1.y, v2.y
        print(x1,x2,y1,y2)
        plt.plot([x1,x2],[y1,y2],color='coral')

    plt.show()
