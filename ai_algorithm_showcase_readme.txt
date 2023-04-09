This is a readme file for ai_algorithm_showcase.py

Main function is ai_algorithm(filename, movemade)
If movemade is True, this iteration (round/turn) is for wolf
If movemade is False, this iteration (round/turn) is for sheep

Inside the main function, the following sub-functions are executed:

1.load_matrix(matrix_file_name) -> read the txt file and load the current state as matrix
2. move
   Parse the current state filename and achieve the current iteration number
  2.1 If movemade is True
     [start_row, start_col, end_row, end_col]=next_move_wolf(matrix)
       start_row, start_col are the start location of row and column
       end_row, end_col are the end location of row and column
       The same below.
     Update the new state as matrix2
  2.2 If movemade is False
     [start_row, start_col, end_row, end_col]=next_move_sheep(matrix)
     Update the new state as matrix2
3. write_matrix(matrix, matrix_file_name_output)
   Update the new state matrix as a new state txt file

