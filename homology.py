# functions for computing homology of a simplicial complex
# mostly what we needed to implement on lab practice 10 with small adjustments

import itertools
import dionysus as d

def homology(simplices):
    """
    Computes homology on the dictionary of simplices
    :param simplices: dictionary: dimension -> list of simplices
    :return: list of Betti numbers
    """
    sx = SimplicialComplex(simplices)

    dim = {}
    for n in range(0, sx.maxdim() + 1):
        dim_ker, dim_im = dimensions(reduce(sx.boundary_matrix(n)))
        dim[n] = (dim_ker, dim_im)

    H = [ dim[n][0] - dim[n+1][1] for n in range(0, sx.maxdim())]

    # edge in one dimension too high (we don't need the image)
    H.append(dim[sx.maxdim()][0])

    return H

def dimensions(M):
    # number of zero columns
    dim_ker = 0
    for j in range(len(M[0])):
        zero = True
        for row in M:
            if row[j] == 1:
                zero = False
                break
        if zero:
            dim_ker += 1

    # number of nonzero rows
    dim_im = 0
    for row in M:
        nonzero = False
        for x in row:
            if x == 1:
                nonzero = True
                break

        if nonzero:
            dim_im += 1

    return dim_ker, dim_im

class SimplicialComplex:
    def __init__(self, simplices):
        """
        :param simplices: dictionary, dimension -> list of simplices
        """
        self.simplices = simplices

        self.boundaries = {}
        self.boundaries[0] = [[0] * len(self.simplices[0])]
        for i in range(0, len(self.simplices) - 1):
            # initialise to zeros
            matrix = [[0 for _ in range(len(self.simplices[i + 1]))] for _ in range(len(self.simplices[i]))]

            # ones on the correct spots - for edges that are in the appropriate simplex
            for j, s in enumerate(self.simplices[i + 1]):
                for c in itertools.combinations(s, i + 1):
                    matrix[self.simplices[i].index(c)][j] = 1

            self.boundaries[i + 1] = matrix

    def C(self, n):
        return self.simplices[n]

    def boundary_matrix(self, n):
        return self.boundaries[n]

    def maxdim(self):
        return len(self.simplices) - 1

def reduce(M):
    """
    reduces the given matrix so that the remaining elements lie on the top-left part of the diagonal

    :param M:
    :return:
    """
    return rec_reduce(M, 0)


def rec_reduce(M, s):
    # recursively on smaller matrix
    if M[s][s] == 0:
        # find a row or column that starts with 1
        row, index = find_nonzero(M, s)

        if index < 0:
            # no nonzero elements, done
            return M

        if row:
            # swap rows
            M[s], M[index] = M[index], M[s]
        else:
            # swap columns
            for row in M:
                row[s], row[index] = row[index], row[s]

    # kill all nonzero items below and right of s
    for i, row in enumerate(M):
        if i > s and row[s] == 1:
            # add the row s to row i
            for j in range(0, len(row)):
                row[j] = (row[j] + M[s][j]) % 2

    for j, c in enumerate(M[s]):
        if j > s and c == 1:
            # add the col s to col j
            for i in range(0, len(M)):
                M[i][j] = (M[i][j] + M[i][s]) % 2

    if s < len(M)-1 and s < len(M[0])-1:
        return rec_reduce(M, s + 1)
    else:
        return M


def find_nonzero(M, s):
    for i, row in enumerate(M):
        if row[s] == 1:
            return True, i
    for j, col in enumerate(M[s]):
        if col == 1:
            return False, j

    return False, -1







def homology_d(complex):
    flat_simplices = [list(s) for slist in complex.values() for s in slist]
    f = d.Filtration(flat_simplices)
    h = d.homology_persistence(f, prime=2)

    H = [0, 0, 0]
    dgms = d.init_diagrams(h, f)
    for i, dgm in enumerate(dgms):
        if i < 3:
            H[i] = len(dgm)

    return H

