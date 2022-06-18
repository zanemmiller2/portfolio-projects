# Author: Zane Miller
# Date: 06/17/2022
# Email: millerzanem@gmail.com
# Description: Places n-queens on a nxn board such that no queens threaten another by moving
#              horizontally, vertically, or diagonally
import copy


class NQueen:
	"""
	temp
	"""

	def __init__(self, n):
		"""
		temp
		"""
		self.n = n

		if self.n > 3:
			self.board_array = self.initialize_board()
			if self.find_solution():
				self.print_solution()

		else:
			print("No Solution: board not big enough")

	def print_solution(self):
		for row in self.board_array:
			print(row)

	def initialize_board(self):
		""" Initializes the game board as a nxn matrix of 0's """

		board = []
		for row in range(self.n):
			column_array = []
			for column in range(self.n):
				column_array.append(0)
			board.append(column_array)

		return board

	def get_board(self):
		""" Returns the current board state """
		return self.board_array

	def find_solution(self, column=0):
		"""
		Finds each solution of the n-queens problem
		"""

		# all queens have been placed
		if column >= self.n:
			return True

		for row in range(self.n):
			if self.check_safe(row, column):

				self.update_queen(row, column)

				if self.find_solution(column + 1):
					return True

				self.board_array[row][column] = 0

		return False

	def check_safe(self, row, column):

		if (self.check_row(row, column)
					and self.check_diagonal_upper(row, column)
					and self.check_diagonal_lower(row, column)):

			return True

		return False

	def update_queen(self, row, column):
		""" Places queen in given row, column """
		self.board_array[row][column] = 1

	def check_row(self, row, column):
		""" Blocks the remaining board spaces in the row """

		for space in range(column):
			if self.board_array[row][space] == 1:
				return False

		return True

	def check_diagonal_upper(self, row, column):
		""" Blocks the board spaces diagonally down right """

		for row_space, column_space in zip(range(row, -1, -1), range(column, -1, -1)):
			if self.board_array[row_space][column_space] == 1:
				return False

		return True

	def check_diagonal_lower(self, row, column):
		""" Checks the board spaces diagonally down left """

		for row_space, column_space in zip(range(row, self.n, 1), range(column, -1, -1)):
			if self.board_array[row_space][column_space] == 1:
				return False

		return True



if __name__ == '__main__':
	test = NQueen(8)
