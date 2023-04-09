#define _CRT_SECURE_NO_DEPRECATE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
# include <malloc.h>  
#include <time.h>
#include <cstring>
#include <fstream>
#include <iostream>
using namespace std;

int** load_matrix(const char* matrix_file_name) {
	FILE *f = fopen(matrix_file_name, "r");
	int data[25];
	int count = 0;
	char line[1024];
	while (fgets(line, sizeof(line), f)) {
		char *num = strtok(line, ",");
		while (num != NULL) {
			data[count] = atoi(num);
			count++;
			num = strtok(NULL, ",");
		}
	}
	fclose(f);

	int** matrix = new int*[5];
	for (int i = 0; i < 5; i++) {
		matrix[i] = new int[5];
		for (int j = 0; j < 5; j++) {
			matrix[i][j] = data[5 * i + j];
		}
	}
	return matrix;
}

void write_matrix(int** matrix, const char* matrix_file_name_output) {
	FILE *f = fopen(matrix_file_name_output, "w");
	for (int i = 0; i < 5; i++) {
		for (int j = 0; j < 5; j++) {
			fprintf(f, "%d", matrix[i][j]);
			if (j < 4) {
				fprintf(f, ",");
			}
			if (j == 4) {
				fprintf(f, "\n");
			}
		}
	}
	fclose(f);
}

int* next_move_wolf(int** matrix) {
	int candidates[100][4];
	int count = 0;
	for (int i = 0; i < 5; i++) {
		for (int j = 0; j < 5; j++) {
			if (matrix[i][j] == 2) {
				if (i + 1 < 5 && matrix[i + 1][j] == 0) {
					candidates[count][0] = i;
					candidates[count][1] = j;
					candidates[count][2] = i + 1;
					candidates[count][3] = j;
					count++;
				}
				if (i - 1 >= 0 && matrix[i - 1][j] == 0) {
					candidates[count][0] = i;
					candidates[count][1] = j;
					candidates[count][2] = i - 1;
					candidates[count][3] = j;
					count++;
				}
				if (j + 1 < 5 && matrix[i][j + 1] == 0) {
					candidates[count][0] = i;
					candidates[count][1] = j;
					candidates[count][2] = i;
					candidates[count][3] = j + 1;
					count++;
				}
				if (j - 1 >= 0 && matrix[i][j - 1] == 0) {
					candidates[count][0] = i;
					candidates[count][1] = j;
					candidates[count][2] = i;
					candidates[count][3] = j - 1;
					count++;
				}
				if (i + 2 < 5 && matrix[i + 2][j] == 1 && matrix[i + 1][j] == 0) {
					candidates[count][0] = i;
					candidates[count][1] = j;
					candidates[count][2] = i + 2;
					candidates[count][3] = j;
					count++;
				}
				if (i - 2 >= 0 && matrix[i - 2][j] == 1 && matrix[i - 1][j] == 0) {
					candidates[count][0] = i;
					candidates[count][1] = j;
					candidates[count][2] = i - 2;
					candidates[count][3] = j;
					count++;
				}
				if (j + 2 < 5 && matrix[i][j + 2] == 1 && matrix[i][j + 1] == 0) {
					candidates[count][0] = i;
					candidates[count][1] = j;
					candidates[count][2] = i;
					candidates[count][3] = j + 2;
					count++;
				}
				if (j - 2 >= 0 && matrix[i][j - 2] == 1 && matrix[i][j - 1] == 0) {
					candidates[count][0] = i;
					candidates[count][1] = j;
					candidates[count][2] = i;
					candidates[count][3] = j - 2;
					count++;
				}
			}

		}
	}

	srand(time(NULL));
	int move_idx = rand() % count;

	static int result[4];
	result[0] = candidates[move_idx][0];
	result[1] = candidates[move_idx][1];
	result[2] = candidates[move_idx][2];
	result[3] = candidates[move_idx][3];

	return result;
}


