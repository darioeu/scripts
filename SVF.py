# -*- coding: utf-8 -*-
'''
Created on 29 nov. 2019

@author: Jaime D.
'''
#---PROGRAMA PARA EL CÁLCULO DEL SKY VIEW FACTOR (SVF) A PARTIR DE IMÁGENES---#

#Binarización de la imágen

import cv2
#import numpy
from matplotlib import pyplot as plt
img = cv2.imread('C:/Users/dario/Desktop/1recortadob.png',0)
ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
#ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
#ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
#ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
#ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)
titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = thresh1
#images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
#miArray = np.arange(6)
#for i in miArray:
#plt.subplot(2,3,i+1),
plt.imshow(images,'gray')
#plt.title(titles[i])
plt.xticks([]),plt.yticks([])

#Conteo de píxeles no nulos (blancos) 

count = cv2.countNonZero(images)
print("Píxeles blancos:",count)
#Guardado de imagen binarizada
retval = cv2.imwrite("C:/Users/dario/Desktop/salida-fotocorrea4n.png",images)
plt.show()