import random
import math
import os
import numpy as np

# ----------- VARIABLES GLOBALES -----------#

os.remove("Lab05.txt")
f = open("Lab05.txt", "a")

# ---------- Ingresar número de la poblacion y variables ------#
def Entradas():
    f.write("\n ----------------------- DATOS ------------------ \n\n")
    poblacion= int(input("Ingrese el número de la poblacion: "))
    f.write("Tamaño de la poblacion: "+str(poblacion)+"\n")

    iteraciones = int(input("Ingrese el número de iteraciones: "))
    f.write("Cantidad de iteraciones: "+str(iteraciones)+"\n")

    prob_rep = float(input("Ingrese probabilidad de reproducción: "))
    f.write("Probabilidad de reproducción: "+str(prob_rep)+"\n")

    prob_cruz = float(input("Ingrese la probabilidad de cruzamiento: "))
    f.write("Probabilidad de cruzamiento: "+str(prob_cruz)+"\n")

    prob_mut = float(input("Ingrese la probabilidad de mutacion: "))
    f.write("Probabilidad de mutacion: "+str(prob_mut))

    return poblacion,iteraciones,prob_rep,prob_cruz,prob_mut


def print_L(Lista):
    f.write("\n ---------------------------")
    f.write("\n|          INDIVIDUOS       |")
    f.write("\n ---------------------------")
    for i in range(len(Lista)):
        print(Lista[i])
        f.write("\n| "+str(Lista[i])+" |")

def print_ES(Lista):
    print(" -----------------------")
    print("|  ENTRADA  |   SALIDA  |")
    print(" -----------------------")
    f.write("\n --------------------")
    f.write("\n|  ENTRADA |  SALIDA |")
    f.write("\n --------------------")
    for i in range(len(Lista)):
        print("|   ",Lista[i][0],"   |  ",Lista[i][1],"  |")
        f.write("\n|   "+str(Lista[i][0])+"   |  "+str(Lista[i][1])+"  |")
    print(" ------------------------")
    f.write("\n ---------------------")

def print_FA(Lista):
    print("\n ------------------------------------------")
    print("|         Individuos         |   Fitness   |")
    print(" ------------------------------------------")
    f.write("\n\n -------------------------------------")
    f.write("\n|        Individuos        |  Fitness |")
    f.write("\n -------------------------------------")
    for i in range(len(Lista)):
        print("|",Lista[i][0],"| ",Lista[i][1]," |")
        f.write("\n|"+str(Lista[i][0])+"| "+str(Lista[i][1])+" |")
    print(" -----------------------------------------")
    f.write("\n ------------------------------------")

def generar():
    individuo = ""
    individuo += "( "
    aux = random.choice(["+", "-", "*","%","/"])
    individuo += aux
    individuo += " ( "
    aux = random.choice(["+", "-", "*","%","/"])
    individuo += aux
    aux = random.choice([" -1", " -2", " -3"," -4"," -5", " 0",
                         " x", " x", " x", " x", " x"," x", " x", " x", " x", " x"," x",
                         " 1", " 2", " 3"," 4"," 5"])
    individuo += aux
    aux = random.choice([" -1", " -2", " -3"," -4"," -5", " 0",
                         " x", " x", " x", " x", " x"," x", " x", " x", " x", " x"," x",
                         " 1", " 2", " 3"," 4"," 5"])
    individuo += aux
    individuo += " ) ( "
    aux = random.choice(["+", "-", "*","%","/"])
    individuo += aux
    aux = random.choice([" -1", " -2", " -3"," -4"," -5", " 0",
                         " x", " x", " x", " x", " x"," x", " x", " x", " x", " x"," x",
                         " 1", " 2", " 3"," 4"," 5"])
    individuo += aux
    aux = random.choice([" -1", " -2", " -3"," -4"," -5", " 0",
                         " x", " x", " x", " x", " x"," x", " x", " x", " x", " x"," x",
                         " 1", " 2", " 3"," 4"," 5"])
    individuo += aux
    individuo += " ) )"

    return individuo

# -------------------- Generar poblacion ---------------------#
def generarPoblacion(poblacion):
    ListaIndividuos = []

    for i in range(poblacion):
        individuo = generar()
        while(Evaluar(individuo,0)=="Dio_cero"):
            # print("Individuo que da 0: ",individuo)
            individuo = generar()
        ListaIndividuos.append(individuo)

    return ListaIndividuos
    # print("Lista de Individuos: ",ListaIndividuos)

