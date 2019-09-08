import random
import math
import os
import matplotlib.pyplot as pl
import numpy as np

# --------------- Variables globales -----------#

os.remove("Lab04.txt")
f = open ("Lab04.txt", "a")

iteraciones = 0
poblacion = 0
limx =5
limy =3

# ---------- Ingresar número de la poblacion y variables ------#
def Entradas():
    f.write("\n ----------------------- DATOS ------------------ \n\n")
    poblacion= int(input("Ingrese el número de la poblacion: "))
    f.write("Tamaño de la poblacion: "+str(poblacion)+"\n")

    iteraciones = int(input("Ingrese el número de iteraciones: "))
    f.write("Cantidad de iteraciones: "+str(iteraciones)+"\n")

    prob_blx = float(input("Ingrese el alpha del cruzamiento BLX: "))
    f.write("Alpha del cruzamiento BLX: "+str(prob_blx)+"\n")

    prob_mut = int(input("Ingrese la probabilidad de mutacion: "))
    f.write("Probabilidad de mutacion: "+str(prob_mut)+"\n\n")

    return poblacion,iteraciones,prob_mut,prob_blx   #,prob_cru


# ----------------------- Eleccion de Nuevos Individuos ---------------------_#


#------------ Generar la poblacion dada las entradas -----------#
def generarPoblacion(pobla):
    ListaIndividuos = []
    for i in range(pobla):
        par = (random.randint(0,limx),
               random.randint(0,limy))
        while(True):
            if(par in ListaIndividuos):
                par = (random.randint(0,limx),
                       random.randint(0,limy))
            elif((par[1],par[0]) in ListaIndividuos):
                par = (random.randint(0,limx),
                       random.randint(0,limy))
            else:
                break
        # print("Par: ",par)
        ListaIndividuos.append(par)

    # print("\nLista de individuos: ",ListaIndividuos)
    # f.write("\nLista de individuos: "+str(ListaIndividuos)+"\n")

    return ListaIndividuos

# --------------------------- Funciones ----------------------------#
def f1(P1):
    (x,y)=P1
    return round((4*pow(x,2) + 4*pow(y,2)),4)

def f2(P1):
    (x,y) = P1
    return round((pow((x-5),2) + pow((y-5),2)),4)

def F(P1):
    return (f1(P1),f2(P1))

#------------------ Evaluando individuos con funcion de aptitud--------------#
def Evaluar(Lista,poblacion):
    # F1 = []
    # F2 = []
    ListaFunciones = []
    for i in range(poblacion):
        (x,y) = Lista[i]
        # F1.append(f1((x,y)))             #F1 = [2,1,3 ..]
        # F2.append(f2((x,y)))             #F2 =[4,3,2 ..]
        ListaFunciones.append(F((x,y)))  #F = [(2,4),(1,3),(3,2) ..]
    # print("F1: ",F1)
    # print("F2: ",F2)
    return ListaFunciones

# --------------------- Cruzamiento mixtura BLX-alpha --------------------#
def BLX(prob):
    return round(random.uniform(0-prob,1+prob),4)

#---------------------------Cruzamiento --------------------#
def Cruzamiento(Lista,ListaFuncion,Fronteras,prob_blx):

    # print("\n                                       ------------ TORNEO ------------                           \n")
    # f.write("\n\n                         ------------ CRUZAMIENTO BLX ------------                       \n\n")
    # Posiciones de los padres

    print("\n                            ------------ TORNEO ------------                           \n")
    f.write("\n\n                            ------------ TORNEO ------------                           \n")
    P1 = GanaTorneo(Lista,ListaFuncion,Fronteras)
    P2 = GanaTorneo(Lista,ListaFuncion,Fronteras)
    while(P1 == P2):
        P2 = GanaTorneo(Lista,ListaFuncion,Fronteras)

    # P1 = random.randint(0,len(Lista)-1)
    # P2 = random.randint(0,len(Lista)-1)

    print("  \nPADRES: ",P1," y ",P2)
    f.write("  \n\nPADRES: "+str(P1)+" y "+str(P2))

    H1 = Lista[0]
    while( True):
        if(H1 in Lista):

            blx = BLX(prob_blx)
            # print("  BLX: ",blx)
            # f.write("\n  BLX: "+str(blx))

            f.write("\n\n    --- Cruzamiento ---\n")
            print("\n    --- Cruzamiento ---")
            c1 = P1[0]+blx*(P2[0]-P1[0])
            while(c1 < 0 or c1 > limx):
                blx2 = BLX(prob_blx)
                c1 = P1[0]+blx2*(P2[0]-P1[0])

            c2 = P1[1]+blx*(P2[1]-P1[1])
            while(c2 < 0 or c2 > limy):
                blx2 = BLX(prob_blx)
                c2 = P1[1]+blx2*(P2[1]-P1[1])

            H1 = (round(c1,4),round(c2,4))
        else:
            break

    return H1
    # return ListaHijos

