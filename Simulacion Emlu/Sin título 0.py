# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 14:28:08 2018

@author: ivans
"""

import pandas as pd
import numpy as np
import random as rnd

df_hogares = pd.read_csv("hogares.csv") 
df_suelos = pd.read_csv("Suelo.csv")
df_suelos = df_suelos.set_index('ZONA')
df_suelos[df_suelos<0] = 0

usos =  ['res_sup','res_inf','com_gra','com_peq','ind_gra','ind_peq','eriazo']
#PARAMETRO DE ESCALA (MU)
mu=1


#----------OFERTA (segun bid)----------------
bid={}
bid[usos[0]]=[-3.85,0.714,8.04,1.2]
bid[usos[1]]=[-3.14,0.454,9.54,2.95]
bid[usos[2]]=[-1.89,0.333,1.08]
bid[usos[3]]=[-3.78,2.56,2.62,2.64]
bid[usos[4]]=[2.04,-0.0261,2.12]
bid[usos[5]]=[3.85,-0.0365,1.63]
#Calculo de cada utilidad
DP_res_sup={} #DP_res_sup  	utilidad	ingzonal	acc_com	den_par
DP_res_inf={} #DP_res_inf	utilidad 	ingzonal	acc_com	den_par	
DP_com_gra={} #DP_com_gra	utilidad	den_hab	den_par	
DP_com_peq={} #DP_com_peq	utilidad	ingzonal	den_hab	den_par
DP_ind_gra={} #DP_ing_gra	utilidad	edad	den_hab	
DP_ind_peq={} #DP_ind_peq	utilidad	edad	den_hab
DP_eriazo={} #DP_ERIAZO=0

P_g={}
R_i={} 

#inicializacion b_h=0; calculo de prob ; calculo de E[P]=renta log suma ; 
b_h={}
b_hi={}
for suelo in usos:
    b_h[suelo]= 0 

def actualizacion_DP(): # Bh+Bhgi
    for i in df_suelos.index:
        aux={}
        aux['res_sup'] = (bid[usos[0]][0] + bid[usos[0]][1] * df_suelos.loc[i][3] + bid[usos[0]][2] * df_suelos.loc[i][0] + bid[usos[0]][3] * df_suelos.loc[i][6])
        aux['res_inf'] = (bid[usos[1]][0] + bid[usos[1]][1] * df_suelos.loc[i][3] + bid[usos[1]][2] * df_suelos.loc[i][0] + bid[usos[1]][3] * df_suelos.loc[i][6])
        aux['com_gra'] = (bid[usos[2]][0] + bid[usos[2]][1] * df_suelos.loc[i][5] + bid[usos[2]][2] * df_suelos.loc[i][6])
        aux['com_peq'] = (bid[usos[3]][0] + bid[usos[3]][1] * df_suelos.loc[i][3] + bid[usos[3]][2] * df_suelos.loc[i][5] + bid[usos[3]][3] * df_suelos.loc[i][6])
        aux['ind_gra'] = (bid[usos[4]][0] + bid[usos[4]][1] * df_suelos.loc[i][4] + bid[usos[4]][2] * df_suelos.loc[i][5])
        aux['ind_peq'] = (bid[usos[5]][0] + bid[usos[5]][1] * df_suelos.loc[i][4] + bid[usos[5]][2] * df_suelos.loc[i][5])
        aux['eriazo'] = 0
        b_hi[i] = aux
        DP_res_sup[i] =  b_hi[i]['res_sup'] + b_h['res_sup']  
        DP_res_inf[i] =  b_hi[i]['res_inf'] + b_h['res_inf']
        DP_com_gra[i] =  b_hi[i]['com_gra'] + b_h['com_gra']
        DP_com_peq[i] =  b_hi[i]['com_peq'] + b_h['com_peq']
        DP_ind_gra[i] =  b_hi[i]['ind_gra'] + b_h['ind_gra'] 
        DP_ind_peq[i] =  b_hi[i]['ind_peq'] +  b_h['ind_peq']
        DP_eriazo[i] = b_hi[i]['eriazo'] + b_h['eriazo']


def iterar():  # realiza calculo de probabilidad, logsuma(renta) y reparticion de suel
    for zona in df_suelos.index:
        aux={}
        sumatoria = H_h['res_sup']*np.exp(mu*DP_res_sup[zona]) + H_h['res_inf']*np.exp(mu*DP_res_inf[zona]) + H_h['com_gra']*np.exp(mu*DP_com_gra[zona]) + H_h['com_peq']*np.exp(mu*DP_com_peq[zona]) + H_h['ind_gra']*np.exp(mu*DP_ind_gra[zona]) + H_h['ind_peq']*np.exp(mu*DP_ind_peq[zona]) + H_h['eriazo']*np.exp(mu*DP_eriazo[zona])
        #RENTA ESPERADA X ZONA SEGUN DP
        R_i[zona] = (1/mu) * np.log (sumatoria) 
        #PROBABILIDAD
        aux['res_sup'] = H_h['res_sup']*np.exp(mu*DP_res_sup[zona]-R_i[zona]) 
        aux['res_inf'] = H_h['res_inf']*np.exp(mu*DP_res_inf[zona]-R_i[zona]) 
        aux['com_gra'] = H_h['com_gra']*np.exp(mu*DP_com_gra[zona]-R_i[zona]) 
        aux['com_peq'] = H_h['com_peq']*np.exp(mu*DP_com_peq[zona]-R_i[zona]) 
        aux['ind_gra'] = H_h['ind_gra']*np.exp(mu*DP_ind_gra[zona]-R_i[zona]) 
        aux['ind_peq'] = H_h['ind_peq']*np.exp(mu*DP_ind_peq[zona]-R_i[zona]) 
        aux['eriazo'] = H_h['eriazo']*np.exp(mu*DP_eriazo[zona]-R_i[zona])
        P_g[zona] = aux
        
        
    #REPARTICION SUELO
      
    for zona in df_suelos.index:
        aux={}
        aux['res_sup'] = P_g[zona]['res_sup']*s[zona]
        aux['res_inf'] = P_g[zona]['res_inf']*s[zona] 
        aux['com_gra'] = P_g[zona]['com_gra']*s[zona] 
        aux['com_peq'] = P_g[zona]['com_peq']*s[zona] 
        aux['ind_gra'] = P_g[zona]['ind_gra']*s[zona]     
        aux['ind_peq'] = P_g[zona]['ind_peq']*s[zona]
        aux['eriazo'] = P_g[zona]['eriazo']*s[zona] 
        matriz_aux[zona] = aux
        



#------------------------------------------------------------------SIMULACION--------------------------------------------------

    
# NUEVA OFERTA (ULTIMOS 5 años)
s={}
for j in df_suelos.index:
    s[j]=1000  # ASUMIENDO QUE TODOS LOS SUELOS GENERAN 10000 UNIDADES  
    
# PARTICIPACION DE MERCADO (en base a los ultimos 5 años)    
ratio={'res_sup':0.225,'res_inf':0.658,'com_gra':0.0168,
       'com_peq':0.0375,'ind_gra':0.00497,'ind_peq':0.034,'eriazo':0.0235}
matriz={}
matriz_aux={}


#CALCULO MATRIZ INICIAL (Loc_0)
for j in s:
    dic={}
    for suelo in ratio:
        dic[suelo]=ratio[suelo]*s[j]    
    matriz[j]=dic



#CALCULO DE "H_h"
    
H_h={}
for j in usos:
    a=0
    for zona in matriz:
        a += matriz[zona][j]
    H_h[j] = a


oferta_eq = True
it=0
while oferta_eq:
    it+=1
    criterio=0
    actualizacion_DP()
    iterar()
    # para construir dif_total
    Dj_aux=[]
    Oi_aux=[]
    Dj=[]
    Oi=[]
    for uso in usos:
        d=0
        d_aux=0
        for zona in df_suelos.index:
            d+=matriz[zona][uso]
            d_aux+=matriz_aux[zona][uso]
        Dj.append(d)
        Dj_aux.append(d_aux)
    
    for zona in df_suelos.index:
        o=0
        o_aux=0
        for uso in usos:
            o+=matriz[zona][suelo]
            o_aux+=matriz_aux[zona][suelo]
        Oi.append(o)
        Oi_aux.append(o_aux)
    #armar criterio
    for k in range(len(usos)): # comparo las matrices
        criterio+=np.abs(Dj[k]-Dj_aux[k])
    for j in range(len(df_suelos.index)):
        criterio+=np.abs(Oi[j]-Oi_aux[j])
    
    #actualizar los bh
    for g in usos:
        suma=0
        for zona in df_suelos.index:
            suma += s[zona]*H_h[g]*np.exp(b_hi[zona][g]-R_i[zona])
        b_h[g]= -(1/mu)*np.log((suma / H_h[g]))
        
    #actualizar la matriz #anterior
    for i in df_suelos.index:
        for j in usos:
            matriz[i][j] = matriz_aux[i][j]
    #parar segun criterio
    if criterio < 0.05:
        break   
    print('iteracion {},'.format(it))
    #print(b_h)
    print(criterio)
    #sino converge al 5% en 1000, para igual
    if it == 100:     
        break
    print("------------------------------Oferta Equilibrada---------------------------------")
  
#-----------------------------------RESULTADOS----------------------------------


#CHECKEO QUE CUMPLA SUMA por fila [H_h por uso]
check_h={}
check_v={}
for g in usos:
    suma_h=0
    for vi in df_suelos.index:
        suma_h+=matriz[vi][g]
    check_h[g]=suma_h
#CHEKCEO QUE CUMPLA SUMA por columna (S[i] por zona)
for vi in df_suelos.index:
    suma_v=0
    for g in usos:
        suma_v+=matriz[vi][g]
    check_v[vi]=suma_v
    
for g in usos:
    if check_h[g] < (H_h[g]* 0.99):
        print("diferencia!")
        print(check_h[g],H_h[g])
    else:
        #print("todo correcto")
        pass
        
for vi in df_suelos.index:
    if check_v[vi] < (s[vi]* 0.99):
        print("diferencia!")
        print(check_v[vi]-s[vi])
    else:
       #print("todo correcto")
       pass

archivo= pd.DataFrame.from_dict(matriz, orient='index')
archivo.to_csv('output.csv',sep='\t',decimal=',')
#print(check_v)
#print(H_h)
#print(check_h)
#print(s)
#-----------------------------REGRESION ri y avaluo_prom
R_i_0={}
for i in df_suelos.index:
    aux={}
    aux['res_sup'] = (bid[usos[0]][0] + bid[usos[0]][1] * df_suelos.loc[i][3] + bid[usos[0]][2] * df_suelos.loc[i][0] + bid[usos[0]][3] * df_suelos.loc[i][6])
    aux['res_inf'] = (bid[usos[1]][0] + bid[usos[1]][1] * df_suelos.loc[i][3] + bid[usos[1]][2] * df_suelos.loc[i][0] + bid[usos[1]][3] * df_suelos.loc[i][6])
    aux['com_gra'] = (bid[usos[2]][0] + bid[usos[2]][1] * df_suelos.loc[i][5] + bid[usos[2]][2] * df_suelos.loc[i][6])
    aux['com_peq'] = (bid[usos[3]][0] + bid[usos[3]][1] * df_suelos.loc[i][3] + bid[usos[3]][2] * df_suelos.loc[i][5] + bid[usos[3]][3] * df_suelos.loc[i][6])
    aux['ind_gra'] = (bid[usos[4]][0] + bid[usos[4]][1] * df_suelos.loc[i][4] + bid[usos[4]][2] * df_suelos.loc[i][5])
    aux['ind_peq'] = (bid[usos[5]][0] + bid[usos[5]][1] * df_suelos.loc[i][4] + bid[usos[5]][2] * df_suelos.loc[i][5])
    aux['eriazo'] = 0
    b_hi[i] = aux
    DP_res_sup[i] =  b_hi[i]['res_sup']   
    DP_res_inf[i] =  b_hi[i]['res_inf'] 
    DP_com_gra[i] =  b_hi[i]['com_gra'] 
    DP_com_peq[i] =  b_hi[i]['com_peq'] 
    DP_ind_gra[i] =  b_hi[i]['ind_gra']  
    DP_ind_peq[i] =  b_hi[i]['ind_peq'] 
    DP_eriazo[i] = b_hi[i]['eriazo'] 
        
for zona in df_suelos.index:
    aux={}
    sumatoria = H_h['res_sup']*np.exp(mu*DP_res_sup[zona]) + H_h['res_inf']*np.exp(mu*DP_res_inf[zona]) + H_h['com_gra']*np.exp(mu*DP_com_gra[zona]) + H_h['com_peq']*np.exp(mu*DP_com_peq[zona]) + H_h['ind_gra']*np.exp(mu*DP_ind_gra[zona]) + H_h['ind_peq']*np.exp(mu*DP_ind_peq[zona]) + H_h['eriazo']*np.exp(mu*DP_eriazo[zona])
    #RENTA ESPERADA X ZONA SEGUN DP
    R_i_0[zona] = (1/mu) * np.log (sumatoria)


rentas= pd.DataFrame.from_dict(R_i_0, orient='index')
rentas.to_csv('output2.csv',sep='\t',decimal=',')

### parametro Alpha_ri = 2,098

#-------------------------------------------------ingreso de cambios de atributos---------------------------
#tamaño promedio por unidad a m^2
#2311,425145	125,2140858	3672,418134	63,69170741	462,6278432	370,1971201	252,242202

tamaño_res_sup = 2311,425145
tamaño_res_inf = 125,2140858
tamaño_com_gra = 3672,418134
tamaño_com_peq = 63,69170741
tamaño_ind_gra = 462,6278432
tamaño_ind_peq = 370,1971201
tamaño_eriazo = 252,242202


#-------------------------------------------------ITERACION DEMANDA-------------------------------------------------
#PROPORCION DE hogares segun ING y 

#a=rnd.ranint(2)


