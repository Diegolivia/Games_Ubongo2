import pyglet
from pyglet.window import key
from pyglet.window import FPSDisplay
from pyglet.window import mouse
from random import randint, choice
import random as rand
import linecache
import os
import sys

window = pyglet.window.Window(1600, 1024)
fps_display = FPSDisplay(window)
fps_display.label.font_size = 50
COUNTDOWN = int(1)

class Timer(object):
    def __init__(self, itb):
        self.sprTimer = pyglet.sprite.Sprite(itb, 340, 580)
        self.sprTimer.scale = 0.3
        self.start = '%s:00' % COUNTDOWN
        self.label = pyglet.text.Label(self.start, font_size=70,
                                       x=590, y=630,
                                       anchor_x='center', anchor_y='center')
        self.reset()

    def reset(self):
        self.time = COUNTDOWN * 60
        self.running = True
        self.label.text = self.start
        self.label.color = (255, 133, 82, 255)

    def update(self, dt):
        if self.running:
            self.time -= dt
            m, s = divmod(self.time, 60)
            self.label.text = '%02d:%02d' % (m, s)
            if m < 0:
                self.running = False
                self.label.text = 'STOP'

class Table:
    def __init__(self, numP, X, Y, imgTab, mtG, mtP, arrP):
        super().__init__()
        self.spr_Tab = pyglet.sprite.Sprite(imgTab, x=X, y=Y)
        self.numPlayer = numP
        self.arrP = ["A", "B", "C", "D"]
        self.row_Play = mtP
        self.arrPlayers = arrP
        #self.curr = self.arrPlayers[0]
        self.curr_Tab = []
        # Gemas
        self.row_Gem = mtG
        # Tablero
        self.mtx_Tab = []
        self.mtx_1stTab = []
        self.FillTablero()

    def FillTablero(self):
        log_Gem = [0, 0, 0, 0, 0, 0]
        for y in range(6):
            t = []
            # Genera las columnas para los jugadores
            for i in range(self.numPlayer):
                t.append(0)
            # Generador de gemas por fila (AGREGAR ALGORITMO DE COMPROBACION)
            for x in range(12):
                gem = True
                while gem:
                    g = rand.randint(1, 6)
                    if(log_Gem[g-1] < 12):
                        t.append(g)
                        log_Gem[g-1] += 1
                        prev = g
                        gem = False
            self.mtx_Tab.append(t)
        # Generador de personajes
        for p in range(self.numPlayer):
            self.mtx_Tab[1+p][p] = self.arrP[p]
        # Guardar las primeras dos columnas de gemas en un arreglo por separado
        for x in range(6):
            self.mtx_1stTab.append(
                [self.mtx_Tab[x][self.numPlayer], self.mtx_Tab[x][self.numPlayer+1], self.numPlayer])

    def Dibujar(self):
        self.spr_Tab.draw()
        # self.curr.Dibujar(self.row_Gem)
        for x in range(len(self.mtx_Tab)):
            for y in range(len(self.mtx_Tab[x])):
                curr = self.mtx_Tab[x][y]
                if(curr != 0):
                    if(type(curr) == str):
                        # Dibujar Jugadores
                        n = ord(curr)-65
                        var = pyglet.sprite.Sprite(
                            self.row_Play[n], 0+50*y, 685+57*x)
                        var.scale = 0.15
                        var.draw()
                        pass
                    else:
                        n = curr
                        # LAS GEMAS INICIAN EN X=280 Y=684
                        # Tamaño original Sprite 600*600 --> incremento +103x +57y
                        var = pyglet.sprite.Sprite(
                            self.row_Gem[n-1], 280+103*(y-self.numPlayer), 685+57*(x))
                        var.scale = 0.08
                        var.draw()

    # Mover al jugador actual, limpia la posicon actual y luego recoloca al jugador
    def MovePlayer(self, player, mov):
        self.curr = player
        self.mtx_Tab[player.Position][player.Turn] = 0
        player.UpdatePosition(mov)
        self.mtx_Tab[player.Position][player.Turn] = self.arrP[player.Color]
        self.ComerPiezas(player)

    # Cada jugador come las dos primeras piezas de la posicon donde se encuentra
    def ComerPiezas(self, player):
        i = self.mtx_1stTab[player.Position][2]
        if(i != 0 and i < 12+self.numPlayer):
            player.AgregarGema(self.mtx_Tab[player.Position][i])
            player.AgregarGema(self.mtx_Tab[player.Position][i+1])
            self.mtx_Tab[player.Position][i] = 0
            self.mtx_Tab[player.Position][i+1] = 0
            if(i+2 == 12+self.numPlayer):
                self.mtx_1stTab[player.Position] = [0, 0, 12+self.numPlayer]
            else:
                self.mtx_1stTab[player.Position] = [
                    self.mtx_Tab[player.Position][i+2], self.mtx_Tab[player.Position][i+3], i+2]
        pass

