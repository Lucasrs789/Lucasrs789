#Snake game on python
import pygame
import random


pygame.init()

pygame.display.set_caption('jogo snake python')

largura, altura = 1200, 800

tela = pygame.display.set_mode ((largura, altura))

relogio = pygame.time.Clock()

#cores    R    G    B
cinza = (160, 160, 160) #pontuation
branco = (255, 255, 255) #white wall
vermelho = (255, 0, 0) #fruit
green = (0, 255, 0) #snake

#snake

tamanho_quadrado = 20
game_speed = 10

#game 

def gerar_comida():
   comida_x = round(random.randrange (0, largura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
   comida_y = round(random.randrange (0, altura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
   return comida_x, comida_y

def desenhar_cobra (tamanho, pixels):
 for pixel in pixels:
   pygame.draw.rect (tela, green, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_comida (tamanho, comida_x, comida_y):
   pygame.draw.rect (tela, vermelho, [comida_x, comida_y, tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
   fonte = pygame.font.SysFont ('Roboto', 35)
   texto = fonte.render(f'Fruits: {pontuacao}', True, cinza)
   tela.blit(texto, [2, 2])
   
def selecionar_velocidade(tecla):
   if tecla == pygame.K_s:
      vx = 0
      vy = tamanho_quadrado
   elif tecla == pygame.K_w:
      vx = 0
      vy = - tamanho_quadrado
   elif tecla == pygame.K_d:
      vx = tamanho_quadrado
      vy = 0
   elif tecla == pygame.K_a:
      vx = - tamanho_quadrado
      vy = 0   
   return vx, vy


def rodar_jogo():   
    game_over = False
    x = largura /2
    y = altura /2

    vx = 0
    vy = 0

    tamanho_snake = 1
    pixels = []
    
    comida_x, comida_y = gerar_comida()

    while not game_over:

     tela.fill(branco)



     for evento in pygame.event.get():
           if evento.type == pygame.QUIT:
             game_over = True
           elif evento.type == pygame.KEYDOWN:
              vx, vy = selecionar_velocidade(evento.key)
              



     desenhar_comida(tamanho_quadrado,comida_x, comida_y)  
      
     pixels.append([x, y])
     if len(pixels) > tamanho_snake:
        del pixels[0] 

     for pixel in pixels[:-1]:
        if pixel == [x, y]:
           game_over = True  



     if x<0 or x> largura:
        game_over = True
     elif y<0 or y >altura:
        game_over = True

     x += vx
     y += vy
     desenhar_cobra(tamanho_quadrado, pixels)      

     desenhar_pontuacao (tamanho_snake - 1)


     pygame.display.update() 

     if x == comida_x and y == comida_y:
        tamanho_snake += 1
        comida_x, comida_y = gerar_comida()
         

     relogio.tick(game_speed)
rodar_jogo()
