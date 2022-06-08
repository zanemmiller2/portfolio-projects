# Author: Zane Miller
# Date: 11/15/2021
# Description: Program for modeling/playing the game Hasami Shogi variant 1.
# Creates multiple classes to deal with creating a game, updating the board,
# the pieces,


class Pieces:
    """ Creates a piece to be used in the game Hasami Shogi Variant 1"""

    def __init__(self, piece_color, piece_location_y,
                 piece_location_x, piece_status="ON_BOARD"):
        """ Represents a piece with a color, location and status """
        self._piece_color = piece_color
        self._piece_location_x = piece_location_x
        self._piece_location_y = piece_location_y
        self._piece_status = piece_status

        self._piece = {"object_id"  : self,
                       "piece_color": self._piece_color,
                       "location"   :
                           [self._piece_location_y, self._piece_location_x],
                       "status"     : self._piece_status}


class HasamiShogiGame:
    """ Creates a Hasami Shogi game """

    def __init__(self, width=9, length=9):
        """
        Initializes width and length of board, dictionaries for red and black
        pieces, a board array, game_state to "UNFINISHED", active player to
        "BLACK", and the number of captured pieces for red and black to 0.
        :param width: initialized to 9
        :param length: initialized to 9
        """
        self._width = width
        self._length = length
        self._alphabet = "abcdefghi"
        self._space = ""
        self._piece_dict_black = {}
        self._piece_dict_red = {}
        self._board = self.initialize_board_array()
        self.create_game_pieces()
        self._game_state = "UNFINISHED"
        self._active_player = "BLACK"
        self._num_captured_pieces_red = 0
        self._num_captured_pieces_black = 0
        self._x_coord = 1
        self._y_coord = "a"
        self._move_from_x = 0
        self._move_from_y = 0
        self._move_to_x = 0
        self._move_to_y = 0
        self._array_north = []
        self._array_south = []
        self._array_east = []
        self._array_west = []
        self._corner_coordinates = ["a1", "a9", "i1", "i9"]
        self._move_to_corner_traps = ["a2", "a8", "b1", "b9",
                                      "h1", "h9", "i2", "i8"]

    def initialize_board_array(self):
        """
        Initializes the board array for the start of the current game. Adds the
        x- and y-coordinates, initializes the header row [1, 9] for printing
        the board, and initializes each space on the board as "NONE" (empty)
        and assigns each space the symbol "." to represent an empty space.
        returns: the self._board since this method is called in __init__ to
        initialize self._board at the creation of the object.
        """
        temp_board_array = []

        # initialize the header row
        for num in range(1, (self._width + 1)):
            temp_board_array += str(num)
        self._board = [temp_board_array]

        # Adds the coordinates (#, letter)
        for letter in self._alphabet:
            for num in range(1, (self._width + 1)):
                self._board += [[letter, num]]

        # Initializes each space as EMPTY and adds a '.' as its symbol
        for index in range(1, (self._width ** 2 + 1)):
            self._board[index].append("NONE")
            if self._board[index][2] == "NONE":
                self._board[index].append(".")

        return self._board

    def get_board_array(self):
        """
        Gets the current board array.
        :return: self._board
        """
        return self._board

    def convert_coordinates_xy(self, coordinate):
        """
        Converts single string coordinate to x- and y- individual coordinate
        values.
        :param coordinate: takes a single string coordinate ("a1").
        :return: returns the string value for coordinate y and the integer
        value for coordinate x.
        """
        self._x_coord = int(coordinate[1])
        self._y_coord = str(coordinate[0])

        return self._x_coord, self._y_coord

    def get_square_occupant(self, coordinate):
        """
        Gets the current occupant, if any, of the given space. Extracts the
        :param coordinate: takes a single string coordinate
        :return: returns the occupant (RED, BLACK, NONE) at that coordinate.
        """
        self._x_coord, self._y_coord = self.convert_coordinates_xy(coordinate)

        for row in self._board[1::]:
            if self._y_coord == row[0] and self._x_coord == row[1]:
                return row[2]
            else:
                continue

    def set_square_occupant(self, x_coord, y_coord, symbol):
        """
        Updates the symbol at a given x- and y-coordinate based on the symbol
        it receives.
        :param x_coord: integer value of the x-coordinate.
        :param y_coord: string value of the y-coordinate
        :param symbol: symbol to be represented in the coordinate.
        :return: none
        """
        for row in self._board[1::]:
            if row[1] == x_coord:
                if row[0] == y_coord:
                    if symbol == 'B':
                        row[2] = "BLACK"
                        row[3] = symbol
                        return
                    elif symbol == "R":
                        row[2] = "RED"
                        row[3] = symbol
                        return
                    elif symbol == ".":
                        row[2] = "NONE"
                        row[3] = symbol
                        return

    def get_game_state(self):
        """
        Gets the current state of the game (UNFINISHED, RED_WON, BLACK_WON)
        :return: self._game_state
        """
        return self._game_state

    def set_game_state(self):
        """
        Sets the current state of the game (UNFINISHED, RED_WON, BLACK_WON)
        :return: none
        """
        if self._num_captured_pieces_red >= 8:
            self._game_state = "BLACK_WON"
        elif self._num_captured_pieces_black >= 8:
            self._game_state = "RED_WON"
        else:
            self._game_state = "UNFINISHED"

    def get_active_player(self):
        """
        Gets the current active player (RED, BLACK)
        :return: self._active_player
        """
        return self._active_player

    def set_active_player(self, player):
        """
        Sets the active player
        :param player: player to assign as the new current player
        :return: none
        """
        self._active_player = player

    def get_piece_object(self, color, coordinate):
        """
        Gets the object id of a piece at a given location
        :param color: the color of the piece we are looking for
        :param coordinate: the location of the piece we are looking for.
        :return: object_id which is the object id of the specific color piece
        at the given coordinate.
        """
        # converts the xy coordinate into x- and y- individual coordinate
        self._x_coord, self._y_coord = self.convert_coordinates_xy(coordinate)

        if color == "BLACK":
            for object_id, value in self._piece_dict_black.items():
                if ((value["location"][0] == self._y_coord)
                        and (value["location"][1] == self._x_coord)):
                    return object_id

        else:
            for object_id, value in self._piece_dict_red.items():
                if ((value["location"][0] == self._y_coord)
                        and (value["location"][1] == self._x_coord)):
                    return object_id

    def get_num_captured_pieces(self, color):
        """
        Gets the number of captured pieces by color
        :param color: the color of the piece we are looking for
        :return: the number of captured pieces for black or red depending on
        the received color.
        """
        if color == "RED":
            return self._num_captured_pieces_red
        if color == "BLACK":
            return self._num_captured_pieces_black

    def set_num_captured_pieces(self, color, num_captured_pieces):
        """
        Increments the number of captured pieces for a specific color
        :param color: color of piece we are incrementing
        :param num_captured_pieces: number of pieces removed
        :return: none
        """
        if color == "RED":
            self._num_captured_pieces_red += num_captured_pieces
        if color == "BLACK":
            self._num_captured_pieces_black += num_captured_pieces

    def print_board(self):
        """
        Prints the board in its current state. Initializes the index of the
        self._alphabet string to 0. Initializes a temporary row string for
        printing. Prints the header row from self._board[0]. Prints the rest of
        the board, row by row.
        :return: none.
        """
        alpha_index = 0
        temp_row_string = ""
        print(" ", *self._board[0], sep=" ")
        num = 1

        # prints the board array row by row
        for row in self._board[1:]:
            if row[0] == self._alphabet[alpha_index]:
                temp_row_string += " " + row[3]
            # start new row
            else:
                print(self._alphabet[alpha_index] + temp_row_string)
                temp_row_string = " " + row[3]
                alpha_index += 1
                num += 1
        print(self._alphabet[alpha_index] + temp_row_string)

    def create_game_pieces(self):
        """
        Initializes the dictionary for the red and black pieces with
        piece_object as the key, and piece color, location, and status as keys
        of a dictionary.
        Initializes the starting coordinates for each piece
        (red: a1 - a9 and black i1 - i9).
        Initializes the arrays for each piece north, south, east, west with
        self.define_arrays_nsew.
        Updates the square occupants in self._board with
        self.set_square_occupant.
        :return: none
        """
        for num in range(1, 10):
            piece = Pieces("B", "i", num)
            self._piece_dict_black


            # initializes the array_north, array_south, array_east, and
            # array_west for all black pieces.
            for key, value in self._piece_dict_black.items():
                coord_y = value["location"][0]
                coord_x = value["location"][1]
                combined_coord = coord_y + str(coord_x)
                self.define_arrays_nsew(combined_coord, "BLACK")

            # initializes the array_north, array_south, array_east, and
            # array_west for all red pieces.
            for key, value in self._piece_dict_red.items():
                coord_y = value["location"][0]
                coord_x = value["location"][1]
                combined_coord = coord_y + str(coord_x)
                self.define_arrays_nsew(combined_coord, "RED")

        # Updates self._board space with the black pieces symbol at specified
        # location
        for key, value in self._piece_dict_black.items():
            self.set_square_occupant(value['location'][1],  # letter
                                     value['location'][0],  # number
                                     'B')  # symbol

        # Updates self._board with the black pieces symbol at specified
        # location
        for key, value in self._piece_dict_red.items():
            self.set_square_occupant(value['location'][1],  # letter
                                     value['location'][0],  # number
                                     'R')  # symbol

    def check_valid_move(self, move_from, move_to):
        """
        Verifies that a move is valid. First checks if the move is invalid if
        a) the x or y coordinates are not the same (move is not strictly
        horizontal or vertical); b) if the player has a piece in the current
        spot; c) the player is trying to move to an occupied spot. If the
        user's move is not invalidated, the method then gathers an array of
        all spaces between where the user is moving from to where the user is
        moving to. The method then sets the range to reflect the appropriate
        move direction. Then validates that none of the spaces in-between
        move_from and move_to are already occupied.
        :param move_from: yx coordinate of where the user is trying to move
        from.
        :param move_to: yx coordinate of where the user is trying to move to.
        :return: False if the user move is invalid. Returns True otherwise
        """
        move_range = 0
        self._move_from_x, self._move_from_y = \
            self.convert_coordinates_xy(move_from)
        self._move_to_x, self._move_to_y = \
            self.convert_coordinates_xy(move_to)

        active_player = self.get_active_player()
        move_from_occupant = self.get_square_occupant(move_from)
        move_to_occupant = self.get_square_occupant(move_to)

        move_range_array = []
        temp_alpha_string = []

        # checks that the move is strictly horizontal or vertical
        if ((self._move_from_x != self._move_to_x)
                and (self._move_from_y != self._move_to_y)):
            return False

        # Checks that the active player has a piece in the move_from space
        elif move_from_occupant != active_player:
            return False

        # Checks that the move_to space is empty
        elif move_to_occupant != "NONE":
            return False

        # Checks if the game is currently finished or not
        elif self.get_game_state() != "UNFINISHED":
            return False

        # gets the range of horizontal/vertical spaces between move_from and
        # move_to
        else:
            # if moving horizontal
            if self._move_from_y == self._move_to_y:
                if self._move_from_x > self._move_to_x:
                    move_range = range(self._move_to_x + 1, self._move_from_x)
                else:
                    move_range = range(self._move_from_x + 1, self._move_to_x)
                for row in self._board[1::]:
                    if row[0] == self._move_to_y and row[1] in move_range:
                        move_range_array += [row]
                    else:
                        continue

            # if moving vertical
            else:
                temp_range_1 = self._alphabet.index(self._move_from_y)
                temp_range_2 = self._alphabet.index(self._move_to_y)
                if temp_range_1 > temp_range_2:
                    move_range_lower = temp_range_2
                    move_range_upper = temp_range_1
                    for letter in self._alphabet[
                                  move_range_lower: move_range_upper]:
                        temp_alpha_string.append(letter)
                else:
                    move_range_lower = temp_range_1
                    move_range_upper = temp_range_2
                    for letter in self._alphabet[
                                  move_range_lower + 1: move_range_upper + 1]:
                        temp_alpha_string.append(letter)

            # checks if any of the horizontal spaces are occupied between
            # move_from and move_to
            if self._move_from_y == self._move_to_y:
                for row in self._board[1::]:
                    if row[1] == self._move_to_x and row[1] in move_range:
                        move_range_array += [row]
                    else:
                        continue
                for space in move_range_array:
                    if space[2] != "NONE":
                        return False
                    else:
                        continue
                return True

            # checks if any of the vertical spaces are occupied between
            # move_from and move_to
            if self._move_from_x == self._move_to_x:
                for row in self._board[1::]:
                    if ((row[0] in temp_alpha_string)
                            and (row[1] == self._move_to_x)):
                        move_range_array += [row]
                    else:
                        continue
                for space in move_range_array:
                    if space[2] != "NONE":
                        # print("Vertical spaces in between are not all empty")
                        return False
                    else:
                        continue
                return True

    def make_move(self, move_from, move_to):
        """
        Makes a move for the active player if the move is verified as valid
        (True). If the move is valid, the method will update the location of
        the piece depending on who is moving. It will then update the NSEW
        arrays for the piece that was moved. Checking for trapped pieces will
        be done after the current players turn before the next player is set,
        so there is no need to update other arrays. Next, the method will check
        for trapped pieces before finally setting the next active player.
        :param move_from: coordinates of where the user is moving from
        :param move_to: coordinates of where the user is moving to.
        :return: False if user move is invalid.
        """
        self._move_from_x, self._move_from_y = \
            self.convert_coordinates_xy(move_from)
        self._move_to_x, self._move_to_y = \
            self.convert_coordinates_xy(move_to)
        current_player = self.get_active_player()

        # Verifies if the move is valid
        if self.check_valid_move(move_from, move_to) is True:

            # moves black piece
            if current_player == "BLACK":
                color_piece_dict = self._piece_dict_black
                for key, value in color_piece_dict.items():
                    if ((value["location"][0] == self._move_from_y)
                            and (value["location"][1] == self._move_from_x)):

                        # update black piece location
                        value["location"][0] = self._move_to_y
                        value["location"][1] = self._move_to_x

                        # update the space symbols
                        self.set_square_occupant(self._move_to_x,
                                                 self._move_to_y, "B")
                        self.set_square_occupant(self._move_from_x,
                                                 self._move_from_y, ".")

                        # once the piece is moved, we do not need to continue
                        # iterating through the dictionary
                        break

            # moves red piece by
            if current_player == "RED":
                color_piece_dict = self._piece_dict_red
                for key, value in color_piece_dict.items():
                    if ((value["location"][0] == self._move_from_y)
                            and (value["location"][1] == self._move_from_x)):

                        # update red piece location
                        value["location"][0] = self._move_to_y
                        value["location"][1] = self._move_to_x

                        # update the space symbols
                        self.set_square_occupant(self._move_to_x,
                                                 self._move_to_y, "R")
                        self.set_square_occupant(self._move_from_x,
                                                 self._move_from_y, ".")

                        # once the piece is moved, we do not need to continue
                        # iterating through the dictionary
                        break

            for key, value in self._piece_dict_black.items():
                coord_y = value["location"][0]
                coord_x = value["location"][1]
                combined_coord = coord_y + str(coord_x)
                self.define_arrays_nsew(combined_coord, "BLACK")

            for key, value in self._piece_dict_red.items():
                coord_y = value["location"][0]
                coord_x = value["location"][1]
                combined_coord = coord_y + str(coord_x)
                self.define_arrays_nsew(combined_coord, "RED")

            # checks for trapped pieces
            self.check_trapped_pieces()

            # check corner traps. First verifies that the user moved to a spot
            # that could even trap a piece in a corner.
            if move_to in self._move_to_corner_traps:
                self.check_corner_traps(move_to, current_player)

            # updates the game state
            self.set_game_state()

            # Sets next active player
            if current_player == "BLACK":
                self.set_active_player("RED")
            else:
                self.set_active_player("BLACK")

            return True

        # returns false if move is invalid.
        else:
            return False

    def check_corner_traps(self, move_to, current_player):
        """
        Checks if the
        :return:
        """
        other_diagonal = ""
        occupants = []

        if current_player == "BLACK":
            next_player = "RED"
        else:
            next_player = "BLACK"

        if move_to == "b1" or move_to == "a2":
            corner_space = "a1"
            if move_to == "b1":
                other_diagonal = "a2"
            else:
                other_diagonal = "b1"

        elif move_to == "a8" or move_to == "b9":
            corner_space = "a9"
            if move_to == "a8":
                other_diagonal = "b9"
            else:
                other_diagonal = "a8"

        elif move_to == "h1" or move_to == "i2":
            corner_space = "i1"
            if move_to == "h1":
                other_diagonal = "i2"
            else:
                other_diagonal = "h1"

        elif move_to == "h9" or move_to == "i8":
            corner_space = "i9"
            if move_to == "h9":
                other_diagonal = "i8"
            else:
                other_diagonal = "h9"

        corner_space_x, corner_space_y = \
            self.convert_coordinates_xy(corner_space)

        other_diagonal_x, other_diagonal_y = \
            self.convert_coordinates_xy(other_diagonal)

        for space in self._board[1::]:
            if ((corner_space_x == space[1])
                    and (corner_space_y == space[0])):
                if space[2] == next_player:
                    for other_diagonal_space in self._board[1::]:
                        if ((other_diagonal_x == other_diagonal_space[1])
                                and (other_diagonal_y ==
                                     other_diagonal_space[0])):
                            if current_player == other_diagonal_space[2]:
                                occupants.append(space)
                            else:
                                return
                else:
                    return
        remove_occupants_list_corner = occupants
        self.remove_occupants(remove_occupants_list_corner)

    def define_arrays_nsew(self, coordinate, color):
        """
        Defines/initializes arrays for each piece that store the occupants in
        spaces to the North, South, East, and West of every piece. Updates
        those arrays after a piece has been moved. Reverses the order of the
        arrays for North and West since default direction is read East and
        South.
        :param coordinate: yx coordinate of the location piece moved to or is
        starting at
        :param color: the color of the piece to be updated so correct
        dictionary is updated.
        :return: none
        """
        self._x_coord, self._y_coord = self.convert_coordinates_xy(coordinate)
        piece_object = self.get_piece_object(color, coordinate)

        if color == "BLACK":
            piece_color_dict = self._piece_dict_black
        else:
            piece_color_dict = self._piece_dict_red

        # array_north
        self._array_north = []
        if self._y_coord == "a" or self._y_coord == "x":
            self._array_north = []
        else:
            for row in self._board[1::]:
                if row[0] < self._y_coord and row[1] == self._x_coord:
                    self._array_north += [row]
                else:
                    continue

        # Reverse the north array to since order up is reversed from order down
        self._array_north.reverse()

        # Assigns the array to the appropriate color.
        piece_color_dict[piece_object]["array_north"] = self._array_north

        # array_south
        self._array_south = []
        if self._y_coord == "i" or self._y_coord == "x":
            self._array_south = []
        else:
            for row in self._board[1::]:
                if row[0] > self._y_coord and row[1] == self._x_coord:
                    self._array_south += [row]
                else:
                    continue

        # Assigns the array to the appropriate color.
        if color == "BLACK":
            self._piece_dict_black[piece_object]["array_south"] = \
                self._array_south
        else:
            self._piece_dict_red[piece_object]["array_south"] = \
                self._array_south

        # array_east
        self._array_east = []
        if self._x_coord == 9 or self._x_coord == "0":
            self._array_east = []
        else:
            for row in self._board[1::]:
                if row[0] == self._y_coord and row[1] > self._x_coord:
                    self._array_east += [row]
                else:
                    continue

        # Assigns the array to the appropriate color.
        if color == "BLACK":
            self._piece_dict_black[piece_object]["array_east"] = \
                self._array_east
        else:
            self._piece_dict_red[piece_object]["array_east"] = \
                self._array_east

        # array_west
        self._array_west = []
        if self._x_coord == 1 or self._x_coord == "0":
            self._array_west = []
        else:
            for row in self._board[1::]:
                if row[0] == self._y_coord and row[1] < self._x_coord:
                    self._array_west += [row]
                else:
                    continue

        # Reverses array_west since left is backwards from right.
        self._array_west.reverse()

        # Assigns the array to the appropriate color.
        if color == "BLACK":
            self._piece_dict_black[piece_object]["array_west"] = \
                self._array_west
        else:
            self._piece_dict_red[piece_object]["array_west"] = \
                self._array_west

    def check_trapped_pieces(self):
        """
        Checks if the player sandwiched any opposing pieces, to the North,
        South, East, West, or corner sandwiches, after a move. If the player
        sandwiched opposing players, they are added to a
        remove_occupants_list_direction, and then removed by calling
        self.remove_occupants.
        :return: none
        """
        current_player = self.get_active_player()

        if current_player == "BLACK":
            next_player = "RED"
            piece_color_dict = self._piece_dict_black
        else:
            next_player = "BLACK"
            piece_color_dict = self._piece_dict_red

        # check for vertically trapped pieces from player who just moved
        for key, value in piece_color_dict.items():
            if value["status"] == "REMOVED":
                break
            # checks for trapped pieces to the north
            occupants = []
            if "array_north" in value:
                for index in range(0, len(value["array_north"])):

                    # Collect lists of trapped pieces
                    if value["array_north"][index][2] == next_player:
                        occupants.append(value["array_north"][index])

                    # ends collecting when reached current player without
                    # encountering any NONEs
                    elif value["array_north"][index][2] == current_player:
                        remove_occupants_list_north = occupants
                        if len(remove_occupants_list_north) > 0:
                            self.remove_occupants(remove_occupants_list_north)
                        break

                    elif ((value["array_north"][index][2] == "NONE")
                          and (index >= 0)):
                        break

            # checks for trapped pieces to the south
            occupants = []
            if "array_south" in value:
                for index in range(0, len(value["array_south"])):

                    # Collect lists of trapped pieces
                    if value["array_south"][index][2] == next_player:
                        occupants.append(value["array_south"][index])

                    # ends collecting when reached current player
                    # without encountering any NONEs
                    elif value["array_south"][index][2] == current_player:
                        remove_occupants_list_south = occupants
                        if len(remove_occupants_list_south) > 0:
                            self.remove_occupants(remove_occupants_list_south)
                        break

                    elif ((value["array_south"][index][2] == "NONE")
                          and (index >= 0)):
                        break

            # checks for trapped pieces to the east
            occupants = []
            if "array_east" in value:
                for index in range(0, len(value["array_east"])):

                    # Collect lists of trapped pieces
                    if value["array_east"][index][2] == next_player:
                        occupants.append(value["array_east"][index])

                    # ends collecting when reached current player
                    # without encountering any NONEs
                    elif value["array_east"][index][2] == current_player:
                        remove_occupants_list_east = occupants
                        if len(remove_occupants_list_east) > 0:
                            self.remove_occupants(remove_occupants_list_east)
                        break

                    elif ((value["array_east"][index][2] == "NONE")
                          and (index >= 0)):
                        break

            # checks for trapped pieces to the west
            occupants = []
            if "array_west" in value:
                for index in range(0, len(value["array_west"])):
                    # Collect lists of trapped pieces
                    if value["array_west"][index][2] == next_player:
                        occupants.append(value["array_west"][index])

                    # ends collecting when reached current player
                    # without encountering any NONEs
                    elif value["array_west"][index][2] == current_player:
                        remove_occupants_list_west = occupants
                        if len(remove_occupants_list_west) > 0:
                            self.remove_occupants(remove_occupants_list_west)
                        break

                    elif ((value["array_west"][index][2] == "NONE")
                          and (index >= 0)):
                        break

    def remove_occupants(self, remove_occupants_list):
        """
        Removes occupants from list of occupants to remove, then updates the
        num_captured_pieces for the color just captured, the status of the
        captured pieces in its dictionary.
        :param remove_occupants_list: list of occupants to remove.
        :return: none
        """
        remove_counter = 0
        for occupant in remove_occupants_list:
            # print("printing occupant:", occupant)

            remove_x_coord = occupant[1]  # number
            remove_y_coord = occupant[0]  # letter
            combined_coord = remove_y_coord + str(remove_x_coord)
            remove_occupant_color = occupant[2]
            remove_occupant_symbol = "."
            piece_object = self.get_piece_object(remove_occupant_color,
                                                 combined_coord)

            # Sets the piece color dict equal to the color being removed in
            # order to update dictionary to reflect status
            if remove_occupant_color == "BLACK":
                piece_color_dict = self._piece_dict_black
            else:
                piece_color_dict = self._piece_dict_red

            # verifies that there is a piece to remove and make
            if ((self.get_square_occupant(combined_coord) ==
                 remove_occupant_color)
                    and (piece_color_dict[piece_object]["status"] !=
                         "REMOVED")):
                self.set_square_occupant(remove_x_coord,
                                         remove_y_coord,
                                         remove_occupant_symbol)

                # Updates the status of the piece in the corresponding
                # dictionary
                for key, value in piece_color_dict.items():
                    if ((piece_color_dict[key]["location"][0] ==
                         remove_y_coord)
                            and (piece_color_dict[key]["location"][1] ==
                                 remove_x_coord)):
                        piece_color_dict[key]["status"] = "REMOVED"
                        piece_color_dict[key]["location"][0] = "x"
                        piece_color_dict[key]["location"][1] = 0

            # Keeps track of the number of pieces removed
            remove_counter += 1

        # updates the number of captured pieces
        self.set_num_captured_pieces(remove_occupant_color, remove_counter)




def main():
    """ Main """
    game = HasamiShogiGame()

    game.make_move("i1", "h1")
    game.make_move("a1", "b1")
    game.print_board()

    game.make_move("i9", "h9")
    game.make_move("a9", "c9")
    game.print_board()

    game.make_move("h1", "g1")
    game.make_move("b1", "b6")
    game.print_board()

    game.make_move("h9", "g9")
    game.make_move("c9", "c5")
    game.print_board()

    game.make_move("g1", "a1")
    game.make_move("a4", "c4")
    game.print_board()

    game.make_move("i3", "c3")
    game.make_move("a5", "a4")
    game.print_board()

    game.make_move("g9", "a9")
    game.make_move("c5", "c6")
    game.print_board()

    game.make_move("i5", "a5")
    game.make_move("c6", "c7")
    game.print_board()

    game.make_move("a9", "a6")
    game.make_move("c7", "c5")
    game.print_board()

    game.make_move("i6", "c6")
    print(game.make_move("a5", "a4"))
    game.print_board()


if __name__ == "__main__":
    main()