class Player:
    def __init__(self, turn, position, color):
        self.posMove = 0
        self.Turn = turn
        self.numMov = 0
        self.Color = color
        self.Position = position
        self.Mochila = [0, 0, 0, 0, 0, 0]

    # La mochila esta ordenada de 1 a 6 segun el color de la gema(el numero de la gema)
    def AgregarGema(self, gem):
        self.Mochila[gem-1] += 1

    def getMov(self):
        return self.numMov

    # Actualiza la posicion del jugador dentro del arreglo
    def UpdatePosition(self, mov):
        if(self.Position+mov < 0 or self.Position+mov > 5):
            pass
        else:
            self.Position += mov

    def SetMovimientos(self, num):
        self.numMov += num

    # Devuelve un arreglo de [tipo de gema, # de gemas] sobre la gema que mas tiene
    def MaximoGemas(self):
        max = 0
        geM = 0
        for i in range(6):
            if(self.Mochila[i] > max):
                max = self.Mochila[i]
                geM = i
        return [geM, max]

    def Dibujar(self, mtxGems):
        for x in range(len(self.Mochila)):
            currG = pyglet.sprite.Sprite(mtxGems[x], 899+52*x, 80)
            label = pyglet.text.Label(text=str(
                self.Mochila[x]), font_name='Times New Roman', font_size=25, x=900+52*x, y=45)
            currG.scale = 0.05
            currG.draw()
            label.draw()
        pass

class AIPlayer(Player):
    def __init__(self, turn, position, color, diff):
        self.Difficulty = diff
        self.Buscar = [0, 0]
        Player.__init__(self, turn, position, color)

    def DefinirBusqueda(self):
        pass

    def DecidirMovimiento(self):
        pass

class Dice:
    def __init__(self, iDice, mtDadCar):
        self.imgDice = iDice
        self.mtx_Caras = mtDadCar
        self.currCara = 2

    def TirarDice(self):
        g = rand.randint(2, 7)
        while g == self.currCara:
            g = rand.randint(2, 7)
        self.currCara = g
        pass

    def Dibujar(self):
        sprDice = pyglet.sprite.Sprite(self.imgDice, 50, 480)
        sprDice.scale = 0.08
        sprFace = pyglet.sprite.Sprite(self.mtx_Caras[self.currCara], 53, 478)
        sprFace.scale = 0.35
        sprDice.draw()
        sprFace.draw()
        pass

