import cv2
import numpy as np
import os

backSub = cv2.createBackgroundSubtractorMOG2()
src = './cars'
dst = './cars_dst'
for filename in os.listdir(dst):
    os.remove(os.path.join(dst, filename))
for filename in os.listdir(src):
    path = os.path.join(src, filename)
    img = cv2.imread(path)
    fgMask = backSub.apply(img)
    #gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #_, thresh = cv2.threshold(gray_img,64,255,cv2.THRESH_BINARY)

    #img_contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]

    #img_contours = sorted(img_contours, key=cv2.contourArea)

    #for k,i in enumerate(img_contours):

    #   if cv2.contourArea(i) > 100:
    #        break
    #    mask = np.zeros(img.shape[:2], np.uint8)
    #    cv2.drawContours(mask, [i],-1, 255, -1)
    #new_img = cv2.bitwise_and(img, img, mask=fgMask)
    cv2.imwrite(os.path.join(dst,filename),fgMask)