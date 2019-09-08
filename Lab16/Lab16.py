import random
import math
import os
import numpy as np
import pandas as pd
import sys
import copy

orig_stdout = sys.stdout
f = open('Lab16.txt', 'w')
sys.stdout = f

def F(x1,x2):
    res = -math.cos(x1)*math.cos(x2)*math.exp(-pow((x1-math.pi),2)-pow((x2-math.pi),2))
    # res = x1*x1 + x2*x2
    return res

# Generaciones = 100 iteraciones
# cells_num = 4
# step_size = 0.1
# Num de etapas de eliminacion y dispersion (Ned) = 2
# Num de etapas de reproduccion (Nre) = 2
# Num de etapas de quimiotaxis (Nc) = 20
# Num de etapas de Nado (Ns) = 5
# Probabilidada de eliminacion y dispersion (Ped) = 0.25
# d_attract = 0.1
# w_attract = 0.2
# h_repellant = 0.1
# w_repellant = 10

class Celula:
    def __init__(self,inf,sup):
        self.par = [0,0]
        self.par[0] = random.uniform(inf,sup)
        self.par[1] = random.uniform(inf,sup)
        self.costo = F(self.par[0],self.par[1])
        self.interaccion = None
        self.fitness = None
        self.health = None

class BFO:
    def __init__(self):
        self.cells_num = int(input("Ingrese el número de la población: "))
        print(self.cells_num)
        self.dim = 2
        self.step_size = 0.2
        self.ned = 3                # Etapas de eliminacion
        self.nre = 3                # Etapas de reproduccion
        self.nc = 40                # Etapas de quimiotaxis
        self.ns = 5                 # Número de swims
        self.ped = 0.25             # Probabilidad de eliminacion
        self.d_attract = 0.1
        self.w_attract = 0.2
        self.h_repellant = self.d_attract
        self.w_repellant = 10
        self.lim_inf = -10
        self.lim_sup = 10
        self.Lista = []
        self.mejorCelula = [0,0,9999,99] # mejor celula: x,y,costo, fitness

    def printL(self,Lis):
        Lis = copy.deepcopy(Lis)
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        print("| i |     x1     |     x2     |         Costo          |        Interaccion       |       Fitness       |       Health         |")
        print(" ------------------------------------------------------------------------------------------------------------------------------")
        for i in range(len(Lis)):
            print("|",i+1,"|",round(Lis[i].par[0],6)," | ",round(Lis[i].par[1],6) ," |  ",Lis[i].costo ," | ",Lis[i].interaccion," | ",Lis[i].fitness," | ",Lis[i].health,"|")
        print(" ------------------------------------------------------------------------------------------------------------------------------")

    def printC(self,Cel):
        print(" [",round(Cel.par[0],6),",",round(Cel.par[1],6) ,"] , costo= ",Cel.costo ,", inter= ",Cel.interaccion,", fitness= ",Cel.fitness)#", health= ",Cel.health,"")

    def generarPoblacion(self):
        for i in range(self.cells_num):
            self.Lista.append(Celula(self.lim_inf,self.lim_sup))
            if(self.Lista[i].costo <= self.mejorCelula[2]):
                self.mejorCelula[0] = self.Lista[i].par[0]
                self.mejorCelula[1] = self.Lista[i].par[1]
                self.mejorCelula[2] = self.Lista[i].costo

    def SortByCellHealth(self):
        self.Lista = sorted(self.Lista, key=lambda x: x.health)
        print("\n Lista ordenada: ")
        self.printL(self.Lista)

    def Interaccion(self,cell):
        sum1 = 0
        sum2 = 0

        cell = copy.deepcopy(cell)
        for i in range(self.cells_num):
            resta = 0
            resta += pow((cell.par[0] - self.Lista[i].par[0]),2)
            resta += pow((cell.par[1] - self.Lista[i].par[1]),2)

            sum1 += -self.d_attract * math.exp(-self.w_attract*resta)
            sum2 += self.h_repellant * math.exp(-self.w_repellant*resta)

        g = sum1 + sum2
        # print(" -> interaccion:  ",g)
        return g

    def takeStep(self,cell,current):
        rand_step_direction = [0,0]

        temp_cell = copy.deepcopy(cell)
        for j in range(self.dim):
            rand_step_direction[j] = random.uniform(-1,1)
            temp_cell.par[j] = self.Lista[current].par[j] + self.step_size*rand_step_direction[j]
            if(temp_cell.par[j] < self.lim_inf):
                temp_cell.par[j] = self.lim_inf
            if(temp_cell.par[j] > self.lim_sup):
                temp_cell.par[j] = self.lim_sup

        return temp_cell

    def chemotaxisAndSwim(self):
        for i in range(self.cells_num):
            sum_nutrientes = 0.0

            self.Lista[i].interaccion = self.Interaccion(self.Lista[i])
            self.Lista[i].fitness = self.Lista[i].costo + self.Lista[i].interaccion
            # self.Lista[i].health = self.Lista[i].fitness

            print("\n-> Célula número: ",i)
            self.printC(self.Lista[i])

            if(self.Lista[i].costo <= self.mejorCelula[2]):
                self.mejorCelula[0] = self.Lista[i].par[0]
                self.mejorCelula[1] = self.Lista[i].par[1]
                self.mejorCelula[2] = self.Lista[i].costo
                self.mejorCelula[3] = self.Lista[i].fitness

            sum_nutrientes += self.Lista[i].fitness

            for j in range(self.ns):
                print(" Swim ",j,": ")

                new_cell = Celula(self.lim_inf,self.lim_sup)
                new_cell = self.takeStep(new_cell,i)
                new_cell.costo = F(new_cell.par[0],new_cell.par[1])
                new_cell.interaccion = self.Interaccion(new_cell)
                new_cell.fitness = new_cell.costo + new_cell.interaccion
                self.printC(new_cell)

                if(self.Lista[i].costo <= self.mejorCelula[2]):
                    self.mejorCelula[0] = self.Lista[i].par[0]
                    self.mejorCelula[1] = self.Lista[i].par[1]
                    self.mejorCelula[2] = self.Lista[i].costo
                    self.mejorCelula[3] = self.Lista[i].fitness

                if(new_cell.fitness > self.Lista[i].fitness):
                    break
                else:
                    self.Lista[i].par[0] = new_cell.par[0]
                    self.Lista[i].par[1] = new_cell.par[1]
                    self.Lista[i].costo = new_cell.costo
                    self.Lista[i].interaccion = new_cell.interaccion
                    self.Lista[i].fitness = new_cell.costo + new_cell.interaccion
                    # self.Lista[i].health += self.Lista[i].fitness
                    sum_nutrientes += self.Lista[i].fitness

            self.Lista[i].health = sum_nutrientes
            print(" --  End swim")
        print("\n >> chemo = ",i, " x= ",self.mejorCelula[0]," y= ",self.mejorCelula[1] ,"f=",self.mejorCelula[3], "cost= ",self.mejorCelula[2])

    def Main(self):
        self.generarPoblacion()
        print("Primera poblacion")
        self.printL(self.Lista)

        for l in range(self.ned):
            print("Ned = ",l)
            for k in range(self.nre):
                print("Nre = ",k)
                for j in range(self.nc):
                    self.chemotaxisAndSwim()
                    self.printL(self.Lista)
                    for i in range(len(self.Lista)):
                        if(self.Lista[i].costo < self.mejorCelula[2]):
                            self.mejorCelula[0] = self.Lista[i].par[0]
                            self.mejorCelula[1] = self.Lista[i].par[1]
                            self.mejorCelula[2] = self.Lista[i].costo
                            self.mejorCelula[3] = self.Lista[i].fitness
                print(" Mejor Celula  x= ",self.mejorCelula[0]," y= ",self.mejorCelula[1] ,"f=",self.mejorCelula[3], "cost= ",self.mejorCelula[2])
                print("Celulas antes de la reproduccion")
                self.printL(self.Lista)

                # REPRODUCCION
                self.SortByCellHealth()
                self.Lista = copy.deepcopy(self.Lista[:len(self.Lista)//2])
                self.Lista += copy.deepcopy(self.Lista)
                print("Celulas despues de la reproduccion")
                self.printL(self.Lista)
                print(" -- End Nre --")
                print("Nre =",k)

            #ELIMINACION
            print("\nCelulas antes de la eliminacion ")
            self.printL(self.Lista)
            for m in range(len(self.Lista)):
                rand = random.uniform(0,1)
                if(rand <= self.ped):
                    nueva_cell = Celula(self.lim_inf,self.lim_sup)
                    self.Lista[i] = copy.deepcopy(nueva_cell)
                    if(self.Lista[i].costo < self.mejorCelula[2]):
                        self.mejorCelula[0] = self.Lista[i].par[0]
                        self.mejorCelula[1] = self.Lista[i].par[1]
                        self.mejorCelula[2] = self.Lista[i].costo

            print("\nCelulas despues de la eliminacion ")
            self.printL(self.Lista)

        print("\n ----------------- Poblacion final ------------------------")
        self.printL(self.Lista)

        print(" Mejor Celula  x= ",self.mejorCelula[0]," y= ",self.mejorCelula[1] ,"f=",self.mejorCelula[3], "cost= ",self.mejorCelula[2])

        # self.SortByCellHealth()

bfo = BFO()
bfo.Main()
