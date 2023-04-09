import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ai_algorithm{
    public static void main(String[] args) {
        int[] ints = AIAlgorithm("./state_0.txt", true);
        System.out.printf("1");
    }

    public static int[][] load_matrix(String matrixFileName) throws FileNotFoundException {

        File file = new File(matrixFileName);
        Scanner scanner = new Scanner(file);
        String data = scanner.useDelimiter("\\A").next();
        scanner.close();
        String[] data2 = data.replace("\n", ",").split(",");
        int[][] matrix = new int[5][5];
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                matrix[i][j] = Integer.parseInt(data2[5 * i + j].replace("\r",""));
            }
        }
        return matrix;
    }

    public static void write_matrix(int[][] matrix, String matrixFileNameOutput) throws FileNotFoundException {
        PrintWriter printWriter = new PrintWriter(new File(matrixFileNameOutput));
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                printWriter.print(matrix[i][j]);
                if (j < 4) {
                    printWriter.print(",");
                }
                if (j == 4) {
                    printWriter.print("\n");
                }
            }
        }
        printWriter.close();
    }

    public static int[] next_move_wolf(int[][] matrix) {
        List<int[]> candidates = new ArrayList<int[]>();
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                if (matrix[i][j] == 2) {
                    if (i + 1 < 5) {
                        if (matrix[i + 1][j] == 0) {
                            int[] candidate = new int[] {i, j, i + 1, j};
                            candidates.add(candidate);
                        }
                    }
                    if (i - 1 >= 0) {
                        if (matrix[i - 1][j] == 0) {
                            int[] candidate = new int[] {i, j, i - 1, j};
                            candidates.add(candidate);
                        }
                    }
                    if (j + 1 < 5) {
                        if (matrix[i][j + 1] == 0) {
                            int[] candidate = new int[] {i, j, i, j + 1};
                            candidates.add(candidate);
                        }
                    }
                    if (j - 1 >= 0) {
                        if (matrix[i][j - 1] == 0) {
                            int[] candidate = new int[] {i, j, i, j - 1};
                            candidates.add(candidate);
                        }
                    }
                    if (i + 2 < 5) {
                        if (matrix[i + 2][j] == 1 && matrix[i + 1][j] == 0) {
                            int[] candidate = new int[] {i, j, i + 2, j};
                            candidates.add(candidate);
                        }
                    }
                    if (i - 2 >= 0) {
                        if (matrix[i - 2][j] == 1 && matrix[i - 1][j] == 0) {
                            int[] candidate = new int[] {i, j, i - 2, j};
                            candidates.add(candidate);
                        }
                    }
                    if (j + 2 < 5) {
                        if (matrix[i][j + 2] == 1 && matrix[i][j + 1] == 0) {
                            int[] candidate = new int[] {i, j, i, j + 2};
                            candidates.add(candidate);
                        }
                    }
                    if (j - 2 >= 0) {
                        if (matrix[i][j - 2] == 1 && matrix[i][j - 1] == 0) {
                            int[] candidate = new int[] {i, j, i, j - 2};
                            candidates.add(candidate);
                        }
                    }
                }
            }
        }
        Random random = new Random();
        int moveIdx = random.nextInt(candidates.size());
        return candidates.get(moveIdx);
    }

    public static int[] next_move_sheep(int[][] matrix) {
        List<int[]> candidates = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                if (matrix[i][j] == 1) {
                    if (i + 1 < 5 && matrix[i + 1][j] == 0) {
                        candidates.add(new int[]{i, j, i + 1, j});
                    }
                    if (i - 1 >= 0 && matrix[i - 1][j] == 0) {
                        candidates.add(new int[]{i, j, i - 1, j});
                    }
                    if (j + 1 < 5 && matrix[i][j + 1] == 0) {
                        candidates.add(new int[]{i, j, i, j + 1});
                    }
                    if (j - 1 >= 0 && matrix[i][j - 1] == 0) {
                        candidates.add(new int[]{i, j, i, j - 1});
                    }
                }
            }
        }
        Random rand = new Random();
        int[] move = candidates.get(rand.nextInt(candidates.size()));
        return move;
    }

    public static int[][] copy_matrix(int[][] matrix) {
        int[][] copy = new int[5][5];
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                copy[i][j] = matrix[i][j];
            }
        }
        return copy;
    }

    public static int[] AIAlgorithm(String filename, boolean movemade) {
        String[] iter_num_arr = filename.split("/");
        String iter_num_str = iter_num_arr[iter_num_arr.length - 1].split("\\.")[0].split("_")[1];
        int iter_num = Integer.parseInt(iter_num_str);
        int[][] matrix = null;
        try{
            matrix = load_matrix(filename);
        } catch (FileNotFoundException e) {
            System.out.println("Error: file not found");
            System.exit(1);
        }
        
        int[] result = new int[4];
        
        if (movemade) {
            int[] next_move_wolf_result = next_move_wolf(matrix);
            int start_row = next_move_wolf_result[0];
            int start_col = next_move_wolf_result[1];
            int end_row = next_move_wolf_result[2];
            int end_col = next_move_wolf_result[3];
            // int[][] matrix2 = null;
            int[][] matrix2 = copy_matrix(matrix);
            matrix2[end_row][end_col] = 2;
            matrix2[start_row][start_col] = 0;
            try{
                write_matrix(matrix2, filename.replace("state_" + iter_num, "state_" + (iter_num + 1)));
            } catch (FileNotFoundException e) {
                System.out.println("Error: file not found");
                System.exit(1);
            }
            // write_matrix(matrix2, filename.replace("state_" + iter_num, "state_" + (iter_num + 1)));
            result[0] = start_row;
            result[1] = start_col;
            result[2] = end_row;
            result[3] = end_col;
        } else {
            int[] next_move_sheep_result = next_move_sheep(matrix);
            int start_row = next_move_sheep_result[0];
            int start_col = next_move_sheep_result[1];
            int end_row = next_move_sheep_result[2];
            int end_col = next_move_sheep_result[3];
            int[][] matrix2 = copy_matrix(matrix);
            matrix2[end_row][end_col] = 1;
            matrix2[start_row][start_col] = 0;
            try{
                write_matrix(matrix2, filename.replace("state_" + iter_num, "state_" + (iter_num + 1)));
            } catch (FileNotFoundException e) {
                System.out.println("Error: file not found");
                System.exit(1);
            }
            // write_matrix(matrix2, filename.replace("state_" + iter_num, "state_" + (iter_num + 1)));
            result[0] = start_row;
            result[1] = start_col;
            result[2] = end_row;
            result[3] = end_col;
        }
        return result;
    }


}

