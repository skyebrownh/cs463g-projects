# A* on the 4-level Pyraminx

This Python 3 program runs the A* search algorithm on the Master Pyraminx.
A few modifications were made to the [MasterPyraminxModel](../MasterPyraminxModel/README.md):
- An equality (__eq__) function that implements how equality is defined between 2 Piece objects, 
2 Face objects, or 2 Pyraminx objects.
- Clockwise v. Counterclockwise moves on a Pyraminx instance

Data structures used in the search:
- A Node class was defined to hold the following relevant information of each pyraminx state
    - state of the pyraminx
    - parent node
    - g, h, and f values
- A "priority queue" implemented as a sorted list to extract the node with the lowest f value to expand next

## How to compile and run

A machine installed with Python 3 and it's corresponding package manager Pip 3 has the ability to run this program.

It would be best to run this project within a python virtual environment like [venv](https://docs.python.org/3/library/venv.html)
so that the dependencies are not installed globally.

To run this program within a Python 3 virtual environment:
- `$ pip install -r requirements.txt`
- `$ python main.py`

## How randomization works

My randomization works the same as it did in my original MasterPyraminxModel with one exception:
single moves can be implemented in clockwise and counterclockwise rotation types.
I've implemented the randomizer to only move clockwise while the solver will move counterclockwise.

The main program will loop through all of the parameters (collections of k values) it will run,
and generates 5 k-randomized puzzles to run A* on.

## My valid admissible heuristic

The basic of my heuristic is based on the following assumptions:
- An out-of-place piece is classified as one that is of a different color than the center piece on that same face
- Counting specific out-of-place pieces and dividing by the maximum number of those type of pieces that can be
changed in a single move

My valid admissible heuristic is implemented in 4 parts:
1. Counting the number of corner pieces (3 total) out of place and dividing by 3
2. Counting the number of edge pieces (6 total) out of place and dividing by 6
3. Counting the number of interior pieces (6 total) out of place and dividing by 9
4. Choosing the maximum of the 3 previous calculations for as the node's optimized h-value

## Graphing the outcomes

X-values come from the k values in the parameters array used to run the main program.
Y-values come from the average of the number of nodes expanded for the 5 instances run for each k.
Data is displayed as a simple line graph using the matplotlib python package.