class MiniGame:
    def __init__(self,mPZ):
        #Crea y Carga las Piezas con las que se construira las plantillas
        self.arr_Pieces = []
        self.LoadPieces()
        #Carga las imagenes para poder dibujar los objetos
        self.arr_img_Piezas = mPZ
        #Genera las Plantillas utilizando las piezas entregadas
        self.GenerateTemplate()
        #Carga la plantilla Actual Para Jugar
        #Del arreglo: currMinigame[0]=template currMinigame[1]=array de Piezas
        self.currMinigame = []
        self.LoadTemplate(1)
        pass

    def LoadPieces(self):
        x = "res/data/Pieces.txt"
        with open(x) as f:
            content = f.read().splitlines()
            for l in content:
                l = l.strip().split('.')
                for x in range(len(l)):
                    l[x] = list(map(int, l[x].split(',')))
                self.arr_Pieces.append(l)
        pass

    def LoadTemplate(self,turno):
        txtTemplate = "res/data/Plantilla.txt"
        txtPieces = "res/data/PlantillaPieces.txt"
        self.currMinigame=[]
        l=linecache.getline(txtTemplate,turno)
        l=l.strip().split('.')
        for x in range(len(l)):
            l[x]=list(map(int,l[x].split(',')))
        pass
        self.currMinigame.append(l)
        a=linecache.getline(txtPieces,turno)
        a=a.strip().split('/')
        for x in range(len(a)):
            a[x]=a[x].split('.')
            for y in range(len(a[x])):
                a[x][y]=list(map(int,a[x][y].split(',')))
        self.currMinigame.append(a)
        pass

    def GenerarPlantilla(self, aP):
        arr_Piece = []
        arr_Plant = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        x = 0
        y = 0
        contPlaced = 0
        FailSafe = 0
        while contPlaced < 4:
            # Configura la primera pieza como una aleatoria
            currP = aP[rand.randint(0, len(aP)-1)]
            Placed = False
            while not Placed:
                if(self.ColocarPieza(arr_Plant, x, y, currP)):
                    Placed = True
                    contPlaced += 1
                    arr_Piece.append(currP)
                if(x >= 3):
                    x = 0
                    y += 1
                if(y >= 3):
                    y = 0
                    x += 1
                y += 1
                FailSafe += 1
                if(FailSafe >= 20):
                    # Si demora mas de 20 iteraciones, es irresolvible
                    # Asi que se resetea y vuelve a generar
                    x = 0
                    y = 0
                    arrP = []
                    contPlaced = 0
                    FailSafe = 0
                    Placed = False
                    arr_Plant = [
                                [0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0]
                    ]
                    arr_Piece = []
                    break
        return [arr_Plant, arr_Piece]
        pass

    def ColocarPieza(self, arP, X, Y, piece):
        snapshot = arP[Y:Y+3]
        for i in range(len(snapshot)):
            snapshot[i] = snapshot[i][X:X+3]

        Available = True
        for yP in range(len(piece)):
            for xP in range(len(piece[yP])):
                if(piece[yP][xP] == 1):
                    if(snapshot[yP][xP] == piece[yP][xP]):
                        Available = False
                        break
            pass

        if(Available):
            for yP in range(len(piece)):
                for xP in range(len(piece[yP])):
                    if(piece[yP][xP] == 1):
                        arP[Y+yP][X+xP] = piece[yP][xP]
            return True
        else:
            return False

    def GenerateTemplate(self):
        with open("res/data/Plantilla.txt", "w") as f:
            with open("res/data/PlantillaPieces.txt", "w") as fP:
                for x in range(36):
                    a = self.GenerarPlantilla(self.arr_Pieces)
                    Temp = a[0]
                    TempP = a[1]
                    for row in range(len(Temp)-1):
                        line = list(map(str, Temp[row]))
                        f.write(",".join(line) + ".")
                    f.write(",".join(list(map(str, Temp[len(Temp)-1])))+"\n")
                    # Navegar por un arreglo de arreglos
                    for piece in TempP[:len(TempP)-1]:
                        for row in piece[:len(piece)-1]:
                            line = list(map(str, row))
                            fP.write(",".join(line)+".")
                        fP.write(",".join(list(map(str, piece[len(piece)-1])))+"/")
                    for pieceF in TempP[len(TempP)-1][:2]:
                        line = list(map(str, pieceF))
                        fP.write(",".join(line)+".")
                    line = list(map(str, TempP[len(TempP)-1][2]))
                    fP.write(",".join(line)+"\n")
                pass

    def Dibujar(self):
        mx=self.currMinigame[0]
        for x in range(len(mx)):
            for y in range(len(mx)):
                f=pyglet.sprite.Sprite(self.arr_img_Piezas[mx[y][x]],1260+50*x,600-60*y)
                f.scale_y=0.6
                f.scale_x=0.5
                f.draw()
        ap=self.currMinigame[1]
        PieceX=850
        PieceY=600
        for curr in range(len(ap)):
            for x in range(len(ap[curr])):
                for y in range(len(ap[curr])):
                    if(ap[curr][y][x]==1):
                        f=pyglet.sprite.Sprite(self.arr_img_Piezas[2],PieceX+50*x,PieceY-60*y)
                        f.scale_y=0.6
                        f.scale_x=0.5
                        f.draw()
            if(curr==0 or curr==2):
                PieceX+=160
            elif curr==1:
                PieceX=850
                PieceY-=190

            
        pass
    
    def Revisar(self):
        #Comprobar si ganaste
        pass

