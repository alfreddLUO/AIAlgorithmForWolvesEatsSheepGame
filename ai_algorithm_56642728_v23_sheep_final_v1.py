import math

import numpy as np
import os
import copy


def load_matrix(matrix_file_name):  # read and load the current state
    with open(matrix_file_name, 'r') as f:
        data = f.read()
        data2 = data.replace('\n', ',').split(',')
    matrix = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            matrix[i, j] = int(data2[5 * i + j])
    return matrix


def write_matrix(matrix, matrix_file_name_output):  # wirte the new state into new txt file
    with open(matrix_file_name_output, 'w') as f:
        for i in range(5):
            for j in range(5):
                f.write(str(int(matrix[i, j])))
                if j < 4:
                    f.write(',')
                if j == 4:
                    f.write('\n')


class Board:
    def __init__(self, player, state):
        self.winner = None
        self.state = state
        self.player = player
        self.wolf1_location = None
        self.wolf2_location = None

    def update_winner(self, winner):
        self.winner = winner

    def makeMove(self, move):
        [start_row, start_col, end_row, end_col] = move
        matrix2 = copy.deepcopy(self.state)
        matrix2[end_row, end_col] = self.player
        matrix2[start_row, start_col] = 0
        nextPlayer = 2 if self.player == 1 else 2
        return Board(nextPlayer, matrix2)

    def currentPlayer(self):
        return self.player

    def check_num_of_sheep(self):
        sheep_cnt = 0
        board = self.state
        for i in range(5):
            for j in range(5):
                if board[i][j] == 1:
                    sheep_cnt += 1
        return sheep_cnt

    def check_total_distance_from_sheep_to_wolf(self):
        wolf1_location = self.wolf1_location
        wolf2_location = self.wolf2_location
        total_distance = 0
        board = self.state
        for i in range(5):
            for j in range(5):
                if board[i][j] == 1:
                    dist_current_to_wolf1 = abs(i - wolf1_location[0]) + abs(j - wolf1_location[1])
                    dist_current_to_wolf2 = abs(i - wolf2_location[0]) + abs(j - wolf2_location[1])
                    total_distance += (dist_current_to_wolf1 + dist_current_to_wolf2)
        return total_distance

    def check_num_of_ways_wolf_trapped(self):
        wolf_locations = [self.wolf1_location, self.wolf2_location]
        num_of_trapped = 0
        trapped_wolf_num = 0
        for wolf_loc in wolf_locations:
            wolf_loc_x = wolf_loc[0]
            wolf_loc_y = wolf_loc[1]
            trapped_ways = [[wolf_loc_x - 1, wolf_loc_y], [wolf_loc_x, wolf_loc_y - 1], [wolf_loc_x, wolf_loc_y + 1],
                            [wolf_loc_x + 1, wolf_loc_y]]
            trapped = False
            for way in trapped_ways:
                if self.check_wolf_trapped_in_this_way(way[0], way[1]):
                    num_of_trapped += 1
            if num_of_trapped == 4:
                trapped_wolf_num += 1
                num_of_trapped -= 4
        return num_of_trapped, trapped_wolf_num

    def check_num_of_to_be_killed_sheep(self):
        board = self.state
        num_of_to_be_killed_sheep = 0
        for i in range(5):
            for j in range(5):
                tmp_num = 0
                if board[i][j]==1:
                    if i + 2 < 5:
                        if board[i + 2, j] == 1 and board[i + 1, j] == 0:
                            tmp_num = 1
                    if i - 2 >= 0:
                        if board[i - 2, j] == 1 and board[i - 1, j] == 0:
                            tmp_num = 1
                    if j + 2 < 5:
                        if board[i, j + 2] == 1 and board[i, j + 1] == 0:
                            tmp_num = 1
                    if j - 2 >= 0:
                        if board[i, j - 2] == 1 and board[i, j - 1] == 0:
                            tmp_num = 1
                    num_of_to_be_killed_sheep += tmp_num
        return num_of_to_be_killed_sheep

    # def check_num_of_block_eating

    @staticmethod
    def calculate_shortened_distance_by_current_move(org_board, cur_board):
        return org_board.check_total_distance_from_sheep_to_wolf()-cur_board.check_total_distance_from_sheep_to_wolf()

    def calculate_sheep_scores(self, num_of_sheep_killed, shortened_distance, num_of_trapped_ways, trapped_wolf_num,num_of_to_be_killed_sheep):
        def calculate_trapped_scores(num):
            # res = 0
            # for i in range(num + 1):
            #     res += 2 * i ** 2
            return num
        return num_of_sheep_killed * (-8000) + shortened_distance * (-100) + calculate_trapped_scores(num_of_trapped_ways)*800 + trapped_wolf_num * 4000 # - num_of_to_be_killed_sheep*200

    def calculate_wolf_scores(self,num_of_sheep_killed, shorten_distance_from_sheep_to_wolf, num_of_trapped_ways, org_board,num_of_to_be_killed_sheep):
        def calculate_trapped_scores(num):
            res = 0
            for i in range(num + 1):
                res += 4 * i ** 2
            return res
        # shorten_distance_from_sheep_to_wolf = shorten_distance_from_sheep_to_wolf if shorten_distance_from_sheep_to_wolf == 0 else 1
        return num_of_sheep_killed * 500 + shorten_distance_from_sheep_to_wolf*20 - 0 * calculate_trapped_scores(num_of_trapped_ways) + 300 * num_of_to_be_killed_sheep

    def evaluate(self, player, gameEnds, org_board):
        if gameEnds:
            if self.winner == player:
                return 100000
            else:
                return -100000
        if player == 2:
            num_of_sheep_killed = org_board.check_num_of_sheep() - self.check_num_of_sheep()
            num_of_trapped_ways, trapped_wolf_num = self.check_num_of_ways_wolf_trapped()
            # total_distance_from_sheep_to_wolf = self.check_total_distance_from_sheep_to_wolf()
            shorten_distance_from_sheep_to_wolf = Board.calculate_shortened_distance_by_current_move(org_board, self)
            num_of_to_be_killed_sheep = self.check_num_of_to_be_killed_sheep()
            # print("Wolf (tmpScores: ", self.calculate_wolf_scores(num_of_sheep_killed, shorten_distance_from_sheep_to_wolf, num_of_trapped_ways, org_board,num_of_to_be_killed_sheep))
            return self.calculate_wolf_scores(num_of_sheep_killed, shorten_distance_from_sheep_to_wolf, num_of_trapped_ways, org_board,num_of_to_be_killed_sheep)
        elif player == 1:
            num_of_sheep_killed = org_board.check_num_of_sheep() - self.check_num_of_sheep()
            org_num_of_trapped_ways, org_trapped_wolf_num = org_board.check_num_of_ways_wolf_trapped()
            cur_num_of_trapped_ways, cur_trapped_wolf_num = self.check_num_of_ways_wolf_trapped()
            delta_num_of_trapped_ways, delta_trapped_wolf_num = cur_num_of_trapped_ways-org_num_of_trapped_ways, cur_trapped_wolf_num-org_trapped_wolf_num
            num_of_to_be_killed_sheep = self.check_num_of_to_be_killed_sheep()
            shorten_distance_from_sheep_to_wolf = Board.calculate_shortened_distance_by_current_move(org_board, self)
            total_scores = self.calculate_sheep_scores(num_of_sheep_killed, shorten_distance_from_sheep_to_wolf, delta_num_of_trapped_ways, delta_trapped_wolf_num, num_of_to_be_killed_sheep)
            # print("Sheep (tmpScores: ",total_scores)
            return total_scores
        print("No")
        return 0

    def check_wolf_trapped_in_this_way(self, i, j):
        board = self.state
        if i < 0 or i > 4 or j < 0 or j > 4:
            return True
        if board[i][j] != 0:
            return True
        return False

    def game_ends(self):
        board = self.state
        sheep_cnt = 0
        wolf1_exist = False
        wolf2_exist = False
        wolf1_trapped = False
        wolf2_trapped = False
        for i in range(5):
            for j in range(5):
                if board[i][j] == 0:
                    continue
                elif board[i][j] == 1:
                    sheep_cnt += 1
                elif board[i][j] == 2:
                    if wolf1_exist == False:
                        wolf1_exist = True
                        self.wolf1_location = [i, j]
                    else:
                        wolf2_exist = True
                        self.wolf2_location = [i, j]
                    if self.check_wolf_trapped_in_this_way(i - 1, j) and self.check_wolf_trapped_in_this_way(i,
                                                                                                             j - 1) and self.check_wolf_trapped_in_this_way(
                        i + 1, j) and self.check_wolf_trapped_in_this_way(i, j + 1):
                        if wolf1_exist and not wolf2_exist:
                            wolf1_trapped = True
                        else:
                            wolf2_trapped = True
        if sheep_cnt <= 2:
            self.update_winner(2)
            return True
        if wolf1_exist and wolf2_exist and wolf1_trapped and wolf2_trapped:
            self.update_winner(1)
            return True
        return False

    def getWolfMoves(self):
        matrix = self.state
        candidates = []
        for i in range(5):
            for j in range(5):
                if matrix[i, j] == 2:
                    if i + 1 < 5:
                        if matrix[i + 1, j] == 0:
                            candidates.append([i, j, i + 1, j])
                    if i - 1 >= 0:
                        if matrix[i - 1, j] == 0:
                            candidates.append([i, j, i - 1, j])
                    if j + 1 < 5:
                        if matrix[i, j + 1] == 0:
                            candidates.append([i, j, i, j + 1])
                    if j - 1 >= 0:
                        if matrix[i, j - 1] == 0:
                            candidates.append([i, j, i, j - 1])
                    if i + 2 < 5:
                        if matrix[i + 2, j] == 1 and matrix[i + 1, j] == 0:
                            candidates.append([i, j, i + 2, j])
                            candidates.remove([i, j, i + 1, j])
                    if i - 2 >= 0:
                        if matrix[i - 2, j] == 1 and matrix[i - 1, j] == 0:
                            candidates.append([i, j, i - 2, j])
                            candidates.remove([i, j, i - 1, j])
                    if j + 2 < 5:
                        if matrix[i, j + 2] == 1 and matrix[i, j + 1] == 0:
                            candidates.append([i, j, i, j + 2])
                            candidates.remove([i, j, i, j+1])
                    if j - 2 >= 0:
                        if matrix[i, j - 2] == 1 and matrix[i, j - 1] == 0:
                            candidates.append([i, j, i, j - 2])
                            candidates.remove([i, j, i, j - 1])
        candidates_array = np.array(candidates)
        np.random.shuffle(candidates_array)
        return candidates_array

    def getSheepMoves(self):
        matrix = self.state
        candidates = []
        for i in range(5):
            for j in range(5):
                if matrix[i, j] == 1:
                    if i + 1 < 5:
                        if matrix[i + 1, j] == 0:
                            candidates.append([i, j, i + 1, j])
                    if i - 1 >= 0:
                        if matrix[i - 1, j] == 0:
                            candidates.append([i, j, i - 1, j])
                    if j + 1 < 5:
                        if matrix[i, j + 1] == 0:
                            candidates.append([i, j, i, j + 1])
                    if j - 1 >= 0:
                        if matrix[i, j - 1] == 0:
                            candidates.append([i, j, i, j - 1])
        candidates_array = np.array(candidates)
        np.random.shuffle(candidates_array)
        return candidates_array