int* next_move_sheep(int** matrix) {
	static int candidates[25][4];
	int candidates_size = 0;
	for (int i = 0; i < 5; i++) {
		for (int j = 0; j < 5; j++) {
			if (matrix[i][j] == 1) {
				if (i + 1 < 5) {
					if (matrix[i + 1][j] == 0) {
						candidates[candidates_size][0] = i;
						candidates[candidates_size][1] = j;
						candidates[candidates_size][2] = i + 1;
						candidates[candidates_size][3] = j;
						candidates_size++;
					}
				}
				if (i - 1 >= 0) {
					if (matrix[i - 1][j] == 0) {
						candidates[candidates_size][0] = i;
						candidates[candidates_size][1] = j;
						candidates[candidates_size][2] = i - 1;
						candidates[candidates_size][3] = j;
						candidates_size++;
					}
				}
				if (j + 1 < 5) {
					if (matrix[i][j + 1] == 0) {
						candidates[candidates_size][0] = i;
						candidates[candidates_size][1] = j;
						candidates[candidates_size][2] = i;
						candidates[candidates_size][3] = j + 1;
						candidates_size++;
					}
				}
				if (j - 1 >= 0) {
					if (matrix[i][j - 1] == 0) {
						candidates[candidates_size][0] = i;
						candidates[candidates_size][1] = j;
						candidates[candidates_size][2] = i;
						candidates[candidates_size][3] = j - 1;
						candidates_size++;
					}
				}
			}
		}
	}

	srand(time(NULL));
	int move_idx = rand() % candidates_size;

	static int result[4];
	result[0] = candidates[move_idx][0];
	result[1] = candidates[move_idx][1];
	result[2] = candidates[move_idx][2];
	result[3] = candidates[move_idx][3];

	return result;
}


int* AIAlgorithm(const char* filename, bool movemade) {
	int iter_num;
	int newsize = strlen(filename);
	char* filename_copy = new char[newsize + 1];

	strcpy(filename_copy, filename);
	char* token = strtok(filename_copy, "/");
	while (token != NULL) {
		if (strstr(token, "state_") != NULL) {
			iter_num = atoi(strtok(token, "_") + 1);
			break;
		}
		token = strtok(NULL, "/");
	}

	int** matrix = load_matrix(filename);
	int start_row, start_col, end_row, end_col;

	if (movemade) {
		int* move = next_move_wolf(matrix);
		start_row = move[0];
		start_col = move[1];
		end_row = move[2];
		end_col = move[3];
	}
	else {
		int* move = next_move_sheep(matrix);
		start_row = move[0];
		start_col = move[1];
		end_row = move[2];
		end_col = move[3];
	}

	int** matrix2 = new int*[5];
	for (int i = 0; i < 5; i++) {
		matrix2[i] = new int[5];
		memcpy(matrix2[i], matrix[i], sizeof(int) * 5);
	}

	matrix2[end_row][end_col] =
		movemade ? 2 : 1;

	matrix2[start_row][start_col] =
		0;

	char buffer[50];
	sprintf(buffer, "state_%d.txt", iter_num + 1);
	
	char* str_filename = new char[newsize + 1];
	strcpy(str_filename, filename);
	char *p = strstr(str_filename, "state_");
	sprintf(p, "%s", buffer);

	write_matrix(matrix2, str_filename);
	// Allocate memory for the result array using new
	int* result = new int[4];

	// Store the four values in the array
	result[0] = start_row;
	result[1] = start_col;
	result[2] = end_row;
	result[3] = end_col;
	return result;
}

//
extern "C"
{
	
	int** load_matrix_c(const char* matrix_file_name) {
		return load_matrix(matrix_file_name);
	}
	void write_matrix_c(int** matrix, const char* matrix_file_name_output) {
		return write_matrix(matrix, matrix_file_name_output);

	}
	int* next_move_sheep_c(int** matrix) {
		return next_move_sheep(matrix);

	}
	int* AIAlgorithm_c(const char* filename, bool movemade)  {
		return AIAlgorithm(filename, movemade);
	}
}


