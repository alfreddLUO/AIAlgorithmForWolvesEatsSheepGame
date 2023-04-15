from WES_Main_org import WES
from WES_Engine import WES_State, Move
import time



if __name__ == '__main__':
    Flag = True
    Play = [0, 1]
    game = WES()
    game.round = 0 # you can set multiple rounds by changing this to 1, 2, ... But remember create a file with name as roundX and include the state_0.txt
    game.LANGUAGE = "PYTHON" #choose your coding language C++, JAVA, PYTHON}
    while Flag:
        mode1 = input('Please choose your game mode for Player 1: 0 for AI, 1 for human player and 2 for quit:')
        mode2 = input('Please choose your game mode for Player 2: 0 for AI, 1 for human player and 2 for quit:')
        if int(mode1) not in Play or int(mode2) not in Play:
            print('Thanks for you participation')
            Flag = not Flag
        else:
            game.PLAY_ROLE = [int(mode1), int(mode2)]
            game.main()