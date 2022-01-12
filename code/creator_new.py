import numpy as np
import pandas as pd
import random
from collections import defaultdict
from solver import update_locally, update_for_squares, find_range, check_truth_matrix, initiate_truth_matrix

def better_check(sudoku, truth_matrix):
    empty_sudoku_indexes = np.where(sudoku == 0)
    coordinates_empty_sudoku = list(zip(empty_sudoku_indexes[0], empty_sudoku_indexes[1]))

    for cor in coordinates_empty_sudoku:
        row_i = cor[0]
        col_i = cor[1]
        frame_i = range(0,9)
        if check_truth_matrix(row_i, col_i, truth_matrix, frame_i, threshold=0):
            return True


def creator():
    sudoku = np.zeros((9,9))
    truth_matrix = np.ones((9,9,9))
    assigned_number = []
    temp_not_to_choose = []

    sudoku_indexes = np.where(sudoku == 0)
    sudoku_coordinates = list(zip(sudoku_indexes[0],  sudoku_indexes[1]))

    i = 0

    while np.sum(sudoku) < 405:
        cor = sudoku_coordinates[i]
        row_i = cor[0]
        col_i = cor[1]

        number_options = list(np.where(truth_matrix[:, row_i, col_i] == 1)[0])
        number_options = [nr for nr in number_options if nr not in temp_not_to_choose]
        random.shuffle(number_options)

        count_till_backtrack = len(number_options)
        for number in number_options:
            # assign random coordinate to sudoku
            sudoku[row_i, col_i] = number + 1
            # update truth matrix for random coordinate
            truth_matrix = update_locally(number, row_i, col_i, truth_matrix)
            truth_matrix = update_for_squares(truth_matrix)

            check = better_check(sudoku, truth_matrix)
            if check:
                sudoku[row_i, col_i] = 0
                truth_matrix = initiate_truth_matrix(sudoku)
                count_till_backtrack -= 1
            else:
                assigned_number.append(number)
                temp_not_to_choose = []
                break

        if count_till_backtrack == 0:
            print("BACKTRACK THIS BITCH")
            print(cor)
            print(number_options)
            temp_not_to_choose.append(assigned_number[i-1])
            assigned_number = assigned_number[0:-1]

            i -= 1
            cor = sudoku_coordinates[i]
            row_i = cor[0]
            col_i = cor[1]
            sudoku[row_i, col_i] = 0
            truth_matrix = initiate_truth_matrix(sudoku)

        else:
            i += 1

        print(sudoku)
        print(assigned_number)



if __name__ == "__main__":
    creator()