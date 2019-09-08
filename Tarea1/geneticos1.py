from random import randint, uniform,random
import math
import os

# --------------- Variables globales -----------#

os.remove("respuesta1.txt")
f = open ("respuesta1.txt", "a")


iteraciones = 0
cromosomas=0
poblacion=0
probMutacion = 0.05
probCruzamiento = 0.9
cruzamiento = 3

ListaBin  = []
ListaDec  = []
ListaProb = []
ListaHijos= []
ListaDecHijos = []
ListaProbHijos = []

# ---------- Ingresar número de la poblacion y cromosomas ------#
def Entradas():
    f.write("\n ----------------------- DATOS ------------------ \n\n")
    poblacion= int(input("Ingrese el número de la poblacion: "))
    f.write("Tamaño de la poblacion: "+str(poblacion)+"\n")
    cromosomas = int(input("Ingrese el número de cromosomas: "))
    f.write("Tamaño de los cromosomas: "+str(cromosomas)+"\n")
    iteraciones = int(input("Ingrese el número de iteraciones: "))
    f.write("Cantidad de iteraciones: "+str(iteraciones)+"\n")
    punto = int(input("Cruzamiento de un punto - punto: "))
    f.write("Cruzamiento de un punto - punto: "+str(punto)+"\n")
    prob_mut = int(input("Ingrese la probabilidad de mutacion: "))
    f.write("Probabilidad de mutacion: "+str(prob_mut)+"\n")
    prob_cru = int(input("Ingrese la probabilidad de Cruzamiento: "))
    f.write("Probabilidad de cruzamiento: "+str(prob_cru)+"\n\n")
    return poblacion,cromosomas,iteraciones,punto,prob_mut,prob_cru

#------------ Generar la poblacion dada las entradas -----------#
def generarPoblacion(cromo,pobla):
    for i in range(pobla):
        indiv = ""
        for j in range(cromo):
            indiv = indiv+str(randint(0,1))
            # print(indiv)
        ListaBin.append(indiv)
    return ListaBin

#------------------------- Imprimir --------------------------#
def Imprimir(Lista):
    print(Lista)

#----------------------- Funcion de aptitud -------------------#
def funcion(num):
    return num*num - 6*num + 1
    # return num+1

#----------------- Normalizar en caso de negativos --------------#
def Normalizar(Lista):
    menor = min(Lista)
    if(menor < 0):
        for i in range(len(Lista)):
            Lista[i] = Lista[i] + (-1)*menor
    return Lista

#---------- Evaluando individuos con funcion de aptitud---------#
def Evaluar(pobla,Lista):
    Lista2=[]
    for i in range(pobla):
        Lista2.append(funcion(int(Lista[i],2)))
    # print("antigua lista: ",ListaDec)
    # Normalizar(Lista2)
    return Lista2

#--------------- Hallar probabilidad de cada poblador ----------#
def Probabilidades(Lista):
    # Total = sumalista(Lista)
    Lista2 = []
    Total = sum(Lista)
    for i in range(len(Lista)):
        prob = (100*Lista[i])/(Total)
        Lista2.append(prob)
    return Lista2
    # print("Suma de prob: ",sum( ListaProb))

# ---------- Funcion para elegir un padre dada una probabilidad ----------#
def Elegir(Lista,prob):
    i = 0
    var = Lista[i]
    # while ((prob >= var) and (i<len(Lista))):
    #     i = i + 1
    #     # print(i)
    #     var = Lista[i] + var
    while(True):
        if((prob > var) and (i+1<len(Lista))):
            i=i+1
            # print("i:",i)
            var = Lista[i] + var
            # continue
        else:
            break
    # print("Ui:",i)
    return i

# ------------------ Seleccionar un padre y madre -----------------#
def Seleccion(ListaProb):
    # num = randint(0,100)
    num = uniform(0,100)
    print("Primer random: ",num)
    f.write("\n\nPrimer random: "+ str(num)+"\n")
    Madre = Elegir(ListaProb,num)

    # num = randint(0,100)
    num = uniform(0,100)
    print("Segundo random:",num)
    f.write("Segundo random: "+ str(num)+"\n")
    Padre = Elegir(ListaProb,num)
    return Madre,Padre

# ----------------------- Muta? ----------------------------#
def Muta(binario,prob):
    num = randint(1,100)
    if(num<=prob):
        return True
    else:
        return False

# ----------------------- Se cruzan? ----------------------------#
def Cruza(prob):
    num = randint(1,100)
    if(num<=prob):
        return True
    else:
        return False

# -----------------------Mutando ----------------------------#
def Mutando(binario):
    var=""
    pos = randint(0,len(binario)-1)
    for i in range(len(binario)):
        if(i!=pos):
            var = var+binario[i]
        else:
            if(binario[i]=='1'):
                var = var+'0'
            elif(binario[i]=='0'):
                var = var+'1'
    return var

# ---------------------- Cruzamiento de padre y madre --------------#
def Cruzamiento(ListaBin,pos,Madre,Padre,prob,prob_cru):
    Mom = ListaBin[Madre]
    Dad = ListaBin[Padre]
    print("\nMadre: ",Mom)
    f.write("\nMadre: "+str(Mom)+"\n")
    print("Padre: ",Dad)
    f.write("Padre: "+str(Dad)+"\n")

    if(Cruza(prob_cru)==True):
        Nuevo1 = Mom[:pos+1] + Dad[pos+1:]
        Nuevo2 = Dad[:pos+1] + Mom[pos+1:]

        f.write("\nCruzamiento")

        f.write("\nHijo 1: "+Nuevo1)
        if(Muta(Nuevo1,prob)==True):
            print("Muto de: ",Nuevo1)
            Nuevo1 = Mutando(Nuevo1)
            print("     a : ",Nuevo1)
            f.write("\n   Mutó a "+Nuevo1)

        f.write("\nHijo 2: "+Nuevo2)
        if(Muta(Nuevo2,prob)==True):
            print("Muto de: ",Nuevo2)
            Nuevo2 = Mutando(Nuevo2)
            print("     a : ",Nuevo2)
            f.write("\n   Mutó a "+Nuevo2)

        ListaHijos.append(Nuevo1)
        ListaHijos.append(Nuevo2)

        return Nuevo1,Nuevo2,True

    else:
        f.write("\nNo se cruzaron")
        print("No se cruzaron")
        return "-1","-1",False


