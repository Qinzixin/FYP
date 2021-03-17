import cv2
import numpy as np
from matplotlib import pyplot as plt

# read the image
img = cv2.imread("image/E/E.png",0)

# property of img
height = img.shape[0]
width = img.shape[1]

# generate a m*n float numbers in range [0,1)
mask = np.random.rand(height,width)

# iterate each pixel, with 1-90% as sample rate
selected_points = []

# Othe file to store data
fo = open("sample_by_rate.data", "w")

plt.figure()
num = 0
density = 0.00079432
num_points = density * height * width
print(num_points)
points = set()
while(len(points) < num_points):
    h = np.random.randint(height)
    w = np.random.randint(width)
    if img[h,w] != 255 and (h,w) not in points:
        points.add((w,height-h))
        plt.plot([w],[height-h],'bo')
        s = "\n" + str(w) + " " + str(height - h)
        fo.write(s)
plt.show()
'''
for h in range(height):
    for w in range(width):
        if img[h,w] != 255 and mask[h,w] > 0.98:
            selected_points.append([w,height-h]) # conversion between two coordinate system
            plt.plot(w,height-h,'bo')
'''
fo.close()
plt.show()
plt.figure()

'''
# sample by fixed number of points
num_points = 1000
points = set()
while(len(points) < num_points):
    rdi = np.random.randint(img.shape[0])
    rdj = np.random.randint(img.shape[1])
    if img[rdi,rdj] != 255 and (rdi,rdj) not in points:
        points.add((rdj,height-rdi))
        plt.plot([rdj],[height-rdi],'bo')
plt.show()
'''