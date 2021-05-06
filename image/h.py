import cv2
import numpy as np
import os

file_path = "C:/Users/Zixin QIN/PycharmProjects/pythonProject5/image/ShapeSet"

for filename in os.listdir(file_path):
    s = file_path+'/'+filename
    print(s)
    img1 = cv2.imread(s)
    print(img1)
    filename = filename.replace('png','')

    img1 = cv2.resize(img1, (256,256))

    # I want to put logo on top-left corner, So I create a ROI
    # 首先获取原始图像roi
    rows, cols, channels = img1.shape
    roi = img1[0:rows, 0:cols]

    # 原始图像转化为灰度值
    # Now create a mask of logo and create its inverse mask also
    img2gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    cv2.imshow('img2gray', img2gray)
    cv2.waitKey(0)
    '''
    将一个灰色的图片，变成要么是白色要么就是黑色。（大于规定thresh值就是设置的最大值（常为255，也就是白色））
    '''
    # 将灰度值二值化，得到ROI区域掩模
    ret, mask = cv2.threshold(img2gray, 254, 255, cv2.THRESH_BINARY)

    cv2.imshow('mask', mask)
    cv2.waitKey(0) 
    cv2.imwrite("C:/Users/Zixin QIN/PycharmProjects/pythonProject5/image/ShapeSet2/"+ filename +'.png',mask)

 