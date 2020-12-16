# -*- coding: utf-8 -*-
'''
Created on 4 dic. 2019

@author: Jaime D.
'''



import numpy as np
#-------CÁLCULO DE COMFA-------
#Balance energetico:
#S=M+Rabs-Conv-E-L

#Datos de entrada:

Ma=88.05            #Tasa metabólica (W/m**2) 1 met = 58 W/m**2 (Valor extraido de BioMet, el mismo que se uso para el cálculo de PMV)
r_c_dato=112.2       #Resistencia del arropamiento(s/m) - 1clo = 187 s/m, se toma el valor 0.6clo = 112.2 s/m
#P=150               #Permeabilidad de la ropa - Valor tomado de la Tabla 2, fila 2 de Brown & Gillespie 1986
P=220               #Permeabilidad de la ropa (Valor para una remera o T shirt - An Introduction to Enviromental Biophysics, table 8.2)

Ta=30.3401          #Temperatura ambiente
HR=42.90059         #Humedad relativa
SVF=0.49            #Sky View Factor (Factor de vista del cielo)
kb=0       #Radiación directa             
kd_diff=90.00237    #Radiación difusa del cielo    
kd_ref=159.10088    #Radiación difusa reflejada
V=0.99468           #Velocidad del aire en flujo libre (velocidad del viento m/s)
Pa=87.225           #Presión atmosférica (kPa) - Valor estándar a la elevación de 1246 msnm extraído del TMY 2003-2017 para Salta-de.Guemes.Intl

ws=60               #Ángulo horario (de 0 a 90. Positivo a la tarde, negativo a la mañana. 15° por cada hora) - 16hs = 60
phi=-24.788         #Latitud
dian=315            #Día juliano

#------Calculo de M
es=0.61094*np.exp((17.625*Ta)/(Ta+243.04))       #presion de vapor de saturación a Ta
e=HR*es                                         #relación de humedad relativa y presiones de vapor
f=0.150-(0.0137*e)-(0.0014*Ta)                   #f:factor de correción de la pérdida de calor por respiración
M=(1-f)*Ma                                      #M:Energía metabólica producida por el organismo
#print("es: ",es)

#-------Calculo de Rabs

#Constantes
rho_h=0.37          #Albedo promedio del humano (0.37 por recomendación de Brown & Gillespie)
#r_cyl=0.0005         #Radio del cilindro (m)                                    |
#h_cyl=0.1          #Altura del cilindo (m)                                      |
#delta_h=0.95        #Emisividad del humano - Kenny et. al 2008 Estimating....   |       
r_cyl=0.117         #Radio del cilindro (m)
h_cyl=1.65          #Altura del cilindo (m)
delta_h=0.95        #Emisividad del humano
A_eff=0.78          #Área efectiva de la persina (para tomar en cuenta irregularidades del cuerpo y el intercambio inter-radiativo entre partes del cuerpo
#Comienzo del calculo
sigma=23.45*np.sin((360*(284+dian)/365)*np.pi/180)      #Declinación
thetaz=np.arccos(np.cos(phi*np.pi/180)*np.cos(sigma*np.pi/180)*np.cos(ws*np.pi/180)+np.sin(phi*np.pi/180)*np.sin(sigma*np.pi/180))  #Ángulo de incidencia para plano horizontal
kp=kb/np.cos(thetaz)
#Acs_cyl=np.pi*r_cyl**2                                  #Área transversal del cilindro (corte seccional)                             
Acs_cyl=2*r_cyl*h_cyl                                   #Área transversal del cilindro (corte longitudinal)
A_cyl=2*np.pi*r_cyl*h_cyl+2*np.pi*r_cyl**2       #Área superficial del cilindro
kb_abs=(1-rho_h)*kp*np.sin(thetaz)*Acs_cyl              #Radiación directa absorbida por el cilindro
kd=kd_diff+kd_ref
kd_abs=0.5*(1-rho_h)*kd*A_cyl                           #Radiación difusa absorbida por el cilindro