class GameEngine:
    def __init__(self, nPl, nHu, mG, mP, mPH, mD,mPZ, iTab, iDice, iTesoro, iButton,iTimer,iMenu):
        super().__init__()
        #GameState=0 es menu, GameState=1 es jugando
        self.GameState=0
        self.Ronda = 0
        self.Turno = 0
        self.numMinigame=1
        # Setup de Jugadores
        self.numPlayers = nPl
        self.numHuman = nHu
        self.numAI = nPl-nHu
        self.arrPlayers = []
        self.mtxPH = []
        self.mtxP = []
        self.PopulatePlayers(mP, mPH)
        # Visualizador de Stats
        self.lblRonda = pyglet.text.Label('RONDA: '+str(self.Ronda),
                                          font_name='Times New Roman',
                                          font_size=30,
                                          x=430, y=530)
        self.lblTurn = pyglet.text.Label('TURNO: '+str(self.Turno),
                                         font_name='Times New Roman',
                                         font_size=30,
                                         x=410, y=470)
        self.lblMov = pyglet.text.Label('Movimientos Disponibles: '+str(self.arrPlayers[self.Turno].numMov),
                                        font_name='Times New Roman',
                                        font_size=30,
                                        x=360, y=400)
        self.lblTurnH = pyglet.sprite.Sprite(
            self.mtxPH[self.Turno], x=600, y=460)
        self.lblTurnH.scale = 0.06
        self.mtxGem = mG
        # Dado
        self.objDice = Dice(iDice, mD)
        # Tesoro
        self.sprTesoro = pyglet.sprite.Sprite(iTesoro, 980, 120)
        self.sprTesoro.scale = 0.12
        # Boton
        self.sprButton = pyglet.sprite.Sprite(iButton, 350, 70)
        self.sprButton.scale = 0.2
        # Tablero --> Tamaño del Table --> 1601*346 aprox
        self.objTable = Table(nPl, 0, 679, iTab, mG,
                              self.mtxP, self.arrPlayers)
        #Minigame-Piezas
        self.objMinigame = MiniGame(mPZ)
        #Timer
        self.timer = Timer(iTimer)
        #Arreglo para el minijuego
        self.arr_Play_Timer=[0,0,0,0]
        #Menu
        self.sprMenu=pyglet.sprite.Sprite(iMenu)

    def PopulatePlayers(self, mP, mPH):
        for i in range(self.numHuman):
            self.arrPlayers.append(Player(i, i+1, i))
        for i in range(self.numAI):
            self.arrPlayers.append(
                AIPlayer(self.numHuman+i, self.numHuman+i+1, self.numHuman+i, 1))
        c = 1
        for x in self.arrPlayers:
            if(type(x) == AIPlayer):
                self.mtxP.append(mP[0])
                self.mtxPH.append(mPH[0])
            else:
                self.mtxP.append(mP[c])
                self.mtxPH.append(mPH[c])
                c += 1
        pass

    def Dibujar(self):
        if(self.GameState==0):
            self.sprMenu.draw()
            pass
        else:
            # Tablero
            self.objTable.Dibujar()
            # Dado
            self.objDice.Dibujar()
            # Ubongo boton
            self.sprButton.draw()
            # Mochila
            self.sprTesoro.draw()
            self.arrPlayers[self.Turno].Dibujar(self.mtxGem)
            # Visualizador
            self.lblRonda.draw()
            self.lblTurn.draw()
            self.lblMov.draw()
            self.lblTurnH.draw()
            #Minijuego
            self.objMinigame.Dibujar()
            #Timer
            self.timer.sprTimer.draw()
            self.timer.label.draw()
            if(not self.timer.running):
                self.PerderTurno()

    def UpdateLabels(self):
        self.lblRonda.text = 'RONDA: '+str(self.Ronda)
        self.lblTurn.text = 'TURNO: '+str(self.Turno)
        self.lblMov.text = 'Movimientos Disponibles: ' + \
            str(self.arrPlayers[self.Turno].numMov)
        self.lblTurnH.image = self.mtxPH[self.Turno]

    def SetTurno(self, turn):
        if(turn <= self.numPlayers-1):
            self.Turno = turn
            self.arrPlayers[turn].SetMovimientos(1)
            self.UpdateLabels()

    def MoverPersonaje(self, mov):
        if(self.arrPlayers[self.Turno].numMov != 0):
            self.objTable.MovePlayer(self.arrPlayers[self.Turno], mov)
            self.arrPlayers[self.Turno].numMov -= 1
            self.UpdateLabels()
        pass

    def CambiarRonda(self):
        self.Ronda+=1
        self.Turno=0
        mov=3
        for au in range(3):
            may=0
            aux=0
            for x in range(self.numPlayers):
                if(self.arr_Play_Timer[x]>may):
                    may=self.arr_Play_Timer[x]
                    aux=x
            self.arr_Play_Timer[aux]=0
            self.arrPlayers[aux].SetMovimientos(mov)
            if(mov!=0):
                mov-=1
        self.arr_Play_Timer = [0,0,0,0]
        pass

    def GanarTurno(self):
        self.arr_Play_Timer[self.Turno]=self.timer.time
        self.RotarTurno()
        pass

    def PerderTurno(self):
        self.arr_Play_Timer[self.Turno]=0
        self.RotarTurno()

    def RotarTurno(self):
        self.objDice.TirarDice();
        self.Turno+=1
        self.numMinigame+=1
        if(self.numMinigame>36):
            self.numMinigame=0
        if(self.Turno==self.numPlayers):
            self.CambiarRonda()
        self.objMinigame.LoadTemplate(self.numMinigame)
        self.UpdateLabels()
        self.timer.reset()
        pass
    
    def iniciarGame(self):
        self.GameState=1

    def Revisar(self):
        pass

