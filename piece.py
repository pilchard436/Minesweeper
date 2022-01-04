class piece: 
    def __init__(self, isMine: bool = False) -> None:
        self.isMine = isMine
        self.around = 0 # The number that players see on a piece if the piece is not a mine. 
        self.clicked = False
        self.flagged = False
        self.neighbors : list[piece] = list() # List of all the neighboring pieces of current piece. Piece A is piece B's neighbor if piece A is one of the 8 pieces surrounding piece B. 
        
    def __str__(self) -> str:
        return (str(self.around) if not self.isMine else str(-1))

    def toggleFlag(self):
        self.flagged = not self.flagged
        return self.flagged

    def handleClick(self):
        self.clicked = True

    def setAround(self):
        res = 0
        for i in self.neighbors:
            if i.isMine:
                res += 1
        self.around = res

if __name__ == '__main__':
    pass
