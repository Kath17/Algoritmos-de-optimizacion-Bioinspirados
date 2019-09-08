import random
# from random import randint, uniform,random,choice
import math
import os

# --------------- Variables globales -----------#

os.remove("Lab02_2.txt")
f = open ("Lab02_2.txt", "a")

iteraciones = 0
variables=0
poblacion=0

# ---------- Ingresar número de la poblacion y variables ------#
def Entradas():
    f.write("\n ----------------------- DATOS ------------------ \n\n")
    poblacion= int(input("Ingrese el número de la poblacion: "))
    f.write("Tamaño de la poblacion: "+str(poblacion)+"\n")

    # prob_blx = float(input("Ingrese el alpha del cruzamiento BLX: "))
    # f.write("Alpha del cruzamiento BLX: "+str(prob_blx)+"\n")

    iteraciones = int(input("Ingrese el número de iteraciones: "))
    f.write("Cantidad de iteraciones: "+str(iteraciones)+"\n")

    prob_mut = int(input("Ingrese la probabilidad de mutacion: "))
    f.write("Probabilidad de mutacion: "+str(prob_mut)+"\n")

    prob_cru = int(input("Ingrese la probabilidad de cruzamiento: "))
    f.write("Probabilidad de cruzamiento: "+str(prob_cru)+"\n\n")

    return poblacion,iteraciones,prob_mut,prob_cru

#------------ Generar la poblacion dada las entradas -----------#
def generarPoblacion(pobla):
    ListaIndividuos = []
    for i in range(pobla):
        individuo = ""
        nodos = "ABCDE"
        while(len(individuo)<5):
            letra_aleatoria = random.choice(nodos)
            while(letra_aleatoria in individuo):
                letra_aleatoria = random.choice(nodos)
            individuo = individuo + letra_aleatoria
        ListaIndividuos.append(individuo)
    return ListaIndividuos

# --------------------------- Distancia ----------------------------#
def funcion(individuo,Grafo):
    sum = 0
    primerNodo = individuo[0]
    segundoNodo = ""
    for i in range(1,len(individuo)):
        segundoNodo = individuo[i]
        sum = sum + Grafo[primerNodo][segundoNodo]
        primerNodo  = segundoNodo
    return sum

#---------- Evaluando individuos con funcion de aptitud---------#
def Evaluar(Lista,poblacion,Grafo):
    Lista2 = []
    for i in range(poblacion):
        Lista2.append(funcion(Lista[i],Grafo))
    # print("antigua lista: ",ListaFuncion)
    # Normalizar(Lista2)
    return Lista2

# ----------------------------- RUleta ---------------------------------#
# def Ruleta():

def ListaFunInversa(ListaFun):
    ListaInversa = []
    for i in range(len(ListaFun)):
        ListaInversa.append(round((1.0/ListaFun[i]),4))
    return ListaInversa

#--------------- Hallar probabilidad de cada poblador ----------#
def Probabilidades(ListaFun):
    #Nueva lista de probabilidades con los valores invertidos
    ListaFun = ListaFunInversa(ListaFun)
    # print("\nLista Inversa: ",ListaFun)
    ListaProb = []
    Total = sum(ListaFun)
    for i in range(len(ListaFun)):
        prob = ((100*(ListaFun[i]))/(Total))
        ListaProb.append(round(prob,4))
    return ListaProb
    # print("Suma de prob: ",sum( ListaProb))

# ---------- Funcion de la Ruleta para elegir un padre dada una probabilidad ----------#
def ElegirPadre(ListaProb,prob):
    i = 0
    var = ListaProb[i]

    while(True):
        if((prob > var) and (i+1 < len(ListaProb))):
            i=i+1
            # print("i:",i)
            var = ListaProb[i] + var
            # continue
        else:
            break
    #retorna posicion del padre elegido
    return i

# ------------------ Seleccionar un padre y madre -----------------#
def SeleccionPadres(Lista,ListaProb):
    # num = randint(0,100)
    print("\n                                 ------------ RULETA ------------                           \n")
    f.write("\n\n                                 ------------ RULETA ------------                           \n")
    print("NUEVOS PADRES: ")
    f.write("\nNUEVOS PADRES: ")
    num = round(random.uniform(0,100),4)
    print("\nPrimer random: ",num)
    f.write("\n\nPrimer random: "+ str(num)+"\n")
    Madre = ElegirPadre(ListaProb,num)

    # num = randint(0,100)
    num = round(random.uniform(0,100),4)
    print("Segundo random:",num)
    f.write("\nSegundo random: "+ str(num)+"\n")
    Padre = ElegirPadre(ListaProb,num)
    return Lista[Madre],Lista[Padre]

