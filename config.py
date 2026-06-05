# Configurações Globais do Simulador
LARGURA = 800
ALTURA = 600
TAMANHO_POPULACAO = 200

PISTAS = {
    "1": "pista1.png",
    "2": "pista2.png",
    "3": "pista3.png"
}

# Coordenadas realinhadas para o centro exato do novo asfalto
PONTOS_LARGADA = {
    "1": (400, 490),
    "2": (200, 100), 
    "3": (200, 100)  
}

# Checkpoints cirurgicamente posicionados no meio das novas pistas
CHECKPOINTS = {
    "1": [
        (550, 490), (690, 400), (690, 200), (550, 110), 
        (400, 110), (250, 110), (110, 200), (110, 400), (250, 490)
    ],
    "2": [
        (300, 100), (500, 100),             
        (650, 175),                         
        (500, 250), (300, 250),             
        (150, 325),                         
        (300, 400), (500, 400),             
        (650, 475),                         
        (500, 550), (200, 550)              
    ],
    "3": [
        (400, 100),                         
        (700, 300),                         
        (450, 500),                         
        (200, 375),                         
        (350, 250),                         
        (500, 325),                         
        (400, 400)                          
    ]
}