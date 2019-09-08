from random import randint, uniform,random
import math
import os

# --------------- Variables globales -----------#

os.remove("Lab02_1.txt")
f = open ("Lab02_1.txt", "a")

iteraciones = 0
variables=0
poblacion=0

# ---------- Ingresar número de la poblacion y variables ------#
def Entradas():
    f.write("\n ----------------------- DATOS ------------------ \n\n")
    poblacion= int(input("Ingrese el número de la poblacion: "))
    f.write("Tamaño de la poblacion: "+str(poblacion)+"\n")

    prob_blx = float(input("Ingrese el alpha del cruzamiento BLX: "))
    f.write("Alpha del cruzamiento BLX: "+str(prob_blx)+"\n")

    iteraciones = int(input("Ingrese el número de iteraciones: "))
    f.write("Cantidad de iteraciones: "+str(iteraciones)+"\n")

    prob_mut = int(input("Ingrese la probabilidad de mutacion: "))
    f.write("Probabilidad de mutacion: "+str(prob_mut)+"\n")

    prob_cru = int(input("Ingrese la probabilidad de cruzamiento: "))
    f.write("Probabilidad de cruzamiento: "+str(prob_cru)+"\n\n")

    return poblacion,iteraciones,prob_mut,prob_cru,prob_blx

#------------ Generar la poblacion dada las entradas -----------#
def generarPoblacion(pobla):
    ListaIndividuos = []
    for i in range(pobla):
        tupla = ( randint(-100,100),
                  randint(-100,100),
                  randint(-100,100),
                  randint(-100,100),
                  randint(-100,100))
            # print(indiv)
        ListaIndividuos.append(tupla)
    return ListaIndividuos

#----------------------- Funcion de aptitud -------------------#
def funcion(V,W,X,Y,Z):
    return V-W+X-Y+Z
    # return num+1

#---------- Evaluando individuos con funcion de aptitud---------#
def Evaluar(pobla,Lista):
    Lista2 = []
    for i in range(pobla):
        Lista2.append(funcion(Lista[i][0],Lista[i][1],Lista[i][2],Lista[i][3],Lista[i][4]))
    # print("antigua lista: ",ListaFuncion)
    # Normalizar(Lista2)
    return Lista2

# ---------- Funcion para elegir posibles padres para el torneo ----------#
def Elegir(Lista):
    i = 0
    tamano = len(Lista)-1
    temp_pob = randint(0,tamano)
    temp_pob2 = randint(0,tamano)
    temp_pob3 = randint(0,tamano)
    # print("Poblador 1 elegido temporal: ",Lista[temp_pob])
    # print("Poblador 2 elegido temporal: ",Lista[temp_pob2])
    # print("Poblador 3 elegido temporal: ",Lista[temp_pob3])

    return temp_pob,temp_pob2,temp_pob3

# --------------------------------- Torneo------------------------------#
def GanaTorneo(Lista):
    Puntuaciones=[]
    t1,t2,t3 = Elegir(Lista)

    # print("Posibles padres: ",Lista[t1],",",Lista[t2],",",Lista[t3])
    f.write("\nPosibles padres: "+str(Lista[t1])+","+str(Lista[t2])+","+str(Lista[t3]))

    Puntuaciones.append((funcion(Lista[t1][0],Lista[t1][1],Lista[t1][2],Lista[t1][3],Lista[t1][4]),t1))
    Puntuaciones.append((funcion(Lista[t2][0],Lista[t2][1],Lista[t2][2],Lista[t2][3],Lista[t2][4]),t2))
    Puntuaciones.append((funcion(Lista[t3][0],Lista[t3][1],Lista[t3][2],Lista[t3][3],Lista[t3][4]),t3))

    Puntuaciones.sort(reverse=True)
    #Retorna la puntuacion y la posición de la tupla v,w,x,y,z
    return Puntuaciones[0][1]

