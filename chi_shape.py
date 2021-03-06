import numpy as np
import matplotlib.pyplot as plt
import math
import time
from vertex import Vertex
from edge import Edge
from graph import Graph

from queue import Queue

from scipy.spatial import Delaunay
import numpy as np


def read_points_data(file_link,points_i):
    node_data = open(file_link, 'r')
    for line in node_data:
        records = line.split()
        x = float(records[0])
        y = float(records[1])
        points_i.append([x,y])
    node_data.close()

def triangulate(points_i):
    points = np.array(points_i)
    tri = Delaunay(points)
    edges = []
    for relation in tri.simplices:
        if not ([relation[0],relation[1]] in edges or [relation[1],relation[0]] in edges ):
            edges.append([relation[0],relation[1]])
        if not ([relation[1], relation[2]] in edges or [relation[2], relation[1]] in edges ):
            edges.append([relation[1],relation[2]])
        if not ([relation[2], relation[0]] in edges or [relation[0], relation[2]] in edges ):
            edges.append([relation[0],relation[2]])
    edges_match = np.array(edges)
    fro = points[edges_match[:,0]]
    to = points[edges_match[:,1]]
    plt.figure(figsize=(10, 10))
    for i in range(len(fro)):
        x = [fro[i][0], to[i][0]]
        y = [fro[i][1], to[i][1]]
        plt.plot(x,y,color='g')
    plt.plot(points[:, 0], points[:, 1], 'o',color="black",markersize=0.5)
    plt.grid()
    plt.show()
    plt.cla()
    plt.close("all")
    return edges

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
    print("The graph contains",i,"points")
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
            '''
              construct edges
            '''
            # generate a edge object
            if i==0:
                anti = e+1
            else:
                anti = e-1
            new_edge = Edge(e, fro, to, gradient,length,anti)
            # append to edge list: id -> edge object
            graph.addEdge(new_edge)
            graph.calculate_distribution()
            e= e+1
    print("The graph contains", e,"edges")
    print("The graph has",graph.numEdges,"edges")
    print("The graph's edge mean length is ", graph.mean,"virance as",graph.variance)
    return graph

