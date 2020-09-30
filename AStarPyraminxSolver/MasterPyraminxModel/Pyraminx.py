import random

from .Face import Face


class Pyraminx:
    # initial colors and unique identifiers for this Pyraminx collection of faces
    initial_faces = [('blue', 100), ('red', 200), ('yellow', 300), ('green', 400)]
    # how to handle Pyraminx rotations
    relationships = {
        100: {
            1: (100, 300, 200),
            2: (100, 400, 300),
            3: (100, 200, 400)
        },
        200: {
            1: (200, 100, 300),
            2: (200, 400, 100),
            3: (200, 300, 400)
        },
        300: {
            1: (300, 200, 100),
            2: (300, 400, 200),
            3: (300, 100, 400)
        },
        400: {
            1: (400, 200, 300),
            2: (400, 100, 200),
            3: (400, 300, 100)
        }
    }

    # data will be pre-populated self.faces data
    def __init__(self, data=None):
        self.pyraminx_orientation = 1  # orientation of all faces in this Pyraminx
        self.faces = list(map(lambda face: Face(face[1], face[0]), Pyraminx.initial_faces)) if data is None else data

    def __eq__(self, other):
        for uid in [100, 200, 300, 400]:
            f = self.get_face_by_uid(uid)
            other_face = other.get_face_by_uid(uid)
            if f != other_face:
                return False
        return True

    def __str__(self):
        print('************** PYRAMINX **************')
        return '\n'.join(map(lambda face: str(face), self.faces)) + '\n'

    # get a face in this Pyraminx by its unique identifier
    def get_face_by_uid(self, uid):
        if uid not in [100, 200, 300, 400]:
            raise Exception('Uid not valid')
        return list(filter(lambda face: face.uid == uid, self.faces))[0]

    # rotate / change the orientation of this Pyraminx
    def rotate(self):
        if self.pyraminx_orientation == 3:
            self.pyraminx_orientation = 1
        else:
            self.pyraminx_orientation += 1

        for face in self.faces:
            face.change_orientation()

    # make a single move on this Pyraminx
    def single_move(self, face_uid, level, rotation_type):
        if face_uid not in [100, 200, 300, 400]:
            raise Exception('Face_uid not valid')
        if level not in [0.5, 1.5, 2.5, 3.5]:
            raise Exception('Level not valid')

        # get the relationship between this face and level to the other faces
        r = Pyraminx.relationships[face_uid][self.pyraminx_orientation]

        swap_face0 = self.get_face_by_uid(r[0])
        swap_face1 = self.get_face_by_uid(r[1])
        swap_face2 = self.get_face_by_uid(r[2])

        # rotate this face in a clockwise direction
        if rotation_type == 'clockwise':
            temp = swap_face0.get_level(level)
            swap_face0.set_level(swap_face1.get_level(level))
            swap_face1.set_level(swap_face2.get_level(level))
            swap_face2.set_level(temp)
        elif rotation_type == 'counterclockwise':
            temp = swap_face2.get_level(level)
            swap_face2.set_level(swap_face1.get_level(level))
            swap_face1.set_level(swap_face0.get_level(level))
            swap_face0.set_level(temp)
        else:
            raise Exception('rotation_type can only be "clockwise" or "counterclockwise"')

    # make the given num_moves number of single random moves to randomize this Pyraminx
    def randomize(self, num_moves):
        for n in range(num_moves):
            # get random face and level
            face_uid = random.choice([100, 200, 300, 400])
            level = random.choice([0.5, 1.5, 2.5, 3.5])
            # make move
            self.single_move(face_uid, level, 'clockwise')
            # rotate pyraminx
            self.rotate()
