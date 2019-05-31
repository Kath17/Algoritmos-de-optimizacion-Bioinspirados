import random
import math
import os
import numpy as np
import pandas as pd
import sys
import copy

orig_stdout = sys.stdout
f = open('Lab12.txt', 'w')
sys.stdout = f

def F(x_1,x_2):
    res = x_1*math.sin(4*math.pi*x_1) - x_2*math.sin(4*math.pi*x_2 + math.pi) + 1
    return round(res,6)

def Resta(x,y,m,n):
    return round(x-m,6),round(y-n,6)

def Suma(x,y,m,n):
    return round(x+m,6),round(y+n,6)

def Mult(esc,x,y):
    return round(esc*x,6),round(esc*y,6)

class Particula:
    def __init__(self):
        self.x_1 = -1
        self.x_2 = -1
        self.v_1 = -1
        self.v_2 = -1
        self.fitness = -1
        self.p1_best = -1
        self.p2_best = -1

class AlgoritmoPSO:
    def __init__(self):
        self.poblacion = int(input("Ingrese el número de la poblacion: "))
        print(self.poblacion)
        self.iteraciones = int(input("Ingrese el número de iteraciones: "))
        print(self.iteraciones)
        self.lim_inf = -1
        self.lim_sup = 2
        self.vel_inf = -1
        self.vel_sup = 1
        self.w = random.uniform(0,1)
        self.phi_1 = 2
        self.phi_2 = 2
        self.rand_1 = random.uniform(0,1)
        self.rand_2 = random.uniform(0,1)
        self.ListaParticulas = []
        self.g_Best = Particula()

    def generarPoblacion(self):
        for i in range(self.poblacion):
            particula = Particula()
            particula.x_1 = round(random.uniform(self.lim_inf,self.lim_sup),6)
            particula.x_2 = round(random.uniform(self.lim_inf,self.lim_sup),6)
            particula.fitness = F(particula.x_1,particula.x_2)
            particula.v_1 = round(random.uniform(self.vel_inf,self.vel_sup),6)
            particula.v_2 = round(random.uniform(self.vel_inf,self.vel_sup),6)
            particula.p1_best = particula.x_1
            particula.p2_best = particula.x_2
            self.ListaParticulas.append(particula)
            #actualizando global
            if(self.g_Best.fitness < particula.fitness):
                self.g_Best = particula

    def Fitness(self):
        for i in range(self.poblacion):
            self.ListaParticulas[i].fitness = F(self.ListaParticulas[i].x_1,self.ListaParticulas[i].x_2)

    def printLista(self):
        print("\n------------------------------------------------------------------------------------------------------")
        print("|                            LISTA                          |   FITNESS  |           P_Best          |")
        print(" -----------------------------------------------------------------------------------------------------")
        for i in range(self.poblacion):
            print("| ( ",self.ListaParticulas[i].x_1,",",self.ListaParticulas[i].x_2 ," ) | ( ",self.ListaParticulas[i].v_1," , ",self.ListaParticulas[i].v_2," ) | ",self.ListaParticulas[i].fitness," | ( ",self.ListaParticulas[i].p1_best ," , ",self.ListaParticulas[i].p2_best," ) |")
        print(" -----------------------------------------------------------------------------------------------------")

    def actualizar_Global(self,particula):
        if(self.g_Best.fitness < particula.fitness):
            print("\n Actualiza g_best con fitness de: ",self.g_Best.fitness," a ", particula.fitness)
            print(" Actualiza g_best de: ",self.g_Best.x_1," , ",self.g_Best.x_2," a ",particula.x_1," , ",particula.x_2)
            self.g_Best = particula
            return particula
        else:
            return self.g_Best

    def actualizar_p_Best(self,particula):
        if(F(particula.p1_best,particula.p2_best) < particula.fitness):
            print("\n Actualiza p_best con fitness de: ",F(particula.p1_best,particula.p2_best)," a ", particula.fitness)
            print(" Actualiza p_best de: ",particula.p1_best," , ",particula.p2_best," a ",particula.x_1," , ",particula.x_2)
            particula.p1_best = particula.x_1
            particula.p2_best = particula.x_2
            return particula.x_1,particula.x_2
        else:
            return particula.p1_best,particula.p2_best

    def actualizar_valores(self):
        for i in range(self.poblacion):

            self.rand_1 = random.uniform(0,1)
            self.rand_2 = random.uniform(0,1)

            # --- actualizando velocidades -----#
            v_1w,v_2w = Mult(self.w,self.ListaParticulas[i].v_1, self.ListaParticulas[i].v_2)
            tmp1,tmp2 = Resta(self.ListaParticulas[i].p1_best,self.ListaParticulas[i].p2_best,self.ListaParticulas[i].x_1,self.ListaParticulas[i].x_2)
            r_1,r_2 = Mult((self.phi_1*self.rand_1), tmp1,tmp2)
            tmp1,tmp2 = Resta(self.g_Best.x_1,self.g_Best.x_2,self.ListaParticulas[i].x_1,self.ListaParticulas[i].x_2)
            r2_1,r2_2 = Mult((self.phi_2*self.rand_2), tmp1,tmp2)
            tmp1,tmp2 =Suma(v_1w,v_2w,r_1,r_2)
            self.ListaParticulas[i].v_1,self.ListaParticulas[i].v_2 = Suma(tmp1,tmp2,r2_1,r2_2)

            # --- actualizando x,y -----#
            self.ListaParticulas[i].x_1,self.ListaParticulas[i].x_2 = Suma(self.ListaParticulas[i].x_1,self.ListaParticulas[i].x_2,self.ListaParticulas[i].v_1,self.ListaParticulas[i].v_2)
            if(self.ListaParticulas[i].x_1 > 2 or self.ListaParticulas[i].x_1 < -1):
                self.ListaParticulas[i].x_1 = round(random.uniform(self.lim_inf,self.lim_sup),6)
            if(self.ListaParticulas[i].x_2 > 2 or self.ListaParticulas[i].x_2 < -1):
                self.ListaParticulas[i].x_2 = round(random.uniform(self.lim_inf,self.lim_sup),6)

            # --- actualizando fitness ---#
            self.ListaParticulas[i].fitness = F(self.ListaParticulas[i].x_1,self.ListaParticulas[i].x_2)
            # --- actualizando p_best ---#
            self.ListaParticulas[i].p1_best,self.ListaParticulas[i].p2_best =self.actualizar_p_Best(self.ListaParticulas[i])
            # --- actualizando global ---#
            self.g_Best = self.actualizar_Global(self.ListaParticulas[i])

        self.printLista()

    def Main(self):
        self.generarPoblacion()
        self.Fitness()
        self.printLista()
        print("\nMejor Global: ",self.g_Best.x_1,",",self.g_Best.x_2 ," con ",self.g_Best.fitness)
        for i in range(self.iteraciones):
            self.w = random.uniform(0,1)
            print("\n-------------------------------------------------------------------------")
            print("\n-------------------------------- ITERACION "+str(i+1)+"----------------------------  ")
            print("\n-------------------------------------------------------------------------")
            self.actualizar_valores()
            print("\nMejor Global: ",self.g_Best.x_1,",",self.g_Best.x_2 ," con ",self.g_Best.fitness)

PSO = AlgoritmoPSO()
PSO.Main()
