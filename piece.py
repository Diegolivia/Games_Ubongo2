# primer valor es parte de la pieza, segundo valor si colisiona
import random
Plantilla = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             ]

P1 = [[9, 1, 9],
      [1, 1, 9],
      [1, 9, 9]]

P2 = [[1, 1, 9],
      [9, 1, 9],
      [9, 1, 9]]

P3 = [[1, 1, 9],
      [1, 1, 9],
      [1, 9, 9]]

P4 = [[9, 1, 1],
      [9, 1, 9],
      [1, 1, 9]]

P5 = [[1, 1, 9],
      [1, 1, 9],
      [9, 9, 9]]

P6 = [[9, 9, 9],
      [9, 1, 9],
      [1, 1, 1]]

P7 = [[1, 1, 9],
      [9, 1, 9],
      [9, 9, 9]]

P8 = [[9, 9, 9],
      [1, 1, 1],
      [9, 9, 9]]

arrPieces = [P1, P2, P3, P4, P5, P6, P7, P8]


#PiezaRandom = random.randrange(1, len(ContenedorPiezas)+1, 1)

"""
def Rotar(pieza):
    rotar = []
    for i in range(len(pieza[0])):
        rotar.append([])
        for j in range(len(pieza)):
            rotar[i].append(pieza[len(pieza)-1-j][i])
    return rotar
"""


def GenerarPlantilla(aP):
    arr_Piece = []
    arr_Plant = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 ]
    x = 0
    y = 0
    contPlaced = 0
    FailSafe = 0
    while contPlaced < 4:
        # Configura la primera pieza como una aleatoria
        currP = aP[random.randint(0, len(aP)-1)]
        Placed = False
        while not Placed:
            if(ColocarPieza(arr_Plant, x, y, currP)):
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
                print("Command took too long, restarting...")
                x = 0
                y = 0
                arrP = []
                contPlaced = 0
                FailSafe = 0
                Placed = False
                arr_Plant = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             ]
                break
    return arr_Plant
    pass


def ColocarPieza(arP, X, Y, piece):
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


arr_Templates = []
for x in range(36):
    arr_Templates.append(GenerarPlantilla(arrPieces))
print("done")
