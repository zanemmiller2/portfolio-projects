# Author: 
# Date:
# Description:
board_size = 3
board_array = [[[0, 0], '8'], [[1, 0], '-'], [[2, 0], '-'], [[0, 1], '#'], [[1, 1], '-'], [[2, 1], '-'], [[0, 2], '-'], [[1, 2], '-'], [[2, 2], '-']]
outline = " "
for row in range(0, board_size):
    for column in range(0, board_size):
        outline += board_array[column + board_size * row][1]
        if column == board_size - 1:
            print(outline)
            outline = " "






