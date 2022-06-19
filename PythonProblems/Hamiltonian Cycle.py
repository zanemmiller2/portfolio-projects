# Author: Zane Miller
# Date: 06/18/2022
# Email: millerzanem@gmail.com
# Description: Defines an object for an Undirected graph and functionality to find a hamiltonian
#       path and hamiltonian cycle in the undirected graph.
#
#       A Hamiltonian Cycle is a path that starts and ends with the same vertex and visits each
#       other vertex exactly once.
#       (https://www.geeksforgeeks.org/hamiltonian-cycle-backtracking-6/)
#
#       A Hamiltonian Path visits each vertex in the graph exactly once but does not necessarily
#       start and end with the same vertex.
#       (https://www.geeksforgeeks.org/hamiltonian-path-using-dynamic-programming/)

import math


class UndirectedGraph:
	""" Creates an object that represents an undirected graph """

	def __init__(self, graph):
		""" Initializes an object for the undirected graph """

		self.graph = graph
		self.n = len(self.graph)
		self.path = []
		self.cycle = []

	def get_graph(self):
		""" Returns the current undirected graph """
		return self.graph

	def is_complete(self):
		""" Returns True if the undirected graph is complete """
		pass

	def num_cycles(self) -> int:
		""" Returns integer of the number of Hamiltonian Cycles in an undirected graph """

		return math.factorial(int(self.n - 1)) // 2

	def get_path(self):
		""" Prints the Hamiltonian Path for the current graph """
		pass

	def hamiltonian_path(self):
		"""
		Finds the hamiltonian path in the undirected graph. A path visits each vertex exactly once
		BUT does not end with the same vertex it starts at.
		"""
		pass

	def is_valid_path(self, vertex, current_position):
		""" Checks that the next move is a valid route through the graph """
		pass

	def get_cycle(self):
		""" Prints the Hamiltonian Cycle for the current graph """
		pass

	def hamiltonian_cycle(self):
		"""
		Finds the hamiltonian cycle in the undirected graph. A path visits each vertex exactly once
		AND ends with the same vertex it starts at.
		"""
		pass

	def all_hamiltonian_cycles(self):
		""" Returns ALL the hamiltonian cycles in the undirected graph. """

if __name__ == '__main__':

	undir_graph = [[0, 1, 0, 0, 0, 1],
	               [1, 0, 1, 0, 0, 0],
	               [0, 1, 0, 0, 1, 0],
	               [0, 0, 1, 1, 0, 1],
	               [1, 0, 0, 1, 1, 0]]