La=213+5.5*Ta                                           #Radiación de onda larga emitida desde el cielo
Lg=320+5.2*Ta                                           #Radiación de onda corta emitida desde el suelo
La_abs=0.5*delta_h*La*A_cyl*SVF                         #Radiación de onda larga emitida desde el cielo que fue absorbida
Lg_abs=0.5*delta_h*Lg*A_cyl                             #Radiación de onda larga emitida desde el suelo que fue absorbida

Rabs=A_eff*(kb_abs+kd_abs+La_abs+Lg_abs)/A_cyl          #Radiación absorbida total por el humano
#print("thetaz:",A_cyl)
#print("thetaz:",Acs_cyl2)

#-------Cálculo de Conv

if V>0.7:
    r_c=r_c_dato*(1-0.05*np.power(0.196*P,0.4)*np.power(V,0.5))
else:
    r_c=r_c_dato
#Constantes
v_c=1.5E-5          #viscosidad cinemática del aire
k=22E-6             #difusividad térmica del aire
Pr=0.71             #Número de Prandtl
rhocp_ai=1212
#Comienzo del cálculo
Tc=36.5+0.0043*M                #Temperatura del núcleo del cuerpo (Core Temperature)
r_t=-0.1*Ma+65                  #Resistencia al flujo de calor debido al tejido corporal
Tsk=Tc-((M*r_t)/(rhocp_ai))     #Temperatura superficial de la piel
Re=0.17*V/v_c                   #Número de Reynolds

if Re>40000:
    A=0.0266
    n=0.805
elif 4000<Re<=40000:
    A=0.193
    n=0.618
else:
    A=0.683
    n=0.466   
  
r_a=0.17/(A*np.power(Re,n)*np.power(Pr,0.33)*k)     #Resistencia al flujo de calor debido a la capa de aire entre la piel y el arropamiento (s/m)
Conv=rhocp_ai*((Tsk-Ta)/(r_c+r_a))


#-------Cálculo de E

#Constantes
rho_ai=1.16         #Densidad del aire (kg/m**3)
L_v=2442            #Calor latente de vaporización (2424J/g a 20°C)
r_tv=7.7E3
#Comienzo del Cálculo
E_s=0.42*(M-58)
es_Tsk=0.61094*np.exp((17.625*Tsk)/(Tsk+243.04))
e_Tsk=HR*es_Tsk
q_s=0.622*(e_Tsk/(Pa-e_Tsk))
q_a=0.622*(e/(Pa-e))
r_cv=r_c
r_av=0.92*r_a
E_i=rho_ai*L_v*((q_s-q_a)/(r_cv+r_av+r_tv))
E=E_s+E_i
E_m=rho_ai*L_v*((q_s-q_a)/(r_cv+r_av))
#print("E_m=",e_Tsk)
#print("E=",E)

#-------Cálculo de L

#Constantes
e_h=0.95            #Emisividad de la piel humana+arropamiento
eb=5.67E-8          #Constante de Stefan-Boltzmann (Wm^-2K^-4)
#Comienzo del cálculo
T_sf=((Tsk-Ta)/(r_c+r_a))*r_a+Ta
L=A_eff*e_h*eb*np.power(T_sf+273.15,4)

#Cálculo de COMFA
S=M+Rabs-Conv-E-L

print("S =",S)
if S<-201:
    print("Interpretación subjetiva: Frío")
elif -200<=S<-121:
    print("Interpretación subjetiva: Fresco")
elif -120<=S<-51:
    print("Interpretación subjetiva: Ligeramente Fresco")
elif -50<=S<50:
    print("Interpretación subjetiva: Neutro. Confort!")
elif 51<=S<120:
    print("Interpretación subjetiva: Ligeramente Cálido")
elif 121<=S<200:
    print("Interpretación subjetiva: Cálido")
else:
    print("Caluroso")