# ------------------------ Evaluar un individuo -------------------#
def Evaluar(cad,num):
    # print(" Cad a hacer split: ",cad)
    cadena = cad.split(" ")
    # print(cadena)
    for i in range(len(cadena)):
        if( cadena[i]== 'x'):
            cadena[i] = str(num)

    try:
        respuesta = eval(cadena[2]+cadena[4]+cadena[3]+cadena[5]+cadena[6]+
                    cadena[1]+cadena[7]+cadena[9]+cadena[8]+cadena[10]+cadena[11])
        return round(respuesta,4)
    except:
        return "Dio_cero"

# ------------------------ Aptitud -------------------------#
def Aptitud(ListaIndividuos, Lista):
    ListaAptitud=[]
    for i in range(len(ListaIndividuos)): # ["(+ x x)"]
        val = 0
        # resta = 0
        acumulado = 0
        print("\n *Individuo: ",ListaIndividuos[i])
        f.write("\n *Individuo: "+str(ListaIndividuos[i]))
        for j in range(len(Lista)):  # [(0, 0.5)]
            val = Evaluar(ListaIndividuos[i],Lista[j][0])
            val_2 = round((val - Lista[j][1]),4)
            val_3 = round(pow(val_2,2),4)
            print("   Con: "+str(Lista[j][0])+" da: "+str(val)+" => "+"   ("+str(val)+" - "+str(Lista[j][1])+")^2  = "+str(val_3))
            # print("   ("+str(val)+" - "+str(Lista[j][1])+") :",val_2)
            # print("   ("+str(val)+" - "+str(Lista[j][1])+")^2 :",val_3)
            acumulado = round((acumulado + val_3),4)

        prom = round((acumulado/ len(Lista)),4)
        print("   Prom: ( "+str(acumulado)+"/"+str(len(Lista))+"): "+str(prom))
        f.write("   Prom: ( "+str(acumulado)+"/"+str(len(Lista))+"): "+str(prom))
        ListaAptitud.append((ListaIndividuos[i],prom))

    return ListaAptitud

# ------------------ Se reproducen, cruzan o mutan? ---------------------#
def Operacion(prob_cruz,prob_rep,prob_mut):
    num = random.randint(1,prob_cruz+prob_rep+prob_mut)
    if(num <= prob_rep):
        print("\n      ------------ REPRODUCCION ------------\n")
        f.write("\n\n      ------------ REPRODUCCION ------------\n")
        print("  Se reproduce con: ",num," de ",prob_rep,"%")
        f.write("\n  Se reproduce con: "+str(num)+" de "+str(prob_rep)+"%")
        return 'r'
    elif(num > prob_rep and num<=(prob_cruz+prob_rep)):
        print("\n      ------------ CRUZAMIENTO ------------\n")
        f.write("\n\n      ------------ CRUZAMIENTO ------------\n")
        print("  Se cruza con: "+str(num)+" de "+str(prob_rep)+" a "+str(prob_cruz+prob_rep)+"%")
        f.write("\n  Se cruza con: "+str(num)+" de "+str(prob_rep)+" a "+str(prob_cruz+prob_rep)+"%")
        return 'c'
    elif(num > (prob_cruz+prob_rep) and num<=(prob_cruz+prob_rep+prob_mut)):
        print("\n      ------------ MUTACION ------------\n")
        f.write("\n\n      ------------ MUTACION ------------\n")
        print("  Muta con: "+str(num)+" de "+str(prob_cruz+prob_rep)+" a "+str(prob_cruz+prob_rep+prob_mut)+"%")
        f.write("\n  Muta con: "+str(num)+" de "+str(prob_cruz+prob_rep)+" a "+str(prob_cruz+prob_rep+prob_mut)+"%")
        return 'm'


