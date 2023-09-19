from random import *
from math import *

class dMap:
    def __init__(self):
        self.salaList = []
        self.cList = []

    def makeMap(self, xsize, ysize, falha, b1, msalas):
        """Gerador de layout de salas e corredores"""
        # makeMap pode ser modificado para aceitar argumentos para valores de falha e percentil de recursos.
        # Cria a primeira sala
        self.size_x = xsize
        self.size_y = ysize
        # Inicializa o mapa com todas as paredes
        self.coordmapa = []
        for y in range(ysize):
            tmp = []
            for x in range(xsize):
                tmp.append(1)
            self.coordmapa.append(tmp)

        w, l, t = self.makeSala()
        while len(self.salaList) == 0:
            y = randrange(ysize - 1 - l) + 1
            x = randrange(xsize - 1 - w) + 1
            p = self.placeSala(l, w, x, y, xsize, ysize, 6, 0)
        falhou = 0
        while falhou < falha:  # Quanto menor o valor de falha, menor o tamanho do calabouço
            escolheSala = randrange(len(self.salaList))
            ex, ey, ex2, ey2, et = self.makeExit(escolheSala)
            recurso = randrange(100)
            if recurso < b1:  # Escolha de recurso (mais recursos podem ser adicionados aqui)
                w, l, t = self.makeCorridor()
            else:
                w, l, t = self.makeSala()
            salaConcluida = self.placeSala(l, w, ex2, ey2, xsize, ysize, t, et)
            if salaConcluida == 0:  # Se a colocação falhar, aumenta a possibilidade de o mapa estar cheio
                falhou += 1
            elif salaConcluida == 2:  # Possibilidade de ligar salas
                if self.coordmapa[ey2][ex2] == 0:
                    if randrange(100) < 7:
                        self.makePortal(ex, ey)
                    falhou += 1
            else:  # Caso contrário, liga as duas salas
                self.makePortal(ex, ey)
                falhou = 0
                if t < 5:
                    tc = [len(self.salaList) - 1, ex2, ey2, t]
                    self.cList.append(tc)
                    self.joinCorridor(len(self.salaList) - 1, ex2, ey2, t, 50)
            if len(self.salaList) == msalas:
                falhou = falha
        self.finalJoins()

    def makeSala(self):
        """Produz tamanho aleatório de sala"""
        rtype = 5
        rwide = randrange(8) + 3
        rlong = randrange(8) + 3
        return rwide, rlong, rtype

    def makeCorridor(self):
        """Produz aleatoriamente o comprimento e a direção do corredor"""
        comprimento_corredor = randrange(18) + 3
        direcao = randrange(4)
        if direcao == 0:  # Norte
            wd = 2
            lg = -comprimento_corredor
        elif direcao == 1:  # Leste
            wd = comprimento_corredor
            lg = 2
        elif direcao == 2:  # Sul
            wd = 2
            lg = comprimento_corredor
        elif direcao == 3:  # Oeste
            wd = -comprimento_corredor
            lg = 2
        return wd, lg, direcao

    def placeSala(self, ll, ww, xposs, yposs, xsize, ysize, rty, ext):

        # Organiza a direção
        xpos = xposs
        ypos = yposs
        if ll < 0:
            ypos += ll + 1
            ll = abs(ll)
        if ww < 0:
            xpos += ww + 1
            ww = abs(ww)
        # Faz o deslocamento se o tipo for sala
        if rty == 5:
            if ext == 0 or ext == 2:
                offset = randrange(ww)
                xpos -= offset
            else:
                offset = randrange(ll)
                ypos -= offset
        # Em seguida, verifica se há espaço
        podeColocar = 1
        if ww + xpos + 1 > xsize - 1 or ll + ypos + 1 > ysize:
            podeColocar = 0
            return podeColocar
        elif xpos < 1 or ypos < 1:
            podeColocar = 0
            return podeColocar
        else:
            for j in range(ll):
                for k in range(ww):
                    if self.coordmapa[(ypos) + j][(xpos) + k] != 1:
                        podeColocar = 2
        # Se houver espaço, adiciona à lista de salas
        if podeColocar == 1:
            temp = [ll, ww, xpos, ypos]
            self.salaList.append(temp)
            for j in range(ll + 2):
                for k in range(ww + 2):
                    self.coordmapa[(ypos - 1) + j][(xpos - 1) + k] = 2
            for j in range(ll):
                for k in range(ww):
                    self.coordmapa[ypos + j][xpos + k] = 0
        return podeColocar

    def makeExit(self, rn):
        """Escolhe parede aleatória e ponto aleatório ao longo dessa parede"""
        sala = self.salaList[rn]
        while True:
            rw = randrange(4)
            if rw == 0:  # Parede Norte
                rx = randrange(sala[1]) + sala[2]
                ry = sala[3] - 1
                rx2 = rx
                ry2 = ry - 1
            elif rw == 1:  # Parede Leste
                ry = randrange(sala[0]) + sala[3]
                rx = sala[2] + sala[1]
                rx2 = rx + 1
                ry2 = ry
            elif rw == 2:  # Parede Sul
                rx = randrange(sala[1]) + sala[2]
                ry = sala[3] + sala[0]
                rx2 = rx
                ry2 = ry + 1
            elif rw == 3:  # Parede Oeste
                ry = randrange(sala[0]) + sala[3]
                rx = sala[2] - 1
                rx2 = rx - 1
                ry2 = ry
            if self.coordmapa[ry][rx] == 2:  # Se o espaço for uma parede, sair
                break
        return rx, ry, rx2, ry2, rw

    def makePortal(self, px, py):
        """Cria portas nas paredes"""
        tipo_portal = randrange(100)
        if tipo_portal > 90:  # Porta secreta
            self.coordmapa[py][px] = 5
            return
        elif tipo_portal > 75:  # Porta fechada
            self.coordmapa[py][px] = 4
            return
        elif tipo_portal > 40:  # Porta aberta
            self.coordmapa[py][px] = 3
            return
        else:  # Buraco na parede
            self.coordmapa[py][px] = 0

    def joinCorridor(self, cno, xp, yp, ed, psb):
        """Verifica o ponto final do corredor e cria uma saída se ele se conectar a outra sala"""
        area_corredor = self.salaList[cno]
        if xp != area_corredor[2] or yp != area_corredor[3]:  # Encontra o ponto final do corredor
            endx = xp - (area_corredor[1] - 1)
            endy = yp - (area_corredor[0] - 1)
        else:
            endx = xp + (area_corredor[1] - 1)
            endy = yp + (area_corredor[0] - 1)
        verificaSaida = []
        if ed == 0:  # Corredor Norte
            if endx > 1:
                coords = [endx - 2, endy, endx - 1, endy]
                verificaSaida.append(coords)
            if endy > 1:
                coords = [endx, endy - 2, endx, endy - 1]
                verificaSaida.append(coords)
            if endx < self.size_x - 2:
                coords = [endx + 2, endy, endx + 1, endy]
                verificaSaida.append(coords)
        elif ed == 1:  # Corredor Leste
            if endy > 1:
                coords = [endx, endy - 2, endx, endy - 1]
                verificaSaida.append(coords)
            if endx < self.size_x - 2:
                coords = [endx + 2, endy, endx + 1, endy]
                verificaSaida.append(coords)
            if endy < self.size_y - 2:
                coords = [endx, endy + 2, endx, endy + 1]
                verificaSaida.append(coords)
        elif ed == 2:  # Corredor Sul
            if endx < self.size_x - 2:
                coords = [endx + 2, endy, endx + 1, endy]
                verificaSaida.append(coords)
            if endy < self.size_y - 2:
                coords = [endx, endy + 2, endx, endy + 1]
                verificaSaida.append(coords)
            if endx > 1:
                coords = [endx - 2, endy, endx - 1, endy]
                verificaSaida.append(coords)
        elif ed == 3:  # Corredor Oeste
            if endx > 1:
                coords = [endx - 2, endy, endx - 1, endy]
                verificaSaida.append(coords)
            if endy > 1:
                coords = [endx, endy - 2, endx, endy - 1]
                verificaSaida.append(coords)
            if endy < self.size_y - 2:
                coords = [endx, endy + 2, endx, endy + 1]
                verificaSaida.append(coords)
        for xxx, yyy, xxx1, yyy1 in verificaSaida:  # Percorre as saídas possíveis
            if self.coordmapa[yyy][xxx] == 0:  # Se se conectar a uma sala
                if randrange(100) < psb:  # Possibilidade de ligar as salas
                    self.makePortal(xxx1, yyy1)

    def finalJoins(self):
        """Estágio final, percorre todos os corredores para ver se algum pode ser conectado a outras salas"""
        for x in self.cList:
            self.joinCorridor(x[0], x[1], x[2], x[3], 10)


MAPA = []

startx = 24
starty = 14
omapa = dMap()
omapa.makeMap(startx, starty, 110, 50, 60)
for y in range(starty):
    linha = ""
    for x in range(startx):
        if omapa.coordmapa[y][x] == 0:
            linha += "0"
        if omapa.coordmapa[y][x] == 1:
            linha += "P"
        if omapa.coordmapa[y][x] == 2:
            linha += "P"
        if omapa.coordmapa[y][x] == 3 or omapa.coordmapa[y][x] == 4 or omapa.coordmapa[y][x] == 5:
            linha += "S"
    MAPA.append(linha)
    print(linha)