# ----------------------- Muta? ----------------------------#
def Muta(prob):
    num = randint(1,100)
    if(num<=prob):
        # print("      Mutaron con: ",num," de ",prob,"%")
        f.write("\n      Mutaron con: "+str(num)+" de "+str(prob)+"%")
        return True
    else:
        return False

# ----------------------- Se cruzan? ----------------------------#
def Cruza(prob):
    num = randint(1,100)
    if(num<=prob):
        # print("    Se cruzaron con: ",num," de ",prob,"%")
        f.write("\n    Se cruzaron con: "+str(num)+" de "+str(prob)+"%")
        return True
    else:
        return False

# --------------------- Cruzamiento mixtura BLX-alpha --------------------#
def BLX(prob):
    return round(uniform(0-prob,1+prob),4)

#---------------------------Cruzamiento --------------------#
def Cruzamiento(Lista,prob_cruz,prob_mut,prob_blx,lim_inf,lim_sup):
    # ListaHijos = []

    # for i in range(len(Lista)):
    # print("\n                                       ------------ TORNEO ------------                           \n")
    f.write("\n\n                                       ------------ TORNEO ------------                           \n\n")
    P1 = GanaTorneo(Lista)
    P2 = GanaTorneo(Lista)
    # print("  \nPADRES: ",Lista[P1]," y ",Lista[P2])
    f.write("  \n\nPADRES: "+str(Lista[P1])+" y "+str(Lista[P2]))

    blx = BLX(prob_blx)
    # print("  BLX: ",blx)
    f.write("\n  BLX: "+str(blx))
    if(Cruza(prob_cruz)==True):
        # print("    Se cruzaron .. ")
        c1 = Lista[P1][0]+blx*(Lista[P2][0]-Lista[P1][0])
        while(c1 < lim_inf or c1 > lim_sup):
            blx2 = BLX(prob_blx)
            c1 = Lista[P1][0]+blx2*(Lista[P2][0]-Lista[P1][0])

        c2 = Lista[P1][1]+blx*(Lista[P2][1]-Lista[P1][1])
        while(c2 < lim_inf or c2 > lim_sup):
            blx2 = BLX(prob_blx)
            c2 = Lista[P1][1]+blx2*(Lista[P2][1]-Lista[P1][1])

        c3 = Lista[P1][2]+blx*(Lista[P2][2]-Lista[P1][2])
        while(c3 < lim_inf or c3 > lim_sup):
            blx2 = BLX(prob_blx)
            c3 = Lista[P1][2]+blx2*(Lista[P2][2]-Lista[P1][2])

        c4 = Lista[P1][3]+blx*(Lista[P2][3]-Lista[P1][3])
        while(c4 < lim_inf or c4 > lim_sup):
            blx2 = BLX(prob_blx)
            c4 = Lista[P1][3]+blx2*(Lista[P2][3]-Lista[P1][3])

        c5 = Lista[P1][4]+blx*(Lista[P2][4]-Lista[P1][4])
        while(c5 < lim_inf or c5 > lim_sup):
            # print("c5: ",c5)
            blx2 = BLX(prob_blx)
            c5 = Lista[P1][4]+blx2*(Lista[P2][4]-Lista[P1][4])

        H1 = ( round(c1,4),round(c2,4) ,round(c3,4),round(c4,4),round(c5,4))
    else:
        # print("    No se cruzaron, se elige a un padre random")
        f.write("\n    No se cruzaron, se elige a un padre random")
        random = randint(1,2)
        if(random==1): H1 = Lista[P1]
        elif(random==2): H1 = Lista[P2]

    # print("Hijo: ",H1)

        # ListaHijos.append(H1)
    return H1
    # return ListaHijos

# ---------------------------------- Mutación ------------------------------------#
def Mutando(Hijo):
    elegido = randint(0,4)
    newC = round(uniform(-100,100),4)
    # Hijo[elegido] = newC

    lst = list(Hijo)
    lst[elegido] = newC
    Hijo = tuple(lst)

    return Hijo

