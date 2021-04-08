from generate_test_set import generate_test_set
import os
filepath = "/image/ShapeSet/"
sup_path = filepath[1:]
fullpath = os.getcwd() + filepath
image_list = []
for fname in os.listdir(fullpath):
    image_list.append(fname)
density = 0.00079432

if __name__ == "__main__":
    # sample points from images
    for imgs in image_list:
        outlink = generate_test_set(sup_path+imgs,density)
        #print(outlink)