'''
#Demo format:
sample_point_link = "data/sample_points/GeographySet/France.data"
output_link = "data/approximation/GeographySet/France_shape.data"
output_link2 = "data/evaluation/GeographySet/France_time.data"
'''
def generate_chi_shape(sample_point_link,output_link,output_link2,chi):
    points_i = []
    # vertex location, in x,y form
    # map = [[1,1],[2,2],[3,4],[4,1],[5,3]]
    # map is okay
    read_points_data(sample_point_link, points_i)
    edges = triangulate( points_i)
    map = points_i

    # edge : start node, end node and length
    matrix = edges
    # matrix = [[1, 3, 1], [1, 4, 2], [2, 3, 3], [2, 4, 4], [3, 5, 5], [4, 5, 6], [1, 2, 7],[2,5,1]]
    # to be generated
    # map is the set of vertex coordinate
    # matrix is the edge relation

    print("The algorithm starts")
    start_time =  time.time()
    s = buildGraph(map,matrix)
    minimum_length = s.mean * chi
    print("The graph has been built. ")
    points = np.array(map)
    ##plt.figure(figsize=(10, 10))
    ##plt.plot(points[:, 0], points[:, 1], 'o',color="black",markersize=1.5)
    bd_e = s.get_boundary_edges
    bd_v = s.get_boundary_vertex(bd_e)
    bd_sorted = s.sort_egdes(bd_e)
    print("The boundary, with",len(bd_e)," edges,  has been sorted")
    q = Queue(maxsize=250000)

    for i in bd_sorted:
        q.put(i)
    print("Start Elimination")
    s.edge_elimination(q,minimum_length,bd_sorted)
    print("\nEnd of elimination")
    bd_f = []
    for edge in s.edgeList.values():
        proposal = edge
        if proposal.is_boundary == True:
            v1 = s.getVertex(edge.fro)
            v2 = s.getVertex(edge.to)
            x1, x2 = v1.x, v2.x
            y1, y2 = v1.y, v2.y
            ##plt.plot([x1,x2],[y1,y2],color='coral')
            bd_f.append(edge)
    end_time =  time.time()
    dtime = end_time - start_time
    print("Program running time：%.8s s" % dtime)
    ##plt.grid()
    ###plt.show()
    ##plt.cla()
    ##plt.close("all")

    current_proposal = bd_f[0]
    record = []
    record.append(s.edgeList[current_proposal.id])
    while len(bd_f) >1:
        signal = False
        for edge in bd_f:
            edge_anti = s.edgeList[current_proposal.anti]
            if (edge.fro == current_proposal.to and edge.id != edge_anti.id) or len(bd_f)==2:
                record.append(edge)
                if edge_anti in bd_f:
                    bd_f.remove(edge_anti)
                bd_f.remove(current_proposal)
                current_proposal = edge
                signal = True
        # deal with dead edges
        print(current_proposal.id)
        if (not signal):
            bd_f.remove(current_proposal)
            current_proposal = bd_f[0]
            for i in range (10):
                print("********************************exception*****************************")
    co = []
    for edge in record:
        str = "edge (%d) is from %d to %d"  % (edge.id,edge.fro,edge.to)
        print(str)
        point_id = edge.fro
        point = s.verList[point_id]
        str = "point (%d) is at %d, %d"  % (point.id,point.x,point.y)
        print(str)
        co.append([point.x,point.y])
    from shapely.geometry import Polygon
    polygon = Polygon(co)
    print(polygon.area)

    # Othe file to store data
    out_link_arr = output_link.split("/",4)
    new_folder = output_link.replace(out_link_arr[-1],"")
    print(new_folder)
    import os
    folder_link = os.getcwd() +"/"+ new_folder
    print(folder_link)
    if not os.path.exists(folder_link):
        os.makedirs(folder_link)
    file_p = open(output_link, "w")
    for coordinate in co:
        s = "%f %f \n" % (coordinate[0],coordinate[1])
        file_p.write(s)
    file_p.close()

    out_link_arr2 = output_link.split("/",4)
    new_folder2 = output_link.replace(out_link_arr2[-1],"")
    import os
    folder_link2 = os.getcwd() + "/" + new_folder2
    if not os.path.exists(folder_link2):
        os.makedirs(folder_link2)
        print(folder_link2)
    output_link2_array = output_link2.split("/",4)
    storage = os.getcwd()+"/"+output_link2
    print(storage)
    if not os.path.exists(folder_link2):
        os.makedirs(folder_link2.replace(output_link2_array[-1]),"")
        print(folder_link2)

    file_t = open(storage, "w")
    s = "%.8s" % dtime
    file_t.write(s)
    file_t.close()



def generate_convex_hull(sample_point_link, output_link, output_link2):
    points_i = []
    read_points_data(sample_point_link, points_i)
    from scipy.spatial import ConvexHull, convex_hull_plot_2d
    points_c = np.array(points_i)
    start_time = time.time()
    hull = ConvexHull(points_c)
    end_time =  time.time()
    dtime = end_time - start_time
    st = "%.8s" % dtime
    ##plt.figure(figsize=(10, 10))
    #axes = ##plt.gca()
    #axes.set_xlim([0, 600])
    #axes.set_ylim([0, 750])
    ##plt.axis('equal')
    ##plt.plot(points_c[:, 0], points_c[:, 1], 'o')
    bd = []
    x,y = points_c[hull.vertices, 0], points_c[hull.vertices, 1]
    #print(x,y)
    for i in range(len(x)):
        bd.append([x[i],y[i]])
        ##plt.plot(x[i], y[i], 'k-')
    ###plt.plot(points_c[hull.vertices, 0], points_c[hull.vertices, 1], 'b')
    ###plt.plot(points_c[hull.vertices[0], 0], points_c[hull.vertices[0], 1], 'ro')
    ##plt.plot(points_c[hull.vertices, 0], points_c[hull.vertices, 1], 'r--', lw=2)
    ###plt.plot(points[hull.vertices[0], 0], points[hull.vertices[0], 1], 'ro')
    ###plt.show()
    ##plt.close()
    #for pt in bd:
        #print(pt)
    print("end of convex hull")
    # Othe file to store data
    out_link_arr = output_link.split("/", 4)
    new_folder = output_link.replace(out_link_arr[-1], "")
    print(new_folder)
    import os
    folder_link = os.getcwd() + "/" + new_folder
    print(folder_link)
    if not os.path.exists(folder_link):
        os.makedirs(folder_link)
    file_p = open(output_link, "w")
    for coordinate in bd:
        #print(coordinate)
        s = "%f %f \n" % (float(coordinate[0]), float(coordinate[1]))
        file_p.write(s)
    file_p.close()
    out_link_arr2 = output_link.split("/", 4)
    new_folder2 = output_link.replace(out_link_arr2[-1], "")
    import os
    folder_link2 = os.getcwd() + "/" + new_folder2
    if not os.path.exists(folder_link2):
        os.makedirs(folder_link2)
        print(folder_link2)
    output_link2_array = output_link2.split("/", 4)
    storage = os.getcwd() + "/" + output_link2
    print(storage)
    if not os.path.exists(folder_link2):
        os.makedirs(folder_link2.replace(output_link2_array[-1]), "")
        print(folder_link2)
    file_t = open(storage, "w")
    file_t.write(st)
    file_t.close()


