import pygame

pygame.init()

# Decidindo uma fornte para colocar em uma superficie
fonte = pygame.font.Font('projeto/assets/fonts\Pixeltype.ttf', 50)

class Superficie:
# Uma superficie é a forma de inserir uma imagem no display. Aqui estou criando uma superficie de teste e dando uma cor a ela para que ela aparece contra o fundo preto
    sup_jogador = pygame.Surface((200,200))
    sup_jogador.fill('Red')
    sup_fundo = pygame.image.load('projeto/assets/background-placeholder.jpg')
    sup_fundo = pygame.transform.scale(sup_fundo, (800,800))
    sup_texto = fonte.render('JOGO MANEIRO', False, 'Black')
    def __init__(self) -> None:
        pass