# ----------------------- Eleccion de Nuevos Individuos ---------------------_#
def NuevaPoblacion(Lista,fitness,poblacion):
    veces = len(Lista) - poblacion
    for i in range(veces):   #Bota al menor
        i_minimo = fitness.index(min(fitness))
        Lista.pop(i_minimo)
        fitness.pop(i_minimo)
    return Lista,fitness

# ------------------------Proceso completo -------------------------#
def Main():
    poblacion,iteraciones,prob_mut,prob_cruz,prob_blx = Entradas()
    ListaIndividuos = generarPoblacion(poblacion)
    ListaHijos = []
    lim_inf = -100
    lim_sup = 100

    f.write(" ---------------- Generando Población Inicial ------------- \n")
    # print("\nLista de poblacion: ",ListaIndividuos)
    f.write("\n\nLista de poblacion: "+str(ListaIndividuos)+"\n")

    # f.write("ITERACION: 0\n\n")
    f.write(" ----------------- Evaluando Individuos -------------------\n")
    ListaFuncion = Evaluar(len(ListaIndividuos),ListaIndividuos)
    f.write("\nLista fitness: "+str(ListaFuncion)+"\n")
    # print("Lista fitness: ",ListaFuncion)

    # f.write("\n ------ Selección de individuos - Torneo --------\n")
    # ListaHijos = Cruzamiento(ListaIndividuos,prob_cru,prob_mut,prob_blx,lim_inf,lim_sup)
    # print("Lista Hijos: ",ListaHijos)
    ListaHijosFuncion = []

    for j in range(iteraciones):
        f.write("\n\n ------------------------------------------------------------\n")
        f.write("------------------------- ITERACION: "+str(j)+" ---------------------\n")
        f.write("------------------------------------------------------------")

        # print("\n          -----------------------------------------------------------------------------------\n")
        # print("          ----------------------------------- ITERACION ",j,"---------------------------------\n")
        # print("          -----------------------------------------------------------------------------------\n")
        nro_cruzamientos = int(poblacion)
        ListaHijos = []
        ListaHijosFuncion = []
        for i in range (nro_cruzamientos):
            Hijo1 = Cruzamiento(ListaIndividuos,prob_cruz,prob_mut,prob_blx,lim_inf,lim_sup)
            # print("    Hijo ",i,": ",Hijo1)
            f.write("\n    Hijo "+str(i)+": "+str(Hijo1))
            if(Muta(prob_mut)==True):
                HijoNuevo = Mutando(Hijo1)
                # print("      De ",Hijo1," a ",HijoNuevo)
                f.write("\n      De "+str(Hijo1)+" a "+str(HijoNuevo))
                Hijo1 = HijoNuevo
            ListaHijos.append(Hijo1)
            ListaHijosFuncion.append(round(funcion(Hijo1[0],Hijo1[1],Hijo1[2],Hijo1[3],Hijo1[4]),4))

        ListaIndividuos = ListaIndividuos + ListaHijos
        ListaFuncion = ListaFuncion + ListaHijosFuncion
        # print("\n\nTotal de individuos nro ",j,": ",ListaIndividuos)
        f.write("\n\nTotal de individuos nro "+str(j)+": "+str(ListaIndividuos))
        # print("Lista total de funciones objetivo: ",ListaFuncion)
        f.write("\nLista total de funciones objetivo: "+str(ListaFuncion))

        # ------------------- Nueva Poblacion ----------------------#
        ListaIndividuos,ListaFuncion = NuevaPoblacion(ListaIndividuos,ListaFuncion,poblacion)
        print("\n\nNueva poblacion nro ",j,": ",ListaIndividuos)
        f.write("\n\nNueva poblacion nro "+str(j)+": "+str(ListaIndividuos))
        print("Nueva Lista de Funciones Objetivo: ",ListaFuncion)
        f.write("\nNueva Lista de Funciones Objetivo: "+str(ListaFuncion))

Main()











#
