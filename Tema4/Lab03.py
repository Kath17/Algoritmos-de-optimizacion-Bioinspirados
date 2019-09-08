import random
import math
import os

# --------------- Variables globales -----------#

os.remove("Lab03.txt")
f = open ("Lab03.txt", "a")

iteraciones = 0
poblacion = 0

# ---------- Ingresar número de la poblacion y variables ------#
def Entradas():
    f.write("\n ----------------------- DATOS ------------------ \n\n")
    poblacion= int(input("Ingrese el número de la poblacion: "))
    f.write("Tamaño de la poblacion: "+str(poblacion)+"\n")

    iteraciones = int(input("Ingrese el número de iteraciones: "))
    f.write("Cantidad de iteraciones: "+str(iteraciones)+"\n")

    # prob_mut = int(input("Ingrese la probabilidad de mutacion: "))
    # f.write("Probabilidad de mutacion: "+str(prob_mut)+"\n")

    # prob_cru = int(input("Ingrese la probabilidad de cruzamiento: "))
    # f.write("Probabilidad de cruzamiento: "+str(prob_cru)+"\n\n")

    return poblacion,iteraciones


# ----------------------- Eleccion de Nuevos Individuos ---------------------_#
# ------------- Dejar a los individuos con la mejor funcion fitness --------_#
def NuevaPoblacion(Lista,fitness,poblacion):
    veces = len(Lista) - poblacion
    for i in range(veces):   #Bota al menor
        i_maximo = fitness.index(max(fitness))
        Lista.pop(i_maximo)
        fitness.pop(i_maximo)
    return Lista,fitness

#------------ Generar la poblacion dada las entradas y optimizar-----------#
def generarPoblacion(pobla,Grafo):
    ListaIndividuos = []
    veces = 3*pobla
    for i in range(veces):
        individuo = ""
        nodos = "ABCDEFGHIJ"
        while(len(individuo)<len(nodos)):
            letra_aleatoria = random.choice(nodos)
            while(letra_aleatoria in individuo):
                letra_aleatoria = random.choice(nodos)
            individuo = individuo + letra_aleatoria
        ListaIndividuos.append(individuo)


    print("\nLista 3M: ",ListaIndividuos)
    f.write("\nLista de poblacion 3M: "+str(ListaIndividuos)+"\n")

    ListaFun = Evaluar(ListaIndividuos,veces,Grafo)
    print("Lista fitness de lista 3M: ",ListaFun)
    f.write("\nFitness de lista 3M: "+str(ListaFun)+"\n")

    ListaIndividuos,Fitness = NuevaPoblacion(ListaIndividuos,ListaFun,pobla)
    # print("Lista de Individuos optimizada: ",ListaIndividuos)
    # print("Lista Funcion optimizada: ",Fitness)

    return ListaIndividuos,Fitness

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

# ----------------------------- Ruleta ---------------------------------#
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

# ---------- Funcion de la RULETA para elegir un padre dada una probabilidad ----------#
def ElegirPadre(ListaProb,prob):
    i = 0
    var = ListaProb[i]

    # print("...Probabilidad para ruleta: ",prob)

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
    f.write("\n\nPrimer random: "+ str(num))
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

# ----------------------------- Cruzamiento OBX-----------------------------#
def Cruzamiento(Madre,Padre):

    posicionesOBX = []
    temp1 = []
    temp2 = []

    orden1 = []
    orden2 = []

    h1 = ""
    h2 = ""

    for i in range(0,len(Madre)):
        ran = random.randint(0,1)
        if(ran == 1):
            temp1.append(Madre[i])
            temp2.append(Padre[i])
            posicionesOBX.append(i)
            # print("Wntro")

    # A B C D

    posicionesOBX.sort()
    print("    Posiciones: ",posicionesOBX)
    f.write("\n    Posiciones: "+str(posicionesOBX))

    for k in range(0,len(Madre)):
        if(Padre[k] in temp1):
            orden1.append(Padre[k])

    for l in range(0,len(Madre)):
        if(Madre[l] in temp2):
            orden2.append(Madre[l])

    ix = 0
    for m in range(0,len(Madre)):
        # if (len(posicionesOBX)>0):
        if (len(posicionesOBX)>0):
            if(posicionesOBX[ix] == m):
                h2 = h2 + orden2[0]
                h1 = h1 + orden1[0]
                orden1.pop(0)
                orden2.pop(0)
                posicionesOBX.pop(0)
                # if((ix+1) < len(posicionesOBX)):
                # ix = ix + 1
                # else:
                #     break
                # m = m + 1
            else:
                h1 = h1 + Madre[m]
                h2 = h2 + Padre[m]
        else:
            h1 = h1 + Madre[m]
            h2 = h2 + Padre[m]

    return h1,h2

# def Random(ListaIndividuos):
#     ran = random.randint(0,len(ListaIndividuos)-1)
#     ran2 = random.randint(0,len(ListaIndividuos)-1)
#     return ListaIndividuos[ran],ListaIndividuos[ran2]


