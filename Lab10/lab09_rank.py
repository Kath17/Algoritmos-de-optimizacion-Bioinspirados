import random
import math
import os
import numpy as np
import pandas as pd
import sys
import copy

# ----------- VARIABLES GLOBALES -----------#

# os.remove("Lab09.txt")
# f = open("Lab09.txt", "a")
orig_stdout = sys.stdout
# f = open('Lab09_2.txt', 'w')
f = open('Lab09-2.txt', 'w')
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
# e = 5
# Q = 1
# Feromona Inicial = 10.0
# Cantidad de Hormigas: 3
# Cantidad de Iteraciones: 100

# ---------- Ingresar número de la poblacion y variables ------#
def Entradas():
    # f.write("\n ----------------------- DATOS ------------------ \n\n")

    poblacion= int(input("Ingrese el número de la poblacion: "))
    print(poblacion)

    iteraciones = int(input("Ingrese el numero de iteraciones: "))
    print(iteraciones)

    alpha = float(input("Ingrese parametro alpha: "))
    print(alpha)

    beta = float(input("Ingrese parametro beta: "))
    print(beta)

    Q = int(input("Constante Q: "))
    print(Q)

    return poblacion,iteraciones, alpha, beta,Q

def GenerarPoblacion(poblacion):
    ListaHormigas = []
    for i in range(poblacion):
        ListaHormigas.append([['A'],['B','C','D','E']])
        # ListaHormigas.append([['D'],['A','B','C','E']])
    return ListaHormigas

def GenerarVisibilidad(Matriz):
    return 1/Matriz

#[ [["A"],["B,"C"]], ["C"]["D","E"]]
def CalcularCiudadSiguiente(Feromona,MatrizVisibilidad,ListHormigas,k,alpha,beta):

    Hormiga = ListHormigas[k]
    ult = ListHormigas[k][0][len(ListHormigas[k][0])-1]
    print("\n               ----- Hormiga ",k,"----                " )
    print("Ciudad Inicial: ",ult)

    ListaCiudades =[]
    sumatoria = 0
    for i in range(len(Hormiga[1])):
        t = Feromona[Hormiga[0][len(Hormiga[0])-1]][Hormiga[1][i]]
        n = round(MatrizVisibilidad[Hormiga[0][len(Hormiga[0])-1]][Hormiga[1][i]],6)
        print(ult,"-",Hormiga[1][i],"  ","t = ",t, "  ","n = ",n, "  ","t*n = ",round(t*n,6))
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

def HallarNuevasFeromonas(MatrizFeromona,ListaHormigas,MejorGlobal,Q,C_mejorGlobal,w):
    # print("Matriz de feromonas")
    # MatrizFeromona = MatrizFeromona * (1-evaporacion)
    # MatrizFeromona = MatrizFeromona * (1)
    Ciudades = MatrizFeromona.keys()
    for i in range(len(Ciudades)):
        for j in range(len(Ciudades)):
            acum = 0
            print(" ->",Ciudades[i],Ciudades[j])
            for k in range(len(ListaHormigas)):
                if(i!=j):
                    if(UsoArco(ListaHormigas[k][0],Ciudades[i],Ciudades[j])):
                        print("   Horm",k," ->  +",MatrizFeromona[Ciudades[i]][Ciudades[j]]," + (",w," - ",ListaHormigas[k][3],"): ",(w-ListaHormigas[k][3])," * ",(1/ListaHormigas[k][2]))
                        MatrizFeromona[Ciudades[i]][Ciudades[j]] = MatrizFeromona[Ciudades[i]][Ciudades[j]] + (w-ListaHormigas[k][3])*(1/ListaHormigas[k][2])
            if(UsoArco(MejorGlobal,Ciudades[i],Ciudades[j])):
                print("   Si esta en el mejor camino"," ->  +",MatrizFeromona[Ciudades[i]][Ciudades[j]]," + ",w,"*",(1/C_mejorGlobal),": ",w*(1/C_mejorGlobal))
                MatrizFeromona[Ciudades[i]][Ciudades[j]] = MatrizFeromona[Ciudades[i]][Ciudades[j]] + w*(1/C_mejorGlobal)
    return MatrizFeromona

def Rank_Hormigas(Lista):
    for i in range(len(Lista)):
        Lista.sort(key = lambda x: x[2])
    for i in range(len(Lista)):
        Lista[i].append(i+1)
    print("Con rank: ",Lista)

def Main():
    poblacion,iteraciones, alpha, beta,Q = Entradas()

    Grafo = {'A':{'A':0,'B':22,'C':47, 'D':15,'E':63},
             'B':{'A':22,'B':0,'C':18, 'D':62,'E':41},
             'C':{'A':47, 'B':18,'C':0, 'D':32,'E':57},
             'D':{'A':15,'B':62,'C':32,'D':0,'E':62},
             'E':{'A':63, 'B':41, 'C':57,'D':62,'E':0}}

    Feromona = { 'A':{'A':0,'B':1.0,'C':1.0,'D':1.0,'E':1.0},
                 'B':{'A':1.0,'B':0,'C':1.0,'D':1.0,'E':1.0},
                 'C':{'A':1.0,'B':1.0,'C':0,'D':1.0,'E':1.0},
                 'D':{'A':1.0,'B':1.0,'C':1.0,'D':0,'E':1.0},
                 'E':{'A':1.0,'B':1.0,'C':1.0,'D':1.0,'E':0}}
    w=4

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
                siguiente = CalcularCiudadSiguiente(MatrizFeromona,MatrizVisibilidad,Lista,k,alpha,beta)
                Lista[k][0].append(siguiente)
                Lista[k][1].remove(siguiente)
                print("Ciudad Siguiente: ",siguiente)
                print("Camino: ",Lista[k])
            print_Hormigas(Lista)

        print_Hormigas_C(Lista)
        Rank_Hormigas(Lista)
        pos = HallarMejorCamino(Lista,Grafo);
        print("\nMejor Hormiga Local: ",Lista[pos][0]," con: ",Lista[pos][2])

        #Actualizando mejor hormiga
        if(Lista[pos][2]<C_mejorGlobal):
            MejorHormiga = Lista[pos]
            C_mejorGlobal = Lista[pos][2]

        print("\nMejor Hormiga Global: ",MejorHormiga[0]," con: ",C_mejorGlobal)

        MatrizFeromona = HallarNuevasFeromonas(MatrizFeromona,Lista,MejorHormiga[0],Q,C_mejorGlobal,w)

        print("\n ------------------------MATRIZ FEROMONA------------------------------\n")
        print(MatrizFeromona.to_string())

Main()

sys.stdout = orig_stdout
f.close()
