# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 14:28:08 2018

@author: ivans
"""

import pandas as pd
import numpy as np

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
        sumatoria = H_g['res_sup']*np.exp(mu*DP_res_sup[zona]) + H_g['res_inf']*np.exp(mu*DP_res_inf[zona]) + H_g['com_gra']*np.exp(mu*DP_com_gra[zona]) + H_g['com_peq']*np.exp(mu*DP_com_peq[zona]) + H_g['ind_gra']*np.exp(mu*DP_ind_gra[zona]) + H_g['ind_peq']*np.exp(mu*DP_ind_peq[zona]) + H_g['eriazo']*np.exp(mu*DP_eriazo[zona])
        #RENTA ESPERADA X ZONA SEGUN DP
        R_i[zona] = (1/mu) * np.log (sumatoria) 
        #PROBABILIDAD
        aux['res_sup'] = H_g['res_sup']*np.exp(mu*DP_res_sup[zona]-R_i[zona]) 
        aux['res_inf'] = H_g['res_inf']*np.exp(mu*DP_res_inf[zona]-R_i[zona]) 
        aux['com_gra'] = H_g['com_gra']*np.exp(mu*DP_com_gra[zona]-R_i[zona]) 
        aux['com_peq'] = H_g['com_peq']*np.exp(mu*DP_com_peq[zona]-R_i[zona]) 
        aux['ind_gra'] = H_g['ind_gra']*np.exp(mu*DP_ind_gra[zona]-R_i[zona]) 
        aux['ind_peq'] = H_g['ind_peq']*np.exp(mu*DP_ind_peq[zona]-R_i[zona]) 
        aux['eriazo'] = H_g['eriazo']*np.exp(mu*DP_eriazo[zona]-R_i[zona])
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
#AQUI SE CALCULA LA DISTRIBUCION DE LA OFERTA SEGUN RENTAS (LOGSUMAS)
rentas = open('rentas.txt','r')
rentas = rentas.readlines() #archivo auxiliar, calcule por fuera las logsumas y un logit por zona con ellas

S = 17000 #total de unidades de suelo nuevas en Temuco
s_aux = {} #diccionario que contiene las unidades de suelo por zona (si)
for fila in rentas:
    fila = fila.split() #separa por tabulacion
    pi = float(fila[3]) #probabilidad del logit
    si = S * pi #unidades de suelo en la zona i
    index = int(fila[0])
    s_aux[index]=float(si) #actualizo el diccionario
    


# NUEVA OFERTA (ULTIMOS 5 años)
s={}
for j in df_suelos.index:
    s[j]=s_aux[j]  # ASUMIENDO QUE TODOS LOS SUELOS GENERAN 10000 UNIDADES  
#print(s) 

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

#CALCULO DE H_g
    
H_g={}
for j in usos:
    a=0
    for zona in matriz:
        a += matriz[zona][j]
    H_g[j] = a 


oferta_eq = False
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
            suma += s[zona]*H_g[g]*np.exp(b_hi[zona][g]-R_i[zona])
        b_h[g]= -(1/mu)*np.log((suma / H_g[g]))
        
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
    if it == 1000:     
        break

  
#-----------------------------------RESULTADOS----------------------------------
print("------------------------------Oferta Equilibrada---------------------------------")

#CHECKEO QUE CUMPLA SUMA por fila [H_g por uso]
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
    if check_h[g] < (H_g[g]* 0.99):
        print("diferencia!")
        print(check_h[g],H_g[g])
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
#print(H_g)
#print(check_h)
#print(s)



#tamaño promedio por unidad a m^2
#Un_Com_Of_Adm_Gra	Un_Com_Of_Adm_Peq 	Un_Ind_Bod_Gra	Un_Ind_Bod_peq	Un_Hab_Sup	Un_Hab_Inf	Un_Eriazo_O

#2311,425145	125,2140858	3672,418134	63,69170741	462,6278432	370,1971201	252,242202

#

tamaño_com_gra = 2311,425145
tamaño_com_peq = 125,2140858
tamaño_ind_gra = 3672,418134
tamaño_ind_peq = 63,69170741
tamaño_res_sup = 462,6278432
tamaño_res_inf = 370,1971201
tamaño_eriazo = 252,242202


# PARTICIPACION DE MERCADO (en base a los ultimos 5 años)    

ratio2={'h_alto_joven':0.25,'h_bajo_joven':0.25,'h_alto_viejo':0.25,'h_bajo_viejo':0.25}


choice=[-0.00000315,-0.014,-0.0117,0.919,0.359,-0.218,2.24,0.0000014]
#utilidad = Acc_com_auto Avalúo_sii Avaluo_sii_ingbajoo densidad_hab densidad_hab_viejo ingzonal ingzonal_alto supT_construida



#print(np.random.rand())
print()

matrix={}
def calculo_utilidades():
    for i in df_suelos.index:
        DP_alto_viejo = choice[0]*df_hogares[i][8]+choice[1]*df_hogares[i][3]+(choice[3]+choice[4])*df_hogares[i][6]+(choice[5]+choice[6])*df_hogares[i][4]+choice[7]*df_hogares[i][2]
        DP_alto_joven = choice[0]*df_hogares[i][1]+choice[1]*df_hogares[i][3]+choice[3]*df_hogares[i][6]+(choice[5]+choice[6])*df_hogares[i][4]+choice[7]*df_hogares[i][2]
        DP_bajo_viejo = choice[0]*df_hogares[i][1]+(choice[1]+choice[2])*df_hogares[i][3]+(choice[3]+choice[4])*df_hogares[i][6]+choice[5]*df_hogares[i][4]+choice[7]*df_hogares[i][2]
        DP_bajo_joven = choice[0]*df_hogares[i][1]+(choice[1]+choice[2])*df_hogares[i][3]+choice[3]*df_hogares[i][6]+choice[5]*df_hogares[i][4]+choice[7]*df_hogares[i][2]
        matrix[(i,'sup')]=DP_alto_viejo,DP_alto_joven,DP_bajo_viejo,DP_bajo_joven
    for i in df_suelos.index:
        DP_alto_viejo = choice[0]*df_hogares[i][1]+choice[1]*df_hogares[i][3]+(choice[3]+choice[4])*df_hogares[i][6]+(choice[5]+choice[6])*df_hogares[i][4]+choice[7]*df_hogares[i][2]
        DP_alto_joven = choice[0]*df_hogares[i][1]+choice[1]*df_hogares[i][3]+choice[3]*df_hogares[i][6]+(choice[5]+choice[6])*df_hogares[i][4]+choice[7]*df_hogares[i][2]
        DP_bajo_viejo = choice[0]*df_hogares[i][1]+(choice[1]+choice[2])*df_hogares[i][3]+(choice[3]+choice[4])*df_hogares[i][6]+choice[5]*df_hogares[i][4]+choice[7]*df_hogares[i][2]
        DP_bajo_joven = choice[0]*df_hogares[i][1]+(choice[1]+choice[2])*df_hogares[i][3]+choice[3]*df_hogares[i][6]+choice[5]*df_hogares[i][4]+choice[7]*df_hogares[i][2]
        matrix[(i,'inf')]=DP_alto_viejo,DP_alto_joven,DP_bajo_viejo,DP_bajo_joven

P_h={}
def calculo_prob(): #POR TIPO DE HOGAR PARA TODAS LAS vi
    d1=0
    d2=0
    d3=0
    d4=0
    for i in matrix:
        d1+=np.exp(matrix[i][0])
        d2+=np.exp(matrix[i][1])
        d3+=np.exp(matrix[i][2])
        d4+=np.exp(matrix[i][3])
    #print(d1,d2,d3,d4)
    for i in matrix:
        aux={}
        aux[1]=np.exp(matrix[i][0]) / d1
        aux[2]=np.exp(matrix[i][1]) / d2
        aux[3]=np.exp(matrix[i][2]) / d3
        aux[4]=np.exp(matrix[i][3]) / d4
        #print(aux)
        P_h[i]=aux
        
#calculo_utilidades()
#calculo_prob()  

d1=0
d2=0
d3=0
d4=0
for i in P_h:
   d1+=P_h[i][1]
   d2+=P_h[i][2]
   d3+=P_h[i][3]
   d4+=P_h[i][4]
   
#print(d1,d2,d3,d4)
idx = {}
prob_acum = 0
for hogar in range(1,2):
    aux={}
    prob_acum = 0
    print(hogar)
    for i in P_h:
        #print(P_h[i][hogar],hogar)
        prob_acum += P_h[i][hogar]
        print(P_h[i][hogar])
        aux[i] = prob_acum 
    idx[hogar] = aux
#for i in P_h:
#    prob_acum+=P_h[i][1]
#    idx[i]
#    print(P_h[i][1])
    



#for i in 
#eleccion_h=
   
   
#ACTUALZIACION PARAMETROS
    
#ACTUALIZACION TOTAL EQ OFERTA : usos localizados cambia => acc_com_A
    
#ACTUALIZACION TOTAL EQ DEMANDA : gente localizada cambia => 
        
    