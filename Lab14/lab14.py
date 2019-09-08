import random
import math
import os
import numpy as np
import pandas as pd
import sys
import copy

orig_stdout = sys.stdout
f = open('Lab14.txt', 'w')
sys.stdout = f

def F(x1,x2):
    res = -math.cos(x1)*math.cos(x2)*math.exp(-pow((x1-math.pi),2)-pow((x2-math.pi),2))
    return res

# StopCondition = 100 iteraciones
# Population size = 4
# Selection size = 4
# RandomCells num = 2
# Clone rate = 0.25
# Mutation factor = -2.5

class Poblador:
    def __init__(self):
        self.bitstring = ""
        self.par=[]
        self.afinidad = -999
        self.costo = -999
        self.mutation_rate = -999

class SeleccionClonal:
    def __init__(self):
        self.SC = int(input("Ingrese el número de iteraciones: ")) #Stop condition
        print(self.SC)
        self.population = int(input("Ingrese el número de la población: "))
        print(self.population)
        self.selection_size = 4
        self.random_cells = 2
        self.clone_rate = 0.25
        self.mutation_factor = -2.5
        self.lim_inf = -10
        self.lim_sup = 10
        self.Lista = []
        self.cantidad_clones = -999
        self.ListaClonados=[]
        self.ListaAleatoria=[]
        self.mejorIndividuo = Poblador()

    def generarBitString(self):
        stri = ""
        for i in range(16):
            stri = stri+str(random.randint(0,1))
        return stri

    def binToDec(self,binary_string):
        return int(binary_string,2)

    def hallarVec(self,binario):
        return round(self.lim_inf + ((self.lim_sup - self.lim_inf)/255) * self.binToDec(binario),8)

    def printL(self,Lis):
        print("--------------------------------------------------------------------------------------------------")
        print("|     Bitstring    |      x1      |       x2      |      Costo     |   Afinidad   | Mutation Rate |")
        print(" -------------------------------------------------------------------------------------------------")
        for i in range(len(Lis)):
            print("|",Lis[i].bitstring,"| ",Lis[i].par[0]," | ",Lis[i].par[1] ," |  ",Lis[i].costo ," | ",Lis[i].afinidad," | ",Lis[i].mutation_rate," |")
        print(" -------------------------------------------------------------------------------------------------------")

    def printLista(self):
        print("--------------------------------------------------------------------------------------------------")
        print("|     Bitstring    |      x1      |       x2      |      Costo     |   Afinidad   | Mutation Rate |")
        print(" -------------------------------------------------------------------------------------------------")
        for i in range(self.population):
            print("|",self.Lista[i].bitstring,"| ",self.Lista[i].par[0]," | ",self.Lista[i].par[1] ," |  ",self.Lista[i].costo ," | ",self.Lista[i].afinidad," | ",self.Lista[i].mutation_rate," |")
        print(" -------------------------------------------------------------------------------------------------------")

    def printListaClonados(self):
        print("---------------------------------------------------------------------")
        print("|     Bitstring    |      x1      |       x2      |      Costo     |")
        print(" ------------------------------------------------------------------")
        for i in range(self.population):
            print("|",self.ListaClonados[i].bitstring,"| ",self.ListaClonados[i].par[0]," | ",self.ListaClonados[i].par[1] ," |  ",self.ListaClonados[i].costo ," |")
        print(" -------------------------------------------------------------------------")

    def generarPoblacion(self):
        for i in range(self.population):
            poblador = Poblador()
            poblador.bitstring = self.generarBitString()
            poblador.par.append(self.hallarVec(poblador.bitstring[:8]))
            poblador.par.append(self.hallarVec(poblador.bitstring[8:]))
            poblador.costo = F(poblador.par[0],poblador.par[1])
            self.Lista.append(poblador)

    def MayorCosto(self):
        mayor = -999
        for i in range(self.population):
            if( self.Lista[i].costo> mayor):
                mayor = self.Lista[i].costo
        return mayor

    def MenorCosto(self):
        menor = 999
        for i in range(self.population):
            if( self.Lista[i].costo < menor):
                menor = self.Lista[i].costo
        return menor

    def Afinidad(self):
        for i in range(self.population):
            try:
                self.Lista[i].afinidad = (1 - (self.Lista[i].costo/(self.MayorCosto() - self.MenorCosto())))
            except:
                self.Lista[i].afinidad = (1 - (self.Lista[i].costo/1))
            if(self.Lista[i].afinidad > 1):
                self.Lista[i].afinidad = 1.0

    def MutationRate(self):
        for i in range(self.population):
            self.Lista[i].mutation_rate = round(math.exp(self.mutation_factor * self.Lista[i].afinidad),8)

    def clone(self,mut_rate, bit):
        rand = random.uniform(0,1)
        if(rand < mut_rate):
            if(bit=="0"):
                return "1"
            else:
                return "0"
        else:
            return bit

    def Clonar(self,n):
        for i in range(self.population):
            poblador = Poblador()
            for j in range(len(self.Lista[i].bitstring)):
                poblador.bitstring = poblador.bitstring + self.clone(self.Lista[i].mutation_rate,self.Lista[i].bitstring[j])
            poblador.par.append(self.hallarVec(poblador.bitstring[:8]))
            poblador.par.append(self.hallarVec(poblador.bitstring[8:]))
            poblador.costo = F(poblador.par[0],poblador.par[1])
            self.ListaClonados.append(poblador)

    def InsercionAleatoria(self):
        for i in range(self.random_cells):
            poblador = Poblador()
            poblador.bitstring = self.generarBitString()
            poblador.par.append(self.hallarVec(poblador.bitstring[:8]))
            poblador.par.append(self.hallarVec(poblador.bitstring[8:]))
            poblador.costo = F(poblador.par[0],poblador.par[1])
            self.ListaAleatoria.append(poblador)

    def DeMenorAMayor(self, Lista_tmp):
        new = []
        new2 = []
        for i in range(len(Lista_tmp)):
            new.append((Lista_tmp[i].costo,Lista_tmp[i]))

        new.sort(key=lambda x: x[0])
        for i in range(self.population):
            new2.append(new[i][1])
        return new2

    def Mejores(self,ListaAgregar):
        ListaNueva = copy.deepcopy(self.Lista)
        for i in range(len(ListaAgregar)):
            ListaNueva.append(copy.deepcopy(ListaAgregar)[i])
        # print("Lista nueva + clon/aleat: ")
        # self.printL(ListaNueva)
        self.Lista = self.DeMenorAMayor(ListaNueva)
        self.ListaClonados = []
        self.ListaAleatoria=[]
        self.mejorIndividuo = self.Lista[0]

    def Main(self):
        self.generarPoblacion()
        self.Afinidad()
        self.MutationRate()
        self.printLista()

        for i in range(self.SC):
            self.cantidad_clones = self.population*self.clone_rate
            print("Cantidad de clones: ",self.cantidad_clones)
            self.Clonar(self.cantidad_clones)
            print("Lista de clonados: ")
            self.printListaClonados()

            self.Mejores(self.ListaClonados)
            self.Afinidad()
            self.MutationRate()
            print("Lista de mejores: ")
            self.printLista()

            self.InsercionAleatoria()
            print("Lista Aletoria: ")
            self.printL(self.ListaAleatoria)

            self.Mejores(self.ListaAleatoria)
            self.Afinidad()
            self.MutationRate()
            print("Lista de mejores: ")
            self.printLista()

            print("Mejor sol: ", self.mejorIndividuo.par[0]," , ",self.mejorIndividuo.par[1], " con costo: ",self.mejorIndividuo.costo)

sc = SeleccionClonal()
sc.Main()
