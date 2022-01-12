import numpy as np
import pandas as pd
import random
import os

def find_range(int):
    if int < 3:
        r = (0, 3)
        return r
    elif int < 6:
        r = (3, 6)
        return r
    elif int < 9:
        r = (6, 9)
        return r
    else:
        raise ValueError("Wrong input in find_range function")


def check_row(frame_i, row_i, truth_matrix, threshold):
    if np.sum(truth_matrix[frame_i, row_i]) == threshold:
        return True
    else:
        return False


def check_column(frame_i, col_i, truth_matrix, threshold):
    if np.sum(truth_matrix[frame_i, :, col_i]) == threshold:
        return True
    else:
        return False


def check_square(frame_i, row_i, col_i, truth_matrix, threshold):
    row_range = find_range(row_i)
    col_range = find_range(col_i)
    if np.sum(truth_matrix[frame_i, row_range[0]:row_range[1], col_range[0]:col_range[1]]) == threshold:
        return True
    else:
        return False


def check_coordinate_option(row_i, col_i, truth_matrix, threshold):
    if np.sum(truth_matrix[:, row_i, col_i]) == threshold:
        return True
    else:
        return False


def check_truth_matrix(row_i, col_i, truth_matrix, frame_i, threshold = 1):
    if check_row(frame_i, row_i, truth_matrix, threshold):
        return True
    elif check_column(frame_i, col_i, truth_matrix, threshold):
        return True
    elif check_square(frame_i, row_i, col_i, truth_matrix, threshold):
        return True
    elif check_coordinate_option(row_i, col_i, truth_matrix, threshold):
        return True
    else:
        return False


def update_locally(number, row_i, col_i, truth_matrix):
    # simple rules
    truth_matrix[number, row_i] = 0
    truth_matrix[number, :, col_i] = 0
    truth_matrix[:, row_i, col_i] = 0

    # get range of square in which the coordinated is located
    row_range = find_range(row_i)
    col_range = find_range(col_i)
    truth_matrix[number, row_range[0]:row_range[1], col_range[0]:col_range[1]] = 0

    return truth_matrix


def update_for_squares(truth_matrix):
    ## function for finding two or three aligned options within a truth square
    ## aligned options within a square allows for eliminating options in that same row or column

    # define all truth squares
    all_truth_squares = [[frame_i, row_i, col_i] for frame_i in range(0,9) for row_i in range(0,9,3) for col_i in range(0,9,3)]

    for square in all_truth_squares:
        # define the square coordinates
        frame_i = square[0]
        row_i = square[1]
        col_i = square[2]

        # define the range of the square
        row_range = find_range(row_i)
        col_range = find_range(col_i)

        # if the square does not contain options then skip
        if np.sum(truth_matrix[frame_i, row_range[0]:row_range[1], col_range[0]:col_range[1]]) == 0:
            continue

        # get the options indexes of within the whole frame
        option_indexes = np.where(truth_matrix[frame_i] == 1)
        total_rows = option_indexes[0]
        total_cols = option_indexes[1]

        # define the rows and columns of the options within the square
        rows = [row for row, col in zip(total_rows, total_cols) if row in range(row_range[0], row_range[1]) and col in range(col_range[0], col_range[1])]
        cols = [col for row, col in zip(total_rows, total_cols) if row in range(row_range[0], row_range[1]) and col in range(col_range[0], col_range[1])]

        # if all options are on the same row or column and they exist of two or three options within the square:
        # remove options for that row or column in the truth matrix
        if len(set(rows)) == 1 and 2 <= len(rows) <= 3:
            row = rows[0]
            truth_matrix[frame_i, row] = truth_matrix[frame_i, row] = [0 if i not in cols else truth_matrix[frame_i, row][i] for i in range(0, 9)]
        elif len(set(cols)) == 1 and 2 <= len(cols) <= 3:
            col = cols[0]
            truth_matrix[frame_i, :, col] = truth_matrix[frame_i, :, col] = [0 if i not in rows else truth_matrix[frame_i, :, col][i] for i in range(0, 9)]


    return truth_matrix


def initiate_truth_matrix(sudoku):
    # define truth matrix
    truth_matrix = np.ones((9, 9, 9))

    for i in range(0,9):
        # get indexes of numbers (1 till 9) in sudoku
        indexes = np.where(sudoku == i+1)

        # zip indexes into coordinates
        rows = indexes[0]
        cols = indexes[1]
        coordinates = list(zip(rows, cols))

        # loop through individual coordinates
        for cor in coordinates:
            row_i = cor[0]
            col_i = cor[1]
            truth_matrix = update_locally(i, row_i, col_i, truth_matrix)

        truth_matrix = update_for_squares(truth_matrix)
    return truth_matrix


def solver(sudoku):
    ## sudoku solver function
    ## based on a truth matrix that keeps the options for every individual number in the sudoku
    ## based on these options the algorithm will select the options that can be filled in the sudoku

    # initate the truth matrix
    truth_matrix = initiate_truth_matrix(sudoku)

    print(sudoku)

    # keep on solving untill the whole sudoku is solved
    while np.isnan(np.sum(sudoku)):
        # get the indexes of all possible options in the truth matrix
        indexes_truths = np.where(truth_matrix == 1)
        # zip indexes into coordinates
        frames = indexes_truths[0]
        rows = indexes_truths[1]
        cols = indexes_truths[2]
        coordinates = list(zip(frames, rows, cols))
        random.shuffle(coordinates)
        # print(coordinates)

        # loop trough all coordinates
        for cor in coordinates:
            frame_i = cor[0]
            row_i = cor[1]
            col_i = cor[2]

            # if the truth option falls within the rules, fill the sudoku with the number of that option
            if check_truth_matrix(row_i, col_i, truth_matrix, frame_i):
                sudoku[row_i, col_i] = frame_i + 1
                truth_matrix = update_locally(frame_i, row_i, col_i, truth_matrix)
                truth_matrix = update_for_squares(truth_matrix)
                break

    print(sudoku)


if __name__ == "__main__":
    main_folder = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    sudoku_folder = main_folder + "/examples"
    sudoku = pd.read_csv(sudoku_folder + "/test_sudoku192.csv", header=None).values
    solver(sudoku)

