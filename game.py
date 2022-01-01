import pygame
import os
from board import board
from piece import piece

class minesweeper:
    def __init__(self, dim: list, num_mine: int) -> None:
        self.board = board(dim, num_mine)
        pygame.init()
        self.sizeScreen = 800, 800
        self.screen = pygame.display.set_mode(self.sizeScreen)
        self.pieceSize = (self.sizeScreen[0] / dim[1], self.sizeScreen[1] / dim[0]) 
        self.loadPictures()
    
    def loadPictures(self):
        self.images = {}
        imagesDirectory = "images"
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):
                continue
            path = imagesDirectory + r"/" + fileName 
            img = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(img, (int(self.pieceSize[0]), int(self.pieceSize[1])))
            self.images[fileName.split(".")[0]] = img

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not (self.board.hasWon or self.board.hasLost):
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    self.click(pygame.mouse.get_pos(), rightClick)
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            if self.board.hasWon:
                self.win()
                running = False
            if self.board.hasLost:
                self.lost()
                running = False
        
        pygame.quit()

    def draw(self):
        topLeft = (0, 0)
        for row in self.board.board:
            for piece in row:
                rect = pygame.Rect(topLeft, self.pieceSize)
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
            elif not piece.flagged and  piece.isMine:
                return "unclicked-bomb"
            else:
                return "empty-block"
        else:
            if piece.flagged:
                return "flag"
            else:
                return "empty-block"

    def click(self, pos:tuple[int, int], rightclick):
        row = int(pos[1] // self.pieceSize[1])
        col = int(pos[0] // self.pieceSize[0])
        piece = self.board.getPiece([row, col])
        self.board.click(piece, rightclick)
    
    def win(self):
        print("You won!")
    
    def lost(self):
        print("You lost!")

if __name__ == '__main__':
    pass