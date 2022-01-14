import numpy as np
import pandas as pd
import random
from collections import defaultdict
from solver import update_locally, update_for_squares, check_truth_matrix, initiate_truth_matrix, solver


def check_legal_move_filling_grid(sudoku, truth_matrix, threshold):
    empty_sudoku_indexes = np.where(sudoku == 0)
    coordinates_empty_sudoku = list(zip(empty_sudoku_indexes[0], empty_sudoku_indexes[1]))

    for cor in coordinates_empty_sudoku:
        row_i = cor[0]
        col_i = cor[1]
        frame_i = range(0,9)
        if check_truth_matrix(row_i, col_i, truth_matrix, frame_i, threshold):
            return False

    return True

def create_random_grid():
    sudoku = np.zeros((9,9))
    truth_matrix = np.ones((9,9,9))
    assigned_number = []
    temp_not_to_choose = [[]]

    sudoku_indexes = np.where(sudoku == 0)
    sudoku_coordinates = list(zip(sudoku_indexes[0],  sudoku_indexes[1]))

    i = 0

    while np.sum(sudoku) < 405:
        cor = sudoku_coordinates[i]
        row_i = cor[0]
        col_i = cor[1]

        number_options = list(np.where(truth_matrix[:, row_i, col_i] == 1)[0])
        number_options = [nr for nr in number_options if nr not in temp_not_to_choose[i]]
        random.shuffle(number_options)

        count_till_backtrack = len(number_options)
        for number in number_options:
            # assign random coordinate to sudoku
            sudoku[row_i, col_i] = number + 1
            # update truth matrix for random coordinate
            truth_matrix = update_locally(number, row_i, col_i, truth_matrix)
            truth_matrix = update_for_squares(truth_matrix)

            legal_move = check_legal_move_filling_grid(sudoku, truth_matrix, threshold=0)
            if legal_move:
                assigned_number.append(number)
                i += 1
                temp_not_to_choose.append([])
                break
            else:
                sudoku[row_i, col_i] = 0
                truth_matrix = initiate_truth_matrix(sudoku)
                count_till_backtrack -= 1

        if count_till_backtrack == 0:
            i -= 1

            temp_not_to_choose[i].append(assigned_number[i])
            temp_not_to_choose = temp_not_to_choose[0:-1]
            assigned_number = assigned_number[0:-1]

            cor = sudoku_coordinates[i]
            row_i = cor[0]
            col_i = cor[1]
            sudoku[row_i, col_i] = 0
            truth_matrix = initiate_truth_matrix(sudoku)

    return sudoku


def check_legal_removing_numbers(cor, removed_number, truth_matrix):
    frame_i = int(removed_number-1)
    row_i = cor[0]
    col_i = cor[1]
    if check_truth_matrix(row_i, col_i, truth_matrix, frame_i, 1):
        return True

    return False

def create_sudoku():
    start_sudoku = create_random_grid()
    sudoku = np.copy(start_sudoku)
    print(sudoku)
    sudoku_indexes = np.where(sudoku != 0)
    sudoku_coordinates = list(zip(sudoku_indexes[0], sudoku_indexes[1]))
    random.shuffle(sudoku_coordinates)
    temp_not_to_use = []

    while len(sudoku_coordinates) > 20:
        random_cor = random.choice(sudoku_coordinates)
        # print(random_cor)
        row_i = random_cor[0]
        col_i = random_cor[1]
        removed_number = sudoku[row_i, col_i]
        sudoku[row_i, col_i] = 0
        truth_matrix = initiate_truth_matrix(sudoku)
        # print(sudoku)


        # kan veel efficiënter --> er moet gewoon altijd minstens één optie open zijn dus in dat er in een rij maar één eentje staat.
        # moet de check daarvoor net wat aanpassen, zou prima te doen moeten zijn.
        frame_i = int(removed_number-1)
        threshold =1
        legal_move = check_truth_matrix(row_i, col_i, truth_matrix, frame_i, threshold)
        if legal_move:
            sudoku_coordinates = [cor for cor in sudoku_coordinates if cor != random_cor]
            temp_not_to_use = []
        else:
            sudoku[row_i, col_i] = removed_number
            temp_not_to_use.append(random_cor)

        # print(sudoku)
        # sudoku_solved = solver(np.copy(sudoku))
        # if np.array_equal(start_sudoku, sudoku_solved):
        #     sudoku_coordinates = [cor for cor in sudoku_coordinates if cor != random_cor]
        #     temp_not_to_use = []
        # else:
        #     sudoku[row_i, col_i] = removed_number
        #     temp_not_to_use.append(random_cor)

        if len(temp_not_to_use) == len(sudoku_coordinates):
            print("ran out of options, stopped by: {}".format(len(sudoku_coordinates)))
            return sudoku


        # print(len(sudoku_coordinates))
        # print(sudoku)

        # legal_move = check_legal_removing_numbers(sudoku, truth_matrix, threshold=0)
        # if legal_move:
        #     sudoku_coordinates = [cor for cor in sudoku_coordinates if cor != random_cor]
        # else:
        #     sudoku[row_i, col_i] = removed_number

    return sudoku


if __name__ == "__main__":
    sudoku = create_sudoku()
    print(sudoku)
    sudoku_solved = solver(sudoku)
    print(sudoku_solved)