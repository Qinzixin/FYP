# this file is the beginning code
# this code generates all the sampled points in a folder
from generate_test_set import generate_test_set
from eval import eval
from data.evaluation.calculate import cal
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

import os
from chi_shape import generate_chi_shape,generate_alpha_shape,generate_convex_hull

# To experiment on the whole data set
filepath = "/image/GeographySet/"
sup_path = filepath[1:]
fullpath = os.getcwd() + filepath
image_list = []

for fname in os.listdir(fullpath):
     image_list.append(fname)

# To only experiment on  sample image
#image_list.append("Australia.png")

import math

# Adjust Parameter m
density = math.exp(-10)
print(density)

# To change dataset, replace all 'geography' into new data set name
sample_point_link = "data/sample_points/GeographySet/"
output_link = "data/approximation/GeographySet/"
output_link2 = "data/evaluation/GeographySet/"

if __name__ == "__main__":

    #sample points from images; comment when it is not necessary
    for imgs in image_list:
        outlink = generate_test_set(sup_path+imgs,density)
        print(outlink)


    # generate chi shape for each image
    import datetime
    starttime = datetime.datetime.now()
    iou_t = 0
    precision_t =0
    recall_t = 0
    f1_t = 0
    for imgs in image_list:
        print("------------------------------------")
        print("       "+imgs+"        ")

        imglink = sup_path + imgs
        smplink = sample_point_link + imgs[:-4]+".data"
        shapelink = output_link + imgs[:-4]+"_shape.data"
        speedlink = output_link2 + imgs[:-4]+"_time.data"

        # choose different algorithms and parameters
        generate_convex_hull(smplink, shapelink, speedlink)
        #generate_alpha_shape(smplink, shapelink, speedlink)
        #generate_chi_shape(smplink,shapelink,speedlink,1.0)
        #generate_chi_shape(smplink, shapelink, speedlink, 1.5)
        scorelink =  "data/evaluation/GeographySet/" + imgs[:-4]+"_score.data"

        # evaluate the result
        tuple = eval(imglink,smplink,shapelink,scorelink)

    # long running
    endtime = datetime.datetime.now()
    print(endtime - starttime)

    # metrics calculation
    cal()



