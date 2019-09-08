import random
import math
import os
import numpy as np
import pandas as pd
import sys
import copy

# ----------- VARIABLES GLOBALES -----------#

orig_stdout = sys.stdout
f = open('Lab10.txt', 'w')
sys.stdout = f

def print_Hormigas(Lista):
    #[ (['A'],['B','C']),(['A','B'],['C','D'])]
    print("\n -----------------------------------------------------------------------")
    print("|   HORMIGA   |             Memoria  -  Vecindario alcanzable           |")
    print(" -----------------------------------------------------------------------")
    for i in range(len(Lista)):
        print("| Hormiga ",i," | ",Lista[i][0],",",Lista[i][1]," |")
    print(" -----------------------------------------------------------------------")

def print_Hormigas_C(Lista):
    #[ (['A'],['B','C']),(['A','B'],['C','D'])]
    print("\n ---------------------------------------------------------------------------------")
    print("|   HORMIGA   |             Memoria  -  Vecindario alcanzable           | Distancia |")
    print(" ---------------------------------------------------------------------------------")
    for i in range(len(Lista)):
        print("| Hormiga ",i," | ",Lista[i][0],",",Lista[i][1]," | ",Lista[i][2]," |")
    print(" --------------------------------------------------------------------------------")

# ρ = 0.99
# α = 1
# β = 1
# Q = 1
# q_0 = 0.7
# φ = 0.05
# Feromona Inicial = 0.1
# Cantidad de Hormigas: 3
# Cantidad de Iteraciones: 100

# ---------- Ingresar número de la poblacion y variables ------#
def Entradas():
    # f.write("\n ----------------------- DATOS ------------------ \n\n")

    poblacion= int(input("Ingrese el número de la poblacion: "))
    print(poblacion)

    iteraciones = int(input("Ingrese el numero de iteraciones: "))
    print(iteraciones)

    evaporacion = float(input("Ingrese la tasa de evaporacion: "))
    print(evaporacion)

    alpha = float(input("Ingrese parametro alpha: "))
    print(alpha)

    beta = float(input("Ingrese parametro beta: "))
    print(beta)

    Q = int(input("Constante Q: "))
    print(Q)

    q_0 = float(input("Ingresar parametro q_0: "))
    print(q_0)

    phi = float(input("Ingresar constante phi"))

    return poblacion,iteraciones,evaporacion, alpha, beta,Q, q_0, phi

def GenerarPoblacion(poblacion):
    ListaHormigas = []
    for i in range(poblacion):
        ListaHormigas.append([['A'],['B','C','D','E','F','G','H','I','J']])
        # ListaHormigas.append([['D'],['A','B','C','E']])
    return ListaHormigas

def GenerarVisibilidad(Matriz):
    return 1/Matriz

#[ [["A"],["B,"C"]], ["C"]["D","E"]]
def CalcularCiudadSiguienteQ_0Menor(Feromona,MatrizVisibilidad,ListHormigas,k,alpha,beta):

    print("\n -----------------   Recorrido por diversificacion -------------------")
    Hormiga = ListHormigas[k]
    ult = ListHormigas[k][0][len(ListHormigas[k][0])-1]
    print("\n               ----- Hormiga ",k,"----                " )
    print("Ciudad Inicial: ",ult)

    ListaCiudades =[]
    sumatoria = 0
    for i in range(len(Hormiga[1])):
        t = Feromona[Hormiga[0][len(Hormiga[0])-1]][Hormiga[1][i]]
        n = round(MatrizVisibilidad[Hormiga[0][len(Hormiga[0])-1]][Hormiga[1][i]],6)
        print(ult,"-",Hormiga[1][i],"  ","t = ",t, "  ","n = ",n, "  ","t*n = ",round(pow(t,alpha)*pow(n,beta),6))
        # ---- SUMATORIA DE PROB
        sumatoria = sumatoria + pow(t,alpha)*pow(n,beta)
        ListaCiudades.append((Hormiga[1][i],pow(t,alpha)*pow(n,beta)))

    ran = random.uniform(0,1)
    acumulado= 0
    siguiente = ListaCiudades[len(ListaCiudades)-1][0]

    print("\nSuma: ", sumatoria)
    idx = 0
    for i in range(len(ListaCiudades)):
        idx = idx + 1
        prob = ListaCiudades[i][1]/sumatoria
        print(ult,"-",ListaCiudades[i][0],": prob = ",round(prob,6))
        acumulado= acumulado+ prob
        if(ran < acumulado):
            siguiente = ListaCiudades[i][0]
            break;

    for i in range(idx,len(ListaCiudades)):
        prob = ListaCiudades[i][1]/sumatoria
        print(ult,"-",ListaCiudades[i][0],": prob = ",round(prob,6))
        acumulado= acumulado+ prob

    print("\nNumero aleatorio: ",ran)
    return siguiente

