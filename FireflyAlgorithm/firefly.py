import random
import math
import os
import numpy as np
import pandas as pd
import sys
import copy
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(22,8))

orig_stdout = sys.stdout
f = open('firefly.txt', 'w')
sys.stdout = f

def F(x,y):
    return - np.power(x,2) - np.power(y,2)
    #return 12 - (np.power(x,2) + np.power(y,2)) /100 #parabolic function
    #four peak function
    # return np.exp(-np.power((x-4),2)-np.power((y-4),2)) + np.exp(-np.power((x+4),2)-np.power((y-4),2)) + 2*abs(np.exp(-np.power(x,2)-np.power(y,2))+np.exp(-np.power(x,2)-np.power((y+4),2)))
    # ratrigin function
    # return 80 -(20 + np.power(x,2) + np.power(y,2) - 10*(np.cos(2*math.pi*x) + np.cos(2*math.pi*y)))

def Graph(lim_inf,lim_sup):
    x = np.linspace(lim_inf, lim_sup, 60)
    y = np.linspace(lim_inf, lim_sup, 60)

    X, Y = np.meshgrid(x, y)
    Z = F(X, Y)

    fig = plt.figure(figsize=(22,8))

    # ------------------------ First subplot -------------------------#
    ax = fig.add_subplot(1, 2, 1, projection = '3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none', alpha = 0.4)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z');
    ax.set_proj_type('ortho')

    fig.colorbar(surf, shrink=0.5, aspect=5)   # barrar de colores

    # ------------------------ Second subplot -----------------------#
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.contour(X, Y, Z, 10, cmap="viridis", linestyles="solid")#, offset=-1)

    return ax,ax2

def plot(ax,ax2,x_point,y_point,z_point,j):

    p1 = ax.scatter(x_point, y_point, z_point,c='r', marker='^')
    p2 = ax2.scatter(x_point, y_point, c='r', marker='^')

    plt.savefig('images/image'+str(j+1)+'.png')

    p1.remove()
    p2.remove()

class Firefly:
    def __init__(self):
        self.pos = []
        self.brightness = 0.0   # attractiveness

