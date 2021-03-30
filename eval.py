import numpy as np
points_i = []
polygon_data = open('image/L/L_est.data', 'r')
for line in polygon_data:
    records = line.split()
    x = float(records[0])
    y = float(records[1])
    points_i.append([x, y])
polygon_data.close()

from shapely.geometry import Polygon,Point
vertices_p = points_i
m = Polygon(vertices_p)
print("generated shape area: %f" % m.area)

import matplotlib.pyplot as plt
import numpy as np
import cv2
# read the image
img = cv2.imread("image/L/L.png",0)

# property of img
height = img.shape[0]
width = img.shape[1]

list_x = []
list_y = []
list_x_o = []
list_y_o = []
list_x_f = []
list_y_f = []
intersection_area = 0
false_img_area = 0
true_empty_area = 0

for h in range(height):
    for w in range(width):
        # transformed coordinate
        i = w
        j = height - h
        if  Point(i,j).intersects(m)== True and img[h,w] != 255:
            list_x.append(h)
            list_y.append(w)
            #print("%f %f" % (i,j))
            intersection_area = intersection_area + 1

        # 没预测的
        elif img[h,w] != 255 and Point(i,j).intersects(m)== False:
            false_img_area = false_img_area + 1
            list_x_o.append(h)
            list_y_o.append(w)

        # 多预测的
        elif Point(i,j).intersects(m)== True and img[h,w] == 255 :
            true_empty_area = true_empty_area + 1
            list_x_f.append(h)
            list_y_f.append(w)

xpoints = np.array(list_x)
ypoints = np.array(list_y)
xpoints_t = np.array(list_x_o)
ypoints_t = np.array(list_y_o)
xpoints_f = np.array(list_x_f)
ypoints_f = np.array(list_y_f)

print("intersection_area:%f" % intersection_area)
print("missing area:%f" % false_img_area)
print("false predicted area:%f" % true_empty_area)
accuracy = intersection_area/(intersection_area + false_img_area)
print("Accuracy: %f" % accuracy)
iou = intersection_area / ((m.area) + false_img_area)
print("IOU:%f" % iou)
plt.plot(xpoints, ypoints, 'o',color='#0099CC',markersize=1.0)
plt.plot(xpoints_t, ypoints_t,'o', color='#CCCCCC',alpha=0.2,markersize=1.0)
plt.plot(xpoints_f, ypoints_f,'o',color='#FF6666',markersize=1.0)
plt.show()