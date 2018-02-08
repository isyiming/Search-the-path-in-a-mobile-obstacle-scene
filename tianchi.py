# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 22:12:24 2017

@author: Administrator
"""
'''
天池挑战赛
author：张一铭
something need recode:
x:1-548
y:1-421

days:5
hours:3-21  18hours

0	142	328
1	84	203
2	199	371
3	140	234
4	236	241
5	315	281
6	358	207
7	363	237
8	423	266
9	125	375
10	189	274

'''
# coding: utf-8
import base 
import random
import cv2
import csv
import scipy.io as sio  
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import io

if __name__ == "__main__":
    height=421#y
    width=548#x
    #base.city_location()
    #base.In_situ()
    #base.Forecastdata()
    
    city0=(142,328)
    citys=((84,203),(199,371),(140,234),(236,241),(315,281),(358,207),(363,237),(423,266),(125,375),(189,274))
    
    
    for j in range(1,2):#day
        for i in range(10):#citynum
            informap=cv2.imread("void.png") 
            road=base.A_star_withtime(j,informap,city0,i)
            #base.writeroad2csv(i+1,j,road)
    