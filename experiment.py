# this file is the beginning code
# this code generates all the sampled points in a folder
from generate_test_set import generate_test_set
from eval import eval

import os
from chi_shape import generate_chi_shape,generate_alpha_shape,generate_convex_hull
filepath = "/image/ShapeSet/"
sup_path = filepath[1:]
fullpath = os.getcwd() + filepath
image_list = []

for fname in os.listdir(fullpath):
    image_list.append(fname)

#image_list.append("France.png")
#density = 0.00079432
import math
density = math.exp(-7.13)
print(density)

sample_point_link = "data/sample_points/ShapeSet/"
output_link = "data/approximation/ShapeSet/"
output_link2 = "data/evaluation/ShapeSet/"

if __name__ == "__main__":
    # sample points from images

    for imgs in image_list:
        outlink = generate_test_set(sup_path+imgs,density)
        print(outlink)

    # generate chi shape for each image
    import datetime
    starttime = datetime.datetime.now()
    for imgs in image_list:
        print("------------------------------------")
        print("       "+imgs+"        ")
        print("------------------------------------")
        imglink = sup_path + imgs
        smplink = sample_point_link + imgs[:-4]+".data"
        shapelink = output_link + imgs[:-4]+"_shape.data"
        speedlink = output_link2 + imgs[:-4]+"_time.data"
        generate_convex_hull(smplink,shapelink,speedlink)
        scorelink =  "data/evaluation/ShapeSet/" + imgs[:-4]+"_score.data"
        eval(imglink,smplink,shapelink,scorelink)
    # long running
    # do something other
    endtime = datetime.datetime.now()
    print(endtime - starttime)