class FireflyAlgorithm:
    def __init__(self,D,P,iterations,alpha,beta0,gamma,lim_inf,lim_sup):
        self.dimension = D
        self.population = P
        self.iterations = iterations
        self.alpha = alpha
        self.Sk = 0.97
        self.beta0 = beta0   # max_attraction(r=0) , original light intensity
        self.gamma = gamma  # light absorption coefficient
        self.nbest = Firefly()   # mejor local
        self.fbest = Firefly()   # mejor global
        self.lim_inf = lim_inf   # limite inferior
        self.lim_sup = lim_sup    #limite superior
        self.fireflies = []

    def InitialPopulation(self):
        for i in range(self.population):
            firefly = Firefly()
            for j in range(self.dimension):
                firefly.pos.append(random.uniform(self.lim_inf,self.lim_sup))
            firefly.brightness = F(firefly.pos[0],firefly.pos[1])
            self.fireflies.append(firefly)

    def euclidean(self,x1,y1,x2,y2):
        r = 0.0
        r += pow((x1 - x2),2)
        r += pow((y1 - y2),2)
        return math.sqrt(r)

    def FindLimits(self, j):
        bool = False
        for i in range(self.dimension):
            if (self.fireflies[j].pos[i] < self.lim_inf):
                print("se pasa con: ",self.fireflies[j].pos[i])
                print("                                                     ... Salió de los límites")
                self.fireflies[j].pos[i] = random.uniform(self.lim_inf,self.lim_sup)
                bool = True
            if (self.fireflies[j].pos[i] > self.lim_sup):
                print("se pasa con: ",self.fireflies[j].pos[i])
                print("                                                     ... Salió de los límites")
                self.fireflies[j].pos[i] = random.uniform(self.lim_inf,self.lim_sup)
                bool = True
        if(bool == True):
            self.fireflies[j].brightness = F(self.fireflies[j].pos[0],self.fireflies[j].pos[1])

    def printL(self):
        print("   ---------------------------------------------")
        print("  | i |     x1     |      x2     |    Fitness   |")
        print("   ---------------------------------------------")
        for i in range(self.population):
            print("  |",i+1,"| ",round(self.fireflies[i].pos[0],6)," | ",round(self.fireflies[i].pos[1],6) ," | ",round(self.fireflies[i].brightness,6) ," |")
        print("   ----------------------------------------------")

    def retornarListas(self):
        X = []
        Y = []
        Z = []
        for i in range(self.population):
            X.append(self.fireflies[i].pos[0])
            Y.append(self.fireflies[i].pos[1])
            Z.append(self.fireflies[i].brightness)
        return X,Y,Z

    def Ordenar(self):  #De mayor a menor
        AOrdenar = []
        Ordenada = []
        for i in range(self.population):
            AOrdenar.append((self.fireflies[i].brightness,self.fireflies[i]))

        AOrdenar.sort(key=lambda x: x[0], reverse=True)
        #AOrdenar.sort(key=lambda x: x[0])
        for i in range(self.population):
            Ordenada.append(AOrdenar[i][1])

        self.nbest = Ordenada[0]
        return Ordenada

    def Main(self):
        self.InitialPopulation()
        #ax,ax2= Graph(self.lim_inf,self.lim_sup)

        for k in range(self.iterations):
            print("\n       #######################################################")
            print("       #################### Iteracion " + str(k) + " ##################### ")
            print("       #######################################################")

            self.fireflies = self.Ordenar()   #Se actualiza el mejor local
            self.alpha = self.alpha * self.Sk
            self.printL()
            print("              Nuevo alpha: ",round(self.alpha,7))

            X,Y,Z = self.retornarListas()
            #plot(ax,ax2,X,Y,Z,k)

            for j in range(0,self.population):
                for i in range(j):
                    # print("  i: ",i," j: ",j)
                    if(self.fireflies[i].brightness > self.fireflies[j].brightness):
                    #if(self.fireflies[i].brightness < self.fireflies[j].brightness):
                        print("\n Luciérnaga ",j+1, " se movió hacia la luciérnaga ",i+1)
                        distance = self.euclidean(self.fireflies[j].pos[0],self.fireflies[j].pos[1],self.fireflies[i].pos[0],self.fireflies[i].pos[1])
                        print("  Distancia: ",round(distance,5))
                        beta = (self.beta0) * math.exp(-self.gamma * math.pow(distance, 2.0))
                        print("       Beta: ",round(beta,6))
                        Rand = np.random.normal(0,1)
                        print("     Normal: ",round(Rand,5))
                        print("         De: ",round(self.fireflies[j].pos[0],5), ",", round(self.fireflies[j].pos[1],5), " con: ",round(self.fireflies[j].brightness,5))
                        self.fireflies[j].pos[0] = self.fireflies[j].pos[0] + beta*(self.fireflies[i].pos[0] - self.fireflies[j].pos[0]) + self.alpha*(Rand-0.5)
                        self.fireflies[j].pos[1] = self.fireflies[j].pos[1] + beta*(self.fireflies[i].pos[1] - self.fireflies[j].pos[1]) + self.alpha*(Rand-0.5)
                        self.fireflies[j].brightness = F(self.fireflies[j].pos[0],self.fireflies[j].pos[1])
                        self.FindLimits(j)
                        print("          A: ",round(self.fireflies[j].pos[0],5), ",", round(self.fireflies[j].pos[1],5), " con: ",round(self.fireflies[j].brightness,5))

            if(self.nbest.brightness > self.fbest.brightness):
                self.fbest = self.nbest

        print("\n       #######################################################")
        print("       #################### RESULTADO FINAL ################## ")
        print("       #######################################################")
        self.fireflies = self.Ordenar()   #Se actualiza el mejor local
        if(self.nbest.brightness > self.fbest.brightness):
            self.fbest = self.nbest
        self.printL()

        return self.fbest


# __init__(D,P,iterations,alpha,beta0,gamma,lim_inf,lim_sup):
FA = FireflyAlgorithm(2,5,2,0.2,1,1,-5,5)
FA.Main()
