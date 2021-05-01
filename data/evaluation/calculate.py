import os,re
path = "ShapeSet"
files= os.listdir(path)
s = []
size = 0
accuracy =0
iou = 0
total = 0
for file in files: #遍历文件夹
     if not os.path.isdir(file) and "score" in file:
         f = open(path+"/"+file)
         data = f.readlines()
         for row in data:
             indices  =  row.split(' ')
             accuracy = accuracy + float(indices[0])
             iou = iou + float(indices[1])
         size += 1

     elif "time" in file:
         f = open(path + "/" + file)
         data = f.readlines()
         for row in data:
             indices = row.split('s')
             time = float(indices[0])
             total += time

print(accuracy/size)
print(iou/size)
print(total)

