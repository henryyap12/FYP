import csv
import os
import cv2
import numpy as np
import pandas as pd
import glob

i = 0
for file in glob.glob('testing\*.*'):
    #print(file)
    width = 4960
    height = 7016
    #width = 850
    #height = 1050
    img = cv2.imread(file)
    img = cv2.resize(img, (width, height))
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray',imggray)
    imgblur = cv2.GaussianBlur(imggray, (5, 5), 1)
    #cv2.imshow('blur',imgblur)
    kernel = np.ones((5, 8), np.uint8)
    #applying dilate() function on the image to dilate the image and display it as the output on the screen
    imgthres = cv2.threshold(imgblur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    savepath="inverse/omr%i.png" % i
    cv2.imwrite(savepath,imgthres)
    i +=1
