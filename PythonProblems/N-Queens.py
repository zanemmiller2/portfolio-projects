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
				self.get_solution()

		else:
			print("No Solution: board not big enough")

	def get_solution(self):
		""" Prints the solution for the given n-queens problem """
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
		""" Finds the first solution of the n-queens problem """

		# all queens have been placed
		if column >= self.n:
			return True

		for row in range(self.n):
			# Check the current space is a valid space to place a queen.
			if self.check_safe(row, column):

				# place the queen at the current index
				self.update_queen(row, column)

				# Check the next column for placing a queen
				if self.find_solution(column + 1):
					return True

				# backtrack - reset the current index and try the next one
				self.board_array[row][column] = 0

		# All the rows in a given column are invalid spaces for a queen
		return False

	def check_safe(self, row, column):
		"""
		Checks if the current index is a valid index to place a queen.
		Checks horizontally and diagonally
		"""

		if (self.check_row(row, column)
					and self.check_diagonal_upper(row, column)
					and self.check_diagonal_lower(row, column)):

			return True

		return False

	def update_queen(self, row, column):
		""" Places queen in given row, column """
		self.board_array[row][column] = 1

	def check_row(self, row, column):
		""" Checks if a queen can be attacked horizontally """

		for space in range(column):
			if self.board_array[row][space] == 1:
				return False

		return True

	def check_diagonal_upper(self, row, column):
		""" Checks if a queen can be attacked diagonally """

		for row_space, column_space in zip(range(row, -1, -1), range(column, -1, -1)):
			if self.board_array[row_space][column_space] == 1:
				return False

		return True

	def check_diagonal_lower(self, row, column):
		""" Checks if a queen can be attacked diagonally """

		for row_space, column_space in zip(range(row, self.n, 1), range(column, -1, -1)):
			if self.board_array[row_space][column_space] == 1:
				return False

		return True



if __name__ == '__main__':
	test = NQueen(8)
	print("9 \n")
	test2 = NQueen(9)
	print("10 \n")
	test3 = NQueen(10)
	print("11 \n")
	test2 = NQueen(11)
	print("12 \n")
	test3 = NQueen(12)
	print("13 \n")
	test2 = NQueen(13)
	print("14 \n")
	test3 = NQueen(14)