def Torneo(ListaAptitud):
    ran = random.randint(0,len(ListaAptitud)-1)
    ran2 = random.randint(0,len(ListaAptitud)-1)

    while(ran==ran2):
        ran2 = random.randint(0,len(ListaAptitud)-1)

    print("  PP1: ",ListaAptitud[ran][0]," con: ",ListaAptitud[ran][1])
    print("  PP2: ",ListaAptitud[ran2][0]," con: ",ListaAptitud[ran2][1])
    f.write("\n  PP1: "+str(ListaAptitud[ran][0])+" con: "+str(ListaAptitud[ran][1]))
    f.write("\n  PP2: "+str(ListaAptitud[ran2][0])+" con: "+str(ListaAptitud[ran2][1]))

    if(ListaAptitud[ran][1] < ListaAptitud[ran2][1]):
        return ran
    else:
        return ran2

def Cruzar(string1, string2):

    part1 = ""
    partF1 = ""
    bool = False
    for i in range(len(string1)):
        if(string1[i] ==")"):
            bool= True
        if(bool==False):
            part1 += string1[i]
        else:
            partF1 += string1[i]

    part2 = ""
    partF2 = ""
    bool = False
    for i in range(len(string2)):
        if(string2[i] == ")"):
            bool= True
        if(bool== False):
            part2 += string2[i]
        else:
            partF2 += string2[i]

    return part1+partF2 , part2+partF1

def Cruzamiento(ListaAptitud):
    print("\n                 --- TORNEO ---         \n")
    f.write("\n\n                 --- TORNEO ---       \n")

    print("  Posibles Padres:")
    f.write("\n  Posibles Padres:")
    P1 = Torneo(ListaAptitud)
    P2 = Torneo(ListaAptitud)

    padre1 = ListaAptitud[P1][0]
    padre2 = ListaAptitud[P2][0]

    hijo1 , hijo2 = Cruzar(padre1,padre2)

    while(Evaluar(hijo1,0)=="Dio_cero"):
        # print("dio nan con: ",hijo1)
        P1 = Torneo(ListaAptitud)
        padre1 = ListaAptitud[P1][0]
        hijo1 , hijo2 = Cruzar(padre1,padre2)

    while(Evaluar(hijo2,0)=="Dio_cero"):
        # print("dio nan con: ",hijo2)
        P2 = Torneo(ListaAptitud)
        padre2 = ListaAptitud[P2][0]
        hijo1 , hijo2 = Cruzar(padre1,padre2)

    print("    Padres:")
    print("    P1: ",padre1)
    print("    P2: ",padre2)
    f.write("\n    Padres:")
    f.write("\n    P1: "+str(padre1))
    f.write("\n    P2: "+str(padre2))

    return hijo1, hijo2

def Reproduccion(ListaAptitud):
    print("\n                 --- TORNEO ---         \n")
    f.write("\n\n                 --- TORNEO ---       \n")

    pos_hijo1 = Torneo(ListaAptitud)
    print("    Padre:")
    print("    P1: ",ListaAptitud[pos_hijo1][0])
    f.write("\n    Padre:")
    f.write("\n    P1: "+str(ListaAptitud[pos_hijo1][0]))
    hijo1 = ListaAptitud[pos_hijo1][0]
    return hijo1

def Mutar(string1):
    indiv = string1.split(" ")
    ran = random.randint(0,len(indiv)-1)

    signos = ["+", "-", "*","%","/"]
    variables = ["-1", "-2", "-3","-4","-5", "x","1", "2", "3","4","5","0"]
    parentesis = ["(",")"]

    while( indiv[ran] in parentesis):
        ran = random.randint(0,len(indiv)-1)

    if( indiv[ran] in signos):
        new = random.choice(["+", "-","/","*","%"])
        indiv[ran] = new
    elif( indiv[ran] in variables):
        new = random.choice(["-1", "-2", "-3","-4","-5","x","1", "2", "3","4","5"])
        indiv[ran] = new

    # print("Anterior : "(" ".join(indiv)), " igual a = ",string1)

    while(Evaluar(" ".join(indiv),0)=="Dio_cero" or ((" ".join(indiv)) == string1)):

        if( indiv[ran] in signos):
            new = random.choice(["+", "-","/","*","%"])
            indiv[ran] = new
        elif( indiv[ran] in variables):
            new = random.choice(["-1", "-2", "-3","-4","-5","0","1", "2", "3","4","5"
                                ,"x","x","x","x","x","x","x","x","x","x"])
            indiv[ran] = new

    hijo = " ".join(indiv)
    return hijo


