from game import minesweeper

def main():
    game = minesweeper([10,10], 200)
    game.run()

if __name__ == '__main__':
    main()