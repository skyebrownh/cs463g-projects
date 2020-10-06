import random, time


class Utils:
    """ Utility functions class """

    @staticmethod
    def remove_duplicates(dup_list):
        """ Removes duplicates from list while preserving the list's order """
        result = []
        for item in dup_list:
            if item not in result:
                result.append(item)
        return result

    @staticmethod
    def equal_lists(list1, list2):
        """ Returns True if lists are equal, False otherwise """
        if len(list1) != len(list2):
            return False
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return False
        return True


class Resolution:
    def __init__(self, phi):
        self.phi = phi  # CNFParser data format
        self.time_taken = 0

    @staticmethod
    def apply_operator(clause1, clause2):
        """ Returns a new clause after applying the resolution operator to clause1 and clause2 """
        final_clause_list = []
        clause1_list = list(clause1)
        clause2_list = list(clause2)

        for literal1 in clause1:
            if -literal1 in clause2:
                new_clause_list = list(filter(lambda l: l != literal1, clause1_list))
                new_clause_list.extend(list(filter(lambda l: l != -literal1, clause2_list)))
                final_clause_list.append(new_clause_list)

        for i, f_clause in enumerate(final_clause_list):
            # remove tautologies
            if len(f_clause) == 2:
                if f_clause[0] == -f_clause[1]:
                    final_clause_list.remove(f_clause)
            elif len(f_clause) > 2:
                # remove True values
                for literal in f_clause:
                    if -literal in f_clause:
                        f_clause.remove(literal)
                        f_clause.remove(-literal)
                final_clause_list[i] = Utils.remove_duplicates(f_clause) # remove duplicates, preserve order

        final_clause = Utils.remove_duplicates(final_clause_list)  # remove duplicates, preserve order
        return final_clause

    def run(self):
        """
        Stopping conditions:
        - Satisfiable if we cannot generate any new clauses by the resolution operator
        - Unsatisfiable if we encounter a contradiction (empty clause)
        """
        start_time = time.perf_counter()

        open_list = self.phi  # clauses that still need to be compared
        closed_list = []  # clauses that have been compared

        while True:
            num_clauses_added = 0
            for clause in open_list:
                others = list(filter(lambda c: c != clause, open_list))
                for other in others:
                    new_clause_list = Resolution.apply_operator(clause, other)
                    # print(f'{clause} and {other} generates {new_clause_list}')

                    for new_clause in new_clause_list:
                        new_clause = tuple(new_clause)  # convert back to tuple

                        if not new_clause:
                            self.time_taken = time.perf_counter() - start_time
                            return False  # contradiction occurred

                        if (new_clause not in closed_list) and (new_clause not in open_list):
                            # if we haven't already seen this clause, add it to our open list
                            open_list.append(new_clause)
                            num_clauses_added += 1

                # we have now viewed and compared this clause
                open_list.remove(clause)
                closed_list.append(clause)

            if num_clauses_added == 0:
                self.time_taken = time.perf_counter() - start_time
                return True  # no new clauses added in this iteration


class LocalSearchOrGSAT:
    """ Implements common methods for LocalSearch and GSAT classes """

    def __init__(self, phi):
        self.phi = phi  # CNFParser data format
        self.c = 0  # highest number of clauses satisfied
        self.time_taken = 0

    @staticmethod
    def generate_guess(n):
        """ Returns a random guess sequence of n variables """
        guess_list = []
        for i in range(n):
            var = random.randint(0, 1)
            guess_list.append(var)
        return tuple(guess_list)

    @staticmethod
    def get_neighbors(guess):
        """ Returns a list of guesses generated by flipping one truth value for each variable in guess """
        neighbors = []
        for i in range(len(guess)):
            flip_var = 0 if guess[i] == 1 else 1
            new_guess_list = list(guess)
            new_guess_list[i] = flip_var
            neighbors.append(tuple(new_guess_list))
        return neighbors

    @staticmethod
    def get_fitness_helper(clause, guess):
        """ Returns True if guess satisfies clause, False otherwise """
        sat_result = []

        for i in range(len(clause)):
            truth_value = guess[abs(clause[i]) - 1]
            if (clause[i] > 0 and truth_value == 0) or (clause[i] < 0 and truth_value == 1):
                sat_result.append(False)
            else:
                sat_result.append(True)

        return True in sat_result

    def get_fitness(self, guess):
        """ Returns an integer representing the number of clauses in phi that are satisfied by guess """
        fitness = 0
        for clause in self.phi:
            if LocalSearchOrGSAT.get_fitness_helper(clause, guess):
                fitness += 1
        return fitness

    def run(self):
        """ Individual algorithm implementations """
        pass


class LocalSearch(LocalSearchOrGSAT):
    """ Inherits methods from LocalSearchOrGSAT """

    def run(self):
        start_time = time.perf_counter()

        # generate initial guess and set c-value
        guess = LocalSearchOrGSAT.generate_guess(len(self.phi))
        self.c = self.get_fitness(guess)

        # check initial guess for satisfiability
        if self.c == len(self.phi):
            self.time_taken = time.perf_counter() - start_time
            return  # SATISFIED

        # only 10 restarts allowed to find highest c-value
        for _ in range(10):
            neighbors = LocalSearchOrGSAT.get_neighbors(guess)

            for neighbor in neighbors:
                neighbor_fitness = self.get_fitness(neighbor)
                if neighbor_fitness > self.c:
                    self.c = neighbor_fitness
                    guess = neighbor
                    break  # choose first improving neighbor

            # check guess for satisfiability
            if self.c == len(self.phi):
                self.time_taken = time.perf_counter() - start_time
                return  # SATISFIED

        # if not satisfied, still calculate time_taken
        self.time_taken = time.perf_counter() - start_time


class GSAT(LocalSearchOrGSAT):
    """ Inherits methods from LocalSearchOrGSAT """

    @staticmethod
    def probability():
        """ Returns True/False based on a fair flip (p = 0.5) """
        value = random.randint(0, 1)
        return value == 1

    def run(self):
        start_time = time.perf_counter()

        # generate initial guess and set c-value
        guess = LocalSearchOrGSAT.generate_guess(len(self.phi))
        self.c = self.get_fitness(guess)

        # check initial guess for satisfiability
        if self.c == len(self.phi):
            self.time_taken = time.perf_counter() - start_time
            return  # SATISFIED

        # only 10 restarts allowed to find highest c-value
        for _ in range(10):
            # flip coin and either randomly guess or choose improving neighbor
            if GSAT.probability():
                guess = LocalSearchOrGSAT.generate_guess(len(self.phi))
                new_fitness = self.get_fitness(guess)
                if new_fitness > self.c:
                    self.c = new_fitness
            else:
                neighbors = LocalSearchOrGSAT.get_neighbors(guess)

                for neighbor in neighbors:
                    neighbor_fitness = self.get_fitness(neighbor)
                    if neighbor_fitness > self.c:
                        self.c = neighbor_fitness
                        guess = neighbor
                        break  # choose first improving neighbor

            # check guess for satisfiability
            if self.c == len(self.phi):
                self.time_taken = time.perf_counter() - start_time
                return  # SATISFIED

        # if not satisfied, still calculate time_taken
        self.time_taken = time.perf_counter() - start_time