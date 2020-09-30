class Piece:
    def __init__(self, color, position):
        self.color = color  # red, blue, yellow, green
        self.position = position  # (x: Int, y: Int)

    def __str__(self):
        return f'{self.color} ({self.position[0]}, {self.position[1]})'

    def __eq__(self, other):
        return self.color == other.color and self.position == other.position
