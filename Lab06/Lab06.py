import random
import math
import os
import numpy as np

# ----------- VARIABLES GLOBALES -----------#

os.remove("Lab06.txt")
f = open("Lab06.txt", "a")

lim_inf=-10
lim_sup=10

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

    print("Opciones: ")
    print("1) (u+1) - EE")
    print("2) (u+A) - EE")
    print("3) (u,A) - EE")
    opcion = int(input("Ingrese la opcion que desea: "))
    A = 0

    poblacion= int(input("Ingrese el número de la poblacion: "))
    f.write("Tamaño de la poblacion: "+str(poblacion)+"\n")

    if( opcion == 2):
        A = int(input("Ingrese valor de A: "))
        f.write("Valor de A para (u+A)-EE: "+str(A)+"\n")

    elif (opcion == 3):
        A = int(input("Ingrese valor de A: "))
        f.write("Valor de A para (u,A)-EE: "+str(A)+"\n")

    iteraciones = int(input("Ingrese el número de iteraciones: "))
    f.write("Cantidad de iteraciones: "+str(iteraciones)+"\n")

    desviacion = float(input("Ingrese valor para desviacion: "))
    f.write("Valor para desviacion: "+str(desviacion)+"\n")


    return poblacion,iteraciones,desviacion,opcion,A

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

def Cruzamiento(ListaAptitud):
    print("\n                 --- TORNEO ---         \n")
    f.write("\n                 --- TORNEO ---       \n")

    print("  Posibles Padres:")
    f.write("  Posibles Padres:")
    P1 = Torneo(ListaAptitud)
    P2 = Torneo(ListaAptitud)

    padre1 = ListaAptitud[P1][0]   #[(-1,2),(0.1,0.1)]
    padre2 = ListaAptitud[P2][0]   #[(-2,1),(0.1,0.1)]

    hijo1 = []
    x1_medio = (padre1[0][0] + padre2[0][0])/2
    x2_medio = (padre1[0][1] + padre2[0][1])/2

    d1_medio = math.sqrt(padre1[1][0] + padre2[1][0])
    d2_medio = math.sqrt(padre1[1][1] + padre2[1][1])

    hijo1= [(round(x1_medio,5),round(x2_medio,5)),(round(d1_medio,5),round(d2_medio,5))]

    print("    Padres:")
    print("    P1: ", padre1)
    print("    P2: ",padre2)
    f.write("\n    Padres:")
    f.write("\n    P1: "+str(padre1))
    f.write("\n    P2: "+str(padre2))

    return hijo1   #[ (-4,2.7),(0.4,0.4) ]

def Mutacion(hijo,poblacion):

    Adesv = 1/(math.sqrt(2*math.sqrt(poblacion)))
    nDesv = round(hijo[1][0]*math.exp(np.random.normal(0,Adesv)),5)
    print("   Nueva desviacion: ",nDesv)
    f.write("   Nueva desviacion: "+ str(nDesv))

    l = list(hijo[1])
    hijo[1] = tuple([nDesv,nDesv])

    x1 = hijo[0][0] + np.random.normal(0,hijo[1][0])
    x2 = hijo[0][1] + np.random.normal(0,hijo[1][1])

    while( (x1 < lim_inf or x1 > lim_sup) or (x2 < lim_inf or x2 > lim_sup)):
        x1 = hijo[0][0] + np.random.normal(0,hijo[1][0])
        x2 = hijo[0][1] + np.random.normal(0,hijo[1][1])

    x1 = round(x1,5)
    x2 = round(x2,5)

    func1 = F((hijo[0]))  #Original
    func2 = F((x1,x2))   #Hijos

    if(func1 < func2):
        print("   Posible mutacion: ", [(x1,x2),(hijo[1][0],hijo[1][1])])
        print("   Padre < Hijo con: ",func1,",hijo: ",func2)
        f.write("\n   Posible mutacion: "+str([(x1,x2),(hijo[1][0],hijo[1][1])]))
        f.write("\n   Padre < Hijo con: "+str(func1)+",hijo: "+str(func2))
        return hijo
    else:
        print("   Mutacion: ", [(x1,x2),(hijo[1][0],hijo[1][1])])
        print("   Hijo < Padre con: ",func2,",padre: ",func1)
        f.write("\n   Mutacion: "+str([(x1,x2),(hijo[1][0],hijo[1][1])]))
        f.write("\n   Hijo < Padre con: "+str(func2)+",padre: "+str(func1))
        return [(x1,x2),(hijo[1][0],hijo[1][1])]

