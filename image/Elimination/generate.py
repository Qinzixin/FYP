import os
os.system("ffmpeg -f image2 -r 5/1 -i %d.png -vcodec mpeg4 -y geometry.mp4")