def getBestMove(board, maxDepth, player):
    def ab_negamax(board, player, maxDepth, currentDepth, alpha, beta, org_board):
        gameEnds = board.game_ends()
        if gameEnds or currentDepth == maxDepth:
            return None, None, None, None, board.evaluate(player, gameEnds, org_board), currentDepth, None
        if board.currentPlayer() == 2:
            all_moves = board.getWolfMoves()
        else:
            all_moves = board.getSheepMoves()
        if board.currentPlayer() == player:
            best_start_row, best_start_col, best_end_row, best_end_col = None, None, None, None
            bestScore = -math.inf
            bestScoreDepth = math.inf
            bestScoreBoard = None
            for move in all_moves:
                newBoard = board.makeMove(move)
                _, _, _, _, currentScore_, currentScoreDepth, _ = ab_negamax(newBoard, player, maxDepth,
                                                                             currentDepth + 1, alpha,
                                                                             beta, org_board)
                currentScore = currentScore_
                alpha = max(alpha, currentScore)
                if currentScore > bestScore or (
                        currentScore == bestScore and currentScoreDepth < bestScoreDepth):
                    # print("Yes")
                    bestScore = currentScore
                    bestScoreDepth = currentScoreDepth
                    best_start_row, best_start_col, best_end_row, best_end_col = move[0], move[1], move[2], move[3]
                    bestScoreBoard = newBoard
                    if alpha >= beta:
                        return best_start_row, best_start_col, best_end_row, best_end_col, bestScore, bestScoreDepth, bestScoreBoard
        else:
            best_start_row, best_start_col, best_end_row, best_end_col = None, None, None, None
            bestScore = math.inf
            bestScoreDepth = math.inf
            bestScoreBoard = None
            for move in all_moves:
                newBoard = board.makeMove(move)
                # if player == 2:
                _, _, _, _, currentScore_, currentScoreDepth, _ = ab_negamax(newBoard, player, maxDepth,
                                                                             currentDepth + 1, alpha,
                                                                             beta, org_board)
                # currentScore = currentScore_
                currentScore = currentScore_
                beta = min(beta,currentScore)
                if currentScore < bestScore or (
                        currentScore == bestScore and currentScoreDepth < bestScoreDepth):  # or currentScore == 1000:
                    bestScore = currentScore
                    bestScoreDepth = currentScoreDepth
                    best_start_row, best_start_col, best_end_row, best_end_col = move[0], move[1], move[2], move[3]
                    bestScoreBoard = newBoard
                    if alpha >= beta:
                        return best_start_row, best_start_col, best_end_row, best_end_col, bestScore, bestScoreDepth, bestScoreBoard

        return best_start_row, best_start_col, best_end_row, best_end_col, bestScore, bestScoreDepth, bestScoreBoard

    best_start_row, best_start_col, best_end_row, best_end_col, bestScore, bestScoreDepth, bestScoreBoard = ab_negamax(board, player, maxDepth, 0,
                                                                                       -math.inf, math.inf, board)
    print("Best Move: ", best_start_row, best_start_col, best_end_row, best_end_col, bestScore, bestScoreDepth)
    return best_start_row, best_start_col, best_end_row, best_end_col, bestScore, bestScoreDepth


