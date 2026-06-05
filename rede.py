import random
import math

def sigmoide(x):
    return 1 / (1 + math.exp(-x))

class RedeNeural:
    def __init__(self):
        # Inicialização bem baixa para garantir curva de evolução
        self.pesos = [[random.uniform(-0.05, 0.05) for _ in range(2)] for _ in range(5)]
        self.bias = [random.uniform(-0.05, 0.05) for _ in range(2)]

    def prever(self, entradas):
        saidas = [0, 0]
        for i in range(2):
            soma = self.bias[i]
            for j in range(5):
                soma += entradas[j] * self.pesos[j][i]
            saidas[i] = sigmoide(soma)
        return saidas

    def mutar(self, taxa=0.15):
        # AJUSTE FINO: Mudado passo para 0.20.
        # Combinado com o multiplicador de 35 do carro, isso garante que eles 
        # consigam evoluir a tempo e quebrar a inércia, sem dar saltos mágicos.
        for i in range(5):
            for j in range(2):
                if random.random() < taxa:
                    self.pesos[i][j] += random.uniform(-0.20, 0.20)
        for i in range(2):
            if random.random() < taxa:
                self.bias[i] += random.uniform(-0.20, 0.20)