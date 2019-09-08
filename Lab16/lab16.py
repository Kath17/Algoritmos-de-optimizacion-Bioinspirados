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

delta = [0,0]
rand_vect = [0,0]

class Celula:
    def __init__(self):
        self.par=[]
        self.costo = 999
        self.interaccion = 0
        self.fitness = 0
        self.health = 0

class BFO:
    def __init__(self):
        self.cells_num = int(input("Ingrese el número de la población: "))
        print(self.cells_num)
        self.dim = 2
        self.step_size = 0.1
        self.ned = 2
        self.nre = 2
        self.nc = 20
        self.ns = 5
        self.ped = 0.25
        self.d_attract = 0.1
        self.w_attract = 0.2
        self.h_repellant = 0.1
        self.w_repellant = 10
        self.lim_inf = -10
        self.lim_sup = 10
        self.Lista = []
        self.ListaClonados=[]
        self.ListaAleatoria=[]
        self.mejorCelula = Celula()

    def printL(self,Lis):
        print("\n---------------------------------------------------------------------------------------------")
        print("| i |     x1     |     x2     |      Costo     |    Interaccion   |   Fitness   |   Health   |")
        print(" --------------------------------------------------------------------------------------------")
        for i in range(len(Lis)):
            print("|",i+1,"|",round(Lis[i].par[0],6)," | ",round(Lis[i].par[1],6) ," |  ",Lis[i].costo ," | ",Lis[i].interaccion," | ",Lis[i].fitness," | ",Lis[i].health,"|")
        print(" --------------------------------------------------------------------------------------------")

    def generarPoblacion(self):
        for i in range(self.cells_num):
            celula = Celula()
            celula.par.append(random.uniform(self.lim_inf,self.lim_sup))
            celula.par.append(random.uniform(self.lim_inf,self.lim_sup))
            celula.costo = F(celula.par[0],celula.par[1])
            if(celula.costo < self.mejorCelula.costo):
                self.mejorCelula = celula
            self.Lista.append(celula)

    def interaccion(self,cell):   # cell -> posicion
        sum1 = 0
        sum2 = 0

        for i in range(self.cells_num): #posicion de cells
            resta = 0
            for j in range(self.dim):   #2 dim
                if(i != cell):
                    resta += pow((self.Lista[cell].par[j]-self.Lista[i].par[j]),2)
            sum1 += -self.d_attract * math.exp(-self.w_attract*resta)
            sum2 += self.h_repellant * math.exp(-self.w_repellant*resta)

        g = sum1 + sum2
        print("inter:  ",g)
        return g

    def interaction(self,new_cell_x,new_cell_y):   # new_cell -> objeto celula
        sum1 = 0
        sum2 = 0

        for i in range(self.cells_num): #posicion de cells
            resta = 0
            # for j in range(self.dim):
            resta += pow((new_cell_x - self.Lista[i].par[0]),2)
            resta += pow((new_cell_y - self.Lista[i].par[1]),2)

            sum1 += -self.d_attract * math.exp(-self.w_attract*resta)
            sum2 += self.h_repellant * math.exp(-self.w_repellant*resta)

        g = sum1 + sum2
        print("inter__:  ",g)
        return g

    def tumble_step(self,current_cell):   # new cell -> celula() , current -> pos
        temp1 = 0.0
        temp2 = 0.0
        temp_cell = [0,0]

        for i in range(self.dim):
            delta[i] = random.uniform(-1,1)
            temp1 += pow(delta[i],2)
        temp2 = math.sqrt(temp1)

        for j in range(self.dim):
            print(" j: ",j)
            rand_vect[j] = delta[j]/temp2
            # new_cell.par[j].append(self.Lista[current_cell].par[j] + self.step_size*rand_vect[j])
            temp_cell[j] = self.Lista[current_cell].par[j] + self.step_size*rand_vect[j]
            if(temp_cell[j] < self.lim_inf):
                temp_cell[j] = self.lim_inf
            if(temp_cell[j] > self.lim_sup):
                temp_cell[j] = self.lim_sup

        return temp_cell

    def swim_step(self,new_cell,current_cell):
        for i in range(self.dim):
            new_cell.par[i] = new_cell.par[i] + self.step_size*rand_vect[i]
            if(new_cell.par[i] < self.lim_inf):
                new_cell.par[i] = self.lim_inf
            if(new_cell.par[i] > self.lim_sup):
                new_cell.par[i] = self.lim_sup

        return new_cell

    def SortByCellHealth(self, Lista_tmp):  #Increasing health value
        new = []
        new2 = []
        Lista_tmp = copy.deepcopy(Lista_tmp)
        for i in range(len(Lista_tmp)):
            new.append((copy.deepcopy(Lista_tmp[i].health),copy.deepcopy(Lista_tmp[i])))

        new.sort(key=lambda x: x[0]) # menor a mayor
        for i in range(self.cells_num):
            new2.append(new[i][1])

        print("Ordenadooooo.... ")
        self.printL(new2)
        return new2

    def SelectByCellHealth(self,iteraciones):
        indx = 0
        var = self.cells_num-iteraciones
        for i in range(var,self.cells_num):
            self.Lista[i] = self.Lista[indx]
            print("   i: ", i)
            print("   indx: ", indx)
            indx += 1

        # for i in range(self.cells_num):
        #     self.Lista[i].health = 0.0

        return self.Lista

    def chemotaxisAndSwim(self):
        Jlast = 0;
        new_cell = Celula()
        new_cell.par = [0,0]

        for i in range(self.cells_num):
            self.Lista[i].interaccion = self.interaccion(i)
            print("interaccion 1: ",self.Lista[i].interaccion)
            self.Lista[i].fitness = self.Lista[i].costo + self.Lista[i].interaccion
            self.Lista[i].health = self.Lista[i].fitness

            Jlast = self.Lista[i].fitness

            temp_cell = self.tumble_step(i)
            new_cell.par[0] = temp_cell[0]
            new_cell.par[1] = temp_cell[1]
            new_cell.costo = F(new_cell.par[0],new_cell.par[1])
            print("costo: ",new_cell.costo)
            inter = self.interaction(new_cell.par[0],new_cell.par[1])
            new_cell.interaccion = inter
            print("inter result: ",inter)
            print("interaccion 2: ",new_cell.interaccion)
            new_cell.fitness = new_cell.costo + new_cell.interaccion

            for j in range(self.dim):
                self.Lista[i].par[j] = new_cell.par[j]

            self.Lista[i].costo = new_cell.costo
            self.Lista[i].fitness = new_cell.fitness
            self.Lista[i].health += new_cell.fitness

            for m in range(self.ns):
                if(new_cell.fitness < Jlast):
                    JLast = new_cell.fitness
                    new_cell = self.swim_step(new_cell,self.Lista[i])
                    new_cell.costo = F(new_cell.par[0],new_cell.par[1])

                    inter = self.interaction(new_cell.par[0],new_cell.par[1])
                    new_cell.interaccion = inter
                    print("interaccion 3: ", new_cell.interaccion)
                    new_cell.fitness = new_cell.costo + inter

                    for k in range(self.dim):
                        self.Lista[i].par[k] = new_cell.par[k]

                    self.Lista[i].costo = new_cell.costo
                    self.Lista[i].interaccion = new_cell.interaccion
                    self.Lista[i].fitness = new_cell.fitness
                    self.Lista[i].health += self.Lista[i].fitness

                else:
                    break;

            # celula.costo = F(celula.par[0],celula.par[1])

    def Main(self):
        self.generarPoblacion()
        cell_best = Celula()

        for l in range(self.ned):
            for k in range(self.nre):
                for j in range(self.nc):
                    self.chemotaxisAndSwim()
                    for i in range(len(self.Lista)):
                        if(self.Lista[i].costo < self.mejorCelula.costo):
                            self.mejorCelula = self.Lista[i]
                    print("Etapa de quimiotaxis")
                    self.printL(self.Lista)

                self.Lista = self.SortByCellHealth(self.Lista)
                self.Lista = copy.deepcopy(self.Lista[:len(self.Lista)//2])
                self.Lista += copy.deepcopy(self.Lista)
                # self.Lista = self.SelectByCellHealth(self.cells_num//2)
                print("Reproduccion")
                self.printL(self.Lista)

            for i in range(self.cells_num):
                rand = random.uniform(0,1)
                print("--------------> i: ",i)
                if( rand <= self.ped):
                    # print("Cambiaa !!")
                    # cell_new = Celula()
                    self.Lista[i].par[0]= random.uniform(self.lim_inf,self.lim_sup)
                    self.Lista[i].par[1]= random.uniform(self.lim_inf,self.lim_sup)
                    self.Lista[i].costo = F(self.Lista[i].par[0],self.Lista[i].par[1])
                    # print("interaccion 1: ",self.Lista[i].interaccion)
                    self.Lista[i].interaccion = 0
                    self.Lista[i].fitness = 0
                    self.Lista[i].health = 0
                    if(self.Lista[i].costo < self.mejorCelula.costo):
                        self.mejorCelula = self.Lista[i]


            print("Despues de eliminacion dispersion")
            self.printL(self.Lista)

        print("Mejor celula: ",self.mejorCelula.par[0]," , ",self.mejorCelula.par[1], " con ",self.mejorCelula.costo)
        return self.mejorCelula

bfo = BFO()
bfo.Main()
