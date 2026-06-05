import pygame
import math
from rede import RedeNeural
import config

class CarroIA:
    def __init__(self, pista_inicial="1"):
        self.rede = RedeNeural()
        self.resetar(pista_inicial)

    def resetar(self, pista_atual):
        cord = config.PONTOS_LARGADA.get(pista_atual, (400, 490))
        self.x, self.y = cord[0], cord[1]
        self.angulo = 0
        self.velocidade = 4
        self.vivo = True
        self.fitness = 0
        self.radares = []
        self.tempo_vida = 0
        self.checkpoints_passados = 0
        self.tempo_sem_checkpoint = 0

    def pensar_e_mover(self, pista_atual):
        if not self.vivo:
            return
            
        self.tempo_vida += 1
        self.tempo_sem_checkpoint += 1
        
        if self.tempo_sem_checkpoint > 1000 or self.tempo_vida > 10000:
            self.vivo = False
            return

        entradas = [r[1] / 150.0 for r in self.radares]
        saidas = self.rede.prever(entradas)
        
        forca_esq = saidas[0] - 0.5
        forca_dir = saidas[1] - 0.5
        
        # SUBIDO O MULTIPLICADOR DE 10 PARA 35
        # Agora, mesmo que a mutação mude só um pouquinho os pesos, o carro 
        # já vai ter força física para responder na tela e tentar desviar.
        if forca_esq > 0:
            self.angulo += (forca_esq * 35)  
        if forca_dir > 0:
            self.angulo -= (forca_dir * 35)

        radianos = math.radians(self.angulo)
        self.x += self.velocidade * math.cos(radianos)
        self.y -= self.velocidade * math.sin(radianos)
        
        lista_cps = config.CHECKPOINTS.get(pista_atual, [])
        if len(lista_cps) > 0:
            idx_alvo = self.checkpoints_passados % len(lista_cps)
            cp_x, cp_y = lista_cps[idx_alvo]
            
            distancia = math.sqrt((self.x - cp_x)**2 + (self.y - cp_y)**2)
            
            if distancia < 70:
                self.checkpoints_passados += 1
                self.tempo_sem_checkpoint = 0 
        else:
            self.tempo_sem_checkpoint = 0
        
        self.fitness = (self.checkpoints_passados * 10000) + self.tempo_vida

    def checar_colisao(self, superficie_fundo):
        if 0 <= int(self.x) < config.LARGURA and 0 <= int(self.y) < config.ALTURA:
            cor_pixel = superficie_fundo.get_at((int(self.x), int(self.y)))
            if cor_pixel[0] < 50 and cor_pixel[1] < 50 and cor_pixel[2] < 50:
                self.vivo = False
        else:
            self.vivo = False

    def calcular_radares(self, superficie_fundo):
        self.radares.clear()
        angulos = [-45, -22.5, 0, 22.5, 45]
        for a in angulos:
            comprimento = 0
            angulo_rad = math.radians(self.angulo + a)
            x_raio, y_raio = int(self.x), int(self.y)
            while comprimento < 150:
                x_raio = int(self.x + comprimento * math.cos(angulo_rad))
                y_raio = int(self.y - comprimento * math.sin(angulo_rad))
                if x_raio < 0 or x_raio >= config.LARGURA or y_raio < 0 or y_raio >= config.ALTURA: 
                    break
                cor_pixel = superficie_fundo.get_at((x_raio, y_raio))
                if cor_pixel[0] < 50 and cor_pixel[1] < 50 and cor_pixel[2] < 50: 
                    break
                comprimento += 2
            self.radares.append(((x_raio, y_raio), comprimento))

    def desenhar(self, superficie, desenhar_radares=False):
        if not self.vivo: return

        if desenhar_radares and len(self.radares) > 0:
            for ponto_alvo, comprimento in self.radares:
                pygame.draw.line(superficie, (0, 255, 100), (int(self.x), int(self.y)), ponto_alvo, 1)
                pygame.draw.circle(superficie, (255, 0, 0), ponto_alvo, 3)

        largura_carro, altura_carro = 30, 14
        carro_surf = pygame.Surface((largura_carro, altura_carro), pygame.SRCALPHA)
        
        if desenhar_radares:
            carro_surf.fill((0, 255, 255))
        else:
            carro_surf.fill((255, 50, 50))
            
        carro_rotacionado = pygame.transform.rotate(carro_surf, self.angulo)
        novo_retangulo = carro_rotacionado.get_rect(center=(int(self.x), int(self.y)))
        superficie.blit(carro_rotacionado, novo_retangulo.topleft)