def Seleccion(ListaAptitud,A):
    ListaNueva = sorted(ListaAptitud,key=lambda x:x[1])
    ListaNueva = ListaNueva[:(len(ListaAptitud)-A)]
    return ListaNueva



# ------------------------Proceso completo -------------------------#
def Main():
    poblacion,iteraciones,desviacion,opcion,A = Entradas()

    ListaIndividuos = GenerarPoblacion(desviacion,poblacion)
    f.write("\n ---------------- Generando Población Inicial ------------- \n")
    print_L(ListaIndividuos)
    # f.write("\nLista de poblacion: "+str(ListaIndividuos)+"\n")

    f.write("\n\n----------------- Lista de Aptitud -------------------\n")
    ListaAptitud = Aptitud(ListaIndividuos)
    print_LF(ListaAptitud)

    for i in range(iteraciones):
        f.write("\n\n  ##################### GENERACION: "+str(i)+" ###################")
        print("\n  #################### GENERACION: "+str(i)+" ###################")

        if(opcion == 1):
            print("\n      ------------ CRUZAMIENTO ------------")
            f.write("\n\n      ------------ CRUZAMIENTO ------------\n")
            hijo1 = Cruzamiento(ListaAptitud)
            print("     Hijo1: ",hijo1)
            f.write("\n     Hijo1: "+str(hijo1))

            print("\n      ------------ MUTACION ------------\n")
            f.write("\n\n      ------------ MUTACION ------------\n")
            hijo1 = Mutacion(hijo1,poblacion)
            print("     Hijo1: ",hijo1)
            f.write("\n     Hijo1: "+str(hijo1))

            print("\n      ------------ Individuo agregado ------------\n")
            f.write("\n\n      ------------ Individuos agregado ------------\n")
            ListaIndividuos.append(hijo1)
            ListaAptitud = Aptitud(ListaIndividuos)
            print_LF(ListaAptitud[len(ListaAptitud)-1:])

            print("\n      ------------ NUEVA POBLACION ------------\n")
            f.write("\n\n      ------------ NUEVA POBLACION ------------\n")
            ListaAptitud = Seleccion(ListaAptitud,1)
            ListaIndividuos, list2 = zip(*ListaAptitud)
            ListaIndividuos = list(ListaIndividuos)
            print_LF(ListaAptitud)

        elif((opcion==2) or (opcion==3)):
            ListaHijos = []
            ListaHijosAptitud = []

            for j in range(A):
                print("\n      ------------ CRUZAMIENTO ------------")
                f.write("\n\n      ------------ CRUZAMIENTO ------------\n")
                hijo1 = Cruzamiento(ListaAptitud)
                print("     Hijo1: ",hijo1)
                f.write("\n     Hijo1: "+str(hijo1))

                print("\n      ------------ MUTACION ------------\n")
                f.write("\n\n      ------------ MUTACION ------------\n")
                hijo1 = Mutacion(hijo1,poblacion)
                print("     Hijo1: ",hijo1)
                f.write("\n     Hijo1: "+str(hijo1))

                ListaHijos.append(hijo1)
                print("\n                                                      ... Hijo n°",j,"\n")
                f.write("\n                                                      ... Hijo n°"+str(j)+"\n")

            print("\n      ------------ Individuos agregados ------------\n")
            f.write("\n\n      ------------ Individuos agregados ------------\n")
            ListaHijosAptitud = Aptitud(ListaHijos)
            print_LF(ListaHijosAptitud)

            ListaAptitud = ListaAptitud + ListaHijosAptitud

            print("\n      ------------ NUEVA POBLACION ------------\n")
            f.write("\n\n      ------------ NUEVA POBLACION ------------\n")
            ListaAptitud = Seleccion(ListaAptitud,A)
            ListaIndividuos, list2 = zip(*ListaAptitud)
            ListaIndividuos = list(ListaIndividuos)
            print_LF(ListaAptitud)


Main()
