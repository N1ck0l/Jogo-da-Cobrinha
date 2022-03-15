from ast import Global
import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

pygame.mixer.music.load('X2Download.com - Relaxing Zelda Ocarina of Time Music (64 kbps).mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

som_de_pontuação = pygame.mixer.Sound('smw_coin.wav')
som_de_pontuação.set_volume(1)

largura = 960
altura = 750
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da cobrinha')
relogio = pygame.time.Clock()

fonte = pygame.font.SysFont('arial', 30, True, True)
pontos = 0

cabeçaDaCobray = altura*3/4
cabeçaDaCobrax = largura*3/4
lista_cobra = list()
xvelocidadeDoJogador = 3
yvelocidadeDoJogador = 0
ladosDoQuadrado = 20
crescimento = 4
morreu = False

xmaçã = randint(5, largura - ladosDoQuadrado)
ymaçã = randint(5, altura - ladosDoQuadrado)

def reiniciar_jogo():
    global pontos, xmaçã, ymaçã, crescimento, morreu, cabeçaDaCobrax, cabeçaDaCobray, lista_cabeça, lista_cobra
    pontos = 0
    xmaçã = randint(5, largura - ladosDoQuadrado)
    ymaçã = randint(5, altura - ladosDoQuadrado)
    crescimento = 4
    morreu = False
    cabeçaDaCobray = altura*3/4
    cabeçaDaCobrax = largura*3/4
    lista_cabeça = []
    lista_cobra = []

def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], ladosDoQuadrado, ladosDoQuadrado))

while True:

    relogio.tick(60)
    tela.fill((255, 255, 255))
    pontuação = f'Pontos: {pontos}'
    pontos_formatado = fonte.render(pontuação, True, (0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_UP and yvelocidadeDoJogador != -3:
                yvelocidadeDoJogador = 3
                xvelocidadeDoJogador = 0
            elif event.key == K_DOWN and yvelocidadeDoJogador != 3:
                yvelocidadeDoJogador = -3
                xvelocidadeDoJogador = 0
            elif event.key == K_RIGHT and xvelocidadeDoJogador != 3:
                xvelocidadeDoJogador = -3
                yvelocidadeDoJogador = 0
            elif event.key == K_LEFT and xvelocidadeDoJogador != -3:
                xvelocidadeDoJogador = 3
                yvelocidadeDoJogador = 0

    cabeça_da_cobra = pygame.draw.rect(tela, (0, 255, 0), (cabeçaDaCobrax, cabeçaDaCobray, ladosDoQuadrado, ladosDoQuadrado))
    maçã = pygame.draw.rect(tela, (255, 0, 0), (xmaçã, ymaçã, ladosDoQuadrado, ladosDoQuadrado))

    cabeçaDaCobray -= yvelocidadeDoJogador
    cabeçaDaCobrax -= xvelocidadeDoJogador

    if cabeça_da_cobra.colliderect(maçã):
        pontos += 1
        xmaçã = randint(5, largura - ladosDoQuadrado)
        ymaçã = randint(5, altura - ladosDoQuadrado)
        crescimento += 2.5
        som_de_pontuação.play()

    lista_cabeça = list()
    lista_cabeça.append(cabeçaDaCobrax)
    lista_cabeça.append(cabeçaDaCobray)
    lista_cobra.append(lista_cabeça)
    
    if len(lista_cobra) > crescimento:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)
    
    if cabeçaDaCobrax + ladosDoQuadrado == largura or cabeçaDaCobray + ladosDoQuadrado > altura or cabeçaDaCobrax == 0 or cabeçaDaCobray < 0 or lista_cobra.count(lista_cabeça) > 1:
        morreu = True
        fonte2 = pygame.font.SysFont('arial', 50, True, True)

        while morreu:
            tela.fill((0, 0, 0))
            fim_de_jogo_formatado = fonte2.render('GAME OVER', True, (255, 0, 0))
            recomeçar_formatado = fonte.render('Precione r para recomeçar', True, (255, 0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()

            tela.blit(recomeçar_formatado, (largura//2 - 190, altura//2 + 50))
            tela.blit(fim_de_jogo_formatado, (largura//2 - 150, altura//2))
            pygame.display.flip()

    tela.blit(pontos_formatado, (50, 50))
    pygame.display.flip()
