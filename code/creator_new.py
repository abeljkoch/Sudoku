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
            print(len(coordinates_empty_sudoku))
            return True


def creator():
    sudoku = np.zeros((9,9))
    truth_matrix = np.ones((9,9,9))
    assigned_coordinates = []
    temp_not_to_choose = []


    while np.sum(sudoku) < 405:
        # get the indexes of all possible options in the truth matrix
        indexes_truths = np.where(truth_matrix == 1)

        # zip indexes into coordinates
        coordinates = list(zip(indexes_truths[0],  indexes_truths[1], indexes_truths[2]))
        # remove temp not to choose
        coordinates = [cor for cor in coordinates if cor not in temp_not_to_choose]

        if len(coordinates) == 0:
            print(assigned_coordinates)
            last_coordinate = assigned_coordinates[-1]
            temp_not_to_choose = [last_coordinate]
            assigned_coordinates = assigned_coordinates[0:-1]
            sudoku[last_coordinate[1], last_coordinate[2]] = 0
            truth_matrix = initiate_truth_matrix(sudoku)
            continue

        # choose random coordinate
        cor = random.choice(coordinates)
        # print("len coordinates: ", len(coordinates))
        # print(cor)
        frame_i = cor[0]
        row_i = cor[1]
        col_i = cor[2]

        # assign random coordinate to sudoku
        sudoku[row_i, col_i] = frame_i + 1
        # update truth matrix for random coordinate
        truth_matrix = update_locally(frame_i, row_i, col_i, truth_matrix)
        truth_matrix = update_for_squares(truth_matrix)

        # check if assigned number is legal
        check = better_check(sudoku, truth_matrix)
        if check:
            sudoku[row_i, col_i] = 0
            truth_matrix = initiate_truth_matrix(sudoku)
            temp_not_to_choose.append(cor)
        else:
            assigned_coordinates.append(cor)
            temp_not_to_choose = []
            print(sudoku)

        # print(temp_not_to_choose)
        # print(sudoku)
        # print()

if __name__ == "__main__":
    creator()