# ------------------------------- MUTACION -------------------------------#
def Mutacion(Hijo,Grafo):

    func = funcion(Hijo,Grafo)
    bestHijo = Hijo

    print("\n    Hijo original: ",Hijo, " con: ",func)
    f.write("\n\n    Hijo original: "+Hijo+ " con: "+str(func))

    for i in range(60):

        ran1= random.randint(0,len(Hijo)-1)
        ran2= random.randint(0,len(Hijo)-1)

        # print("      Se intercambia: ",bestHijo[ran1]," con ", bestHijo[ran2])
        # f.write("\n      Se intercambia: "+str(bestHijo[ran1])+" con "+str(bestHijo[ran2]))
        temp = bestHijo[ran2]
        lista = list(bestHijo)
        lista[ran2] = bestHijo[ran1]
        lista[ran1] = temp
        HijoNuevo = ''.join(lista)

        funcTemp = funcion(HijoNuevo,Grafo)

        if(funcTemp < func):
            bestHijo = HijoNuevo
            func = funcTemp
            print("    Se reemplaza por ",bestHijo," con: ",func)
            f.write("\n    Se reemplaza por "+bestHijo+" con: "+str(func))

    print("    Mejor Nuevo Hijo: ",bestHijo, " con: ",func)
    f.write("\n    Mejor Nuevo Hijo: "+bestHijo+ " con: "+str(func))
    # print("      Nuevo Hijo: ",Hijo)
    return bestHijo, func


# ------------------------Proceso completo -------------------------#
def Main():
    prob_cruz = 100
    poblacion,iteraciones = Entradas()
    # ListaHijos = []
    Grafo = {'A':{'A':0,'B':12,'C':3, 'D':23,'E':1, 'F':5, 'G':23,'H':56,'I':12,'J':11},
             'B':{'A':12,'B':0,'C':9, 'D':18,'E':3, 'F':41,'G':45,'H':5, 'I':41,'J':27},
             'C':{'A':3, 'B':9,'C':0, 'D':89,'E':56,'F':21,'G':12,'H':48,'I':14,'J':29},
             'D':{'A':23,'B':18,'C':89,'D':0,'E':87,'F':46,'G':75,'H':17,'I':50,'J':42},
             'E':{'A':1, 'B':3, 'C':56,'D':87,'E':0,'F':55,'G':22,'H':86,'I':14,'J':33},
             'F':{'A':5 ,'B':41,'C':21,'D':46,'E':55,'F':0,'G':21,'H':76,'I':54,'J':81},
             'G':{'A':23,'B':45,'C':12,'D':75,'E':22,'F':21,'G':0,'H':11,'I':57,'J':48},
             'H':{'A':56,'B':5, 'C':48,'D':17,'E':86,'F':76,'G':11,'H':0,'I':63,'J':24},
             'I':{'A':12,'B':41,'C':14,'D':50,'E':14,'F':54,'G':57,'H':63,'I':0,'J':9 },
             'J':{'A':11,'B':27,'C':29,'D':42,'E':33,'F':81,'G':48,'H':24,'I':9,'J':0 }}


    ListaIndividuos,ListaFuncion = generarPoblacion(poblacion,Grafo)
    f.write("\n ---------------- Generando Población Inicial ------------- ")
    print("\nLista de poblacion optimizada: ",ListaIndividuos)
    f.write("\nLista de poblacion optimizada: "+str(ListaIndividuos)+"\n")

    f.write("\n----------------- Evaluando Individuos -------------------")
    # ListaFuncion = Evaluar(ListaIndividuos,len(ListaIndividuos),Grafo)
    f.write("\nLista fitness optimizada: "+str(ListaFuncion)+"\n")
    print("Lista fitness optimizada: ",ListaFuncion)

    f.write("\n----------------- Sacando Probabilidad -------------------")
    ListaProbabilidades = Probabilidades(ListaFuncion)
    f.write("\nLista de probabilidades: "+str(ListaProbabilidades)+"\n")
    print("Lista de probabilidades: ",ListaProbabilidades)

    for j in range(iteraciones):
        f.write("\n\n      ------------------------------------------------------------\n")
        f.write("      ------------------------- ITERACION: "+str(j)+" ---------------------\n")
        f.write("      ------------------------------------------------------------")

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
            # if(Cruza(prob_cruz)==True):
            f.write("\n\n    --- Cruzamiento ---\n")
            print("\n    --- Cruzamiento ---\n")
            hijo1, hijo2 = Cruzamiento(Madre,Padre)
            # else:
                # f.write("\n\n  --- No hay cruzamiento, padres son hijos ---")
                # print("\n  --- No hay cruzamiento, padres son hijos ---")
                # hijo1, hijo2 = Madre, Padre
            f.write("\n\n    Hijo1: "+hijo1)
            f.write("\n    Hijo2: "+hijo2)
            print("\n    Hijo1: ",hijo1)
            print("    Hijo2: ",hijo2)

            # ------------------ Hill Climbing -------------------#
            f.write("\n\n    --- Hill Climbing Algorithm ---")
            print("\n    --- Hill Climbing Algorithm ---")

            hijo1,func1 = Mutacion(hijo1,Grafo)
            f.write("\n\n       Hijo1 muta a: "+hijo1)
            print("\n       Hijo1 muta a: ",hijo1)

            hijo2,func2 = Mutacion(hijo2,Grafo)
            f.write("\n\n       Hijo2 muta a: "+hijo2)
            print("\n       Hijo2 muta a: ",hijo2)

            ListaHijos.append(hijo1)
            ListaHijos.append(hijo2)
            ListaHijosFuncion.append(func1)
            ListaHijosFuncion.append(func2)

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