# ---------------------------------- Mutación ------------------------------------#
def Mutacion(Hijo):
    elegido = random.randint(0,1)

    if(elegido == 0):
        newC = round(random.uniform(0,5),4)
        lst = list(Hijo)
        lst[elegido] = newC
        Hijo = tuple(lst)
    if(elegido == 1):
        newC = round(random.uniform(0,3),4)
        lst = list(Hijo)
        lst[elegido] = newC
        Hijo = tuple(lst)
    # Hijo[elegido] = newC

    return Hijo

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

# ----------------------------- Fronteras -----------------------------#
def Fronteras(ListaFunciones):

    Lista = ListaFunciones.copy()
    TotalFronteras = []

    while(len(Lista)!=0):
        Frontera = []
        for i in range(len(Lista)):
            temp = Lista[i]
            cont = 0
            for j in range(len(Lista)):
                # if( (temp[0] == Lista[j][0]) and temp[1] == Lista[j][1] ):   #Admite pares que ya estan en la lista
                #     cont = cont +1                                          #Admite pares que ya estan en la lista
                if( (temp[0] < Lista[j][0]) or temp[1] < Lista[j][1] ):
                    # print("es: ",temp[0]," menor que ",Lista[j][0]," o ",)
                    cont = cont + 1
            if(cont == len(Lista)-1 ): # -1 # Si dejamos de admitir repetidoss
                Frontera.append(temp)
            # print("cont: ",cont)
        Frontera.sort()                            #Frontera esta ordenada en x
        TotalFronteras.append(Frontera)

        for k in range(len(Frontera)):
            if(Frontera[k] in Lista):
                Lista.remove(Frontera[k])

    # TotalFronteras.sort()
    # TotalFronteras.sort(reverse=True)
    return TotalFronteras

# --------------- Devolver lista con cada integrante de una frontera y su perimetro -----------------#
def HallarPerimetro(Frontera):

    perimetro = []
    perimetro.append((1000,Frontera[0]))

    for i in range(1,len(Frontera)-1):
        (x1,y1) = Frontera[i-1]
        (x2,y2) = Frontera[i+1]
        sum = round((abs(y2-y1)*2 + abs(x2-x1)*2),4)
        # print("Frontera: ",Frontera[i]," con: ",sum)
        perimetro.append((sum,Frontera[i]))

    perimetro.append((1000,Frontera[len(Frontera)-1]))

    return perimetro

def HallarPromPerimetro(Frontera):

    perimetro = []
    # perimetro.append((1000,Frontera[0]))
    for i in range(1,len(Frontera)-1):
        (x1,y1) = Frontera[i-1]
        (x2,y2) = Frontera[i+1]
        suma = round((abs(y2-y1)*2 + abs(x2-x1)*2),4)
        # print("Frontera: ",Frontera[i]," con: ",suma)
        perimetro.append(suma)

    Promedio = sum(perimetro)*1.0/(len(perimetro)+2)
    # perimetro.append((1000,Frontera[len(Frontera)-1]))
    return Promedio


# Le busca al par (f1,f2) su coordenada (x,y) y devuelve una lista de ellos
def DevolverIndividuos(ListaIndividuos,ListaFuncion):
    ListaNuevaIndividuos = []
    for i in range(len(ListaIndividuos)):
        for j in range(len(ListaFuncion)):
            if(F(ListaIndividuos[i]) == ListaFuncion[j]):
                ListaNuevaIndividuos.append(ListaIndividuos[i])
                break
    return ListaNuevaIndividuos


