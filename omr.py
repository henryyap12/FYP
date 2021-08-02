import csv
import os
import cv2
import numpy as np
import pandas as pd
from detect import detect


def omrmarking(path, csvpath, mark, choice):
    reader = csv.reader(open(csvpath))
    ANSWER_KEY = {}
    next(reader, None)
    for row in reader:
        key = int(row[0]) - 1
        ANSWER_KEY[key] = row[1]
        if row[1] == 'A' or row[1] == 'a':
            ANSWER_KEY[key] = 0
        elif row[1] == 'B' or row[1] == 'b':
            ANSWER_KEY[key] = 1
        elif row[1] == 'C' or row[1] == 'c':
            ANSWER_KEY[key] = 2
        elif row[1] == 'D' or row[1] == 'd':
            ANSWER_KEY[key] = 3
        elif row[1] == 'E' or row[1] == 'e':
            ANSWER_KEY[key] = 4
        elif row[1] is None or row[1] == '':
            ANSWER_KEY[key] = -1
    question = {key:val for key, val in ANSWER_KEY.items() if val != -1}
    width = 1240
    height = 1748
    img = cv2.imread(path)
    img = cv2.resize(img, (width, height))
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgthres = cv2.threshold(imggray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    savepath = 'C:/Users/Asus/PycharmProjects/PSM/thrs/1.png'
    cv2.imwrite(savepath,imgthres)

    cmd='python detect.py --source C:/Users/Asus/PycharmProjects/PSM/thrs/1.png --weights runs/train/yolov5s_results/weights/best.pt --conf 0.4'
    os.system(cmd)
    data = pd.read_csv("GFG.csv")
    arr = data.to_numpy()
    j = arr.tolist()
    x=0
    res = []
    if len(j)<2:
        for x in list(j)[0][1:5]:
            res.append(x)
    elif len(j)>=2:
        for x in list(j):
            for y in list(x)[1:5]:
                res.append(y)
    #print(res)
    b = int(len(res) / 4)
    i = 0
    for i in range(b):
        n = int(i * 4 + 1)
        croped_img = imgthres[int(res[int(n)]):int(res[int(n + 2)]), int(res[int(n - 1)]):int(res[int(n + 1)])]
        #croped_img = cv2.cvtColor(croped_img, cv2.COLOR_BGR2GRAY)

        if i == 0:
            shape = croped_img.shape
            print(shape)
            pppp = np.zeros((shape[0] * b, shape[1])).astype('uint8')
            pppp[shape[0] * (i):shape[0] * (i + 1), :] = croped_img
        else:
            croped_img = cv2.resize(croped_img, (shape[1], shape[0]))
            #cv2.imshow('bine',croped_img)
            pppp[shape[0] * (i):shape[0] * (i + 1), :] = croped_img
    
    aaa = pppp
    question_num = len(ANSWER_KEY)
    h, w = aaa.shape
    c_h = int(h / question_num)
    c_w = int(w / float(choice))
    

    ans_lists = []

    for row in range(question_num):
        y1 = int(c_h * row)
        y2 = y1 + c_h
        x1 = 0
        option_list = []
        for column in range(int(choice)):
            x1 = int(c_w * column)
            x2 = x1 + c_w
            x = np.sum(aaa[y1:y2, x1:x2])
            option_list.append(x/1000)
        ans_lists.append(option_list)
    #print(ans_lists)

    ans = []
    for ans_list in ans_lists:
        m = np.max(ans_list)
        #print(m)
        max_accept = int(m * 1.5)
        min_accept = int(m * 0.95)
        sum_of_white = np.sum(ans_lists)
        v = 1 + (1/float(choice))
        filter = (question_num/v) * float(choice)
        filter = sum_of_white/filter
        print(filter)
        if question_num>40:
            filter = filter*0.95
        else:
            filter = filter*0.75
        detected_ans_num = 0
        for i in ans_list:
            if i in range(min_accept, max_accept):
                    detected_ans_num += 1
        if detected_ans_num > 1:
            ans.append(999)
        else:
            if m > filter:
                ans.append(ans_list.index(m))
            else:
                ans.append(999)
    print(ans)

    row = 1
    for a in ans:
        print('question : ', row, 'ans : ', a)
        row += 1

    correct = 0
    for y in range(len(question)):
        if ans[y] == question[y]:
            correct += 1
       
    print(correct)
    score = (correct / len(question)) * int(mark)

    return score