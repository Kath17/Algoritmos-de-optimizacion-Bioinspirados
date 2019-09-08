import random
import math
import os
import numpy as np

# ----------- VARIABLES GLOBALES -----------#

os.remove("Lab07.txt")
f = open("Lab07.txt", "a")

lim_inf = -10
lim_sup = 10
alpha= 2

def print_L(Lista):
    #[ [(2,3),(0.1,0.1)] ]
    print(" -------------------------------")
    f.write("\n -------------------------------")
    print("|             LISTA             |")
    f.write("\n|             LISTA             |")
    print(" -------------------------------")
    f.write("\n -------------------------------")
    for i in range(len(Lista)):
        print("|",Lista[i][0],",",Lista[i][1],"|")
        f.write("\n|"+str(Lista[i][0])+","+str(Lista[i][1])+"|")
    print(" ------------------------------")
    f.write("\n ------------------------------")

def print_LF(Lista):
    #[ ( [(2,3),(0.1,0.1)] , 5) ]
    print(" --------------------------------------------------------")
    f.write("\n -------------------------------------------------")
    print("|                   LISTA                  |   FITNESS   |")
    f.write("\n|                LISTA                |  FITNESS  |")
    print(" --------------------------------------------------------")
    f.write("\n -------------------------------------------------")
    for i in range(len(Lista)):
        print("|",Lista[i][0][0],",",Lista[i][0][1],"| ",Lista[i][1]," |")
        f.write("\n|"+str(Lista[i][0][0])+","+str(Lista[i][0][1])+"| "+str(Lista[i][1])+" |")
    print(" --------------------------------------------------------")
    f.write("\n -------------------------------------------------")

## Datos: 10 , iteraciones: 200-250 desv =0.3

# ---------- Ingresar número de la poblacion y variables ------#
def Entradas():
    f.write("\n ----------------------- DATOS ------------------ \n\n")

    poblacion= int(input("Ingrese el número de la poblacion: "))
    f.write("Tamaño de la poblacion: "+str(poblacion)+"\n")

    iteraciones = int(input("Ingrese el número de iteraciones: "))
    f.write("Cantidad de iteraciones: "+str(iteraciones)+"\n")

    desviacion = float(input("Ingrese valor para desviacion: "))
    f.write("Valor para desviacion: "+str(desviacion)+"\n")

    return poblacion,iteraciones,desviacion

def F(Par):
    (x1,x2) = Par
    res = -math.cos(x1)*math.cos(x2)*math.exp(-pow((x1-math.pi),2)-pow((x2-math.pi),2))
    # return round(res)
    return round(res,5)


def GenerarPoblacion(desviacion,poblacion):
    Lista = []
    for i in range(poblacion):
        x= round(random.uniform(lim_inf,lim_sup),5)
        y= round(random.uniform(lim_inf,lim_sup),5)
        # x= round(random.randint(lim_inf,lim_sup),5)
        # y= round(random.randint(lim_inf,lim_sup),5)
        Lista.append([(x,y),(desviacion,desviacion)])   #[ [(2,3),(0.1,0.1)] ]
    return Lista

def Aptitud(Lista):
    ListaAptitud = []
    for i in range(len(Lista)):
        ListaAptitud.append([Lista[i],F(Lista[i][0])]) #[ ([(2,3),(0.1,0.1)],5) ]
    return ListaAptitud

def Torneo(ListaAptitud):
    ran = random.randint(0,len(ListaAptitud)-1)
    ran2 = random.randint(0,len(ListaAptitud)-1)

    while(ran==ran2):
        ran2 = random.randint(0,len(ListaAptitud)-1)

    print("  PP1: ", ListaAptitud[ran][0]," con: ",ListaAptitud[ran][1])
    print("  PP2: ", ListaAptitud[ran2][0]," con: ",ListaAptitud[ran2][1])
    f.write("\n  PP1: "+str(ListaAptitud[ran][0])+" con: "+str(ListaAptitud[ran][1]))
    f.write("\n  PP2: "+str(ListaAptitud[ran2][0])+" con: "+str(ListaAptitud[ran2][1]))

    if(ListaAptitud[ran][1] < ListaAptitud[ran2][1]):
        return ran
    else:
        return ran2

