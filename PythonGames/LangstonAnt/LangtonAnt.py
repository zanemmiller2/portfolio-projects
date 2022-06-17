# Name: Zane Miller
# Date: August 2, 2021
# Description: Simulation for a virtual "ant" that moves about a two-dimensional square matrix, whose spaces can be
#              designated white or black, according to specific rules.

class Ant:
    """ Represents an Ant that simulates Langton's Ant """

    def __init__(self, board_size, ant_y_coord, ant_x_coord, orientation, simulation_steps):
        """
        creates a new Ant simulation with board size, initial ant coordinates and orientation,
        and number of steps the simulation will iterate
        """
        x_coord = 0
        y_coord = 0
        color = "_"
        board_array = []
        ant_location = ant_x_coord + (board_size * ant_y_coord)
        board_matrix = ""

        self._board_size = board_size
        self._ant_y_coord = ant_y_coord
        self._ant_x_coord = ant_x_coord
        self._orientation = orientation
        self._simulation_steps = simulation_steps
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._color = color
        self._board_array = board_array
        self._ant_location = ant_location
        self._board_matrix = board_matrix
        self.board_array()

    def board_array(self):
        """ creates a list that represents the initial coordinate and color of each square on the board """
        for num in range(0, (self._board_size**2)):
            while self._x_coord < self._board_size:
                self._board_array.append([[self._x_coord, self._y_coord], self._color])
                self._x_coord += 1
            self._x_coord = 0
            self._y_coord += 1
            if self._y_coord == self._board_size:
                return self._board_array

    def run_simulation(self):
        """ runs the Langton Ant simulation and calls the board_array function """
        step_counter = 1
        if self._board_size == 0:
            return False
        while step_counter <= self._simulation_steps:
            # turns ant right when on white
            if self._board_array[self._ant_location][1] == "_":
                if self._orientation == 3:
                    self._orientation = 0
                else:
                    self._orientation = self._orientation + 1

            # turns ant left when on black
            if self._board_array[self._ant_location][1] == "#":
                if self._orientation == 0:
                    self._orientation = 3
                else:
                    self._orientation = self._orientation - 1

            # moves ant in direction according to its orientation
            if self._orientation == 0:
                self.move_up()
            elif self._orientation == 1:
                self.move_right()
            elif self._orientation == 2:
                self.move_down()
            elif self._orientation == 3:
                self.move_left()
            step_counter += 1
        return self.print_board()

    def move_up(self):
        """ moves the ant up """
        # update ant coordinates
        if self._ant_y_coord != 0:
            self._ant_y_coord = self._ant_y_coord - 1
        elif self._ant_y_coord == 0:  # sets condition for looping
            self._ant_y_coord = self._ant_y_coord + (self._board_size - 1)
        self._ant_location = self._ant_x_coord + self._board_size * self._ant_y_coord

        # update color
        if self._ant_y_coord < (self._board_size - 1):
            if self._board_array[self._ant_location + self._board_size][1] == "_":
                self._board_array[self._ant_location + self._board_size][1] = "#"
            elif self._board_array[self._ant_location + self._board_size][1] == "#":
                self._board_array[self._ant_location + self._board_size][1] = "_"
        elif self._ant_y_coord == (self._board_size - 1):
            if self._board_array[self._ant_location - (self._ant_y_coord * self._board_size)][1] == "_":
                self._board_array[self._ant_location - (self._ant_y_coord * self._board_size)][1] = "#"
            elif self._board_array[self._ant_location - (self._ant_y_coord * self._board_size)][1] == "#":
                self._board_array[self._ant_location - (self._ant_y_coord * self._board_size)][1] = "_"

        return self._ant_x_coord, self._ant_y_coord

    def move_right(self):
        """ moves the ant right """
        # update ant coordinates
        if self._ant_x_coord < (self._board_size - 1):
            self._ant_x_coord = self._ant_x_coord + 1
        elif self._ant_x_coord == (self._board_size - 1):  # sets condition for looping
            self._ant_x_coord = self._ant_x_coord - (self._board_size - 1)
        self._ant_location = self._ant_x_coord + self._board_size * self._ant_y_coord

        # update color
        if self._ant_x_coord > 0:
            if self._board_array[self._ant_location - 1][1] == "_":
                self._board_array[self._ant_location - 1][1] = "#"
            elif self._board_array[self._ant_location - 1][1] == "#":
                self._board_array[self._ant_location - 1][1] = "_"
        elif self._ant_x_coord == 0:
            if self._board_array[self._ant_location + (self._board_size - 1)][1] == "_":
                self._board_array[self._ant_location + (self._board_size - 1)][1] = "#"
            elif self._board_array[self._ant_location + (self._board_size - 1)][1] == "#":
                self._board_array[self._ant_location + (self._board_size - 1)][1] = "_"

        return self._ant_x_coord, self._ant_y_coord

    def move_down(self):
        """ moves the ant down """
        # update ant coordinates
        if self._ant_y_coord < (self._board_size - 1):
            self._ant_y_coord = self._ant_y_coord + 1
        elif self._ant_y_coord == (self._board_size - 1):  # sets condition for looping
            self._ant_y_coord = self._ant_y_coord - (self._board_size - 1)
        self._ant_location = self._ant_x_coord + self._board_size * self._ant_y_coord

        # update color
        if self._ant_y_coord > 0:
            if self._board_array[self._ant_location - self._board_size][1] == "_":
                self._board_array[self._ant_location - self._board_size][1] = "#"
            elif self._board_array[self._ant_location - self._board_size][1] == "#":
                self._board_array[self._ant_location - self._board_size][1] = "_"
        elif self._ant_y_coord == 0:
            if self._board_array[self._ant_location + (self._board_size * (self._board_size - 1))][1] == "_":
                self._board_array[self._ant_location + (self._board_size * (self._board_size - 1))][1] = "#"
            elif self._board_array[self._ant_location + (self._board_size * (self._board_size - 1))][1] == "#":
                self._board_array[self._ant_location + (self._board_size * (self._board_size - 1))][1] = "_"

        return self._ant_x_coord, self._ant_y_coord

    def move_left(self):
        """ moves the ant left """
        # update ant coordinates
        if self._ant_x_coord != 0:
            self._ant_x_coord = self._ant_x_coord - 1
        elif self._ant_x_coord == 0:  # sets condition for looping
            self._ant_x_coord = self._ant_x_coord + (self._board_size - 1)
        self._ant_location = self._ant_x_coord + self._board_size * self._ant_y_coord

        # update color
        if self._ant_x_coord < (self._board_size - 1):
            if self._board_array[self._ant_location + 1][1] == "_":
                self._board_array[self._ant_location + 1][1] = "#"
            elif self._board_array[self._ant_location + 1][1] == "#":
                self._board_array[self._ant_location + 1][1] = "_"
        elif self._ant_x_coord == (self._board_size - 1):
            if self._board_array[self._ant_location - (self._board_size - 1)][1] == "_":
                self._board_array[self._ant_location - (self._board_size - 1)][1] = "#"
            elif self._board_array[self._ant_location - (self._board_size - 1)][1] == "#":
                self._board_array[self._ant_location - (self._board_size - 1)][1] = "_"

        return self._ant_x_coord, self._ant_y_coord

    def print_board(self):
        """ prints the ending board after simulation has run """
        self._board_array[self._ant_location][1] = "8"  # updates symbol to represent ant's location on board
        for row in range(0, self._board_size):
            for column in range(0, self._board_size):
                self._board_matrix += self._board_array[column + self._board_size * row][1]
                if column == self._board_size - 1:
                    print(self._board_matrix)
                    self._board_matrix = ""
        if self._simulation_steps == 0:
            return self._board_matrix
        return self._board_matrix


def main():
    """ collects user inputs """
    board_size = int(input("First, please enter a number no larger than 100 for the size of the square board:\n"))
    ant_y_coord = int(input("Choose the ant’s starting location, please enter a number as the starting row number"
                            " (where 0 is the first row from the top):\n"))
    ant_x_coord = int(input("Please enter a number as the starting column number (where 0 is the first column from"
                            " the left):\n"))
    orientation = int(input("Please choose the ant’s starting orientation, 0 for up, 1 for right, 2 for down, 3 for"
                            " left:\n"))
    simulation_steps = int(input("Please enter the number of steps for the simulation:\n"))
    ant = Ant(board_size, ant_y_coord, ant_x_coord, orientation, simulation_steps)
    ant.run_simulation()


main()
