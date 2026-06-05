import pygame
import sys
import pickle
import random
import config
from carro import CarroIA

# Inicialização
pygame.init()
pygame.font.init()
tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
pygame.display.set_caption("Simulador IA - Apresentação Final")
fonte = pygame.font.SysFont("Arial", 16)
fonte_vitoria = pygame.font.SysFont("Arial", 40, bold=True)

pista_atual = "1"
fundo = pygame.image.load(config.PISTAS[pista_atual])

carros = [CarroIA(pista_atual) for _ in range(config.TAMANHO_POPULACAO)]
geracao = 1
pista_concluida = False
geracao_da_vitoria = 0

def evoluir_populacao():
    global geracao
    
    carros_ordenados = sorted(carros, key=lambda c: c.fitness, reverse=True)
    melhor_carro = carros_ordenados[0]
    segundo_melhor = carros_ordenados[1]
    
    melhor_brain = melhor_carro.rede
    segundo_brain = segundo_melhor.rede
    
    for i, carro in enumerate(carros):
        carro.resetar(pista_atual)
        if i == 0:
            # Elitismo
            carro.rede.pesos = [linha[:] for linha in melhor_brain.pesos]
            carro.rede.bias = melhor_brain.bias[:]
        else:
            # Crossover
            for j in range(5):
                for k in range(2):
                    if random.random() > 0.5:
                        carro.rede.pesos[j][k] = melhor_brain.pesos[j][k]
                    else:
                        carro.rede.pesos[j][k] = segundo_brain.pesos[j][k]
            for k in range(2):
                if random.random() > 0.5:
                    carro.rede.bias[k] = melhor_brain.bias[k]
                else:
                    carro.rede.bias[k] = segundo_brain.bias[k]
            
            carro.rede.mutar(taxa=0.20)
            
    geracao += 1

def desenhar_painel_neural(superficie, carro):
    if not carro or not carro.vivo or len(carro.radares) < 5: return
    start_x, start_y = 610, 50
    painel_surf = pygame.Surface((175, 230), pygame.SRCALPHA)
    painel_surf.fill((15, 15, 15, 200))
    superficie.blit(painel_surf, (start_x - 45, start_y - 20))
    
    y_entradas = [start_y + i * 38 for i in range(5)]
    y_saidas = [start_y + 40, start_y + 130]
    entradas = [r[1] / 150.0 for r in carro.radares]
    saidas = carro.rede.prever(entradas)
    pesos = carro.rede.pesos
    
    for j in range(5):
        for k in range(2):
            peso_val = pesos[j][k]
            cor_linha = (0, 200, 80) if peso_val > 0 else (220, 50, 50)
            espessura = max(1, min(4, int(abs(peso_val) * 1.5)))
            pygame.draw.line(superficie, cor_linha, (start_x, y_entradas[j]), (start_x + 90, y_saidas[k]), espessura)
            
    nomes_sensores = ["E45", "E22", "Fren", "D22", "D45"]
    for i in range(5):
        val = entradas[i]
        cor_no = (int((1 - val) * 255), int(val * 255), 40)
        pygame.draw.circle(superficie, cor_no, (start_x, y_entradas[i]), 10)
        pygame.draw.circle(superficie, (200, 200, 200), (start_x, y_entradas[i]), 10, 1)
        superficie.blit(fonte.render(nomes_sensores[i], True, (255, 255, 255)), (start_x - 38, y_entradas[i] - 8))
        
    nomes_saidas = ["Esq", "Dir"]
    for i in range(2):
        cor_no = (0, 230, 255) if saidas[i] > 0.5 else (60, 60, 60)
        pygame.draw.circle(superficie, cor_no, (start_x + 90, y_saidas[i]), 12)
        pygame.draw.circle(superficie, (200, 200, 200), (start_x + 90, y_saidas[i]), 12, 1)
        superficie.blit(fonte.render(nomes_saidas[i], True, (255, 255, 255)), (start_x + 110, y_saidas[i] - 8))

relogio = pygame.time.Clock()
executando = True