# Cargar Las imagenes ---> Modificar para cargar un res library
imgBackground = pyglet.image.load('res\img\Background.png')
# Tamaño original Table 1801*608
imgTable = pyglet.image.load('res\img\Piezas\TableroRefix.png')
# Tamaño original Sprite 600*600 --> incremento +103x +57y
imgGem1 = pyglet.image.load('res\img\Gem1.png')
imgGem2 = pyglet.image.load('res\img\Gem2.png')
imgGem3 = pyglet.image.load('res\img\Gem3.png')
imgGem4 = pyglet.image.load('res\img\Gem4.png')
imgGem5 = pyglet.image.load('res\img\Gem5.png')
imgGem6 = pyglet.image.load('res\img\Gem6.png')
imgPlayer1 = pyglet.image.load('res\img\Players\Player1.png')
imgPlayer2 = pyglet.image.load('res\img\Players\Player2.png')
imgPlayer3 = pyglet.image.load('res\img\Players\Player3.png')
imgPlayer4 = pyglet.image.load('res\img\Players\Player4.png')
imgPlayer5 = pyglet.image.load('res\img\Players\Player5.png')
imgPlayer1Head = pyglet.image.load('res\img\Players\Player1Head.png')
imgPlayer2Head = pyglet.image.load('res\img\Players\Player2Head.png')
imgPlayer3Head = pyglet.image.load('res\img\Players\Player3Head.png')
imgPlayer4Head = pyglet.image.load('res\img\Players\Player4Head.png')
imgPlayer5Head = pyglet.image.load('res\img\Players\Player5Head.png')
imgTesoro = pyglet.image.load('res\img\Tesoro.png')
imgDice = pyglet.image.load('res\img\Dado\Dado.png')
imgSide1 = pyglet.image.load('res\img\Dado\Dado1.png')
imgSide2 = pyglet.image.load('res\img\Dado\Dado2.png')
imgSide3 = pyglet.image.load('res\img\Dado\Dado3.png')
imgSide4 = pyglet.image.load('res\img\Dado\Dado4.png')
imgSide5 = pyglet.image.load('res\img\Dado\Dado5.png')
imgSide6 = pyglet.image.load('res\img\Dado\Dado6.png')
imgSide7 = pyglet.image.load('res\img\Dado\Dado7.png')
imgSide8 = pyglet.image.load('res\img\Dado\Dado8.png')
imgButton = pyglet.image.load('res\img\Button.png')
imgTimer = pyglet.image.load('res\img\Timer.png')
imgPiezaNegra = pyglet.image.load('res\img\Piezas\PiezaNegra.png')
imgPiezaBlanca = pyglet.image.load('res\img\Piezas\PiezaBlanca.png')
imgPiezaRoja = pyglet.image.load('res\img\Piezas\PiezaRoja.png')
imgMenu=pyglet.image.load('res\img\Main.png')