def NuevaPoblacion(ListaIndividuos,Fronteras,poblacion):

    ix = 0
    cont = 0
    nuevaPoblacion = []
    nFaltan = poblacion - len(nuevaPoblacion)

    while(cont < poblacion):

        if( len(Fronteras[ix]) <= nFaltan ):
            for i in range(len(Fronteras[ix])):
                nuevaPoblacion.append(Fronteras[ix][i])
            nFaltan = poblacion - len(nuevaPoblacion)
            cont = cont + len(Fronteras[ix])
        else:
            nFaltan = poblacion - len(nuevaPoblacion)
            Nuevos = HallarPerimetro(Fronteras[ix])
            Nuevos.sort(reverse=True)                      #Seleccionamos los de mayor perimetro
            # print("PERIMETROS: ",Nuevos)
            p, indv = zip(*Nuevos)
            indiv = list(indv)[:nFaltan]                   #Seleccionamos los n mayores que necesitamos
            nuevaPoblacion = nuevaPoblacion + indiv
            cont = cont + nFaltan

        ix = ix + 1

    # print("nuevaPoblacion: ",nuevaPoblacion)
    nuevaPoblacion = DevolverIndividuos(ListaIndividuos,nuevaPoblacion)
    # print("nuevaPoblacion _ (xy): ",nuevaPoblacion)
    return nuevaPoblacion


#El primer punto en la frontera si se mantiene, pero el ultimo punto no se mantiene, buscar


# ---------- Funcion para elegir posibles padres para el torneo ----------#
def Elegir(Lista):
    tamano = len(Lista)-1
    # print("tamano: ",tamano)
    temp_pob = random.randint(0,tamano)
    temp_pob2 = random.randint(0,tamano)

    while(temp_pob == temp_pob2):
        temp_pob2 = random.randint(0,tamano)
    # print("Poblador 1 elegido temporal: ",Lista[temp_pob])
    # print("Poblador 2 elegido temporal: ",Lista[temp_pob2])

    return temp_pob,temp_pob2

def Domina_a(Par1,Par2):

    if(Par2[0]>= Par1[0] and Par2[1]>=Par1[1]):
        return True
    else:
        return False

def GanaTorneo(Lista,ListaFuncion,Fronteras):

    # Puntuaciones=[]
    # print("Len: ",len(Lista))
    t1,t2 = Elegir(Lista)           #Devuelve las posiciones de los posibles padres

    print("\nPosibles padres: ",Lista[t1],",",Lista[t2])        #(x,y) ,(w,z)
    f.write("\n\nPosibles padres: "+str(Lista[t1])+","+str(Lista[t2]))

    #Hallando dominancia:
    F1 = F(Lista[t1])
    F2 = F(Lista[t2])
    if(Domina_a( F1, F2)):
        print(F1," domina a ",F2)
        f.write("\n"+str(F1)+" domina a "+str(F2))
        return Lista[t1]
    elif(Domina_a(F2,F1)):
        f.write("\n"+str(F2)+" domina a "+str(F1))
        print(F2," domina a ",F1)
        return Lista[t2]
    else:
        #Si ninguno domina a otro, entonces hallar el que sea más disperso
        Front = []
        Front2 = []
        ix1 = 0
        ix2 = 0

        # print("Fronteras: ",Fronteras)
        # print("F1: ",F1)
        # print("F2: ",F2)
        for i in range(len(Fronteras)):
            if (F1 in Fronteras[i]):
                # print("encontro primera frontera")
                Front = Fronteras[i]
                ix1 = i
            if(F2 in Fronteras[i]):
                # print("encontro segunda frontera")
                Front2 = Fronteras[i]
                ix2 = i
            elif(len(Front)>0 and len(Front2)>0):  #Si ya encontro ambas fronteras terminar busqueda
                break

        sum1 = sum2 = -1
        # Si los elementos pertenecen a distinta frontera se elige el que esta en la
        # frontera más a la izquierda (ya que queremos minimizar)
        if(ix1 <ix2):
            f.write("\nEsta en la frontera mas a la izquierda: "+str(Lista[t1])+" con "+str(F1))
            print("Esta en la frontera mas a la izquierda: ",Lista[t1]," con ",F1)
            return Lista[t1]

        elif(ix2 < ix1):
            f.write("\nEsta en la frontera mas a la izquierda: "+str(Lista[t2])+" con "+str(F2))
            print("Esta en la frontera mas a la izquierda: ",Lista[t2]," con ",F2)
            return Lista[t2]

        #Si pertenecen a la misma frontera, se halla su dispersion y elegimos al de mayor perimetro
        elif(ix1==ix2):
            # print("Front: ",Front)
            perimetro = HallarPerimetro(Front)
            for j in range(len(perimetro)):           #Buscar en la lista de Perimetros [(sum,Par),...]
                (sum,Par) = perimetro[j]
                if(Par == F1):
                    sum1 = sum
                elif(Par == F2):
                    sum2 = sum
                if(sum1!=-1 and sum2!=-1):  #Si ya encontro las dos sumas
                    break;

            if(sum2 > sum1):
                f.write("\n"+str(F2)+" de "+str(Lista[t2])+" tiene mas distancia con: "+str(sum2)+" > "+str(sum1))
                print(F2," de ",Lista[t2]," tiene mas distancia con: ",sum2," > ",sum1)
                return Lista[t2]
            elif(sum1 > sum2):
                f.write("\n"+str(F1)+" de "+str(Lista[t1])+" tiene mas distancia con: "+str(sum1)+" > "+str(sum2))
                print(F1," de ",Lista[t1]," tiene mas distancia con: ",sum1," > ",sum2)
                return Lista[t1]
            else:
                #Si son de igual dispersion se toma uno al azar
                print("Se elige random")
                f.write("\nSe elige random")
                ran = random.randint(0,1)
                if( ran ==0): return Lista[t1]
                elif(ran ==1): return Lista[t2]

