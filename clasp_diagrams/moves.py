from clasp_diagrams.objects import ChordForMatrix, ChordForArray, ClaspDiagram
from clasp_diagrams.utils import matrix_chords_intersect, consecutive_heights, ImplementationError

# ==================== move A: exchange_heights ====================
def valid_exchange_heights(matrix: ClaspDiagram, i, j, n):
    """
    Checks that the chosen chords and clasp diagram are suitable for applying move A.
    """
    # More than one chord check
    if n < 2:
        raise ValueError(f"Clasp diagram has less than two chords ({n})")

    # Valid indices check
    if not 1 <= i <= n or not 1 <= j <= n:
        raise ValueError(f"Chord indices {i}, {j} out of bounds for diagram with {n} chords.")
    
    # Different chords check
    if i == j:
        raise ValueError(f"Chord indices i, j must be different.")

    chord1 = matrix[i-1]
    chord2 = matrix[j-1]

    # Non-intersecting chords check
    if matrix_chords_intersect(chord1=chord1, chord2=chord2):
        raise ValueError(f"Chords {chord1} and {chord2} intersect.")

    # Consecutive height check (mod n)
    if not consecutive_heights(chord1=chord1, chord2=chord2, n=n):
        raise ValueError(f"Chords {chord1} and {chord2} don't have consecutive heights.")
    
    return chord1, chord2

def exchange_heights(clasp: ClaspDiagram, *, i, j) -> ClaspDiagram:
    """
    Move A: Exchange the heights of two non-intersecting chords with consecutive heights.

    Parameters
    ----------
    clasp : ClaspDiagram
        The diagram to apply the move to.
    i : int
        Index of first chord.
    j : int
        Index of second chord.

    Returns
    -------
    ClaspDiagram
        New diagram with move applied.

    Raises
    ------
    ValueError
        If the move conditions are not satisfied.

    n is the number of chords in the clasp diagram.

    Time complexity: O(n)
    Space complexity: O(n)
    """
    matrix = clasp.matrix
    n = len(matrix)

    # Check if the chosen chords are suitable
    chord1, chord2 = valid_exchange_heights(matrix, i, j, n)

    # If no errors are raised, construct the new clasp that results from performing the move
    new_matrix = []

    for k in range(n):
        if k == i-1:
            new_matrix.append(ChordForMatrix(start_point=chord1.start_point,
                                             end_point=chord1.end_point,
                                             sign=chord1.sign,
                                             height=chord2.height)) 
        elif k == j-1:
            new_matrix.append(ChordForMatrix(start_point=chord2.start_point,
                                             end_point=chord2.end_point,
                                             sign=chord2.sign,
                                             height=chord1.height))
        else:
            new_matrix.append(matrix[k])

    new_matrix = tuple(new_matrix)

    new_clasp = ClaspDiagram.from_matrix(matrix=new_matrix)

    if clasp.alexander == new_clasp.alexander:
        return new_clasp
    else:
        raise ImplementationError("Move A failed to produce an isotopic clasp.")

# ==================== move B and -B: cyclic_height_shift ====================
def cyclic_height_shift(clasp: ClaspDiagram, *, i=None, j=None) -> ClaspDiagram:
    """
    Move B: Cyclic height shift (+1 to each chord's height).
    This move can always be applied.

    Parameters
    ----------
    clasp : ClaspDiagram
        The diagram to apply the move to.
    
    Returns
    -------
    ClaspDiagram
        New diagram with move applied.

    n is the number of chords in the clasp diagram.

    Time complexity: O(n)
    Space complexity: O(n)
    """

    n = len(clasp.matrix)

    new_matrix = []
    for chord in clasp.matrix:
        new_matrix.append(ChordForMatrix(start_point=chord.start_point,
                                         end_point=chord.end_point,
                                         sign=chord.sign,
                                         height=(chord.height % n) + 1)
                                        )

    new_matrix = tuple(new_matrix)
    new_clasp = ClaspDiagram.from_matrix(matrix=new_matrix)

    if clasp.alexander == new_clasp.alexander:
        return new_clasp
    else:
        raise ImplementationError("Move B failed to produce an isotopic clasp.")
    
def inverse_cyclic_height_shift(clasp: ClaspDiagram, *, i=None, j=None) -> ClaspDiagram:
    """
    Move -B: Inverse cyclic height shift (-1 to each chord's height).
    This move can always be applied.

    Parameters
    ----------
    clasp : ClaspDiagram
        The diagram to apply the move to.

    Returns
    -------
    ClaspDiagram
        New diagram with move applied.

    n is the number of chords in the clasp diagram.

    Time complexity: O(n)
    Space complexity: O(n)
    """
    n = len(clasp.matrix)

    new_matrix = []
    for chord in clasp.matrix:
        new_matrix.append(ChordForMatrix(start_point=chord.start_point,
                                         end_point=chord.end_point,
                                         sign=chord.sign,
                                         height=((chord.height - 2) % n) + 1)
                                        )

    new_matrix = tuple(new_matrix)
    new_clasp = ClaspDiagram.from_matrix(matrix=new_matrix)

    if clasp.alexander == new_clasp.alexander:
        return new_clasp
    else:
        raise ImplementationError("Move -B failed to produce an isotopic clasp.")