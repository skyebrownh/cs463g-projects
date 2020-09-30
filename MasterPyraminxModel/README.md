# CS463G Fall 2020 Master Pyraminx Model

Implements a representation of a Master Pyraminx in Python 3

## Description of Data Structure

The data structure used is a combination of 3 models:

- Piece: represents a single sticker/triangle
    - color: the color of the sticker
    - position: an (x, y) coordinate of it's placement on a Face
- Face: represents a collection of Pieces arranged in a pyramid shape
    - uid: unique identifier
    - orientation: the rotation of this Face (see more below)
    - pieces: array of Pieces (16 total)
    - change_orientation: ability for this Face to turn clockwise (when viewing the face straight on)
- Pyraminx
    - pyraminx_orientation: the rotation of this Pyraminx which gets passed down to each of it's Faces
    - faces: array of Faces (4 total)
    - relationships between Faces, based on pyraminx_orientation, to determine how to make a move
    - rotate: ability for this Pyraminx to change it's (associated Face's) orientations
    - single_move: takes a face and a level (# of rows deep to make move on) and makes a clockwise (as viewing from top down) move on that level
    - randomize: takes a number of moves and makes that number of random single moves, rotating after each iteration

The coordinate system used to identify the position of a Piece is based on the pyramid layout of a Face being centered on an 2D graph with the baseline at y = 0.

- 1/2 sizes are used to represent the point at the center of each triangle Piece since their corners can overlap and change based on orientation
- x positions can be (-1.5, -1, -0.5, 0, 0.5, 1, 1.5)
- y positions can be (0.5, 1.5, 2.5, 3.5)
- In this system:
    - top middle piece would be (0, 3.5)
    - bottom left piece would be (-1.5, 0.5)
    - bottom right piece would be (1.5, 0.5)
    - center piece would be (0, 1.5)

A uid (unique identifier) is used to objectively identify a Face. Initially, the center piece of the Face was used, but a center piece can change with a 3rd-row level rotation.
A Face's orientation is changed through a class method that describes a mapping between the current Face layout and the rotated Face layout of Pieces.
Faces only rotate 180 degrees clockwise in its randomization process.
Instead of implementing diagonal rotations on a Face, we instead use orientation changes to perform the same action by first rotation the face, then making a horizontal move.

## GUI

The graphical user interface is a simple plain-text shown through the command line.
All of the above models in the data structure have string representations that make it easy to display using a print() statement.
A Piece simply displays its color and position.
A Face displays a pyramid-like structure of the colors and positions of each of its Pieces.
A Pyraminx displays the string representation of each of its Faces separated by a new line.

## Description of Randomizer

My randomizer function is implemented on the Pyraminx model as the randomize() method.
It takes an integer as the number of moves to make in order to randomize the Pyraminx.
Each iteration, it will select a random face at a random level, and perform a single_move() with those parameters.
Then the Pyraminx will rotate() to make the randomization more interesting and unpredictable.

## Admissible Heuristic

An admissible heuristic is a way to estimate how many moves away that a particular state of the Pyraminx is from being solved. For the heuristic to be admissible, it can never overestimate the actual number of moves it would take to solve.

A full description of a valid admissible heuristic can be found in the [A* Master Pyraminx solver](../AStarPyraminxSolver/README.md).
 
