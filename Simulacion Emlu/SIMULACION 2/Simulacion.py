# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 14:28:08 2018

@author: ivans
"""

## COMENTARIOS

#ZONA 3 TIENE MUCHA DISPOSICON AL PAGO (TIENE ALTA DENSIDAD DE APRADEROS)
#ESO DA UNA LOGSUMAGIGANTE

#con la EOD 
#alto viejo 5%
#alto joven 17%
#bajo_viejo 21%
#bajo_joven 57%



import pandas as pd
import numpy as np

df_hogares = pd.read_csv("montecarloint5.csv")
df_hogares = df_hogares.set_index('Zona') 
df_suelos = pd.read_csv("Sueloint5.csv")
df_suelos = df_suelos.set_index('ZONA')
df_suelos[df_suelos<0] = 0


#AVALUO=26.0423
#INGRESO=0,6369
#EDAD=39

usos =  ['res_sup','res_inf','com_gra','com_peq','ind_gra','ind_peq','eriazo']
#PARAMETRO DE ESCALA (MU)
mu=1


#----------OFERTA (segun bid)----------------
bid={}
#NO MODIFICADOS
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
rentas = open('Logsuma.txt','r')
rentas = rentas.readlines() #archivo auxiliar, calcule por fuera las logsumas y un logit por zona con ellas
# PARTICIPACION DE MERCADO (en base a los ultimos 5 años)
S = 25000 #total de unidades de suelo nuevas en Temuco
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





#original   
#ratio={'res_sup':0.225,'res_inf':0.658,'com_gra':0.0168,
#       'com_peq':0.0375,'ind_gra':0.00497,'ind_peq':0.034,'eriazo':0.0235}

ratio={'res_sup':0.22,'res_inf':0.58,'com_gra':0.017,
       'com_peq':0.0963,'ind_gra':0.0092,'ind_peq':0.054,'eriazo':0.0235}

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
            suma += s[zona]*H_g[g]*np.exp(b_hi[zona][g]-R_i[zona])
        b_h[g]= -(1/mu)*np.log((suma / H_g[g]))
        
    #actualizar la matriz #anterior
    for i in df_suelos.index:
        for j in usos:
            matriz[i][j] = matriz_aux[i][j]
    #parar segun criterio
    print(R_i)
    if criterio < 0.05:
        print("------------------------------Oferta Equilibrada---------------------------------")
        break   
    #print('iteracion {},'.format(it))
    #print(b_h)
    #print(criterio)
    #sino converge al 5% en 1000, para igual
    if it == 1000:     
        break

  
#-----------------------------------RESULTADOS----------------------------------
#print("------------------------------Oferta Equilibrada---------------------------------")

#CHECKEO QUE CUMPLA SUMA por fila [H_g por uso]
def check():
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
    print(check_v)
    print(H_g)
    print(check_h)
    print(s)

archivo= pd.DataFrame.from_dict(matriz, orient='index')
archivo.to_csv('salidas/output1.csv',sep=';',decimal=',')
#print(check_v)
#print(H_g)
#print(check_h)
#print(s)


#-------------------------------PASO INTERMEDIO CONVERSION DE UNIDADES DE SUELO A UNIDADES EN M2 y UNIDADES HAB

#tamaño promedio por unidad a m^2

#Un_Com_Of_Adm_Gra	Un_Com_Of_Adm_Peq 	Un_Ind_Bod_Gra	Un_Ind_Bod_peq	Un_Hab_Sup	Un_Hab_Inf	Un_Eriazo_O

#2311,425145	125,2140858	3672,418134	63,69170741	462,6278432	370,1971201	252,242202

#

tamaño_com_gra = 2311.425145
tamaño_com_peq = 125.2140858
tamaño_ind_gra = 3672.418134
tamaño_ind_peq = 63.69170741
tamaño_res_sup = 462.6278432
tamaño_res_inf = 370.1971201
tamaño_eriazo = 252.242202


a,b,c,d,e,f,g = ratio['res_sup']*25000*tamaño_res_sup, ratio['res_inf']*25000*tamaño_res_inf, ratio['com_gra']*25000*tamaño_com_gra, ratio['com_peq']*25000*tamaño_com_peq,ratio['ind_gra']*25000*tamaño_ind_gra,ratio['ind_peq']*25000*tamaño_ind_peq,ratio['eriazo']*25000
#print(a+b+c+d+e+f+g)


#m2_prom = {'res_sup':462.6278432,'res_inf':370.1971201,'com_gra':2311.425145,'com_peq':125.2140858,'ind_gra':3672.418134,'ind_peq':63.69170741, 'eriazo':252.24220}

#un_G_M2 = pd.DataFrame()
#CONVIERTO UND DE PREDIO A M2
#for uso in usos:
#    asd=archivo[uso]*m2_prom[uso]

#    un_G_M2 = pd.concat([un_G_M2,asd], axis=1)    



#PASO de M2 de hab a VIVIENDAS:
#ASUMO 200 m2 de vivienda sup y 100 m2 de vivienda inf
oferta_casas=pd.DataFrame()
factor = 1 # 1 predio genera 1 vivenda
for uso in ['res_sup','res_inf']:
    asd=archivo[uso]*factor
    oferta_casas = pd.concat([oferta_casas,asd], axis=1)
    
#print(oferta_casas['res_sup'][1])
#asumir 1 a 1.
#TOTAL casas de res sup    
#print(S_h['res_sup'].sum())
#TOTAL casas res inf
#print(S_h['res_inf'].sum())
 
 
#und_res_sup=un_G_M2['res_sup']/200
#und_res_inf=un_G_M2['res_inf']/100



###-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



hogares=['alto_viejo','alto_joven','bajo_viejo','bajo_joven']

#15000

 




# PARTICIPACION DE MERCADO (en base a los ultimos 5 años) 
# del total de res_sup+res_inf = 0,8
#20000 del total de res segun 25000*0,8
#alto viejo 5%
#alto joven 17%
#bajo_viejo 21%
#bajo_joven 57%   
H_h = {'alto_viejo':1000,'alto_joven':3400,'bajo_viejo':4200,'bajo_joven':11400}


choice=[-0.00000315,-0.014,-0.0117,0.919,0.359,-0.218,2.24,0.0000014]
#utilidad = 

#0 Acc_com_auto 
#1 Avalúo_sii 
#2 Avaluo_sii_ingbajoo 
#3 densidad_hab 
#4 densidad_hab_viejo 
#5 ingzonal 
#6 ingzonal_alto 
#7 supT_construida


#DFRAME
#0 Acc_com_A
#1 T_sup_const
#2 P_avaluo_Sii
#3 P_ing_zonal
#4 P_edad_zona
#5 Densidad_hab
#6 Densidad_par


### INICIALIZACION UTILIDADES;PROBABILIDADES
matrix={}
def calculo_utilidades(): ## calcula las utilidades para cada tipo de hogar{bajo_jovenes,bajo_viejos,alto_jovenes,alto_viejos}, según 180 opc (90zonasX2tiposdehogar)
    for i in df_suelos.index:
        DP_alto_viejo = choice[0]*df_hogares.loc[i][0]+choice[1]*df_hogares.loc[i][2]+(choice[3]+choice[4])*df_hogares.loc[i][5]+(choice[5]+choice[6])*df_hogares.loc[i][3]+choice[7]*df_hogares.loc[i][1]
        DP_alto_joven = choice[0]*df_hogares.loc[i][0]+choice[1]*df_hogares.loc[i][2]+choice[3]*df_hogares.loc[i][5]+(choice[5]+choice[6])*df_hogares.loc[i][3]+choice[7]*df_hogares.loc[i][1]
        DP_bajo_viejo = choice[0]*df_hogares.loc[i][0]+(choice[1]+choice[2])*df_hogares.loc[i][2]+(choice[3]+choice[4])*df_hogares.loc[i][5]+choice[5]*df_hogares.loc[i][3]+choice[7]*df_hogares.loc[i][1]
        DP_bajo_joven = choice[0]*df_hogares.loc[i][0]+(choice[1]+choice[2])*df_hogares.loc[i][2]+choice[3]*df_hogares.loc[i][5]+choice[5]*df_hogares.loc[i][3]+choice[7]*df_hogares.loc[i][1]
        matrix[(i,'sup')]=DP_alto_viejo,DP_alto_joven,DP_bajo_viejo,DP_bajo_joven
    for i in df_suelos.index:
        DP_alto_viejo = choice[0]*df_hogares.loc[i][0]+choice[1]*df_hogares.loc[i][2]+(choice[3]+choice[4])*df_hogares.loc[i][5]+(choice[5]+choice[6])*df_hogares.loc[i][3]+choice[7]*df_hogares.loc[i][1]
        DP_alto_joven = choice[0]*df_hogares.loc[i][0]+choice[1]*df_hogares.loc[i][2]+choice[3]*df_hogares.loc[i][5]+(choice[5]+choice[6])*df_hogares.loc[i][3]+choice[7]*df_hogares.loc[i][1]
        DP_bajo_viejo = choice[0]*df_hogares.loc[i][0]+(choice[1]+choice[2])*df_hogares.loc[i][2]+(choice[3]+choice[4])*df_hogares.loc[i][5]+choice[5]*df_hogares.loc[i][3]+choice[7]*df_hogares.loc[i][1]
        DP_bajo_joven = choice[0]*df_hogares.loc[i][0]+(choice[1]+choice[2])*df_hogares.loc[i][2]+choice[3]*df_hogares.loc[i][5]+choice[5]*df_hogares.loc[i][3]+choice[7]*df_hogares.loc[i][1]
        matrix[(i,'inf')]=DP_alto_viejo,DP_alto_joven,DP_bajo_viejo,DP_bajo_joven


def calculo_prob(): #POR TIPO DE HOGAR PARA TODAS LAS vi
    P_h={}
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
        aux['alto_viejo']=np.exp(matrix[i][0]) / d1
        aux['alto_joven']=np.exp(matrix[i][1]) / d2
        aux['bajo_viejo']=np.exp(matrix[i][2]) / d3
        aux['bajo_joven']=np.exp(matrix[i][3]) / d4
        #print(aux)
        P_h[i]=aux
    return P_h
        
 

   
#MONTECARLO 
###INICIALIZACION MONTECARLO
#CONSTRUYO LAS PROBABILIDADES ACUMULADAS
df_prob = pd.DataFrame()
def probabilidades_acum():  
    prob_acum=0
    df_prob = pd.DataFrame()
    for hogar in ['alto_viejo','alto_joven','bajo_viejo','bajo_joven']:
        aux={} # DICC GUARDA LAS PROB ACUMULADAS SEGUN ALTERNATIVA AUX[alternativa]=PROBACUMULADA.
        prob_acum=0
        for i in P_h:
            #print(P_h[i][hogar])
            prob_acum += P_h[i][hogar]
            #print(prob_acum)
            aux[i]=prob_acum
        probabilidad = pd.DataFrame.from_dict(aux, orient='index',columns=[hogar])
        df_prob = pd.concat([df_prob, probabilidad], axis=1)
    return df_prob




# REALIZO ITERACION HASTA EQ:
calculo_utilidades()
P_h = calculo_prob()
df_probA = probabilidades_acum()

demanda_eq = False
matriz_loc_vi={}
matriz_loc_h={}
dic2={}
#inicializo la matriz de localizacion en 0 
for j in P_h:
    matriz_loc_vi[j]=0
for zona in df_suelos.index:
    matriz_loc_h[zona]={'alto_viejo':0,'alto_joven':0,'bajo_viejo':0,'bajo_joven':0}

it=0
while demanda_eq:
    it+=1
    #selecciona 1 hogar al azar
    eleccion = np.random.choice(hogares, p=[0.25, 0.25, 0.25, 0.25]) # escoje un hogar
    #si de ese hogar hay cantidad entonces procede a simular montecarlo.
    if H_h[eleccion] > 0:
        montecarlo=np.random.rand()
        serie = df_probA[eleccion][df_probA[eleccion] > montecarlo]  # escojo todas las filas que sean del hogar elegido y superiores a la probabilidad "montecarlo"
        zona = serie.index[0]
        print(montecarlo,'la zona elegida:{}, residencia de calidad: {}'.format(zona[0],zona[1]))
        if zona[1]== 'inf':
            a='res_inf'
        elif zona[1]=='sup':
            a='res_sup'
        
        if oferta_casas[a][zona[0]] >= 0:
            #localiza
            matriz_loc_h[zona[0]][eleccion]+=1
            matriz_loc_vi[zona]+=1 # como se localizan las viviendas 
            #le resto al total de hogares de ese tipo
            H_h[eleccion]-=1
            #le resto la casa a la oferta
            oferta_casas[a][zona[0]]-=1
        else:
            #nolocaliza y saca de la probabilidad y acumulada
            matrix.pop((zona[0], zona[1]),None)
            P_h = calculo_prob()
            df_probA = probabilidades_acum()

        
    if H_h['alto_viejo'] == 0 and H_h['alto_joven'] == 0 and H_h['bajo_viejo'] == 0 and H_h['bajo_joven'] == 0:  #SI YA NO HAY MAS VIVIENDAS
        print("------------------------------Demanda Equilibrada---------------------------------")
        #genera output
        for i in df_hogares.index:
            aux={}
            aux['res_sup'] = matriz_loc_vi[(i,'sup')]
            aux['res_inf'] = matriz_loc_vi[(i,'inf')]
            dic2[i]=aux
            #print(i[0])
        
        break
    #print(it)
    if it>100000000:
        print("ALCANZO IT MAX")
        break
    

        

#print(dic2['res_sup']).sum()
#print(dic2['res_inf']).sum()

archivo2= pd.DataFrame.from_dict(dic2, orient='index')
archivo3= pd.DataFrame.from_dict(matriz_loc_h, orient='index')
print(archivo2['res_sup'].sum())
print(archivo2['res_inf'].sum())
print(archivo3['alto_viejo'].sum())
print(archivo3['alto_joven'].sum())
print(archivo3['bajo_viejo'].sum())
print(archivo3['bajo_joven'].sum())
archivo2.to_csv('salidas/output2.csv',sep=';',decimal=',')
archivo3.to_csv('salidas/output3.csv',sep=';',decimal=',')
   
#ACTUALZIACION PARAMETROS

df_atributos = pd.read_csv("ATRIBUTOS_AUX.csv")


#print(archivo)
#print(archivo2)   
 
#segun las caracteristicas del uso de suelo: (equivalencia en m^2) y equivalencia en unidades de res_sup


#ACTUALIZACION TOTAL EQ OFERTA : usos localizados cambia => acc_com_A
    
#ACTUALIZACION TOTAL EQ DEMANDA : gente localizada cambia => 
        
    