def Mutacion(ListaAptitud):
    print("\n                 --- TORNEO ---         \n")
    f.write("\n\n                 --- TORNEO ---       \n")

    pos_hijo1 = Torneo(ListaAptitud)
    print("    Padre:")
    print("    P1: ",ListaAptitud[pos_hijo1][0])
    f.write("\n    Padre:")
    f.write("\n    P1: "+str(ListaAptitud[pos_hijo1][0]))

    hijo1 = ListaAptitud[pos_hijo1][0]
    hijo1 = Mutar(hijo1)
    return hijo1

def NuevaPoblacion(ListaAptitud,poblacion):
    ordenado = sorted(ListaAptitud,key=lambda x:x[1])
    return ordenado[:poblacion]

# ------------------------Proceso completo -------------------------#
def Main():
    poblacion,iteraciones,prob_rep,prob_cruz,prob_mut = Entradas()

    Lista = [(0.0,0.0),(0.1,0.005),(0.2,0.020),(0.3,0.045),(0.4,0.080),(0.5,0.125),
             (0.6,0.180),(0.7,0.245),(0.8,0.320),(0.9,0.405)]
    # Lista = [(0,0),(2.0,2.0),(5.0,5.0),(0,0)]

    print("\n ---------------- La lista de Entrada y Salida Esperada ---------------\n")
    f.write("\n\n ---------------- La lista de Entrada y Salida Esperada ---------------\n")
    print_ES(Lista)

    f.write("\n\n ---------------- Generando Población Inicial -------------\n ")
    print("\n -------------------- La lista de individuos ----------------------\n")
    ListaIndividuos = generarPoblacion(poblacion)
    print_L(ListaIndividuos)

    print("\n --------------------- Sacando Lista de aptitud ------------------")
    f.write("\n\n --------------------- Lista de aptitud ------------------")
    ListaAptitud = Aptitud(ListaIndividuos,Lista)
    print_FA(ListaAptitud)

    for i in range(iteraciones):

        f.write("\n\n  ##################### GENERACION: "+str(i)+" ###################")
        print("\n  #################### GENERACION: "+str(i)+" ###################")

        ListaHijos = []
        ListaHijosAptitud = []
        individuals = 0
        while(individuals < poblacion):
            opcion = Operacion(prob_cruz,prob_rep, prob_mut)
            if('c'==opcion):
                hijo1,hijo2 = Cruzamiento(ListaAptitud)
                print("     Hijo1: ",hijo1)
                print("     Hijo2: ",hijo2)
                f.write("\n     Hijo1: "+str(hijo1))
                f.write("\n     Hijo2: "+str(hijo2))
                ListaHijos.append(hijo1)
                ListaHijos.append(hijo2)
                individuals += 2
            elif('r'==opcion):
                hijo1 = Reproduccion(ListaAptitud)
                print("     Hijo1: ",hijo1)
                f.write("\n     Hijo1: "+str(hijo1))
                ListaHijos.append(hijo1)
                individuals += 1
            elif('m'==opcion):
                hijo1 = Mutacion(ListaAptitud)
                print("     Hijo1: ",hijo1)
                f.write("\n     Hijo1: "+str(hijo1))
                ListaHijos.append(hijo1)
                individuals += 1
            print("                                                      ... N° Individuos: ",individuals)
            f.write("\n                                                      ... N° Individuos: "+str(individuals))

        ListaIndividuos = ListaHijos
        # ListaIndividuos = ListaIndividuos + ListaHijos

        f.write("\n\n ---------------- CALCULANDO FITNESS -------------")
        print("\n -------------------- CALCULANDO FITNESS ----------------------\n")
        ListaAptitud = Aptitud(ListaIndividuos,Lista)
        # ListaAptitud = NuevaPoblacion(ListaAptitud,poblacion)
        ListaIndividuos, list2 = zip(*ListaAptitud)
        ListaIndividuos = list(ListaIndividuos)

        f.write("\n\n ---------------- NUEVA POBLACION -------------")
        print("\n -------------------- NUEVA POBLACION ----------------------\n")
        # print_L(ListaIndividuos)
        # f.write("\nLista de poblacion: "+str(ListaIndividuos)+"\n")

        # print("\n --------------------- NUEVA LISTA FITNESS ------------------")
        print_FA(ListaAptitud)

Main()