def AIAlgorithm(filename, movemade):  # a showcase for random walk
    iter_num = filename.split('/')[-1]
    iter_num = iter_num.split('.')[0]
    iter_num = int(iter_num.split('_')[1])
    matrix = load_matrix(filename)
    if movemade == True:
        board = Board(2, matrix)
        [start_row, start_col, end_row, end_col, scores,depth] = getBestMove(board, 3, 2)
        print("Wolf Scores: ", scores, "Depth: ", depth)
        matrix2 = copy.deepcopy(matrix)
        matrix2[end_row, end_col] = 2
        matrix2[start_row, start_col] = 0

    if movemade == False:
        board = Board(1, matrix)
        [start_row, start_col, end_row, end_col, scores,depth] = getBestMove(board, 4, 1)
        print("Sheep Scores: ", scores, "Depth: ", depth)
        matrix2 = copy.deepcopy(matrix)
        matrix2[end_row, end_col] = 1
        matrix2[start_row, start_col] = 0

    matrix_file_name_output = filename.replace('state_' + str(iter_num), 'state_' + str(iter_num + 1))
    write_matrix(matrix2, matrix_file_name_output)

    return start_row, start_col, end_row, end_col

# def minmax(board, player, maxDepth, currentDepth):
#     if board.game_ends() or currentDepth == maxDepth:
#         return None, None, None, None, board.evaluate(player)
#     best_start_row, best_start_col, best_end_row, best_end_col = None, None, None, None
#     if board.currentPlayer() == player:
#         bestScore = -math.inf
#     else:
#         bestScore = math.inf
#     if player == 2:
#         all_moves = board.getWolfMoves()
#     else:
#         all_moves = board.getSheepMoves()
#     for move in all_moves:
#         newBoard = board.makeMove(move)
#         start_row, start_col, end_row, end_col, currentScore = minmax(newBoard, player, maxDepth, currentDepth + 1)
#         if board.currentPlayer() == player:
#             if currentScore > bestScore:
#                 bestScore = currentScore
#                 best_start_row, best_start_col, best_end_row, best_end_col = move[0], move[1], move[2], move[3]
#         else:
#             if currentScore < bestScore:
#                 bestScore = currentScore
#                 best_start_row, best_start_col, best_end_row, best_end_col = move[0], move[1], move[2], move[3]
#     return best_start_row, best_start_col, best_end_row, best_end_col, bestScore