def CalcularCiudadSiguienteQMenor(Feromona,MatrizVisibilidad,ListHormigas,k,alpha,beta):

    print("\n  -----------   Recorrido por intensificación ----------------------")
    Hormiga = ListHormigas[k]
    ult = ListHormigas[k][0][len(ListHormigas[k][0])-1]
    print("\n               ----- Hormiga ",k,"----                " )
    print("Ciudad Inicial: ",ult)

    ListaCiudades =[]
    mayor = -1
    indx = -1
    siguiente =""
    for i in range(len(Hormiga[1])):
        t = Feromona[Hormiga[0][len(Hormiga[0])-1]][Hormiga[1][i]]
        n = round(MatrizVisibilidad[Hormiga[0][len(Hormiga[0])-1]][Hormiga[1][i]],6)
        print(ult,"-",Hormiga[1][i],"  ","t = ",t, "  ","n = ",n, "  ","t*n = ",round(t*pow(n,beta),6))
        ListaCiudades.append((Hormiga[1][i],t*pow(n,beta)))
        if(t*pow(n,beta)>mayor):
            mayor = t*pow(n,beta)
            indx = i

    siguiente = ListaCiudades[indx][0]

    print("Ciudad con mayor valor es: ",siguiente)
    return siguiente

def Distancia(List,Grafo):
    sum = 0
    primerNodo = List[0]
    segundoNodo = ""
    for i in range(1,len(List)):
        segundoNodo = List[i]
        sum = sum + Grafo[primerNodo][segundoNodo]
        primerNodo  = segundoNodo
    return sum

def HallarMejorCamino(Lista,Grafo):
    mejor = 0
    mejor_dist = 9999
    for i in range(len(Lista)):
        dist = Distancia(Lista[i][0],Grafo)
        Lista[i].append(dist)
        if (dist < mejor_dist):
            mejor_dist = dist
            mejor = i
    return mejor

def UsoArco(ListaCamino,Ciudad1,Ciudad2):
    for i in range(0,len(ListaCamino)-1):
        if((ListaCamino[i]==Ciudad1 or ListaCamino[i]==Ciudad2) and (ListaCamino[i+1]==Ciudad1 or ListaCamino[i+1]==Ciudad2)):
            return True
    return False

def HallarNuevasFeromonas(MatrizFeromona,ListaHormigas,MejorGlobal,evaporacion,Q,C_mejorGlobal):
    # print("Matriz de feromonas")
    # MatrizFeromona = MatrizFeromona * (evaporacion)
    Ciudades = MatrizFeromona.keys()
    for i in range(len(Ciudades)):
        for j in range(len(Ciudades)):
            # print(" ->",Ciudades[i],Ciudades[j])
            if(UsoArco(MejorGlobal,Ciudades[i],Ciudades[j])):
                # print("   Si esta en el mejor camino"," ->  +",MatrizFeromona[Ciudades[i]][Ciudades[j]]," + ",(1-evaporacion)*(1/C_mejorGlobal))
                MatrizFeromona[Ciudades[i]][Ciudades[j]] = MatrizFeromona[Ciudades[i]][Ciudades[j]] + (1-evaporacion)*(1/C_mejorGlobal)
                # MatrizFeromona[Ciudades[i]][Ciudades[j]] = MatrizFeromona[Ciudades[i]][Ciudades[j]] + (1/C_mejorGlobal)
    return MatrizFeromona

def actualizarArco(Feromonas,Ciudad1,Ciudad2,phi,t_0):
    a = (1-phi)* Feromonas[Ciudad1][Ciudad2] + phi*t_0
    Feromonas[Ciudad1][Ciudad2] = a
    Feromonas[Ciudad2][Ciudad1] = a
    return a