# ------------------------Proceso completo -------------------------#
def Main():
    poblacion,iteraciones,prob_mut,prob_blx = Entradas()

    ListaIndividuos = generarPoblacion(poblacion)
    f.write("\n ---------------- Generando Población Inicial ------------- ")
    print("\nLista de poblacion: ",ListaIndividuos)
    f.write("\nLista de poblacion: "+str(ListaIndividuos)+"\n")

    f.write("\n----------------- Evaluando Individuos -------------------")
    ListaFuncion = Evaluar(ListaIndividuos,poblacion)
    f.write("\nLista Funcion: "+str(ListaFuncion)+"\n")
    print("Lista Funcion: ",ListaFuncion)

    #Graficar
    x,y = zip(*ListaFuncion)
    pl.scatter(x, y)
    pl.savefig("Images/fig_"+"0"+".png")
    pl.clf()
    # pl.show()

    f.write(" ----------------- Fronteras -------------------")
    ListaFronteras = Fronteras(ListaFuncion)
    f.write("\nLista de fronteras: "+str(ListaFronteras)+"\n")
    print("Lista de fronteras: ",ListaFronteras)

    # Prom = 1000

    for j in range(iteraciones):

        f.write("\n\n ------------------------------------------------------------\n")
        f.write("------------------------- ITERACION: "+str(j)+" ---------------------\n")
        f.write("------------------------------------------------------------")

        print("\n      -----------------------------------------------------------------------------------\n")
        print("      ----------------------------------- ITERACION ",j,"---------------------------------\n")
        print("      -----------------------------------------------------------------------------------")

        nro_cruzamientos = int(poblacion)
        ListaHijos = []
        ListaHijosFuncion = []
        # ListaHijosFuncion2 = []
        for i in range (nro_cruzamientos):

            hijo1 = Cruzamiento(ListaIndividuos,ListaFuncion,ListaFronteras,prob_blx)

            while( True):
                if(hijo1 in ListaHijos):
                    hijo1 = Cruzamiento(ListaIndividuos,ListaFuncion,ListaFronteras,prob_blx)
                else:
                    break

            f.write("\n    Hijo: "+str(hijo1))
            print("    Hijo: ",hijo1)

            if(Muta(prob_mut)==True):
                HijoNuevo = Mutacion(hijo1)
                while( True):
                    if((HijoNuevo in ListaIndividuos) or (HijoNuevo in ListaHijos)):
                        HijoNuevo = Mutacion(hijo1)
                    else:
                        break

                print("      De ",hijo1," a ",HijoNuevo)
                f.write("\n      De "+str(hijo1)+" a "+str(HijoNuevo))
                hijo1 = HijoNuevo

            ListaHijos.append(hijo1)
            ListaHijosFuncion.append(F(hijo1))

        ListaIndividuos = ListaIndividuos + ListaHijos
        ListaFuncion = ListaFuncion + ListaHijosFuncion

        # print("Lista de Individuos: ",ListaIndividuos)
        # points = [(1,4),(4,2),(5,1),(3,4),(2,2),(2,6),(5,5),(1,2)]
        # points = [(2,6),(3,4),(4,3),(4,6),(5,4),(6,2),(7,3),(8,1),(9,2)]
        # Lista = [(2,6),(3,4),(4,3),(4,6),(5,4),(6,2),(7,3),(8,1),(9,2)]
        fronteras = Fronteras(ListaFuncion)
        # print("FRONTERAS: ",fronteras)
        # fronteras = Fronteras(Lista)

        f.write("\n\n                ---------------- NUEVA POBLACION ------------- \n")
        print("\n                      ---------------- NUEVA POBLACION ------------- \n")
        # print("Nueva: ",nueva)
        # print("ListaIndividuos ",j,": ",ListaIndividuos)
        ListaIndividuos = NuevaPoblacion(ListaIndividuos,fronteras,poblacion)
        print("Nueva poblacion nro ",j,": ",ListaIndividuos)
        f.write("\nNueva poblacion nro "+str(j)+": "+str(ListaIndividuos))

        # ListaFuncion1,ListaFuncion2 = NuevaListaFuncion(ListaIndividuos)
        print("\n----------------- Funcion -------------------")
        f.write("\n\n----------------- Funcion -------------------")
        ListaFuncion = Evaluar(ListaIndividuos,poblacion)
        f.write("\nNueva Lista (F1,F2): "+str(ListaFuncion))
        print("Nueva Lista (F1,F2): ",ListaFuncion)

        print("\n----------------- Fronteras -------------------")
        f.write("\n\n----------------- Fronteras -------------------")
        ListaFronteras = Fronteras(ListaFuncion)
        f.write("\nLista de fronteras: "+str(ListaFronteras)+"\n")
        print("Lista de fronteras: ",ListaFronteras)

        j = j+1

        x,y = zip(*ListaFuncion)
        pl.scatter(x, y)
        pl.savefig("Images/fig_"+str(j)+".png")
        pl.clf()
        # pl.show()

        # plt.scatter(x, y)
        # plt.savefig("ImagesC/fig_"+"0"+".png")
        # plt.clear()

        # points = [(2,6),(2,4),(4,3),(4,6),(5,4),(6,5),(6,2),(7,3),(8,1),(8,5),(9,2),(9,5)]
        # fronteras = Fronteras(points)
        # print("Fronteras: ",fronteras)
        # lista = NuevaPoblacion(fronteras,9)
        # print("Lista: ",lista)
        # points= [(0, 0), (0.0, 0.0002), (0.003, 0.0), (0.0, 0.0037), (0.0032, 0.0002), (0.0237, 0.0), (0.0, 0.0051), (0.0138, 0.0048), (0.018, 0.0003), (0.0239, 0.0), (0.0, 0.009), (0.0013, 0.0052), (0.0274, 0.0017), (0.0277, 0.0001), (0.0463, 0.0), (0.0227, 0.0003), (0.001, 0.0034), (0.0219, 0.0004), (0.0, 0.005), (0.0239, 0.0), (0.0, 0.005), (0.0032, 0.0078), (0.019, 0.0003), (0.0102, 0.0003), (0.0, 0.0025), (0.0, 0.0031), (0.0285, 0.0055), (3.7358, 0.0052), (0.0009, 0.0002), (0.0006, 0.0065)]
        # x,y = zip(*points)
        # pl.scatter(x,y)
        # pl.show()
        # print("FRONTERAS: ",fronteras)
        # padre = GanaTorneo(points,fronteras)
        # print("Padre: ",padre)

Main()