# ---------------------- Nueva Poblacion ---------------------------#
def NuevaPoblacion(nro,Lista):
    veces= len(Lista)-nro
    for i in range(veces):
        i_minimo = Lista.index(min(Lista))
        Lista.pop(i_minimo)

# ------------------------Proceso completo -------------------------#
def Main():
    poblacion,cromosomas,iteraciones,punto,prob_mut,prob_cru = Entradas()
    ListaBin = generarPoblacion(cromosomas,poblacion)
    f.write(" ---------------- Generando Población Inicial ------------- \n")

    f.write("Lista de poblacion: "+str(ListaBin)+"\n"+"\n")
    print("Lista de poblacion: ",ListaBin)

    # f.write("ITERACION: 0\n\n")
    f.write(" ----------------- Evaluando Individuos -------------------\n")
    ListaDec = Evaluar(len(ListaBin),ListaBin)
    f.write("Lista decimales sin normalizar: "+str(ListaDec)+"\n")
    print("Lista decimales sin normalizar: ",ListaDec)
    ListaDec = Normalizar(ListaDec)
    f.write("Lista decimales normalizada: "+str(ListaDec)+"\n")
    print("Lista decimales normalizada: ",ListaDec)

    f.write("\n ------ Selección de individuos - Método de la Ruleta --------\n")
    ListaProb = Probabilidades(ListaDec)
    f.write("Lista de probabilidades: "+str(ListaProb)+"\n")
    print("Lista de probabilidad: ",ListaProb)

    for i in range(iteraciones):
        f.write("\n\n ------------------------------------------------------------\n")
        f.write("------------------------- ITERACION: "+str(i)+" ---------------------\n")
        f.write("------------------------------------------------------------")
        nro_cruzamientos = int(poblacion/2)
        ListaHijos = []
        for i in range (nro_cruzamientos):
            Madre,Padre = Seleccion(ListaProb)
            print("Madre: ",Madre)
            print("Padre: ",Padre)
            Hijo1,Hijo2,se_cruzo=Cruzamiento(ListaBin,punto,Madre,Padre,prob_mut,prob_cru)
            if(se_cruzo == True):
                print("Hijo 1: ",Hijo1)
                print("Hijo 2: ",Hijo2)
                ListaHijos.append(Hijo1)
                ListaHijos.append(Hijo2)
            # ListaBin.append(Hijo1,Hijo2)

        print("Lista de hijos: ",ListaHijos)
        ListaDecHijos = Evaluar(len(ListaHijos),ListaHijos)
        print("Lista decimales de hijos: ",ListaDecHijos)
        # ListaProbHijos = Probabilidades(ListaDecHijos)
        # print("Lista Probabilidades de hijos: ",ListaProbHijos)


        ListaBin = ListaBin + ListaHijos

        f.write("\n\n-------------- Seleccion de la siguiente poblacion: --------------\n")
        f.write("Lista total resultante: "+str(ListaBin))
        print("Lista total: ",ListaBin)

        ListaDec = ListaDec + ListaDecHijos
        f.write("\nLista decimal total sin normalizar: "+str(ListaDec))
        print("Lista decimal total sin normalizar: ",ListaDec)

        ListaDec = Normalizar(ListaDec)
        f.write("\nLista decimal total normalizada: "+str(ListaDec))
        print("Lista decimal total normalizada: ",ListaDec)
        # ListaProb = Probabilidades(ListaDec)
        # print("Lista de probabilidades total: ",ListaProb)

        # --------- Seleccion de siguiente poblacion -------------#
        f.write("\n\n ---------------------- Nueva poblacion: ------------------------\n")
        # nro_sig_pob = int(len(ListaBin)/2)
        nro_sig_pob = poblacion
        NuevaPoblacion(nro_sig_pob,ListaBin)
        f.write("\nLista Nueva poblacion: "+str(ListaBin))
        print("Lista nueva total: ",ListaBin)
        ListaDec = Evaluar(len(ListaBin),ListaBin)
        f.write("\nLista Nueva poblacion decimal sin normalizar: "+str(ListaDec))
        print("Lista decimales sin normalizar: ",ListaDec)
        ListaDec = Normalizar(ListaDec)
        f.write("\nLista Nueva poblacion decimal normalizada: "+str(ListaDec))
        print("Lista decimales normalizada: ",ListaDec)
        ListaProb = Probabilidades(ListaDec)
        f.write("\nLista de la nueva poblacion probabilidad: "+str(ListaProb))
        print("Lista de probabilidad: ",ListaProb)

    f.close()


Main()

    # Evaluar(poblacion,ListaHijos)


# poblacion,cromosomas = Entradas()
# generarPoblacion(cromosomas,poblacion)
# Imprimir(ListaBin)
# Evaluar(poblacion,ListaBin)
# Imprimir(ListaDec)
# Probabilidades(ListaDec)
# Imprimir(ListaProb)
# Madre,Padre = Seleccion(ListaProb)
# # print(Seleccion(ListaProb))
# Cruzamiento(ListaBin,2,Madre,Padre)
# Imprimir(ListaHijos)
