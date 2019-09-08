import random
import math
import os
import numpy as np

# ----------- VARIABLES GLOBALES -----------#

os.remove("Lab08.txt")
f = open("Lab08.txt", "a")

lim_inf = -1
lim_sup = 2
alpha= 2

def print_L(Lista):
    #[(2,3)]
    print(" -------------------------------")
    f.write("\n -------------------------------")
    print("|             LISTA             |")
    f.write("\n|             LISTA             |")
    print(" -------------------------------")
    f.write("\n -------------------------------")
    for i in range(len(Lista)):
        print("|",Lista[i],"|")
        f.write("\n|"+str(Lista[i])+"|")
    print(" ------------------------------")
    f.write("\n ------------------------------")

def print_LF(Lista):
    #[ [(2,3), 5] ]
    print(" ----------------------------------")
    f.write("\n ---------------------------------")
    print("|        LISTA       |   FITNESS   |")
    f.write("\n|       LISTA        |  FITNESS  |")
    print(" ----------------------------------")
    f.write("\n --------------------------------")
    for i in range(len(Lista)):
        print("|",Lista[i][0],"| ",Lista[i][1]," |")
        f.write("\n|"+str(Lista[i][0])+"| "+str(Lista[i][1])+" |")
    print(" ----------------------------------")
    f.write("\n --------------------------------")

## Datos: 10 , iteraciones: 200-250 desv =0.3

# ---------- Ingresar número de la poblacion y variables ------#
def Entradas():
    f.write("\n ----------------------- DATOS ------------------ \n\n")

    poblacion= int(input("Ingrese el número de la poblacion: "))
    f.write("Tamaño de la poblacion: "+str(poblacion)+"\n")

    dimension= int(input("Ingrese el número de dimensiones: "))
    f.write("Numero de dimensiones: "+str(dimension)+"\n")

    F = float(input("Ingrese el peso F: "))
    f.write("Peso F: "+str(F)+"\n")

    CR= float(input("Ingrese la cosntante de cruzamiento: "))
    f.write("Constante de cruzamiento: "+str(CR)+"\n")

    iteraciones = int(input("Ingrese el número de iteraciones: "))
    f.write("Cantidad de iteraciones: "+str(iteraciones)+"\n")

    return poblacion,iteraciones,dimension,F,CR

def Funcion(Par):
    (x1,x2) = Par
    res = x1*math.sin(4*math.pi*x1)-x2*math.sin(4*math.pi*x2+math.pi) + 1
    # return round(res)
    return round(res,5)

def GenerarPoblacion(poblacion):
    Lista = []
    for i in range(poblacion):
        x= round(random.uniform(lim_inf,lim_sup),5)
        y= round(random.uniform(lim_inf,lim_sup),5)
        Lista.append((x,y))   #[ [(2,3),(0.1,0.1)] ]
    return Lista

def Aptitud(Lista):
    ListaAptitud = []
    for i in range(len(Lista)):
        ListaAptitud.append([Lista[i],Funcion(Lista[i])]) #[ [(2,3),5] ]
    return ListaAptitud

def Elegir(Lista,ListaAptitud):

    L=[]
    for i in range(len(Lista)):
        L.append(i)

    sampling = random.sample(L, 3)
    idx1 = sampling[0]
    idx2 = sampling[1]
    idx3 = sampling[2]

    print("  Idx1: ", ListaAptitud[idx1][0], " con: ",ListaAptitud[idx1][1])
    print("  Idx2: ", ListaAptitud[idx2][0], " con: ",ListaAptitud[idx2][1])
    print("  Idx3: ", ListaAptitud[idx3][0], " con: ",ListaAptitud[idx3][1])
    f.write("\n  Idx1: "+str(ListaAptitud[idx1][0])+ " con: "+str(ListaAptitud[idx1][1]))
    f.write("\n  Idx2: "+str(ListaAptitud[idx2][0])+ " con: "+str(ListaAptitud[idx2][1]))
    f.write("\n  Idx3: "+str(ListaAptitud[idx3][0])+ " con: "+str(ListaAptitud[idx3][1]))

    return idx1,idx2,idx3

