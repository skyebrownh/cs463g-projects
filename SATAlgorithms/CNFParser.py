class CNFParser:
    """
    Parses .cnf files into data that SATAlgorithms will understand
    Format:
        List of tuples with positive or negative (!) integer values
        representing clauses and their corresponding variables
        Ex. [(1, -5, 4), (-1, 5, 3, 4), (-3, -4)] -> (x1 + !x5 + x4) & (!x1 + x5 + x3 + x4) & (!x3 + !x4)
    """
    @staticmethod
    def read_cnf(filename):
        data = []

        f = open(filename, 'r')
        for line in f:
            if line.startswith('%'):
                break
            if not line.startswith('c') and not line.startswith('p'):
                data_line = line.split(' ')
                data_line.remove('0\n')  # all clauses end in 0
                data_line_list = []
                for i in range(len(data_line)):
                    if data_line[i] == '':
                        continue
                    data_line_list.append(int(data_line[i]))
                data.append(tuple(data_line_list))
        f.close()
        return data