while executando:
    relogio.tick(60)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                pista_atual = evento.unicode
                fundo = pygame.image.load(config.PISTAS[pista_atual])
                geracao = 1
                pista_concluida = False
                carros = [CarroIA(pista_atual) for _ in range(config.TAMANHO_POPULACAO)]
            
            if evento.key == pygame.K_l:
                try:
                    with open("melhor_carro_auto.pickle", "rb") as f:
                        cerebro_carregado = pickle.load(f)
                    for carro in carros:
                        carro.resetar(pista_atual)
                        carro.rede.pesos = [linha[:] for linha in cerebro_carregado.pesos]
                        carro.rede.bias = cerebro_carregado.bias[:]
                    
                    pista_concluida = False # Destrava a tela para o carro poder andar
                    print("-> Cérebro Supremo Carregado!")
                except FileNotFoundError:
                    print("Treine e vença uma pista primeiro!")

    if not pista_concluida:
        carros_vivos = 0
        carro_lider = None
        maior_fitness_atual = -1
        total_cps_pista = len(config.CHECKPOINTS.get(pista_atual, []))

        for carro in carros:
            if carro.vivo:
                carro.calcular_radares(fundo)
                carro.pensar_e_mover(pista_atual)
                carro.checar_colisao(fundo)
                carros_vivos += 1
                
                if carro.fitness > maior_fitness_atual:
                    maior_fitness_atual = carro.fitness
                    carro_lider = carro
                    
                # BLINDAGEM DE SALVAMENTO: Só salva se pisar no último checkpoint!
                if total_cps_pista > 0 and carro.checkpoints_passados >= total_cps_pista:
                    if not pista_concluida: 
                        with open("melhor_carro_auto.pickle", "wb") as f:
                            pickle.dump(carro.rede, f)
                        print(f"VITÓRIA! Cérebro da Geração {geracao} salvo com sucesso!")
                    pista_concluida = True
                    geracao_da_vitoria = geracao

        if carros_vivos == 0 and not pista_concluida:
            evoluir_populacao()

    tela.blit(fundo, (0, 0))
    for cp in config.CHECKPOINTS.get(pista_atual, []):
        pygame.draw.circle(tela, (0, 100, 255), cp, 6, 2)
    
    for carro in carros:
        is_lider = (carro == carro_lider)
        carro.desenhar(tela, desenhar_radares=is_lider)
        
    if carro_lider and not pista_concluida:
        desenhar_painel_neural(tela, carro_lider)
    
    painel = [
        f"Pista: {pista_atual}",
        f"Geração: {geracao}",
        f"Vivos: {carros_vivos}/{config.TAMANHO_POPULACAO}",
        f"Score Líder: {maior_fitness_atual if maior_fitness_atual > 0 else 0}",
        "[L] Injetar Campeão"
    ]
    y = 20
    for linha in painel:
        tela.blit(fonte.render(linha, True, (255, 255, 0)), (20, y))
        y += 22
        
    if pista_concluida:
        sombreado = pygame.Surface((config.LARGURA, config.ALTURA), pygame.SRCALPHA)
        sombreado.fill((0, 0, 0, 180))
        tela.blit(sombreado, (0, 0))
        
        texto_sucesso = fonte_vitoria.render(f"🏆 PISTA {pista_atual} COMPLETADA!", True, (0, 255, 100))
        texto_geracao = fonte_vitoria.render(f"Demorou {geracao_da_vitoria} gerações.", True, (255, 255, 255))
        texto_dica = fonte.render("Pressione 1, 2 ou 3 para ir para outra pista.", True, (200, 200, 200))
        
        tela.blit(texto_sucesso, (config.LARGURA // 2 - texto_sucesso.get_width() // 2, config.ALTURA // 2 - 50))
        tela.blit(texto_geracao, (config.LARGURA // 2 - texto_geracao.get_width() // 2, config.ALTURA // 2 + 10))
        tela.blit(texto_dica, (config.LARGURA // 2 - texto_dica.get_width() // 2, config.ALTURA // 2 + 80))

    pygame.display.flip()

pygame.quit()
sys.exit()