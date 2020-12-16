# -*- coding: utf-8 -*-
'''
Created on 31 ene. 2020

@author: Jaime D.
'''
#import numpy as np

#Datos de Entrada
Rad_T=292.21547
Ta=32.64183
HR=35.29016
v=1.59318

#Cálculo de IZA
IZA=-1.3032+0.0647*Ta-0.3673*v+0.0110*HR+0.0000161*Rad_T+0.0005*Ta*HR

print("IZA = ", IZA)