mtx_Gem = [imgGem1, imgGem2, imgGem3, imgGem4, imgGem5, imgGem6]
mtx_Player = [imgPlayer5, imgPlayer1, imgPlayer3, imgPlayer4, imgPlayer2]
mtx_Dice = [imgSide1, imgSide5, imgSide2, imgSide3,
            imgSide4, imgSide6, imgSide7, imgSide8]
mtx_PlayerHead = [imgPlayer5Head, imgPlayer1Head,
                  imgPlayer3Head, imgPlayer4Head, imgPlayer2Head]
mtx_Piezas = [imgPiezaNegra,imgPiezaBlanca,imgPiezaRoja]

sprBck = pyglet.sprite.Sprite(imgBackground, 0, 0)
engine = GameEngine(4, 4, mtx_Gem, mtx_Player, mtx_PlayerHead, mtx_Dice,mtx_Piezas,
                    imgTable, imgDice, imgTesoro, imgButton,imgTimer,imgMenu)

clock = pyglet.clock.Clock()

def draw_rect(x, y, width, height):
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
        ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]))

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        engine.MoverPersonaje(1)
    elif symbol == key.S:
        engine.MoverPersonaje(-1)
    elif symbol == key.P:
        engine.PerderTurno()
    elif symbol == key.O:
        engine.GanarTurno()

@window.event
def on_draw():
    window.clear()
    sprBck.draw()
    engine.Dibujar()
    fps_display.draw()
    
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT and engine.GameState==1:
        if((x>=350 and x<=820) and (y>=70 and y<=220)):
            engine.GanarTurno()
    if button == mouse.LEFT and engine.GameState==0:
        if((x>=350 and x<=920) and (y>=100 and y<=420)):
            engine.iniciarGame()
pyglet.clock.schedule_interval(engine.timer.update, 1)
pyglet.app.run()
