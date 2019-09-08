import random
import math
import os
import numpy as np
import pandas as pd
import sys
import copy

orig_stdout = sys.stdout
f = open('Lab15.txt', 'w')
sys.stdout = f

def F(x1,x2):
    res = -math.cos(x1)*math.cos(x2)*math.exp(-pow((x1-math.pi),2)-pow((x2-math.pi),2))
    return res

# Generaciones = 150 iteraciones
# Population size = 5
# Problem size = 2
# Num clones = 5
# N rand = 2
# Affinity threshold = 0.5
#          (lmax - lmin) *0.05
# Beta = 100

class Celula:
    def __init__(self):
        self.par=[]
        self.afinidad = -999
        self.costo = -999
        self.norm_cost = -999
        self.mutation_rate = -999

class aiNet:
    def __init__(self):
        self.Generaciones = int(input("Ingrese el número de iteraciones: ")) #Stop condition
        print(self.Generaciones)
        self.population = int(input("Ingrese el número de la población: "))
        print(self.population)
        self.problem_size = 2
        self.n_clones = 5
        self.n_rand = 2
        self.affinity_threshold = 1
        self.beta = 100
        self.lim_inf = -10
        self.lim_sup = 10
        self.Lista = []
        self.ListaClonados=[]
        self.ListaAleatoria=[]
        self.prom_costo = 0
        self.mejorCelula = Celula()

    def printL(self,Lis):
        print("\n-----------------------------------------------------------------------------------")
        print("| i |     x1     |     x2     |      Costo     |    Norm cost   |   Afinidad   |")
        print(" ---------------------------------------------------------------------------------")
        for i in range(len(Lis)):
            print("|",i+1,"|",round(Lis[i].par[0],6)," | ",round(Lis[i].par[1],6) ," |  ",Lis[i].costo ," | ",Lis[i].norm_cost," | ",Lis[i].afinidad," |")
        print(" ---------------------------------------------------------------------------------")

    def generarPoblacion(self):
        for i in range(self.population):
            celula = Celula()
            celula.par.append(random.uniform(self.lim_inf,self.lim_sup))
            celula.par.append(random.uniform(self.lim_inf,self.lim_sup))
            celula.costo = F(celula.par[0],celula.par[1])
            self.Lista.append(celula)

    def MaxMin(self):
        max = -999
        min = 999
        for i in range(self.population):
            if( self.Lista[i].costo > max):
                max = self.Lista[i].costo
            if( self.Lista[i].costo < min):
                min = self.Lista[i].costo
        return max,min

    def Costo(self):
        for i in range(self.population):
            self.Lista[i].costo = F(self.Lista[i].par[0],self.Lista[i].par[1])

    def normalizarCosto(self):
        max,min = self.MaxMin()
        for i in range(self.population):
            # self.Lista[i].norm_cost = 1 - (self.Lista[i].costo/(max-min))
            self.Lista[i].norm_cost = ((self.Lista[i].costo - min)/(max-min))

    def Afinidad(self):
        max,min = self.MaxMin()
        for i in range(self.population):
            try:
                self.Lista[i].afinidad = (1 - (self.Lista[i].costo/(max - min)))
            except:
                self.Lista[i].afinidad = (1 - (self.Lista[i].costo/1))
            if(self.Lista[i].afinidad > 1):
                self.Lista[i].afinidad = 1.0

    def DeMenorAMayor(self, Lista_tmp):
        new = []
        new2 = []
        for i in range(len(Lista_tmp)):
            new.append((Lista_tmp[i].costo,Lista_tmp[i]))

        new.sort(key=lambda x: x[0])
        for i in range(self.population):
            new2.append(new[i][1])

        self.mejorCelula = new2[0]
        return new2

    def promCosto(self):
        self.prom_costo = 0
        for i in range(self.population):
            self.prom_costo+= self.Lista[i].costo
        self.prom_costo = self.prom_costo/self.population

    def promedio(self,Lista):
        prom_costo = 0
        for i in range(self.population):
            prom_costo+= Lista[i].costo
        prom_costo = prom_costo/self.population
        return prom_costo

    def clone(self,par,norm_cost):
        alpha = (1/self.beta)*math.exp(-1*norm_cost)
        menor = Celula()
        min = 999
        print(" clones:")
        for i in range(self.n_clones):
            cel = Celula()
            norma = np.random.normal(0,1)
            cel.par.append(par[0] + alpha*norma)
            cel.par.append(par[1] + alpha*norma)
            cel.costo = F(cel.par[0],cel.par[1])
            print(" vector: ",cel.par[0],",",cel.par[1]," cost: ",cel.costo)
            if(cel.costo < min):
                min = cel.costo
                menor = cel
        print("")
        return menor

    def Clonar(self):
        self.ListaClonados = []
        for i in range(self.population):
            self.ListaClonados.append(self.clone(self.Lista[i].par,self.Lista[i].norm_cost))

    def SuppressByAffinity(self):
        indices = []
        for i in range(self.population):
            if(self.Lista[i].afinidad < self.affinity_threshold):
                indices.append(i)

        for index in sorted(indices, reverse=True):
            del self.Lista[index]
            self.population -= 1

    def createRandom(self):
        for i in range(self.n_rand):
            celula = Celula()
            celula.par.append(random.uniform(self.lim_inf,self.lim_sup))
            celula.par.append(random.uniform(self.lim_inf,self.lim_sup))
            celula.costo = F(celula.par[0],celula.par[1])
            self.Lista.append(celula)
        self.population +=2

    def Main(self):
        promedio = 999
        self.generarPoblacion()
        self.normalizarCosto()
        self.Afinidad()
        self.DeMenorAMayor(self.Lista)
        self.promCosto()
        self.printL(self.Lista)
        print("Obtener el mejor de la poblacion")
        print("vector: ",self.mejorCelula.par[0]," , ",self.mejorCelula.par[1], " con costo: ",self.mejorCelula.costo,"\n")
        print("Calcular el promedio del costo ")
        print(self.prom_costo,"\n")
        for i in range(self.Generaciones):
            promedio = 999
            while(promedio > self.prom_costo):
                print("\n    ------------- El promedio de los clones fue mayor al promedio general ---------------")
                self.Clonar()
                # self.printL(self.ListaClonados)
                promedio = self.promedio(self.ListaClonados)
                print("\n Promedio clones: ",promedio)
            self.Lista = self.ListaClonados
            print("\n *************** Clones Finales o Nueva Poblacion *****************")
            self.normalizarCosto()
            self.Afinidad()
            self.printL(self.Lista)
            print("\n ---------------- Poblacion despues del supresor de afinidad ---------------")
            self.SuppressByAffinity()
            self.printL(self.Lista)
            print("\n  ++++++++++++++++ Insertar Individuos Aleatorios +++++++++++++++ ")
            self.createRandom()
            self.normalizarCosto()
            self.Afinidad()
            self.DeMenorAMayor(self.Lista) # Hallar el mejor
            self.promCosto() # Hallar el promedio general
            print("\n       #######################################################")
            print("       ################### Nueva poblacion ##################### ")
            print("       #######################################################")
            self.printL(self.Lista)
            print(" Obtener el mejor de la poblacion")
            print(" vector: ",self.mejorCelula.par[0],",",self.mejorCelula.par[1], " con costo: ",self.mejorCelula.costo,"\n")
            print(" Calcular el promedio del costo ")
            print(" ",self.prom_costo)

ainet = aiNet()
ainet.Main()
