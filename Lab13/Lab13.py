import random
import math
import os
import numpy as np
import pandas as pd
import sys
import copy

orig_stdout = sys.stdout
f = open('Lab13.txt', 'w')
sys.stdout = f

def F(x_1,x_2):
    res = x_1*math.sin(4*math.pi*x_1) - x_2*math.sin(4*math.pi*x_2 + math.pi) + 1
    return round(res,6)

def fit(func):
    if(func >= 0):
        return round(1/(1/(1+func)),6)
        # return round((1/(1+func)),6)
    else:
        return round(1/(1+abs(func)),6)
        # return round(1+abs(func),6)

# Tamaño de la colmena (CS),
# Máximo número de ciclos o veces que se ejecutara el algoritmo (MCN),
# Número de Soluciones (SN),
# Dimensión del problema (D), y
# Límite calculado como L = (CS*D)/2.

class Fuente:
    def __init__(self):
        self.par = []
        self.funcion = -9999
        self.fitness = -9999
        self.cont = 0
        self.prob_i = 0
        self.prob_acum = 0

class Candidata:
    def __init__(self):
        self.v = []
        self.funcion = 0
        self.fitness = 0
        self.cont = 0
        self.K = -1
        self.J = -1
        self.phi = -1

class AlgoritmoABC:
    def __init__(self):
        self.SN = int(input("Ingrese el número de soluciones: "))
        print(self.SN)
        self.MCN = int(input("Ingrese el número de ciclos máximo: "))
        print(self.MCN)
        self.CS = 6    #Tamaño de la colmena
        self.D = 2  #Dimension
        self.L = (self.CS*self.D)/2  #Límite
        self.lim_inf = -1
        self.lim_sup = 2
        self.mejor_fuente = Fuente()
        self.mayor_fun = self.mejor_fuente.funcion
        self.K = random.randint(1,self.SN)   # k != i
        self.J = random.randint(1,self.D)
        self.phi = random.uniform(-1,1)
        self.ListaFuentes = []
        self.ListaCandidatas = []

    def generarPoblacion(self):
        for i in range(self.SN):
            fuente = Fuente()
            fuente.par.append(round(random.uniform(self.lim_inf,self.lim_sup),6))
            fuente.par.append(round(random.uniform(self.lim_inf,self.lim_sup),6))
            fuente.funcion = F(fuente.par[0],fuente.par[1])
            fuente.fitness = fit(fuente.funcion)
            self.ListaFuentes.append(fuente)

    def printLista(self):
        print("-----------------------------------------------------------------------")
        print("| FUENTE |      x1     |     x2     |    F(xi)    |    Fit_i   | cont |")
        print(" ----------------------------------------------------------------------")
        for i in range(self.SN):
            print("|   ",i+1,"  | ",self.ListaFuentes[i].par[0]," | ",self.ListaFuentes[i].par[1] ," |  ",self.ListaFuentes[i].funcion ," | ",self.ListaFuentes[i].fitness," |  ",self.ListaFuentes[i].cont,"  |")
        print(" ----------------------------------------------------------------------")

    def printMejores(self):
        print(" ------------------------------------------------------------------------------------------------")
        print("| FUENTE |      x1     |     x2     |    F(xi)    |    Fit_i   |   prob_i   |  prob_acum  | cont |")
        print(" -----------------------------------------------------------------------------------------------")
        for i in range(self.SN):
            print("|   ",i+1,"  | ",self.ListaFuentes[i].par[0]," | ",self.ListaFuentes[i].par[1] ," |  ",self.ListaFuentes[i].funcion ," | ",self.ListaFuentes[i].fitness," |  ",self.ListaFuentes[i].prob_i ," | ",self.ListaFuentes[i].prob_acum," |  ",self.ListaFuentes[i].cont,"  |")
        print(" -----------------------------------------------------------------------------------------------")

    def printCandidatas(self):
        print("--------------------------------------------------------------------------------------")
        print("| i | k | j |     phi     |     v1     |     v2     |    F(xi)    |    Fit_i   | cont |")
        print(" -------------------------------------------------------------------------------------")
        for i in range(self.SN):
            print("|",i+1,"|",self.ListaCandidatas[i].K,"|",self.ListaCandidatas[i].J,"| ",self.ListaCandidatas[i].phi," | ",self.ListaCandidatas[i].v[0]," | ",self.ListaCandidatas[i].v[1] ," |  ",self.ListaCandidatas[i].funcion ," | ",self.ListaCandidatas[i].fitness," | ",self.ListaCandidatas[i].cont," |")
        print(" -------------------------------------------------------------------------------------")

    def SolucionesCandidatas(self):
        self.ListaCandidatas = []
        for i in range(self.SN):
            candidata = Candidata()

            self.J = random.randint(1,self.D) -1
            self.K = random.randint(1,self.SN) -1   # k != i
            self.phi = round(random.uniform(-1,1),6)
            while(self.K == i):
                self.K = random.randint(1,self.SN) -1   # k != i

            if(self.J == 0):
                v_2 = self.ListaFuentes[i].par[1]
                v_1 = round(self.ListaFuentes[i].par[self.J] + self.phi*(self.ListaFuentes[i].par[self.J] - self.ListaFuentes[self.K].par[self.J]),6)
                if(v_1 < self.lim_inf or v_1 > self.lim_sup):
                    v_1 = round(random.uniform(self.lim_inf,self.lim_sup),6)
            elif(self.J == 1):
                v_1 = self.ListaFuentes[i].par[0]
                v_2 = round(self.ListaFuentes[i].par[self.J] + self.phi*(self.ListaFuentes[i].par[self.J] - self.ListaFuentes[self.K].par[self.J]),6)
                if(v_2 < self.lim_inf or v_2 > self.lim_sup):
                    v_2 = round(random.uniform(self.lim_inf,self.lim_sup),6)

            candidata.v.append(v_1)
            candidata.v.append(v_2)
            candidata.K = self.K +1
            candidata.J = self.J +1
            candidata.phi = self.phi
            candidata.funcion = F(candidata.v[0],candidata.v[1])
            candidata.fitness = fit(candidata.funcion)

            if(candidata.fitness > self.ListaFuentes[i].fitness):
                candidata.cont = 0
            else:
                candidata.cont = self.ListaFuentes[i].cont + 1

            self.ListaCandidatas.append(candidata)

    def mejoresSoluciones(self):

        for i in range(self.SN):
            if(self.ListaCandidatas[i].cont == 0):
                self.ListaFuentes[i].par[0] = self.ListaCandidatas[i].v[0]
                self.ListaFuentes[i].par[1] = self.ListaCandidatas[i].v[1]
                self.ListaFuentes[i].funcion = self.ListaCandidatas[i].funcion
                self.ListaFuentes[i].fitness = self.ListaCandidatas[i].fitness
                self.ListaFuentes[i].cont = 0
            else:
                self.ListaFuentes[i].cont += 1

    def hallarProbabilidades(self):

        acum = 0
        for i in range(self.SN):
            acum += self.ListaFuentes[i].fitness
        prob_acum = 0
        for i in range(self.SN):
            self.ListaFuentes[i].prob_i = round((self.ListaFuentes[i].fitness/acum),6)
            prob_acum += self.ListaFuentes[i].prob_i
            self.ListaFuentes[i].prob_acum = round(prob_acum,6)

    def reemplazarFuenteAgotada(self):
        bool = False
        for j in range(self.SN):
            if(self.ListaFuentes[j].cont > self.L):
                print("\n ----------------------------------- REEMPLAZANDO ", j+1,"---------------------------------------\n")
                self.ListaFuentes[j].par[0] = round(self.lim_inf + random.uniform(0,1)*(self.lim_sup-self.lim_inf),6)
                self.ListaFuentes[j].par[1] = round(self.lim_inf + random.uniform(0,1)*(self.lim_sup-self.lim_inf),6)
                self.ListaFuentes[j].funcion = F(self.ListaFuentes[j].par[0],self.ListaFuentes[j].par[1])
                self.ListaFuentes[j].fitness = fit(self.ListaFuentes[j].funcion)
                self.ListaFuentes[j].cont = 0
                bool = True

        if(bool ==True):
            self.hallarProbabilidades()
            self.printMejores()

    def Mejor(self):
        ListaF = copy.deepcopy(self.ListaFuentes)
        for j in range(self.SN):
            if(self.mayor_fun < ListaF[j].funcion):
                self.mayor_fun = ListaF[j].funcion
                self.mejor_fuente = ListaF[j]

        print("\n La mejor Fuente es: ",self.mejor_fuente.par[0]," , ",self.mejor_fuente.par[1]," con fitness de: ",self.mejor_fuente.fitness, " y valor de: ",self.mejor_fuente.funcion)

    def SolucionesObservadoras(self):

        for k in range(self.SN):
            print("\n %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBSERVADORA ", k+1," %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
            self.J = random.randint(1,self.D) -1
            self.phi = round(random.uniform(-1,1),6)
            num_aleatorio = random.uniform(0,1)
            i = 0
            for j in range(self.SN):
                if(self.ListaFuentes[j].prob_acum < num_aleatorio):
                    i = j+1    # i tiene la pos de j

            print(" Numero aleatorio: ",num_aleatorio," es menor que: ",self.ListaFuentes[i].prob_acum, " entonces: i=",i+1,"\n")

            self.K = random.randint(1,self.SN) -1   # k != i
            while(self.K == i):
                self.K = random.randint(1,self.SN) -1   # k != i

            print("-----------------------------------------------------------------------")
            print("| FUENTE |      x1     |     x2     |    F(xi)    |    Fit_i   | k | j |")
            print(" ----------------------------------------------------------------------")
            print("|   ",i+1,"   | ",self.ListaFuentes[i].par[0]," | ",self.ListaFuentes[i].par[1] ," |  ",self.ListaFuentes[i].funcion ," | ",self.ListaFuentes[i].fitness," |",self.K+1,"|",self.J+1,"|")
            print("|   ",self.K+1,"   | ",self.ListaFuentes[self.K].par[0]," | ",self.ListaFuentes[self.K].par[1],"|")
            print(" -----------------------------------")

            if(self.J == 0):
                v_2 = self.ListaFuentes[i].par[1]
                v_1 = round(self.ListaFuentes[i].par[self.J] + self.phi*(self.ListaFuentes[i].par[self.J] - self.ListaFuentes[self.K].par[self.J]),6)
                if(v_1 < self.lim_inf or v_1 > self.lim_sup):
                    v_1 = round(random.uniform(self.lim_inf,self.lim_sup),6)
            elif(self.J == 1):
                v_1 = self.ListaFuentes[i].par[0]
                v_2 = round(self.ListaFuentes[i].par[self.J] + self.phi*(self.ListaFuentes[i].par[self.J] - self.ListaFuentes[self.K].par[self.J]),6)
                if(v_2 < self.lim_inf or v_2 > self.lim_sup):
                    v_2 = round(random.uniform(self.lim_inf,self.lim_sup),6)

            funcion = F(v_1,v_2)
            fitness = fit(funcion)

            # Comparar las aptitudes
            if(fitness > self.ListaFuentes[i].fitness):   # Mejora la aptitud
                self.ListaFuentes[i].cont = 0
                self.ListaFuentes[i].par[0] = v_1
                self.ListaFuentes[i].par[1] = v_2
                self.ListaFuentes[i].funcion = funcion
                self.ListaFuentes[i].fitness = fitness
                print("-----------------------------------------------------------------------------------")
                print("|    phi    |     v1     |     v2     |    F(xi)    |    Fit_i   | Mejora? | cont |")
                print(" ---------------------------------------------------------------------------------")
                print("|",self.phi,"| ",v_1," | ",v_2 ," |  ",funcion ," | ",fitness," |    SI    |  ",0,"  |")
                print(" ---------------------------------------------------------------------------------")
            else:                                          # Empeora la aptitud
                self.ListaFuentes[i].cont += 1
                print("----------------------------------------------------------------------------------")
                print("|    phi    |     v1     |     v2     |    F(xi)    |    Fit_i   | Mejora? | cont |")
                print(" ---------------------------------------------------------------------------------")
                print("|",self.phi,"| ",v_1," | ",v_2 ," |  ",funcion ," | ",fitness," |    NO    |  ",self.ListaFuentes[i].cont,"  |")
                print(" ---------------------------------------------------------------------------------")

            self.hallarProbabilidades()
            print("\n -----------------------------------------------------------------------------------------------")
            print("|                                         MEJORES SOLUCIONES                                    |")
            self.printMejores()

            print("   mejor hasta ahora: ",self.mejor_fuente.funcion)
            # Abejas exploradoras reemplazando fuentes de comida agotadas
            self.reemplazarFuenteAgotada()

    def Main(self):
        self.generarPoblacion()
        print("\n-----------------------------------------------------------------------")
        print("|                    FUENTE DE ALIMENTOS INICIALES                     |")
        self.printLista()
        for i in range(self.MCN):
            print("\n    #########################################################################")
            print("\n    ################################ ITERACION "+str(i+1)+"############################  ")
            print("\n    #########################################################################")

            print("\n--------------------------------------------------------------------------------------")
            print("|                                SOLUCIONES CANDIDATAS                                |")
            self.SolucionesCandidatas()   #Abejas obreras (3) = SN
            self.printCandidatas()
            print("\n -----------------------------------------------------------------------------------------------")
            print("|                                         MEJORES SOLUCIONES                                    |")
            self.mejoresSoluciones()   # Se comparana con las soluciones candidatas y se quedan las mejores
            self.hallarProbabilidades()
            self.printMejores()
            self.SolucionesObservadoras()  #Abejas observadoras (3) = SN
            self.Mejor()         # Se actualiza a la mejor fuente de comida

ABC = AlgoritmoABC()
ABC.Main()