def Procreate(ListaAptitud):
    print("\n                 --- TORNEO ---         \n")
    f.write("\n                 --- TORNEO ---       \n")

    print("  Posibles Padres:")
    f.write("  Posibles Padres:")
    P1 = Torneo(ListaAptitud)
    P2 = Torneo(ListaAptitud)

    padre1 = ListaAptitud[P1][0]   #[(-1,2),(0.1,0.1)]
    padre2 = ListaAptitud[P2][0]   #[(-2,1),(0.1,0.1)]

    hijo1 = []
    d1_medio = (padre1[1][0])*(1+alpha*np.random.normal(0,1))
    d2_medio = (padre1[1][1])*(1+alpha*np.random.normal(0,1))

    x1_medio = (padre1[0][0] + d1_medio* np.random.normal(0,1))
    x2_medio = (padre1[0][1] + d2_medio* np.random.normal(0,1))

    while(x1_medio<lim_inf or x1_medio>lim_sup or x2_medio<lim_inf or x2_medio>lim_sup):
        d1_medio = (padre1[1][0])*(1+alpha*np.random.normal(0,1))
        d2_medio = (padre1[1][1])*(1+alpha*np.random.normal(0,1))

        x1_medio = (padre1[0][0] + d1_medio* np.random.normal(0,1))
        x2_medio = (padre1[0][1] + d2_medio* np.random.normal(0,1))

    hijo1= [(round(x1_medio,5),round(x2_medio,5)),(round(d1_medio,5),round(d2_medio,5))]

    print("    Padres:")
    print("    P1: ", padre1)
    print("    P2: ",padre2)
    f.write("\n    Padres:")
    f.write("\n    P1: "+str(padre1))
    f.write("\n    P2: "+str(padre2))

    return hijo1   #[ (-4,2.7),(0.4,0.4) ]

def Seleccion(ListaAptitud,ListaHijos):
    Lista = sorted(ListaAptitud,key=lambda x:x[1])
    ListaH = sorted(ListaHijos,key=lambda x:x[1],reverse=True)
    # ListaNueva = ListaNueva[:(len(ListaAptitud)-A)]
    num = int(len(Lista)/2)

    ListaNueva = Lista[:num]+ListaH[num:]
    return ListaNueva

# ------------------------Proceso completo -------------------------#
def Main():
    poblacion,iteraciones,desviacion = Entradas()

    ListaIndividuos = GenerarPoblacion(desviacion,poblacion)
    f.write("\n ---------------- Generando Población Inicial ------------- \n")
    print_L(ListaIndividuos)

    f.write("\n\n----------------- Lista de Aptitud -------------------\n")
    ListaAptitud = Aptitud(ListaIndividuos)
    print_LF(ListaAptitud)
    ListaIndividuos, list2 = zip(*ListaAptitud)
    ListaIndividuos = list(ListaIndividuos)

    for i in range(iteraciones):
        f.write("\n\n  ##################### GENERACION: "+str(i)+" ###################")
        print("\n  #################### GENERACION: "+str(i)+" ###################")

        ListaHijos = []
        for j in range(poblacion):
            print("\n      ------------ PROCREATE ------------")
            f.write("\n\n      ------------ PROCREATE ------------\n")
            hijo1 = Procreate(ListaAptitud)
            print("     Hijo1: ",hijo1)
            f.write("\n     Hijo1: "+str(hijo1))

            # ListaIndividuos.append(hijo1)
            ListaHijos.append(hijo1)
            # ListaAptitud = Aptitud(ListaIndividuos)

        print("\n      ------------ Lista ascendientes ------------\n")
        f.write("\n\n      ------------ Lista ascendientes ------------\n")
        print_LF(ListaAptitud)

        print("\n      ------------ Lista descendientes ------------\n")
        f.write("\n\n      ------------ Lista descendientes ------------\n")
        ListaAptitudHijos = Aptitud(ListaHijos)
        print_LF(ListaAptitudHijos)

        print("\n      ------------ NUEVA POBLACION ------------\n")
        f.write("\n\n      ------------ NUEVA POBLACION ------------\n")
        ListaAptitud = Seleccion(ListaAptitud,ListaAptitudHijos)
        # ListaAptitud = Aptitud(ListaIndividuos)
        ListaIndividuos, list2 = zip(*ListaAptitud)
        ListaIndividuos = list(ListaIndividuos)
        print_LF(ListaAptitud)

Main()