def generate_alpha_shape(sample_point_link, output_link, output_link2):
    points_i = []
    read_points_data(sample_point_link, points_i)
    from descartes import PolygonPatch
    import matplotlib.pyplot as plt
    import alphashape
    plt.figure(figsize=(10, 10))
    axes = plt.gca()
    axes.set_xlim([0, 600])
    axes.set_ylim([0, 750])
    plt.axis('equal')
    points_a = np.array(points_i)
    start_time  = time.time()
    alpha_shape = alphashape.alphashape(points_a)
    bd = alpha_shape.boundary.coords
    end_time =  time.time()
    dtime = end_time - start_time
    st = "%.8s" % dtime
    print(bd)
    fig, ax = plt.subplots()
    ax.scatter(*zip(*points_a))
    #ax.add_patch(PolygonPatch(alpha_shape,alpha=0.2))
    print("End of alpha shape")
    plt.show()
    ##plt.cla()
    ##plt.close("all")



    # Output file to store data
    out_link_arr = output_link.split("/", 4)
    new_folder = output_link.replace(out_link_arr[-1], "")
    print(new_folder)
    import os
    folder_link = os.getcwd() + "/" + new_folder
    print(folder_link)
    if not os.path.exists(folder_link):
        os.makedirs(folder_link)
    file_p = open(output_link, "w")
    for coordinate in bd:
        coordinate = str(coordinate).replace("(","")
        coordinate = str(coordinate).replace(")","")
        coordinate = str(coordinate).split(",")
        #print(coordinate)
        s = "%f %f \n" % (float(coordinate[0]), float(coordinate[1]))
        file_p.write(s)
    file_p.close()
    out_link_arr2 = output_link.split("/", 4)
    new_folder2 = output_link.replace(out_link_arr2[-1], "")
    import os
    folder_link2 = os.getcwd() + "/" + new_folder2
    if not os.path.exists(folder_link2):
        os.makedirs(folder_link2)
        print(folder_link2)
    output_link2_array = output_link2.split("/", 4)
    storage = os.getcwd() + "/" + output_link2
    print(storage)
    if not os.path.exists(folder_link2):
        os.makedirs(folder_link2.replace(output_link2_array[-1]), "")
        print(folder_link2)
    file_t = open(storage, "w")
    file_t.write(st)
    file_t.close()



