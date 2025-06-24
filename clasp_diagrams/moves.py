from clasp_diagrams.objects import ChordForMatrix, ChordForArray, ClaspDiagram
from utils import matrix_chords_intersect, consecutive_heights

# ==================== move A: exchange_heights ====================
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

    # If no errors are raised, construct the new clasp after performing the move
    new_matrix = []

    for k in range(n):
        if k == i:
            new_matrix.append(ChordForMatrix(start_point=chord1.start_point,
                                             end_point=chord1.start_point,
                                             sign=chord1.sign,
                                             height=chord2.height)) 
        elif k == j:
            new_matrix.append(ChordForMatrix(start_point=chord2.start_point,
                                             end_point=chord2.start_point,
                                             sign=chord2.sign,
                                             height=chord1.height))
        else:
            new_matrix.append(matrix[k])

    new_matrix = tuple(new_matrix)

    return ClaspDiagram.from_matrix(matrix=new_matrix)

def valid_exchange_heights(matrix: ClaspDiagram, i, j, n):
    """
    Checks that the chosen chords and clasp diagram are suitable for applying move A.
    """
    # More than one chord check
    if n < 2:
        raise ValueError(f"Clasp diagram has less than two chords ({n})")

    # TODO: Check this logic. Valid indices check
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










# DELETEME
if __name__ == "__main__":
    cd_5_2 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 3, '+', 3),
                                              ChordForMatrix(1, 5, '+', 2),
                                              ChordForMatrix(2, 4, '+', 1)))
    
    res = exchange_heights(cd_5_2, i=2, j=3)

    print("Modified clasp:")
    print(res)

    print("\nID check:")
    print(f"{id(cd_5_2)} , {id(res)}")