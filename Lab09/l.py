import pandas as pd
import numpy as np

Grafo = {'A':{'A':0,'B':22,'C':47, 'D':15,'E':63},
             'B':{'A':22,'B':0,'C':18, 'D':62,'E':41},
             'C':{'A':47, 'B':18,'C':0, 'D':32,'E':57},
             'D':{'A':15,'B':62,'C':32,'D':0,'E':62},
             'E':{'A':63, 'B':41, 'C':57,'D':62,'E':0}}

Matriz = pd.DataFrame(Grafo)

def GenerarVisibilidad(Matriz):
    return 1/Matriz

print(GenerarVisibilidad(Matriz))	
