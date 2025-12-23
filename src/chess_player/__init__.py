from .MainChessApp import MainChessApp

def main():
    #Instantiate Application
    chessApp = MainChessApp()
    #Build Application UI and show it
    chessApp.buildUI()

if __name__ == '__main__':
    main()
