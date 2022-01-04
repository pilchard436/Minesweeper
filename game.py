import pygame
from pygame_textinput import *
import os
import sys
import time

from pygame.constants import K_DOWN, K_ESCAPE, K_UP, K_RETURN

from board import board
from piece import piece

MENUHEIGHT = 20
INFOHEIGHT = 50
OFFSETHEIGHT = MENUHEIGHT + INFOHEIGHT
MENUBUTTONWIDTH = 90

MAXSIZE = (16, 30)

class minesweeper:
    def __init__(self, dim: list, num_mine: int) -> None:
        self.dim = dim
        self.num_mine = num_mine
        self.hasRanWin = False
        self.hasRanWin = False
        self.isRunning = False
        self.isTimerRunning = False
        self.timeElapsed = 0
        pygame.init()

        # Each piece is 30 by 30 pixels
        self.pieceSize = 30, 30

    @property
    def sizeScreen(self):
        # Screen size is dependent on how many pieces we have
        return self.pieceSize[1] * self.dim[1], self.pieceSize[0] * self.dim[0] + OFFSETHEIGHT

    def displayText(self, font: pygame.font.Font, text: str, pos: tuple[int, int], color: tuple[int, int, int] = (0, 0, 0)):
        textt = font.render(text, True, color)
        self.screen.blit(textt, pos)

    @property
    def timer(self):
        if not self.isTimerRunning and self.isRunning:
            self.isTimerRunning = True
            self.startTime = time.time()
            return 0
        elif not self.isTimerRunning and not self.isRunning:
            return self.timeElapsed
        elif self.isTimerRunning and self.isRunning:
            self.timeElapsed = int(time.time() - self.startTime)
            return self.timeElapsed
        elif self.isTimerRunning and not self.isRunning:
            self.isTimerRunning = False
            self.timeElapsed = int(time.time() - self.startTime)
            return self.timeElapsed

    def options(self):
        # Initialize option menu
        # Set font
        font = pygame.font.Font('freesansbold.ttf', 16)
        # Make 3 text entry boxes. Row and col can only be <= 50
        rowManager = TextInputManager(initial=str(self.dim[0]), validator=lambda input: (
            input.isdigit() and int(input) <= MAXSIZE[0]) or input == "")
        colManager = TextInputManager(initial=str(self.dim[1]), validator=lambda input: (
            input.isdigit() and int(input) <= MAXSIZE[1]) or input == "")
        mineManager = TextInputManager(initial=str(
            self.num_mine), validator=lambda input: input.isdigit() or input == "")
        rowInput = TextInputVisualizer(manager=rowManager, font_object=font)
        colInput = TextInputVisualizer(manager=colManager, font_object=font)
        mineInput = TextInputVisualizer(manager=mineManager, font_object=font)

        # allow holding down key to enter or delete
        pygame.key.set_repeat(200, 25)

        textboxSelect = 0

        while True:
            self.screen.fill((255, 255, 255))

            # Display "Option" in the middle of the screen
            self.displayText(
                font, "Option", (self.sizeScreen[0] / 2 - font.size("Option")[0] / 2, 0))

            # Display "Height: "
            self.displayText(font, "Height: ", (0, 32))

            # Display "Width: "
            self.displayText(font, "Width: ", (0, 64))

            # Display "Number of mines: "
            self.displayText(font, "Number of mines: ", (0, 96))

            # Display textboxes for height width and mine
            self.screen.blit(rowInput.surface, (font.size("Height: ")[0], 32))
            self.screen.blit(colInput.surface, (font.size("Width: ")[0], 64))
            self.screen.blit(mineInput.surface,
                             (font.size("Number of mines: ")[0], 96))

            # Display OK Button + text "OK"
            okButton = pygame.Rect(
                (self.sizeScreen[0] / 2 - MENUBUTTONWIDTH, self.sizeScreen[1] - 100), (MENUBUTTONWIDTH, MENUHEIGHT))
            pygame.draw.rect(self.screen, (255, 0, 0), okButton)
            self.displayText(font, "OK", (self.sizeScreen[0] / 2 - MENUBUTTONWIDTH / 2 - font.size(
                "OK")[0] / 2, self.sizeScreen[1] - 100), (255, 255, 255))

            # Display Cancel Button + text "Cancel"
            cancelButton = pygame.Rect(
                (self.sizeScreen[0] / 2, self.sizeScreen[1] - 100), (MENUBUTTONWIDTH, MENUHEIGHT))
            pygame.draw.rect(self.screen, (0, 0, 128), cancelButton)
            self.displayText(font, "Cancel", (self.sizeScreen[0] / 2 + MENUBUTTONWIDTH / 2 - font.size(
                "Cancel")[0] / 2, self.sizeScreen[1] - 100), (255, 255, 255))

            # Determine which textbox to enter
            events = pygame.event.get()
            if textboxSelect == 0:
                rowInput.update(events)
            elif textboxSelect == 1:
                colInput.update(events)
            else:
                mineInput.update(events)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if (event.type == pygame.KEYDOWN and event.key == K_ESCAPE) or (event.type == pygame.MOUSEBUTTONDOWN and cancelButton.collidepoint(pygame.mouse.get_pos())):
                    return False

                # Logic for changing which textbox to enter
                elif event.type == pygame.KEYDOWN and event.key == K_UP:

                    # Disable cursor display for all 3 textboxes
                    rowInput.cursor_visible = False
                    colInput.cursor_visible = False
                    mineInput.cursor_visible = False

                    if textboxSelect > 0:
                        textboxSelect -= 1

                elif event.type == pygame.KEYDOWN and event.key == K_DOWN:

                    # Disable cursor display for all 3 textboxes
                    rowInput.cursor_visible = False
                    colInput.cursor_visible = False
                    mineInput.cursor_visible = False

                    if textboxSelect < 2:
                        textboxSelect += 1
                elif (event.type == pygame.MOUSEBUTTONDOWN and okButton.collidepoint(pygame.mouse.get_pos())) or (event.type == pygame.KEYDOWN and event.key == K_RETURN):
                    self.dim = [int(rowInput.value), int(colInput.value)]
                    self.num_mine = int(mineInput.value)
                    return True

            pygame.display.update()

    def loadPictures(self):
        self.images = {}
        imagesDirectory = "images"
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):
                continue
            path = imagesDirectory + r"/" + fileName
            img = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(
                img, (int(self.pieceSize[0]), int(self.pieceSize[1])))
            self.images[fileName.split(".")[0]] = img

    def state1(self):
        while True:
            print("state 1")
            self.screen = pygame.display.set_mode(self.sizeScreen)
            pygame.display.set_caption('Minesweeper')
            self.loadPictures()
            self.state2()

    def state2(self):
        print("state 2")
        menuFont = pygame.font.Font('freesansbold.ttf', 16)
        infoFont = pygame.font.Font('freesansbold.ttf', 50)
        self.optionButton = pygame.Rect((0, 0), (MENUBUTTONWIDTH, MENUHEIGHT))
        self.restartButton = pygame.Rect(
                (MENUBUTTONWIDTH, 0), (MENUBUTTONWIDTH, MENUHEIGHT))
        restart = False
        while not restart:
            self.screen.fill((255, 255, 255))

            # Display Option Button + text "Option"
            pygame.draw.rect(self.screen, (255, 0, 0), self.optionButton)
            self.displayText(menuFont, "Option", (MENUBUTTONWIDTH /
                            2 - menuFont.size("Option")[0] / 2, 0), (255, 255, 255))

            # Display Option Button + text "Option"
            pygame.draw.rect(self.screen, (0, 0, 128), self.restartButton)
            self.displayText(menuFont, "Restart", (3 * MENUBUTTONWIDTH /
                            2 - menuFont.size("Restart")[0] / 2, 0), (255, 255, 255))

            # Display remaining mine count
            self.displayText(infoFont, str(self.num_mine), (10, MENUHEIGHT + 5))

            # Display timer
            self.displayText(infoFont, str(0),
                            (self.sizeScreen[0] - infoFont.size(str(0))[0] - 10, MENUHEIGHT + 5))

            topLeft = (0, OFFSETHEIGHT)

            # Draw empty blocks
            for i in range(self.dim[0]):
                for j in range(self.dim[1]):
                    image = self.images["empty-block"]
                    self.screen.blit(image, topLeft)
                    topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
                topLeft = (0, topLeft[1] + self.pieceSize[1])
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.optionButton.collidepoint(pygame.mouse.get_pos()):
                    restart = self.options()
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[1] > OFFSETHEIGHT:
                    # Figure out which piece the player clicked, generate board, click that piece, start the game
                    pos = pygame.mouse.get_pos()
                    row = int((pos[1] - OFFSETHEIGHT) // self.pieceSize[1])
                    col = int(pos[0] // self.pieceSize[0])
                    self.board = board(self.dim, self.num_mine, (row, col))
                    self.clickPiece(pygame.mouse.get_pos(), False)
                    self.startTime = time.time()
                    self.running()
                    restart = True
            pygame.display.update()

    def running(self):
        print("state running")
        self.isRunning = True
        restart = False
        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and not (self.board.hasWon or self.board.hasLost) and pygame.mouse.get_pos()[1] > OFFSETHEIGHT:
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    self.clickPiece(pygame.mouse.get_pos(), rightClick)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.optionButton.collidepoint(pygame.mouse.get_pos()):
                    restart = self.options()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.restartButton.collidepoint(pygame.mouse.get_pos()):
                    restart = True

            self.drawGame()  # Display game
            pygame.display.update()
            if self.board.hasWon:
                self.win()
                self.isRunning = False
                self.state4()
                restart = True

            if self.board.hasLost:
                self.lost()
                self.isRunning = False
                self.state4()
                restart = True


    def state4(self):
        print("state 4")
        restart = False
        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.optionButton.collidepoint(pygame.mouse.get_pos()):
                    restart = self.options()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.restartButton.collidepoint(pygame.mouse.get_pos()):
                    restart = True

            self.drawGame()  # Display game
            pygame.display.update()

    def drawGame(self):
        self.screen.fill((255, 255, 255))
        menuFont = pygame.font.Font('freesansbold.ttf', 16)
        infoFont = pygame.font.Font('freesansbold.ttf', 50)

        # Display Option Button + text "Option"
        self.optionButton = pygame.Rect((0, 0), (MENUBUTTONWIDTH, MENUHEIGHT))
        pygame.draw.rect(self.screen, (255, 0, 0), self.optionButton)
        self.displayText(menuFont, "Option", (MENUBUTTONWIDTH /
                         2 - menuFont.size("Option")[0] / 2, 0), (255, 255, 255))

        # Display Option Button + text "Option"
        self.restartButton = pygame.Rect(
            (MENUBUTTONWIDTH, 0), (MENUBUTTONWIDTH, MENUHEIGHT))
        pygame.draw.rect(self.screen, (0, 0, 128), self.restartButton)
        self.displayText(menuFont, "Restart", (3 * MENUBUTTONWIDTH /
                         2 - menuFont.size("Restart")[0] / 2, 0), (255, 255, 255))

        # Display remaining flag count
        self.displayText(infoFont, str(
            self.board.remainingMine), (10, MENUHEIGHT + 5))

        # Display timer
        timeElapsed = str(self.timer)
        self.displayText(infoFont, timeElapsed,
                         (self.sizeScreen[0] - infoFont.size(timeElapsed)[0] - 10, MENUHEIGHT + 5))

        topLeft = (0, OFFSETHEIGHT)
        for row in self.board.board:
            for piece in row:
                image = self.images[self.getImageString(piece)]
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = (0, topLeft[1] + self.pieceSize[1])

    def getImageString(self, piece: piece):
        if piece.clicked:
            if piece.isMine:
                return "bomb-at-clicked-block"
            else:
                return str(piece.around)
        if self.board.hasLost:
            if piece.flagged and piece.isMine:
                return "flag"
            elif piece.flagged and not piece.isMine:
                return "wrong-flag"
            elif not piece.flagged and piece.isMine:
                return "unclicked-bomb"
            else:
                return "empty-block"
        else:
            if piece.flagged:
                return "flag"
            else:
                return "empty-block"

    def clickPiece(self, pos: tuple[int, int], rightclick):
        row = int((pos[1] - OFFSETHEIGHT) // self.pieceSize[1])
        col = int(pos[0] // self.pieceSize[0])
        piece = self.board.getPiece(row, col)
        self.board.click(piece, rightclick)

    def win(self):
        print("You won!")

    def lost(self):
        print("You lost!")


class recursionlimit:
    def __init__(self, limit):
        self.limit = limit

    def __enter__(self):
        self.old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)


def main():
    game = minesweeper([9, 9], 10)
    game.state1()


if __name__ == '__main__':
    with recursionlimit(1500):
        main()