# for debug use only
if __name__ == '__main__':
    sample_point_link = "data/test_case.data"
    output_link = "data/approximation/test_case.data"
    output_link2 = "data/evaluation/test_case.data"
    points_i = []
    # vertex location, in x,y form
    # map = [[1,1],[2,2],[3,4],[4,1],[5,3]]
    # map is okay
    read_points_data(sample_point_link, points_i)

    axes = plt.gca()
    plt.figure(figsize=(10, 10))
    plt.axis('equal')
    for xy in points_i:
        x = xy[0]
        y = xy[1]
        plt.scatter(x,y,c='b')
    plt.show()

    edges = triangulate(points_i)
    map = points_i

    # edge : start node, end node and length
    matrix = edges
    # matrix = [[1, 3, 1], [1, 4, 2], [2, 3, 3], [2, 4, 4], [3, 5, 5], [4, 5, 6], [1, 2, 7],[2,5,1]]
    # to be generated
    # map is the set of vertex coordinate
    # matrix is the edge relation

    print("The algorithm starts")
    start_time = time.time()
    s = buildGraph(map, matrix)
    minimum_length = 0
    print("The graph has been built. ")
    points = np.array(map)
    plt.figure(figsize=(10, 10))
    plt.plot(points[:, 0], points[:, 1], 'o',color="black",markersize=1.5)
    bd_e = s.get_boundary_edges
    bd_v = s.get_boundary_vertex(bd_e)
    bd_sorted = s.sort_egdes(bd_e)
    print("The boundary, with", len(bd_e), " edges,  has been sorted")
    q = Queue(maxsize=250000)

    for i in bd_sorted:
        q.put(i)
    print("Start Elimination")
    s.edge_elimination(q, minimum_length, bd_sorted)
    print("\nEnd of elimination")
    bd_f = []
    for edge in s.edgeList.values():
        proposal = edge
        if proposal.is_boundary == True:
            v1 = s.getVertex(edge.fro)
            v2 = s.getVertex(edge.to)
            x1, x2 = v1.x, v2.x
            y1, y2 = v1.y, v2.y
            plt.plot([x1,x2],[y1,y2],color='coral')
            bd_f.append(edge)
    end_time = time.time()
    dtime = end_time - start_time
    print("Program running time：%.8s s" % dtime)
    plt.grid()
    plt.show()
    plt.cla()
    plt.close("all")

    current_proposal = bd_f[0]
    record = []
    record.append(s.edgeList[current_proposal.id])
    while len(bd_f) > 1:
        signal = False
        for edge in bd_f:
            edge_anti = s.edgeList[current_proposal.anti]
            if (edge.fro == current_proposal.to and edge.id != edge_anti.id) or len(bd_f) == 2:
                record.append(edge)
                if edge_anti in bd_f:
                    bd_f.remove(edge_anti)
                bd_f.remove(current_proposal)
                current_proposal = edge
                signal = True
        # deal with dead edges
        print(current_proposal.id)
        if (not signal):
            bd_f.remove(current_proposal)
            current_proposal = bd_f[0]
            for i in range(10):
                print("********************************exception*****************************")
    co = []
    for edge in record:
        str = "edge (%d) is from %d to %d" % (edge.id, edge.fro, edge.to)
        print(str)
        point_id = edge.fro
        point = s.verList[point_id]
        str = "point (%d) is at %d, %d" % (point.id, point.x, point.y)
        print(str)
        co.append([point.x, point.y])
    from shapely.geometry import Polygon
    polygon = Polygon(co)
    print(polygon.area)

    # Othe file to store data
    out_link_arr = output_link.split("/", 4)
    new_folder = output_link.replace(out_link_arr[-1], "")
    print(new_folder)
    import os
    folder_link = os.getcwd() + "/" + new_folder
    print(folder_link)
    if not os.path.exists(folder_link):
        os.makedirs(folder_link)
    file_p = open(output_link, "w")
    for coordinate in co:
        s = "%f %f \n" % (coordinate[0], coordinate[1])
        file_p.write(s)
    file_p.close()

    out_link_arr2 = output_link.split("/", 4)
    new_folder2 = output_link.replace(out_link_arr2[-1], "")
    import os
    folder_link2 = os.getcwd() + "/" + new_folder2
    if not os.path.exists(folder_link2):
        os.makedirs(folder_link2)
        print(folder_link2)
    output_link2_array = output_link2.split("/", 4)
    storage = os.getcwd() + "/" + output_link2
    print(storage)
    if not os.path.exists(folder_link2):
        os.makedirs(folder_link2.replace(output_link2_array[-1]), "")
        print(folder_link2)

    file_t = open(storage, "w")
    s = "%.8s" % dtime
    file_t.write(s)
    file_t.close()

