from .Piece import Piece


class Face:
    # Piece positions for a face
    positions = [
        (0, 3.5),
        (-0.5, 2.5), (0, 2.5), (0.5, 2.5),
        (-1, 1.5), (-0.5, 1.5), (0, 1.5), (0.5, 1.5), (1, 1.5),
        (-1.5, 0.5), (-1, 0.5), (-0.5, 0.5), (0, 0.5), (0.5, 0.5), (1, 0.5), (1.5, 0.5)
    ]
    # mapping of Pieces to new positions when this face's orientation changes
    orientation_positions = {
        (0, 3.5): (1.5, 0.5),
        (-0.5, 2.5): (1, 1.5),
        (0, 2.5): (1, 0.5),
        (0.5, 2.5): (0.5, 0.5),
        (-1, 1.5): (0.5, 2.5),
        (-0.5, 1.5): (0.5, 1.5),
        (0, 1.5): (0, 1.5),
        (0.5, 1.5): (0, 0.5),
        (1, 1.5): (-0.5, 0.5),
        (-1.5, 0.5): (0, 3.5),
        (-1, 0.5): (0, 2.5),
        (-0.5, 0.5): (-0.5, 2.5),
        (0, 0.5): (-0.5, 1.5),
        (0.5, 0.5): (-1, 1.5),
        (1, 0.5): (-1, 0.5),
        (1.5, 0.5): (-1.5, 0.5)
    }

    def __init__(self, uid, color):
        self.uid = uid  # unique identifier for this face
        self.orientation = 1  # orientation of this face
        self.pieces = list(map(lambda pos: Piece(color, pos), Face.positions))

    def __str__(self):
        # filter each row by it's y-position
        first_row = self.get_piece((0, 3.5))
        second_row = list(filter(lambda piece: piece.position[1] == 2.5, self.pieces))
        third_row = list(filter(lambda piece: piece.position[1] == 1.5, self.pieces))
        fourth_row = list(filter(lambda piece: piece.position[1] == 0.5, self.pieces))

        # map pieces to their color / string representation
        first_row = str(first_row)
        second_row = ' '.join(list(map(lambda piece: str(piece), second_row)))
        third_row = ' '.join(list(map(lambda piece: str(piece), third_row)))
        fourth_row = ' '.join(list(map(lambda piece: str(piece), fourth_row)))

        return f'\nface uid: {self.uid}\n\t\t\t{first_row}\n\t\t{second_row}\n\t{third_row}\n{fourth_row}'

    def __eq__(self, other):
        for p in self.pieces:
            other_piece = other.get_piece(p.position)
            if p != other_piece:
                return False
        return True

    # get a piece in this face by a given position
    def get_piece(self, pos):
        if pos not in Face.positions:
            raise Exception('Position not valid')
        return list(filter(lambda piece: piece.position == pos, self.pieces))[0]

    # get a level in this face by a given y-position
    def get_level(self, level):
        if level not in [0.5, 1.5, 2.5, 3.5]:
            raise Exception('Level not valid')
        return list(filter(lambda piece: piece.position[1] == level, self.pieces))

    # set a level on this face with the given new Pieces
    def set_level(self, new_pieces):
        for p in new_pieces:
            replace_index = self.pieces.index(self.get_piece(p.position))
            self.pieces[replace_index] = p

    # change the orientation of this face using the mapping dictionary, orientation_positions
    def change_orientation(self):
        if self.orientation == 3:
            self.orientation = 1
        else:
            self.orientation += 1

        new_pieces = []
        for key in Face.orientation_positions:
            piece = self.get_piece(key)
            new_pieces.append(Piece(piece.color, Face.orientation_positions[key]))

        self.pieces = new_pieces
