from clasp_diagrams.objects import ChordForMatrix, ChordForArray
from clasp_diagrams.utils import matrix_chords_intersect
import sympy as sp
import numpy as np

def get_e_matrix(clasp_matrix: tuple[ChordForMatrix]) -> np.ndarray:
    """
    'E is the diagonal matrix encoding the signs of all chords, 
    that is, with Eii = ±1 being the sign of the chord i'.

    Not tested, trivial.

    Time complexity: O(n)
    Space complexity: O(n²)
    """
    signs = np.array([1 if chord.sign == '+' else -1 for chord in clasp_matrix])
    return np.diag(signs)

def get_l_matrix(clasp_matrix: tuple[ChordForMatrix]) -> np.ndarray:
    """
    'For a pair i, j of intersecting chords with i passing over j 
    define lij = 1 if i<j and lij=−1 if i>j. 
    Set all remaining elements of L to be 0'.

    Time complexity: O(n²)
    TODO: (Eventually) consider switch to an interval tree.
    Space complexity: O(n²)
    """
    n = len(clasp_matrix)
    L = np.zeros(shape=(n,n))

    for i in range(n):
        for j in range(i+1, n):
            if matrix_chords_intersect(clasp_matrix[i], clasp_matrix[j]):
                if clasp_matrix[i].height > clasp_matrix[j].height:
                    L[i][j] = 1
                else:
                    L[j][i] = -1

    return L

def get_le_matrix(e_matrix: np.ndarray, l_matrix: np.ndarray) -> sp.Matrix:
    """
    Returns L + E.

    Not tested, trivial.
    """
    return l_matrix + e_matrix

def get_sd_matrix(le_matrix: np.ndarray) -> sp.Matrix:
    """
    'For each pair i, j of intersecting chords with i passing over j define 
    sij= t − 1, sji= t^−1 − 1 if i<j; 
    and sij = 1 − t, sji = 1 − t^−1 if i>j. 
    Set sii = −eii for all i
    and let all remaining elements of S to be 0.'

    Time complexity: O(n²) 
    Space complexity: O(n²)
    """
    n, n = le_matrix.shape
    SD = sp.zeros(n, n)
    t = sp.symbols('t')
    
    for i in range(n):
        for j in range(n):
            if i == j:
                SD[i, i] = -1 * le_matrix[i][i]
            elif le_matrix[i][j] == 1:
                SD[i, j] = t - 1
                SD[j, i] = t**-1 - 1
            elif le_matrix[i][j] == -1:
                SD[i, j] = 1 - t
                SD[j, i] = 1 - t**-1

    return SD

def get_alexander_polynomial(sd_matrix: sp.Matrix) -> sp.Expr:
    """
    Returns the alexander polynomial associated to the clasps's S_D matrix.

    Important: handles t-scaling so that each polynomial lives in K[t] (no negative powers of t),
    e.g., t + 2t^2 instead of 1/t + 2t

    Time complexity: O(n³)
    Space complexity: O(n²) 

    TODO: revisit the determinant computation and t-scaling. Maybe complexity can be improved.
    """
    alpo = sd_matrix.det()
    t = sp.symbols('t')

    # Find minimal exponent of t
    powers = [monom.as_powers_dict().get(t, 0) for monom in alpo.expand().as_ordered_terms()]
    min_power = min(powers)

    if min_power < 0:
        alpo = alpo * t**(-min_power)
    
    return sp.collect(alpo.expand(), t)