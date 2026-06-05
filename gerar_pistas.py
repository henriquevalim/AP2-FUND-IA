import pygame

# Inicialização e Configurações
pygame.init()
LARGURA = 800
ALTURA = 600
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

def desenhar_caminho(superficie, pontos, largura_linha):
    for i in range(len(pontos) - 1):
        # Desenha as retas da pista
        pygame.draw.line(superficie, BRANCO, pontos[i], pontos[i+1], largura_linha)
        # Desenha círculos nas pontas para que as curvas fiquem redondas e suaves
        pygame.draw.circle(superficie, BRANCO, pontos[i], largura_linha // 2)
        pygame.draw.circle(superficie, BRANCO, pontos[i+1], largura_linha // 2)

print("Gerando pistas com obstáculos avançados...")

# =========================================================
# PISTA 1 - OVAL (Com pilares laterais)
# =========================================================
p1 = pygame.Surface((LARGURA, ALTURA))
p1.fill(PRETO)
# Desenha o anel branco e o buraco preto no meio
pygame.draw.ellipse(p1, BRANCO, (50, 50, 700, 500))
pygame.draw.ellipse(p1, PRETO, (170, 170, 460, 260))

# Obstáculos estratégicos nas curvas para forçar desvio
pygame.draw.circle(p1, PRETO, (110, 300), 20)
pygame.draw.circle(p1, PRETO, (690, 300), 20)


# =========================================================
# PISTA 2 - ZIG-ZAG (O Campo de Treinamento Supremo)
# =========================================================
p2 = pygame.Surface((LARGURA, ALTURA))
p2.fill(PRETO)
pontos_p2 = [
    (150, 100), (650, 100), 
    (650, 250), (150, 250),
    (150, 400), (650, 400),
    (650, 550), (150, 550)
]
# Desenha a pista com 100 pixels de largura
desenhar_caminho(p2, pontos_p2, 100)

# Obstáculos no meio de cada reta. Fim do "Sucesso Acidental"!
pygame.draw.circle(p2, PRETO, (400, 100), 20)
pygame.draw.circle(p2, PRETO, (400, 250), 20)
pygame.draw.circle(p2, PRETO, (400, 400), 20)
pygame.draw.circle(p2, PRETO, (400, 550), 20)


# =========================================================
# PISTA 3 - CARACOL (Desafio de Manobrabilidade)
# =========================================================
p3 = pygame.Surface((LARGURA, ALTURA))
p3.fill(PRETO)
pontos_p3 = [
    (150, 100), (700, 100),
    (700, 500), (200, 500),
    (200, 250), (500, 250),
    (500, 400), (350, 400)
]
desenhar_caminho(p3, pontos_p3, 90)

# Obstáculos para impedir atalhos diretos
pygame.draw.circle(p3, PRETO, (425, 100), 20)
pygame.draw.circle(p3, PRETO, (700, 300), 20)
pygame.draw.circle(p3, PRETO, (450, 500), 20)

# Salva as imagens na pasta atual
pygame.image.save(p1, "pista1.png")
pygame.image.save(p2, "pista2.png")
pygame.image.save(p3, "pista3.png")

print("Sucesso! As imagens pista1.png, pista2.png e pista3.png foram atualizadas.")