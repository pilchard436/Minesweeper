import random

from piece import piece

class board:
    def __init__(self, dim: list, num_mine: int) -> None:
        '''
        "dim" is a list of 2 int. Ex: board([10, 10], 20) generates a 10x10 board with 20 mines. 
        '''
        self.dim = dim
        self.num_mine = num_mine
        self.board : list[list[piece]] = list()
        self.size = self.getSize()
        self.hasWon = False
        self.hasLost = False

        if self.num_mine > self.size:
            raise Exception("The number of mines cannot be bigger than the board size")
            
        self.setBoard()
        self.setMine()
        self.setNeighbors()
        self.setAround()

    def __str__(self) -> str:
        return str('\n'.join([''.join(['{:4}'.format(str(piece)) for piece in row]) for row in self.board]))

    def getSize(self):
        return self.dim[0] * self.dim[1]
    
    def getPiece(self, index: list[int]):
        return self.board[index[0]][index[1]]

    def setBoard(self):
        '''
        Populate the board with empty pieces without mines
        '''
        board = []
        for i in range(self.dim[0]):
            row = []
            for j in range(self.dim[1]):
                row.append(piece())
            board.append(row)
        self.board = board

    def setMine(self):
        '''
        Replace some of the empty pieces with mines
        '''
        templist = []
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                templist.append([i,j])
        minePosList = random.sample(templist, self.num_mine)
        for minePos in minePosList:
            self.getPiece(minePos).isMine = True
            
    def setNeighbors(self):
        '''
        Set "neighbors" attribute of all the pieces in the board. Piece A is piece B's neighbor if piece A is one of the 8 pieces surrounding piece B. 
        '''
        for rowIndex, rowOfPieces in enumerate(self.board):
            for colIndex, piece in enumerate(rowOfPieces):
                for row in range(rowIndex - 1, rowIndex + 2):
                    for col in range(colIndex - 1, colIndex + 2):
                        if row == rowIndex and col == colIndex:
                            continue
                        if (row < 0 or row > self.dim[0] - 1) or (col < 0 or col > self.dim[1] - 1):
                            continue
                        piece.neighbors.append(self.getPiece([row, col]))
                

    def setAround(self): 
        '''
        Set "around" attribute of all the pieces. 
        '''
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                self.getPiece([row, col]).setAround()
                
    def click(self, piece: piece, rightclick):
        if piece.clicked or (piece.flagged and not rightclick):
            return
        if rightclick:
            piece.toggleFlag()
            self.hasWon = self.checkWin()
            return
        else:
            piece.clicked = True
            if piece.isMine:
                self.hasLost = True
                return
        if piece.around == 0:
            for neighbor in piece.neighbors:
                self.click(neighbor, False)

        self.hasWon = self.checkWin()

    def checkWin(self) -> bool:
        for row in self.board:
            for piece in row:
                if piece.isMine and not piece.flagged:
                    return False
        return True
        


if __name__ == '__main__':
    pass