def Main():

    poblacion,iteraciones,evaporacion, alpha, beta,Q, q_0, phi = Entradas()

    Grafo = {'A':{'A':0,'B':12,'C':3, 'D':23,'E':1, 'F':5, 'G':23,'H':56,'I':12,'J':11},
             'B':{'A':12,'B':0,'C':9, 'D':18,'E':3, 'F':41,'G':45,'H':5, 'I':41,'J':27},
             'C':{'A':3, 'B':9,'C':0, 'D':89,'E':56,'F':21,'G':12,'H':48,'I':14,'J':29},
             'D':{'A':23,'B':18,'C':89,'D':0,'E':87,'F':46,'G':75,'H':17,'I':50,'J':42},
             'E':{'A':1, 'B':3, 'C':56,'D':87,'E':0,'F':55,'G':22,'H':86,'I':14,'J':33},
             'F':{'A':5 ,'B':41,'C':21,'D':46,'E':55,'F':0,'G':21,'H':76,'I':54,'J':81},
             'G':{'A':23,'B':45,'C':12,'D':75,'E':22,'F':21,'G':0,'H':11,'I':57 ,'J':48},
             'H':{'A':56,'B':5, 'C':48,'D':17,'E':86,'F':76,'G':11,'H':0,'I':63,'J':24},
             'I':{'A':12,'B':41,'C':14,'D':50,'E':14,'F':54,'G':57,'H':63,'I':0,'J':9 },
             'J':{'A':11,'B':27,'C':29,'D':42,'E':33,'F':81,'G':48,'H':24,'I':9,'J':0 }}

    Feromona = { 'A':{'A':0,'B':0.1,'C':0.1,'D':0.1,'E':0.1,'F':0.1,'G':0.1,'H':0.1,'I':0.1,'J':0.1},
                 'B':{'A':0.1,'B':0,'C':0.1,'D':0.1,'E':0.1,'F':0.1,'G':0.1,'H':0.1,'I':0.1,'J':0.1},
                 'C':{'A':0.1,'B':0.1,'C':0,'D':0.1,'E':0.1,'F':0.1,'G':0.1,'H':0.1,'I':0.1,'J':0.1},
                 'D':{'A':0.1,'B':0.1,'C':0.1,'D':0,'E':0.1,'F':0.1,'G':0.1,'H':0.1,'I':0.1,'J':0.1},
                 'E':{'A':0.1,'B':0.1,'C':0.1,'D':0.1,'E':0,'F':0.1,'G':0.1,'H':0.1,'I':0.1,'J':0.1},
                 'F':{'A':0.1,'B':0.1,'C':0.1,'D':0.1,'E':0.1,'F':0,'G':0.1,'H':0.1,'I':0.1,'J':0.1},
                 'G':{'A':0.1,'B':0.1,'C':0.1,'D':0.1,'E':0.1,'F':0.1,'G':0,'H':0.1,'I':0.1,'J':0.1},
                 'H':{'A':0.1,'B':0.1,'C':0.1,'D':0.1,'E':0.1,'F':0.1,'G':0.1,'H':0,'I':0.1,'J':0.1},
                 'I':{'A':0.1,'B':0.1,'C':0.1,'D':0.1,'E':0.1,'F':0.1,'G':0.1,'H':0.1,'I':0,'J':0.1},
                 'J':{'A':0.1,'B':0.1,'C':0.1,'D':0.1,'E':0.1,'F':0.1,'G':0.1,'H':0.1,'I':0.1,'J':0}}

    # Feromona = { 'A':{'A':0,'B':0.01,'C':0.01,'D':0.01,'E':0.01,'F':0.01,'G':0.01,'H':0.01,'I':0.01,'J':0.01},
    #              'B':{'A':0.01,'B':0,'C':0.01,'D':0.01,'E':0.01,'F':0.01,'G':0.01,'H':0.01,'I':0.01,'J':0.01},
    #              'C':{'A':0.01,'B':0.01,'C':0,'D':0.01,'E':0.01,'F':0.01,'G':0.01,'H':0.01,'I':0.01,'J':0.01},
    #              'D':{'A':0.01,'B':0.01,'C':0.01,'D':0,'E':0.01,'F':0.01,'G':0.01,'H':0.01,'I':0.01,'J':0.01},
    #              'E':{'A':0.01,'B':0.01,'C':0.01,'D':0.01,'E':0,'F':0.01,'G':0.01,'H':0.01,'I':0.01,'J':0.01},
    #              'F':{'A':0.01,'B':0.01,'C':0.01,'D':0.01,'E':0.01,'F':0,'G':0.01,'H':0.01,'I':0.01,'J':0.01},
    #              'G':{'A':0.01,'B':0.01,'C':0.01,'D':0.01,'E':0.01,'F':0.01,'G':0,'H':0.01,'I':0.01,'J':0.01},
    #              'H':{'A':0.01,'B':0.01,'C':0.01,'D':0.01,'E':0.01,'F':0.01,'G':0.01,'H':0,'I':0.01,'J':0.01},
    #              'I':{'A':0.01,'B':0.01,'C':0.01,'D':0.01,'E':0.01,'F':0.01,'G':0.01,'H':0.01,'I':0,'J':0.01},
    #              'J':{'A':0.01,'B':0.01,'C':0.01,'D':0.01,'E':0.01,'F':0.01,'G':0.01,'H':0.01,'I':0.01,'J':0}}

    t_0 = 0.1
    print("\n ------------------------ MATRIZ DISTANCIAS --------------------\n")

    Matriz = pd.DataFrame(Grafo)
    print(Matriz)

    print("\n -------------------------POBLACION INICIAL------------------------------")
    ListaHormigas = GenerarPoblacion(poblacion)
    print_Hormigas(ListaHormigas)

    print("\n ------------------------MATRIZ VISIBILIDAD------------------------------\n")
    MatrizVisibilidad = GenerarVisibilidad(Matriz)
    print(MatrizVisibilidad.to_string())

    print("\n ------------------------MATRIZ FEROMONA------------------------------\n")
    MatrizFeromona = pd.DataFrame(Feromona)
    print(MatrizFeromona)

    MejorHormiga = []
    C_mejorGlobal = 9999
    siguiente = ""

    for i in range(iteraciones):
        Lista = copy.deepcopy(ListaHormigas)
        print("\n-------------------------------------------------------------------------")
        print("\n-------------------------------- ITERACION "+str(i)+"----------------------------  ")
        print("\n-------------------------------------------------------------------------")
        print_Hormigas(Lista)

        for k in range(poblacion):
            print("\n------------------- HORMIGA "+str(k)+"----------------------")
            while(len(Lista[k][1])>0): #Mientras hayan ciudades por recorrer
                q = random.uniform(0,1)
                print("q: ",q)
                if(q<=q_0):
                    siguiente = CalcularCiudadSiguienteQMenor(MatrizFeromona,MatrizVisibilidad,Lista,k,alpha,beta)
                else:
                    siguiente = CalcularCiudadSiguienteQ_0Menor(MatrizFeromona,MatrizVisibilidad,Lista,k,alpha,beta)

                print("Ciudad Siguiente: ",siguiente)
                Lista[k][0].append(siguiente)
                Lista[k][1].remove(siguiente)
                print("Actualizar: ",Lista[k][0][-2]," con ",siguiente," y phi: ",phi)
                res = actualizarArco(MatrizFeromona,Lista[k][0][-2],siguiente,phi,t_0)
                print("Camino: ",Lista[k])

            print_Hormigas(Lista)

        pos = HallarMejorCamino(Lista,Grafo);
        print_Hormigas_C(Lista)
        print("\nMejor Hormiga Local: ",Lista[pos][0]," con: ",Lista[pos][2])
        #Actualizando mejor hormiga
        if(Lista[pos][2]<C_mejorGlobal):
            MejorHormiga = Lista[pos]
            C_mejorGlobal = Lista[pos][2]

        print("\nMejor Hormiga Global: ",MejorHormiga[0]," con: ",C_mejorGlobal)

        MatrizFeromona = HallarNuevasFeromonas(MatrizFeromona,Lista,MejorHormiga[0],evaporacion,Q,C_mejorGlobal)

        print("\n ------------------------MATRIZ FEROMONA------------------------------\n")
        print(MatrizFeromona.to_string())

Main()

sys.stdout = orig_stdout
f.close()
