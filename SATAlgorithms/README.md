# CS463G SAT Programs

This assignment implements three satisfiability algorithms to a given set of Boolean formulas provided in conjunctive normal form (CNF) and graphs the outcomes.

## How To Run

1. Activate your [python 3 virtual environment](https://docs.python.org/3/library/venv.html)
2. `$ pip install -r requirements.txt`
3. `$ python main.py`

## Description of Algorithms Used

The algorithms implemented are the following:
- Resolution
    - takes a Boolean formula as _phi_
    - returns either **True** or **False** to indicate whether _phi_ was satisfiable or not
    - extensive data (like highest number of clauses satisfied) could not be collected based on the nature of this algorithm
- Local Search
    - takes a Boolean formula as _phi_
    - uses a randomly generated sequence for the initial guess
    - calculates highest number of clauses satisfied (_c_) if formula not satisfiable and the truth values for the closest guess; or returns variable values of the guess that satisfies _phi_
- GSAT
    - takes a Boolean formula as _phi_
    - 10 runs per formula since randomness is used to generate guesses
    - subsequent guesses chosen by the first one with the highest fitness after flipping the variable that minimizes harm or another randomly generated guess (p = 0.5)
    - calculates highest number of clauses satisfied (_c_) if formula not satisfiable and the truth values for the closest guess; or returns variable values of the guess that satisfies _phi_

## Data Collected

Because resolution has no c-value, there is a simple output of the average time it took for satisfiable v. unsatisfiable
formulas to complete.

Local Search and GSAT are graphed by the highest number of clauses satisfied to the amount of time taken for that particular run.

