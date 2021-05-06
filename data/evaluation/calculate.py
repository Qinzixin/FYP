def cal():
    import os,re
    path = "data/evaluation/GeographySet"
    files= os.listdir(path)
    s = []
    size = 0
    iou = 0
    recall =0
    precision = 0
    f1score = 0
    total = 0

    for file in files: #遍历文件夹
         if not os.path.isdir(file) and "score" in file:
             f = open(path+"/"+file)
             data = f.readlines()
             size += 1
             for row in data:
                indices  =  row.split(' ')
                iou = iou + float(indices[0])
                precision = precision + float(indices[1])
                recall += float(indices[2])
                f1score += float(indices[3])
         if "time" in file:
             f = open(path + "/" + file)
             data = f.readlines()
             for row in data:
                 indices = row.split(' ')
                 time = float(indices[0])
                 total += time

    iou /= size
    precision /= size
    recall /= size
    f1score /= size
    print(iou," ",precision," ",recall," ",f1score," ",total)

    result = str(iou)+" "+str(precision)+" "+str(recall)+" "+str(f1score)+" "+str(total)
    with open('result.txt', 'w') as f:
        f.write(result)  # 文件的写操作
