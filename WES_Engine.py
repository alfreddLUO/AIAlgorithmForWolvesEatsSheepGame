'''
This class is responsible for storing all the information about current state of the WES Game. It will also
responsible for determining the valid moves at the current state. It will also keep a move log.
'''

class WES_State(object):
    def __init__(self):
        # board is 5x5 2d list, each element has two characters,
        # the first character represents the color of the piece, 'black' or 'white'
        # the second character represents the type of piece, 'Wolf' or 'Sheep'
        # '0' represents an empty space with no piece
        # this is the initial state

        self.board = [
            ['1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1'],
            ['0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0'],
            ['0', '2', '0', '2', '0']]


        self.blackToMove = True
        self.movelog = []

    '''
    Takes a move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '0'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)  # log the move so we can undo it later
        self.blackToMove = not self.blackToMove # swap players


    def undoMove(self):
        if len(self.movelog) != 0: # make sure there is a move to undo
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.blackToMove = not self.blackToMove # switch turns back

    '''
    All moves considering checks
    '''

    def getValidMoves(self, move, moveMade):
        startRow = move.startRow
        startCol = move.startCol
        endRow = move.endRow
        endCol = move.endCol

        distance = abs(startRow - endRow) + abs(startCol - endCol)
        self.blackToMove = moveMade
        #print(self.blackToMove)
        if self.blackToMove and distance <= 2 and self.board[startRow][startCol] == '2':
            valid_ = self.getValidWolf(move, distance)
        elif not self.blackToMove and distance == 1 and self.board[startRow][startCol] == '1':
            valid_ = self.getValidSheep(move)
        else:
            valid_ = False

        return valid_

    '''
    check wolf moves for validation
    '''

    def getValidWolf(self, move, distance):
        startRow = move.startRow
        startCol = move.startCol
        endRow = move.endRow
        endCol = move.endCol
        if distance == 2:
            if self.board[endRow][endCol] == '1' and self.board[(startRow + endRow) // 2][(startCol + endCol) // 2] == '0':
                return True
            else:
                return False
        else:
            if self.board[endRow][endCol] == '0':
                return True
            else:
                return False

    '''
    check sheep moves for validation
    '''
    def getValidSheep(self, move):
        endRow = move.endRow
        endCol = move.endCol
        if self.board[endRow][endCol] == '0':
            return True
        else:
            return False


    def checkWinning(self):
        # 1: wolf wins, 2: sheep wins, 0: continually gaming
        # check wolves winning
        sheep_num = 0
        wolf_neighbour = []
        wolf_win = True
        sheep_win = True
        winner = 0
        line_range = [0, 1, 2, 3, 4]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == '1':
                    sheep_num += 1
                elif self.board[r][c] == '2':
                    if r - 1 in line_range:
                        wolf_neighbour.append((r-1, c))
                    if r + 1 in line_range:
                        wolf_neighbour.append((r + 1, c))
                    if c - 1 in line_range:
                        wolf_neighbour.append((r, c - 1))
                    if c + 1 in line_range:
                        wolf_neighbour.append((r, c + 1))
                else:
                    pass
        for item in wolf_neighbour:
            if self.board[item[0]][item[1]] == '0':
                sheep_win = not sheep_win
                break
        if sheep_num > 2:
            wolf_win = not wolf_win

        if wolf_win:
            winner = 1
        if sheep_win:
            winner = 2

        return winner




class Move(object):
    # maps keys to values
    # key: value
    ranksToRows = {'y1': 4, 'y2': 3, 'y3': 2, 'y4': 1, 'y5': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'x1': 0, 'x2': 1, 'x3': 2, 'x4': 3, 'x5': 4}
    colsTofiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]


    def getChessNotation(self):
        # you can add to make the real chess notation
        return self.getRankfile(self.startRow, self.startCol) + '->' + self.getRankfile(self.endRow, self.endCol)

    def getRankfile(self, r, c):
        return self.colsTofiles[c] + self.rowsToRanks[r]

