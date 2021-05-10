import cv2
import numpy as np
from matplotlib import pyplot as plt

def generate_test_set(link,density):
    # read the image

    img = cv2.imread(link,0)

    # property of img
    height = img.shape[0]
    width = img.shape[1]

    # generate a m*n float numbers in range [0,1)
    mask = np.random.rand(height,width)

    # iterate each pixel, with 1-90% as sample rate
    selected_points = []

    # Othe file to store data
    out_link = "/data/sample_points"+link[5:-4] + ".data"
    file_link = out_link.split("/",4)
    import os
    new_folder = (os.getcwd() + out_link).replace(file_link[-1], "")
    if not os.path.exists(new_folder):  # if the path does not exist, create new folder
        os.makedirs(new_folder)
    fo = open(out_link[1:], 'w')
    plt.figure()
    num = 0
    num_points = density * height * width
    print(num_points)
    points = set()
    while(len(points) < num_points):
        h = np.random.randint(height)
        w = np.random.randint(width)
        if img[h,w] != 255 and (h,w) not in points:
            points.add((w,height-h))
            plt.plot([w],[height-h],'bo')
            s =  str(w) + " " + str(height - h)+ "\n"
            fo.write(s)
    plt.show()
    #plt.cla()
    #plt.close("all")
    fo.close()
    #plt.show()
    #plt.figure()
    #plt.close()
    print("file %s has been generated" % out_link)
    return out_link
