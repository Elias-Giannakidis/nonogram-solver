import pygame as pg
import numpy as np
import nonoGram2 as puzzle

columns = 30
rows = 30

columnConstrains = puzzle.columnConstrains;
rowConstrains = puzzle.rowConstrains


def makeFirstLine(constrains, length):
    line = []
    sum = 0
    for num in constrains:
        for _ in range(num):
            sum = sum + 1
            line.append(1)
        sum = sum + 1
        if(sum < length + 1):
            line.append(0)
    for _ in range(length - sum):
        line.append(0)
    return line

def getFreePoints(line):
    freePoints = 0
    for num in line:
        freePoints = freePoints + 1 - num * (freePoints + 1)
    return freePoints + 1

def countNumbers(line):
    numbers = 0
    newLine = True
    for num in line:
        if newLine and num == 1:
            numbers = numbers + 1
            newLine = False
        if num == 0:
            newLine = True
    return numbers


def getSpaces(numbers, freePoints):
    spaces = []
    for freePoint in range(freePoints):
        spaces.append([freePoint])

    for _ in range(numbers - 1):
        copySpaces = spaces.copy()
        spaces = []
        for space in copySpaces:
            space.reverse()
            freePoint = space[0]
            space.reverse()
            for i in range(freePoint + 1):
                newSpace = space.copy()
                newSpace.append(i)
                spaces.append(newSpace)

    for space in spaces:
        space.reverse()
    return spaces

def transformLine(space, line, length):
    trLine = line.copy()
    trLine.reverse()
    newLine = []
    newSpace = space.copy()
    newSpace.reverse()
    newSpace.append(0)
    onNumber = False
    pos = 0
    for i in range(length):
        move = newSpace[pos]
        if (i + move < length):
            newLine.append(trLine[i + move])
            trLine[i + move] = 0
        else:
            newLine.append(0)
        if (newLine[i] == 1):
            onNumber = True
        if (onNumber and newLine[i] == 0):
            onNumber = False
            pos = pos + 1
    newLine.reverse()
    return newLine

def getPosLines(constrains, length):
    lines = []
    line = makeFirstLine(constrains, length)
    numbers = countNumbers(line)
    freePoints = getFreePoints(line)
    spaces = getSpaces(numbers, freePoints)
    for space in spaces:
        newLine = transformLine(space, line, length)
        lines.append(newLine)
    return lines

def getLinesToAdd(lineLists, length):
    linesToAdd = []
    for lineList in lineLists:
        iniLine = np.zeros(length)
        count = 0
        for line in lineList:
            count = count + 1
            for i in range(length):
                iniLine[i] = iniLine[i] + line[i]

        for i in range(length):
            if (iniLine[i] < 1):
                iniLine[i] = -1
            if (iniLine[i] > 0 and iniLine[i] < count):
                iniLine[i] = 0
            if (iniLine[i] == count):
                iniLine[i] = 1

        linesToAdd.append(iniLine)
    return linesToAdd

def mergeLinesToBoard(board, columnsToAdd, columns, rowsToAdd, rows):
    for i in range(rows):
        for j in range(columns):
            if (columnsToAdd[j][i] == 1 or rowsToAdd[i][j] == 1):
                board[i][j] = 1
            if (columnsToAdd[j][i] == -1 or rowsToAdd[i][j] == -1):
                board[i][j] = -1
    return board

def checkIfSolved(board):
    for line in board:
        for box in line:
            if box == 0:
                return False
    return True


def main():

    board = np.zeros((rows, columns))

    columnLines = []
    for constrains in columnConstrains:
        newLine = getPosLines(constrains, rows)
        columnLines.append(newLine)

    rowLines = []
    for constrains in rowConstrains:
        newLine = getPosLines(constrains, columns)
        rowLines.append(newLine)

    epoch = 0
    solved = False
    while not solved:
        epoch = epoch + 1
        print(epoch)
        columnsToAdd = getLinesToAdd(columnLines, rows)
        rowsToAdd = getLinesToAdd(rowLines, columns)

        board = mergeLinesToBoard(board, columnsToAdd, columns, rowsToAdd, rows)

        # --- Test section ----

        for j in range(columns):
            boardColumn = []
            for i in range(columns):
                boardColumn.append(board[i][j])

            columnLine = columnLines[j]

            newColumnLine = columnLine.copy()
            columnLine = []

            for line in newColumnLine:
                add = True
                for i in range(rows):
                    if(boardColumn[i] == 1 and line[i] == 0):
                        add = False
                    if(boardColumn[i] == -1 and line[i] == 1):
                        add = False
                if(add):
                    columnLine.append(line)

            columnLines[j] = columnLine

        for j in range(rows):
            boardRow = []
            for i in range(rows):
                boardRow.append(board[j][i])

            rowLine = rowLines[j]

            newRowLine = rowLine.copy()
            rowLine = []

            for line in newRowLine:
                add = True
                for i in range(rows):
                    if(boardRow[i] == 1 and line[i] == 0):
                        add = False
                    if(boardRow[i] == -1 and line[i] == 1):
                        add = False
                if(add):
                    rowLine.append(line)

            rowLines[j] = rowLine

        solved = checkIfSolved(board)

    return board


if __name__ == '__main__':
    board = main()

    WIDTH = 1000
    HEIGHT = 1000
    BACKGROUND = pg.color.THECOLORS.get("antiquewhite")
    BLACK = pg.color.THECOLORS.get("black")
    RED = pg.color.THECOLORS.get("white")
    win = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Nonogram solver !!!")
    win.fill(BACKGROUND)

    run = True
    while run:
        # ----- catch events ----- #
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        # ----- catch events ----- #

        # ----- Draw the Board ----- #
        zeroPoint = 5
        thick = 2
        width = 25
        boxWidth = 25 * (columns) + thick
        boxHeight = 25 * (rows) + thick
        pg.draw.rect(win, BLACK, [zeroPoint - thick / 2, zeroPoint - thick / 2, boxWidth, boxHeight])
        for i in range(columns):
            for j in range(rows):
                x = zeroPoint + i * width
                y = zeroPoint + j * width
                boxWidth = width - 2 * thick
                if (board[j][i] == 0):
                    pg.draw.rect(win, BACKGROUND, [x + thick, y + thick, boxWidth, boxWidth])
                if (board[j][i] == -1):
                    pg.draw.rect(win, RED, [x + thick, y + thick, boxWidth, boxWidth])
        # ----- Draw the Board ----- #

        pg.display.update()
        win.fill(BACKGROUND)
    pg.quit()