# ----------------------- Muta? ----------------------------#
def Muta(prob):
    num = random.randint(1,100)
    if(num<=prob):
        print("\n      --- Mutación ---")
        f.write("\n\n      --- Mutación ---")
        print("      Muta con: ",num," de ",prob,"%")
        f.write("\n      Muta con: "+str(num)+" de "+str(prob)+"%")
        return True
    else:
        return False

# ----------------------- Se cruzan? ----------------------------#
def Cruza(prob):
    num = random.randint(1,100)
    if(num<=prob):
        print("\n    Se cruzaron con: ",num," de ",prob,"%")
        f.write("\n\n    Se cruzaron con: "+str(num)+" de "+str(prob)+"%")
        return True
    else:
        return False

def Intercambiar(hijo,hijo2,char):
    for i in range(len(hijo)):
        if(char == hijo[i]):
            return hijo2[i]


# ----------------------------- Cruzamiento -----------------------------#
def Cruzamiento(Madre,Padre):
    puntosCorte=len(Madre)-2
    # puntosCorte=len(Madre)
    # posicion = random.randint(0,puntosCorte)
    posicion = random.randint(1,puntosCorte)
    posicion2 = random.randint(1,puntosCorte)
    while( posicion == posicion2):
        posicion = random.randint(1,puntosCorte)
        posicion2 = random.randint(1,puntosCorte)
    if(posicion2 < posicion):
        temp = posicion2
        posicion2 = posicion
        posicion = temp

    # madre = "ABCDE"
    # padre = "BCDEA"

    hijo1 = Madre
    hijo2 = Padre

    print("    Posiciones: ",posicion," a ",posicion2)
    f.write("\n    Posiciones: "+str(posicion)+" a "+str(posicion2))

    for i in range(posicion, posicion2+1):
        # print("i: ", i)
        aux1 = hijo1[i]
        aux2 = hijo2[i]
        # print("Aux: ",aux1," y ", aux2)
        if(aux1 != aux2):
            for j in range(len(Madre)):
                if( hijo1[j] == aux2 ):
                    list1 = list(hijo1)
                    list1[j] = aux1
                    hijo1 = ''.join(list1)
                    break
            for k in range(len(Padre)):
                if(hijo2[k] == aux1):
                    list2 = list(hijo2)
                    list2[k] = aux2
                    hijo2 = ''.join(list2)
                    break

        list1 = list(hijo1)
        list1[i] = aux2
        hijo1 = ''.join(list1)

        list2 = list(hijo2)
        list2[i] = aux1
        hijo2 = ''.join(list2)

    return hijo1,hijo2

# def Random(ListaIndividuos):
#     ran = random.randint(0,len(ListaIndividuos)-1)
#     ran2 = random.randint(0,len(ListaIndividuos)-1)
#     return ListaIndividuos[ran],ListaIndividuos[ran2]


# ------------------------------- MUTACION -------------------------------#
def Mutacion(Hijo):
    ran1= random.randint(0,len(Hijo)-1)
    ran2= random.randint(0,len(Hijo)-1)

    print("      Se intercambia: ",Hijo[ran1]," con ", Hijo[ran2])
    f.write("\n      Se intercambia: "+str(Hijo[ran1])+" con "+str(Hijo[ran2]))
    temp = Hijo[ran2]
    lista = list(Hijo)
    lista[ran2] = Hijo[ran1]
    lista[ran1] = temp
    Hijo = ''.join(lista)

    # print("      Nuevo Hijo: ",Hijo)
    return Hijo


# ----------------------- Eleccion de Nuevos Individuos ---------------------_#
def NuevaPoblacion(Lista,fitness,poblacion):
    veces = len(Lista) - poblacion
    for i in range(veces):   #Bota al menor
        i_maximo = fitness.index(max(fitness))
        Lista.pop(i_maximo)
        fitness.pop(i_maximo)
    return Lista,fitness



