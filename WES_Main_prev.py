import time

import pygame as p
import WES_Engine
from PastVersionsForAIAlgorithm import ai_algorithm_showcase as ai
import ai_algorithm_56642728 as ai2
import jpype


# os.environ['JAVA_HOME'] = r'C:/Program Files/Java/jdk-19'

class WES(object):

    def __init__(self):
        self.WIDTH = self.HEIGHT = 512
        self.DIMENSIONS = 5 # dimensions of a chess board are 5x5
        self.SQ_SIZE = self.HEIGHT // self.DIMENSIONS
        self.MAX_FPS = 15 #for animations
        self.IMAGES = {}
        self.LANGUAGE = "PYTHON" #{C++, JAVA, PYTHON}

        self.PLAY_ROLE = [0, 0] # index: 0 for player 1 as wolf and 1 for player 2 as sheep. value: 0 for AI and 1 for human.
        self.initial_board = [
                    ['1', '1', '1', '1', '1'],
                    ['1', '1', '1', '1', '1'],
                    ['0', '0', '0', '0', '0'],
                    ['0', '0', '0', '0', '0'],
                    ['0', '2', '0', '2', '0']] # the index of each chess is their real position in pygame
        '''
        Initialize a global dictionary of images. This will be called exactly once in the main
        '''
        self.round = 0
        self.current_round = 'round' + str(self.round) + '/'

    # return board status by reading the board file
    def read_board(self, filename):
        board_digits = list()
        board_current = list()
        with open(filename, 'r+') as fin:
            board_digits = fin.read().split('\n')
            for item in board_digits:
                items = item.split(',')
                board_current.append(items)
        return board_current



    def loadImages(self):
        pieces = ['2', '1']
        for piece in pieces:
            if piece == '2':
                self.IMAGES[piece] = p.transform.scale(p.image.load('images/'+'bW'+'.png'), (self.SQ_SIZE, self.SQ_SIZE))
            else:
                self.IMAGES[piece] = p.transform.scale(p.image.load('images/'+'wS'+'.png'), (self.SQ_SIZE, self.SQ_SIZE))
    #Note: We can access an image by saying IMAGES[piece], the size can be reset by SQ_SIZE * shape

    '''
    Responsible for all graphics within a current game state
    '''





    '''
    make move by human manipulation
    '''
    def click_move(self, e, sqSelection, playerClicks, gs, moveMade):
        if e.type == p.MOUSEBUTTONDOWN:
            location = p.mouse.get_pos()  # (x, y) ->location of mouse[[0,0],...[4,4]] from left top to right bottom
            col = location[0] // self.SQ_SIZE
            row = location[1] // self.SQ_SIZE

            if sqSelection == (row, col):  # the user clicked the same square twice
                sqSelection = ()  # deselect
                playerClicks = []  # clear player click
            else:
                sqSelection = (row, col)
                playerClicks.append(sqSelection)  # append for both 1st and 2nd clicks
            if len(playerClicks) == 2:  # after 2nd click
                move = WES_Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                if gs.getValidMoves(move, moveMade):
                    #print('finished')
                    gs.makeMove(move)
                    moveMade = not moveMade
                    # print(moveMade, '1111')
                    sqSelection = ()  # reset user clicks
                    playerClicks = []
                else:
                    sqSelection = ()  # reset user clicks
                    playerClicks = []

        return gs, moveMade, sqSelection, playerClicks

    def drawGameState(self, screen, gs):
        self.drawBoard(screen)
        self.drawPieces(screen, gs.board)

    '''
    Draw the squares on the board
    '''
    def drawBoard(self, screen):
        colors = [p.Color('lightgreen'), p.Color('lightblue')]
        for r in range(self.DIMENSIONS):
            for c in range(self.DIMENSIONS):
                color = colors[(r + c) % 2]
                p.draw.rect(screen, color, p.Rect(c*self.SQ_SIZE, r*self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    '''
    Draw the pieces on the board using the current game state on board
    '''
    def drawPieces(self, screen, board):
        for r in range(self.DIMENSIONS):
            for c in range(self.DIMENSIONS):
                piece = board[r][c]
                if piece != '0':
                    screen.blit(self.IMAGES[piece], p.Rect(c*self.SQ_SIZE, r*self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))


    '''
    ai_algorithm, input is the board status, output the start position and end position of a chess
    '''

    def ai2_algorithm(self, gs, count, moveMade): # or replace the gs with filename
        record_file = self.current_round + 'state_' + str(count-1) +'.txt'
        if self.LANGUAGE == "PYTHON":
            start_row, start_col, end_row, end_col = ai2.AIAlgorithm(record_file, moveMade)
        return start_row, start_col, end_row, end_col

    def ai_algorithm(self, gs, count, moveMade): # or replace the gs with filename
        record_file = self.current_round + 'state_' + str(count-1) +'.txt'
        if self.LANGUAGE == "PYTHON":
            start_row, start_col, end_row, end_col = ai.AIAlgorithm(record_file, moveMade)
        elif self.LANGUAGE == "C++":
            start_row, start_col, end_row, end_col = ai2.AIAlgorithm(record_file, moveMade)
            # # Compile a .cpp to .so: g++ --shared -o aiAlgorithm.so aiAlgorithm.cpp
            # # Load the shared library
            # lib = ctypes.CDLL('./c++/ai_algorithm.so') # If Python >= 3.8, please use this coomand: lib = ctypes.CDLL('./c++/aiAlgorithm.so', winmode=0)
            # lib.AIAlgorithm_c.restype = ctypes.POINTER(ctypes.c_long) #ctypes.POINTER(ctypes.c_int)
            # lib.AIAlgorithm_c.argtypes = [ctypes.c_char_p, ctypes.c_bool]
            # result = lib.AIAlgorithm_c(ctypes.c_char_p(record_file.encode('utf-8')), moveMade)
            # # result = lib.ai_algorithm(record_file, moveMade)
            # move = [result[i] for i in range(4)]
            # del result
            # start_row, start_col, end_row, end_col = move[0], move[1], move[2], move[3]

        elif self.LANGUAGE == "JAVA":
            # compile a .java file to .jar:
            # 1. javac AIAlgorithm.java
            # 2. jar cf AIAlgorithm.jar AIAlgorithm.class
            # Create a Java object that corresponds to the AI_Algorithm class
            jarpath = r'./java/ai_algorithm.jar'  # the path to jar file

            JVMPath = jpype.getDefaultJVMPath()
            Djava = "-Djava.class.path=" + jarpath
            if not jpype.isJVMStarted():
                jpype.startJVM(JVMPath, "-ea", Djava)
            JDClass = jpype.JClass("ai_algorithm")
            jd = JDClass()

            # Call the ai_algorithm function
            result = jd.AIAlgorithm(record_file, moveMade)

            # Convert the result to a Python list
            result = list(result)
            start_row, start_col, end_row, end_col = result[0], result[1], result[2], result[3]

        return start_row, start_col, end_row, end_col


    def ai_move(self, gs, count, moveMade):
        start_row, start_col, end_row, end_col = self.ai_algorithm(gs, count, moveMade)
        start = (int(start_row), int(start_col))
        end = (int(end_row), int(end_col))

        move = WES_Engine.Move(start, end, gs.board)
        # print(move.getChessNotation())
        if gs.getValidMoves(move, moveMade):
            gs.makeMove(move)
            moveMade = not moveMade
        else:
            #print(moveMade)
            #print(start, '\n', end)
            #print(gs.board)
            raise ValueError('The move is invalid')
        return gs, moveMade

    def ai2_move(self, gs, count, moveMade):
        start_row, start_col, end_row, end_col = self.ai2_algorithm(gs, count, moveMade)
        start = (int(start_row), int(start_col))
        end = (int(end_row), int(end_col))

        move = WES_Engine.Move(start, end, gs.board)
        # print(move.getChessNotation())
        if gs.getValidMoves(move, moveMade):
            gs.makeMove(move)
            moveMade = not moveMade
        else:
            #print(moveMade)
            #print(start, '\n', end)
            #print(gs.board)
            raise ValueError('The move is invalid')
        return gs, moveMade

    def board_record(self, gs, count_n):
        board = gs.board
        record_name = self.current_round + 'state_' + str(count_n) + '.txt'
        board_str = ''
        for item in board:
            count = 0
            for chess in item:
                if count < 4:
                    board_str += chess + ','
                    count += 1
                else:
                    board_str += chess + '\n'

        with open(record_name, 'w+') as fin:
            fin.write(board_str)

        return count_n + 1

    '''
    The main driver for our code, This will handle user input and updating the graphics
    '''
    def main(self):
        p.init()
        screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color('white'))
        gs = WES_Engine.WES_State()
        moveMade = True # True for wolf and False for Sheep

        self.loadImages() # only load images once before the while loop
        running = True

        sqSelection = () # no square is selected, keep track of the last click of the user{tuple: (row, col)}
        playerClicks = [] # keey track of player clicks {two tuples:[beginning position, ending position]}

        initial_file = 'state_0.txt'

        font = p.font.init()
        my_font = p.font.SysFont('Comic Sans MS', 30)
        p.display.set_caption('Wolves Eat Sheep')
        count = 1
        self.drawGameState(screen, gs)
        count_mode = True
        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                if moveMade:
                    if self.PLAY_ROLE[0] == 1:
                        gs, moveMade = self.ai2_move(gs, count, moveMade)
                        #print('2222', moveMade, playerClicks)
                        if count_mode == moveMade:
                            count = self.board_record(gs, count)
                            count_mode = not count_mode
                    elif self.PLAY_ROLE[0] == 0:
                        gs, moveMade = self.ai_move(gs, count, moveMade)
                        if count_mode == moveMade:
                            count = self.board_record(gs, count)
                            count_mode = not count_mode
                    else:
                        raise ValueError('The setting of playing is wrong')


                if not moveMade:
                    if self.PLAY_ROLE[1] == 1:
                        gs, moveMade = self.ai2_move(gs, count, moveMade)
                        #print('1111', moveMade, playerClicks)
                        if count_mode == moveMade:
                            count = self.board_record(gs, count)
                            count_mode = not count_mode
                    elif self.PLAY_ROLE[1] == 0:
                        gs, moveMade = self.ai_move(gs, count, moveMade)
                        if count_mode == moveMade:
                            count = self.board_record(gs, count)
                            count_mode = not count_mode

                    else:
                        raise ValueError('The setting of playing is wrong')

            self.drawGameState(screen, gs)
            clock.tick(self.MAX_FPS)
            winner = gs.checkWinning()
            if winner != 0:
                if winner == 1:
                    surface_1 = my_font.render('Wolves Win!', False, (220, 0, 0))
                    surface_2 = my_font.render('Input mode for A New Game', False, (220, 0, 0))
                    screen.blit(surface_1, (1.7 * self.SQ_SIZE, 2 * self.SQ_SIZE))
                    screen.blit(surface_2, (0.2 * self.SQ_SIZE, 2.4 * self.SQ_SIZE))
                    p.display.flip()
                    time.sleep(5)
                    p.quit()
                    return True
                if winner == 2:
                    surface_1 = my_font.render('Sheep Win!', False, (220, 0, 0))
                    surface_2 = my_font.render('Input mode for A New Game', False, (220, 0, 0))
                    screen.blit(surface_1, (1.7 * self.SQ_SIZE, 2 * self.SQ_SIZE))
                    screen.blit(surface_2, (0.2 * self.SQ_SIZE, 2.4 * self.SQ_SIZE))
                    p.display.flip()
                    time.sleep(5)
                    p.quit()
                    return True
            p.display.flip()
