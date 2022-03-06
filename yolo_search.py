# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 16:56:38 2022

@author: sayori
"""

import cv2
import numpy as np
import copy

def yolo_search(pathIn,db,
                label_path='yolo/coco.names',
                config_path='yolo/yolov4.cfg',
                weights_path='yolo/yolov4.weights',
                confidence_thre=0.5,
                nms_thre=0.3,
                jpg_quality=100):

    '''
    confidence_thre：0-1，置信度（概率/打分）阈值，即保留概率大于这个值的边界框，默认为0.5
    nms_thre：非极大值抑制的阈值，默认为0.3
    '''

    LABELS = open(label_path).read().strip().split("\n")
    nclass = len(LABELS)

    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(nclass, 3), dtype='uint8')

    img = cv2.imread(pathIn)
    ori_img=copy.deepcopy(img)
    (H, W) = img.shape[:2]

    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > confidence_thre:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_thre, nms_thre)
    matched_data=[]

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            '''
            if w<40 or y<40:
                continue
            '''
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            text = '{}: {:.3f}'.format(LABELS[classIDs[i]], confidences[i])
            
            if LABELS[classIDs[i]]=='person':
                print('oooo')
                matched_data.append(match_face(ori_img[y:y+w,x:x+w],db))
            
            (text_w, text_h), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(img, (x, y-text_h-baseline), (x + text_w, y), color, -1)
            cv2.putText(img, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    return img,matched_data

def match_face(img,db):
    ret=None
    max_match=0
    bf=cv2.BFMatcher(crossCheck=True)
    img=cv2.resize(img,(178,218))
    mat1=sift(img)
    for i in db:
        img2=i['图片']
        img2=cv2.cvtColor(np.asarray(img2),cv2.COLOR_RGB2BGR)
        mat2=sift(img2)
        if len(bf.match(mat1, mat2))>max_match:
            max_match=len(bf.match(mat1, mat2))
            ret=i
    return ret
        
        
    
def sift(img):
    shift=cv2.SIFT_create()
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp=shift.detect(gray,None)
    kp,des=shift.compute(gray,kp)
    return des
    
        