# ------------------------Proceso completo -------------------------#
def Main():
    poblacion,iteraciones,prob_mut,prob_cruz = Entradas()
    ListaIndividuos = generarPoblacion(poblacion)
    # ListaHijos = []
    Grafo = {'A':{'B':2,'C':2,'D':1,'E':4},
             'B':{'A':2,'C':3,'D':2,'E':3},
             'C':{'A':2,'B':3,'D':2,'E':2},
             'D':{'A':1,'B':2,'C':2,'E':4},
             'E':{'A':4,'B':3,'C':2,'D':4}}

    f.write("\n ---------------- Generando Población Inicial ------------- ")
    print("\nLista de poblacion: ",ListaIndividuos)
    f.write("\nLista de poblacion: "+str(ListaIndividuos)+"\n")

    f.write(" ----------------- Evaluando Individuos -------------------")
    ListaFuncion = Evaluar(ListaIndividuos,len(ListaIndividuos),Grafo)
    f.write("\nLista fitness: "+str(ListaFuncion)+"\n")
    print("Lista fitness: ",ListaFuncion)

    f.write(" ----------------- Sacando Probabilidad -------------------")
    ListaProbabilidades = Probabilidades(ListaFuncion)
    f.write("\nLista de probabilidades: "+str(ListaProbabilidades)+"\n")
    print("Lista de probabilidades: ",ListaProbabilidades)

    for j in range(iteraciones):
        f.write("\n\n ------------------------------------------------------------\n")
        f.write("------------------------- ITERACION: "+str(j)+" ---------------------\n")
        f.write("------------------------------------------------------------")

        print("\n      -----------------------------------------------------------------------------------\n")
        print("      ----------------------------------- ITERACION ",j,"---------------------------------\n")
        print("      -----------------------------------------------------------------------------------")

        nro_cruzamientos = int(poblacion/2)
        ListaHijos = []
        ListaHijosFuncion = []
        for i in range (nro_cruzamientos):
            Madre,Padre = SeleccionPadres(ListaIndividuos,ListaProbabilidades)
            f.write("\n\n  Madre: "+Madre)
            f.write("\n  Padre: "+Padre)
            print("\n  Madre: ",Madre)
            print("  Padre: ",Padre)
            if(Cruza(prob_cruz)==True):
                f.write("\n\n    --- Cruzamiento ---")
                print("\n    --- Cruzamiento ---")
                hijo1, hijo2 = Cruzamiento(Madre,Padre)
            else:
                f.write("\n\n  --- No hay cruzamiento, random: ---")
                print("\n  --- No hay cruzamiento, random: ---")
                hijo1, hijo2 = Madre, Padre
            f.write("\n\n    Hijo1: "+hijo1)
            f.write("\n    Hijo2: "+hijo2)
            print("\n    Hijo1: ",hijo1)
            print("    Hijo2: ",hijo2)

            if(Muta(prob_mut)==True):
                hijo1 = Mutacion(hijo1)
                f.write("\n\n      Hijo1 muta a: "+hijo1)
                print("\n      Hijo1 muta a: ",hijo1)
            if(Muta(prob_mut)==True):
                hijo2 = Mutacion(hijo2)
                f.write("\n\n      Hijo2 muta a: "+hijo2)
                print("\n      Hijo2 muta a: ",hijo2)

            ListaHijos.append(hijo1)
            ListaHijos.append(hijo2)
            ListaHijosFuncion.append(funcion(hijo1,Grafo))
            ListaHijosFuncion.append(funcion(hijo2,Grafo))

        ListaIndividuos = ListaIndividuos + ListaHijos
        ListaFuncion = ListaFuncion + ListaHijosFuncion
        # ListaProbabilidades = ListaProbabilidades + Probabilidades(ListaHijosFuncion)

        print("\n\nTotal de individuos nro ",j,": ",ListaIndividuos)
        f.write("\n\n\nTotal de individuos nro "+str(j)+": "+str(ListaIndividuos))
        print("Lista total de funciones objetivo: ",ListaFuncion)
        f.write("\nLista total de funciones objetivo: "+str(ListaFuncion))


        # ------------------- Nueva Poblacion ----------------------#
        f.write("\n\n                ---------------- Nueva Poblacion ------------- \n")
        print("\n                      ---------------- Nueva Poblacion ------------- \n")
        ListaIndividuos,ListaFuncion = NuevaPoblacion(ListaIndividuos,ListaFuncion,poblacion)
        print("Nueva poblacion nro ",j,": ",ListaIndividuos)
        f.write("\nNueva poblacion nro "+str(j)+": "+str(ListaIndividuos))
        print("Nueva Lista de Funciones Objetivo: ",ListaFuncion)
        f.write("\nNueva Lista de Funciones Objetivo: "+str(ListaFuncion))
        ListaProbabilidades = Probabilidades(ListaFuncion)
        print("Lista nueva de probabilidades: ",ListaProbabilidades)
        f.write("\nLista nueva de probabilidades: "+str(ListaProbabilidades))

Main()
