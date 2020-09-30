import random

from .Face import Face


class Pyraminx:
    initial_faces = [('blue', 100), ('red', 200), ('yellow', 300), ('green', 400)]
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

    def __init__(self):
        self.pyraminx_orientation = 1
        self.faces = list(map(lambda face: Face(face[1], face[0]), Pyraminx.initial_faces))

    def __str__(self):
        print('************** PYRAMINX **************')
        return '\n'.join(map(lambda face: str(face), self.faces)) + '\n'

    def get_face_by_uid(self, uid):
        return list(filter(lambda face: face.uid == uid, self.faces))[0]  # possible error

    def rotate(self):
        if self.pyraminx_orientation == 3:
            self.pyraminx_orientation = 1
        else:
            self.pyraminx_orientation += 1

        for face in self.faces:
            face.change_orientation()

    def single_move(self, face_uid, level):
        r = Pyraminx.relationships[face_uid][self.pyraminx_orientation]

        swap_face0 = self.get_face_by_uid(r[0])
        swap_face1 = self.get_face_by_uid(r[1])
        swap_face2 = self.get_face_by_uid(r[2])

        temp = swap_face0.get_level(level)
        swap_face0.set_level(swap_face1.get_level(level))
        swap_face1.set_level(swap_face2.get_level(level))
        swap_face2.set_level(temp)

    def randomize(self, num_moves):
        for n in range(num_moves):
            # get random face and level
            face_uid = random.choice([100, 200, 300, 400])
            level = random.choice([0.5, 1.5, 2.5, 3.5])
            # make move
            self.single_move(face_uid, level)
            # rotate pyraminx
            self.rotate()
