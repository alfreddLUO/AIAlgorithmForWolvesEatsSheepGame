import numpy as np
import os 
import copy

def load_matrix(matrix_file_name): # read and load the current state
    with open(matrix_file_name, 'r') as f:
        data = f.read()
        data2=data.replace('\n',',').split(',')
    matrix = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            matrix[i,j]=int(data2[5*i+j])
    return matrix

def write_matrix(matrix, matrix_file_name_output): # wirte the new state into new txt file
    with open(matrix_file_name_output, 'w') as f:
        for i in range(5):
            for j in range(5):
                f.write(str(int(matrix[i,j])))
                if j<4:
                    f.write(',')
                if j==4:
                    f.write('\n')

def next_move_wolf(matrix): # random walk for wolf
    candidates=[]
    for i in range(5):
        for j in range(5):
            if matrix[i,j]==2:
                if i+1<5:
                    if matrix[i+1,j]==0:
                        candidates.append([i,j,i+1,j])
                if i-1>=0:
                    if matrix[i-1,j]==0:
                        candidates.append([i,j,i-1,j])
                if j+1<5:
                    if matrix[i,j+1]==0:
                        candidates.append([i,j,i,j+1])
                if j-1>=0:
                    if matrix[i,j-1]==0:
                        candidates.append([i,j,i,j-1])
                if i+2<5:
                    if matrix[i+2,j]==1 and matrix[i+1,j]==0:
                        candidates.append([i,j,i+2,j])
                if i-2>=0:
                    if matrix[i-2,j]==1 and matrix[i-1,j]==0:
                        candidates.append([i,j,i-2,j])
                if j+2<5:
                    if matrix[i,j+2]==1 and matrix[i,j+1]==0:
                        candidates.append([i,j,i,j+2])
                if j-2>=0:
                    if matrix[i,j-2]==1 and matrix[i,j-1]==0:
                        candidates.append([i,j,i,j-2])
    move_idx=np.random.randint(0, len(candidates))
    return candidates[move_idx]

def next_move_sheep(matrix): # random walk for sheep
    candidates=[]
    for i in range(5):
        for j in range(5):
            if matrix[i,j]==1:
                if i+1<5:
                    if matrix[i+1,j]==0:
                        candidates.append([i,j,i+1,j])
                if i-1>=0:
                    if matrix[i-1,j]==0:
                        candidates.append([i,j,i-1,j])
                if j+1<5:
                    if matrix[i,j+1]==0:
                        candidates.append([i,j,i,j+1])
                if j-1>=0:
                    if matrix[i,j-1]==0:
                        candidates.append([i,j,i,j-1])
    move_idx=np.random.randint(0, len(candidates))
    return candidates[move_idx]

def AIAlgorithm(filename, movemade): # a showcase for random walk
    iter_num=filename.split('/')[-1]
    iter_num=iter_num.split('.')[0]
    iter_num=int(iter_num.split('_')[1])
    matrix=load_matrix(filename)
    if movemade==True:
        [start_row, start_col, end_row, end_col]=next_move_wolf(matrix)
        matrix2=copy.deepcopy(matrix)
        matrix2[end_row, end_col]=2
        matrix2[start_row, start_col]=0
            
    if movemade==False:
        [start_row, start_col, end_row, end_col]=next_move_sheep(matrix)
        matrix2=copy.deepcopy(matrix)
        matrix2[end_row, end_col]=1
        matrix2[start_row, start_col]=0
        
    matrix_file_name_output=filename.replace('state_'+str(iter_num), 'state_'+str(iter_num+1)) 
    write_matrix(matrix2, matrix_file_name_output)

    return start_row, start_col, end_row, end_col

# import numpy as np
# import os 
# import copy

# def load_matrix(matrix_file_name): # read and load the current state
#     with open(matrix_file_name, 'r') as f:
#         data = f.read()
#         data2=data.replace('\n',',').split(',')
#     matrix = np.zeros((5, 5))
#     for i in range(5):
#         for j in range(5):
#             matrix[i,j]=int(data2[5*i+j])
#     return matrix

# def write_matrix(matrix, matrix_file_name_output): # wirte the new state into new txt file
#     with open(matrix_file_name_output, 'w') as f:
#         for i in range(5):
#             for j in range(5):
#                 f.write(str(int(matrix[i,j])))
#                 if j<4:
#                     f.write(',')
#                 if j==4:
#                     f.write('\n')

# def next_move_wolf(matrix): # random walk for wolf
#     candidates=[]
#     for i in range(5):
#         for j in range(5):
#             if matrix[i,j]==2:
#                 if i+1<5:
#                     if matrix[i+1,j]==0:
#                         candidates.append([i,j,i+1,j])
#                 if i-1>=0:
#                     if matrix[i-1,j]==0:
#                         candidates.append([i,j,i-1,j])
#                 if j+1<5:
#                     if matrix[i,j+1]==0:
#                         candidates.append([i,j,i,j+1])
#                 if j-1>=0:
#                     if matrix[i,j-1]==0:
#                         candidates.append([i,j,i,j-1])
#                 if i+2<5:
#                     if matrix[i+2,j]==1 and matrix[i+1,j]==0:
#                         candidates.append([i,j,i+2,j])
#                 if i-2>=0:
#                     if matrix[i-2,j]==1 and matrix[i-1,j]==0:
#                         candidates.append([i,j,i-2,j])
#                 if j+2<5:
#                     if matrix[i,j+2]==1 and matrix[i,j+1]==0:
#                         candidates.append([i,j,i,j+2])
#                 if j-2>=0:
#                     if matrix[i,j-2]==1 and matrix[i,j-1]==0:
#                         candidates.append([i,j,i,j-2])
#     move_idx=np.random.randint(0, len(candidates))
#     return candidates[move_idx]

# def next_move_sheep(matrix): # random walk for sheep
#     candidates=[]
#     for i in range(5):
#         for j in range(5):
#             if matrix[i,j]==1:
#                 if i+1<5:
#                     if matrix[i+1,j]==0:
#                         candidates.append([i,j,i+1,j])
#                 if i-1>=0:
#                     if matrix[i-1,j]==0:
#                         candidates.append([i,j,i-1,j])
#                 if j+1<5:
#                     if matrix[i,j+1]==0:
#                         candidates.append([i,j,i,j+1])
#                 if j-1>=0:
#                     if matrix[i,j-1]==0:
#                         candidates.append([i,j,i,j-1])
#     move_idx=np.random.randint(0, len(candidates))
#     return candidates[move_idx]

# def ai_algorithm(filename, movemade): # a showcase for random walk
#     iter_num=filename.split('/')[-1]
#     iter_num=iter_num.split('.')[0]
#     iter_num=int(iter_num.split('_')[1])
#     matrix=load_matrix(filename)
#     if movemade==True:
#         [start_row, start_col, end_row, end_col]=next_move_wolf(matrix)
#         matrix2=copy.deepcopy(matrix)
#         matrix2[end_row, end_col]=2
#         matrix2[start_row, start_col]=0
            
#     if movemade==False:
#         [start_row, start_col, end_row, end_col]=next_move_sheep(matrix)
#         matrix2=copy.deepcopy(matrix)
#         matrix2[end_row, end_col]=1
#         matrix2[start_row, start_col]=0
        
#     matrix_file_name_output=filename.replace('state_'+str(iter_num), 'state_'+str(iter_num+1)) 
#     write_matrix(matrix2, matrix_file_name_output)

#     return start_row, start_col, end_row, end_col

