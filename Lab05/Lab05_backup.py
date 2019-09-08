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

    prob_cruz = int(input("Ingrese la probabilidad de cruzamiento: "))
    f.write("Probabilidad de cruzamiento: "+str(prob_cruz)+"\n\n")

    prob_mut = int(input("Ingrese la probabilidad de mutacion: "))
    f.write("Probabilidad de mutacion: "+str(prob_mut)+"\n\n")

    return poblacion,iteraciones,prob_rep,prob_cruz,prob_mut


def print_L(Lista):
    for i in range(len(Lista)):
        print(Lista[i])

def generar():
    individuo = ""
    individuo += "( "
    aux = random.choice(["+", "-", "*","%","/"])
    individuo += aux
    individuo += " ( "
    aux = random.choice(["+", "-", "*","%","/"])
    individuo += aux
    aux = random.choice([" -1", " -2", " -3"," -4"," -5",
                         " x"," x"," x"," x"," x",
                         " 1", " 2", " 3"," 4"," 5"," 0",
                         " x"," x"," x"," x"," x"])
    individuo += aux
    aux = random.choice([" -1", " -2", " -3"," -4"," -5",
                         " x"," x"," x"," x"," x",
                         " 1", " 2", " 3"," 4"," 5"," 0",
                         " x"," x"," x"," x"," x"])
    individuo += aux
    individuo += " ) ( "
    aux = random.choice(["+", "-", "*","%","/"])
    individuo += aux
    aux = random.choice([" -1", " -2", " -3"," -4"," -5",
                         " x"," x"," x"," x"," x",
                         " 1", " 2", " 3"," 4"," 5"," 0",
                         " x"," x"," x"," x"," x"])
    individuo += aux
    aux = random.choice([" -1", " -2", " -3"," -4"," -5",
                         " x"," x"," x"," x"," x",
                         " 1", " 2", " 3"," 4"," 5"," 0",
                         " x"," x"," x"," x"," x"])
    individuo += aux
    individuo += " ) )"

    if()
    return individuo

# -------------------- Generar poblacion ---------------------#
def generarPoblacion(poblacion):
    ListaIndividuos = []

    for i in range(poblacion):
        individuo =generar()
        ListaIndividuos.append(individuo)

    return ListaIndividuos
    # print("Lista de Individuos: ",ListaIndividuos)

# ------------------------ Evaluar un individuo -------------------#
def Evaluar(cad,num):
    print(" Cad a hacer split: ",cad)
    cadena = cad.split(" ")
    # print(cadena)
    for i in range(len(cadena)):
        if( cadena[i]== 'x'):
            cadena[i] = str(num)
    #for i in range(len(cadena)):
    try:
        respuesta = eval(cadena[2]+cadena[4]+cadena[3]+cadena[5]+cadena[6]+
                    cadena[1]+cadena[7]+cadena[9]+cadena[8]+cadena[10]+cadena[11])
        return respuesta
    except:
        return generar()

# ------------------------ Aptitud -------------------------#
def Aptitud(ListaIndividuos, Lista):
    ListaAptitud=[]
    for i in range(len(ListaIndividuos)): # ["(+ x x)"]
        val = 0
        acumulado = 0
        for j in range(len(Lista)):  # [(0, 0.5)]
            val = Evaluar(ListaIndividuos[i],Lista[j][0])
            if( type(val) is int or type(val) is float):
                print("Reemplazando: "+str(Lista[j][0])+" da: "+str(val))
                acumulado = acumulado + pow((val - Lista[j][1]),2)
                print("  Acumulado + (x - y)^2: ",acumulado)
            else:
                print("Se encontro division entre 0")
                ListaIndividuos[i] = val
                return ListaIndividuos
                break
        ListaAptitud.append((ListaIndividuos[i],val))

    return ListaAptitud

# ------------------------Proceso completo -------------------------#
def Main():
    poblacion,iteraciones,prob_rep,prob_cruz,prob_mut = Entradas()

    # Lista = [(0,0),(0.1,0.005),(0.2,0.02),(0.3,0.045),(0.4,0.08),(0.5,0.125),
    #          (0.6,0.18),(0.7,0.245),(0.8,0.32),(0.9,0.405)]
    Lista = [(0,0),(2.0,2.0),(5.0,5.0),(0,0)]

    f.write("\n ---------------- Generando Población Inicial ------------- ")
    ListaIndividuos = generarPoblacion(poblacion)

    print("\n -------------------- La lista de individuos ----------------------\n")
    print_L(ListaIndividuos)
    f.write("\nLista de poblacion: "+str(ListaIndividuos)+"\n")

    print("\n --------------------- Sacando Lista de aptitud ------------------")
    ListaAptitud = Aptitud(ListaIndividuos,Lista)
    while( type(ListaAptitud[0]) is not tuple ):
        print("Entro a generar nuevo individuo")
        ListaIndividuos = ListaAptitud
        print("Lista Individuos nueva: ",ListaIndividuos)
        ListaAptitud = Aptitud(ListaIndividuos,Lista)
    print("Aptitud: ",ListaAptitud)



Main()
