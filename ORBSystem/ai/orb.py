# coding=utf-8
import os

import cv2
import numpy as np
import pickle


# from matplotlib import pyplot as plt


def compute_orb(img):
    d_img = cv2.imread(os.path.join("./static/uploads", img))
    orb = cv2.ORB_create(1000)
    kp, des = orb.detectAndCompute(d_img, None)
    c_img = cv2.drawKeypoints(d_img, kp, None, (255, 0, 0), flags=0)
    cv2.imwrite(os.path.join("./static/uploads", img + ".jpg"), c_img)
    # cv2.imwrite(os.path.join("./static/uploads", img), c_img)
    return des


def compute_orb_percent(image1_des, image2_des):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(image1_des, image2_des, k=2)
    hits = 0.0
    for (m, n) in matches:
        if m.distance < 0.75 * n.distance:
            hits += 1
    hits_per = hits / np.minimum(len(image1_des), len(image2_des)) * 1000

    if hits_per > 100:
        return 100
    else:
        return hits_per