def Sumar(par,par2):
    (x,y) = par
    (x2,y2) = par2
    return (round(x+x2,5),round(y+y2,5))

def Restar(par,par2):
    (x,y) = par
    (x2,y2) = par2
    return (round(x-x2,5),round(y-y2,5))

def Mult(escalar,par):
    (x,y) = par
    return (round(x*escalar,5), round(y*escalar,5))

# ------------------------Proceso completo -------------------------#
def Main():
    poblacion,iteraciones,dimension,F,CR = Entradas()

    ListaIndividuos = GenerarPoblacion(poblacion)
    f.write("\n ---------------- Generando Población Inicial ------------- \n")
    print_L(ListaIndividuos)

    f.write("\n\n----------------- Lista de Aptitud -------------------\n")
    ListaAptitud = Aptitud(ListaIndividuos)
    print_LF(ListaAptitud)

    for i in range(iteraciones):
        f.write("\n\n  ##################### GENERACION: "+str(i)+" ###################")
        print("\n  #################### GENERACION: "+str(i)+" ###################")

        for j in range(poblacion):
            print("\n      ------------ Seleccionar individuos ------------")
            f.write("\n\n      ------------ Seleccionar individuos ------------\n")

            idx1,idx2,idx3 = Elegir(ListaIndividuos,ListaAptitud)
            vector_mutado = Sumar( ListaIndividuos[idx3], Mult(F, Restar(ListaIndividuos[idx1],ListaIndividuos[idx2])))
            while(vector_mutado[0]<lim_inf or vector_mutado[0]>lim_sup or vector_mutado[1]<lim_inf or vector_mutado[1]>lim_sup ):
                idx1,idx2,idx3 = Elegir(ListaIndividuos,ListaAptitud)
                vector_mutado = Sumar( ListaIndividuos[idx3], Mult(F, Restar(ListaIndividuos[idx1],ListaIndividuos[idx2])))
            print("   Vector mutado: ",vector_mutado)
            f.write("\n     Vector mutado: "+str(vector_mutado))

            print("\n      ------------ Cruzamiento ------------")
            f.write("\n\n      ------------ Cruzamiento ------------\n")
            target = ListaIndividuos[j]
            print("   Target vector:",target)
            f.write("\n   Target vector:"+str(target))

            trial_vector = []
            for k in range(0,dimension):
                nj = random.randint(1,100)
                if(nj < CR):
                    print("   nj: ",nj)
                    f.write("   nj: "+str(nj))
                    n_pop = vector_mutado[k]
                    print("   .. agrega: ",n_pop)
                    f.write("   .. agrega: "+str(n_pop))
                else:
                    print("   nj: ",nj)
                    f.write("   nj: "+str(nj))
                    n_pop = target[k]
                    print("   .. agrega: ",n_pop)
                    f.write("   .. agrega: "+str(n_pop))
                trial_vector.append(n_pop)

            trial_vector = tuple(trial_vector)

            fit_target = Funcion(target)
            fit_trial = Funcion(trial_vector)
            print("   Trial vector: ",trial_vector," con:",fit_trial)
            print("   Target vector: ",target," con:",fit_target)
            f.write("\n   Trial vector: "+str(trial_vector)+" con:"+str(fit_trial))
            f.write("\n   Target vector: "+str(target)+" con:"+str(fit_target))

            if(fit_trial > fit_target):
                ListaIndividuos[j]=trial_vector
            else:
                ListaIndividuos[j]=target

            print("\n      ------------ Individuos ------------\n")
            f.write("\n\n      ------------ Individuos ------------\n")
            ListaAptitud = Aptitud(ListaIndividuos)
            print_LF(ListaAptitud)

Main()
