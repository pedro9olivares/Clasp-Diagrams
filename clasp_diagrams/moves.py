from clasp_diagrams.objects import ChordForMatrix, ChordForArray, ClaspDiagram
from clasp_diagrams.utils import matrix_chords_intersect, consecutive_heights, ImplementationError
import numpy as np
from dataclasses import astuple

# ==================== move A: exchange_heights ====================
def valid_exchange_heights(matrix: tuple[ChordForMatrix], i, j, n):
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

    if clasp.alexander.equals(new_clasp.alexander) or clasp.alexander.equals(-new_clasp.alexander):
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

    if clasp.alexander.equals(new_clasp.alexander) or clasp.alexander.equals(-new_clasp.alexander):
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

    if clasp.alexander.equals(new_clasp.alexander) or clasp.alexander.equals(-new_clasp.alexander):
        return new_clasp
    else:
        raise ImplementationError("Move -B failed to produce an isotopic clasp.")

# ==================== move C1: erase isolated chord ====================
def valid_erase_isolated_chord(clasp: ClaspDiagram, i):
    """
    Checks that the chosen chord and clasp diagram are suitable for applying move C1.
    """
    matrix = clasp.matrix
    n = len(matrix)

    # Empty clasp diagram check
    if n < 1:
        raise ValueError("Clasp diagram needs to have at least one chord.")
    
    # Invalid index chosen check
    if not 1 <= i <= n:
        raise ValueError(f"Invalid chord index chosen ({i}). Must be between 1 and {n}.")
    
    # Non-isolated chord check: check if i-th row (in 1-indexing) and column of L-matrix is all zeros.
    row = clasp.l_matrix[i - 1, :]  # Row vector
    col = clasp.l_matrix[:, i - 1]  # Column vector

    if np.any(row != 0) or np.any(col != 0):
        raise ValueError(f"{matrix[i-1]} with chord index {i} is not isolated.")
    
    return matrix[i - 1]

def erase_isolated_chord(clasp: ClaspDiagram, *, i, j=None) -> tuple[ClaspDiagram, ChordForMatrix]:
    """
    Move C1: Erase an isolated chord.

    Parameters
    ----------
    clasp : ClaspDiagram
        The diagram to apply the move to.
    i : int
        Index of the chord to erase.
    
    Returns
    -------
    tuple
        - ClaspDiagram: New diagram with move applied.

        - ChordForMatrix: The erased chord.

    n is the number of chords in the clasp diagram.

    Time complexity: O(n)
    Space complexity: O(n)
    """
    # If the following function doesn't raise any errors, the move can be performed.
    chord_to_erase = valid_erase_isolated_chord(clasp, i=i)

    height_to_erase = chord_to_erase.height
    array = clasp.array
    new_array = []
    chord_cache = {} # A cache for object interning of the form {chord: chord} (same key and value!)

    # The following loop removes the chord and adjusts indices/heights of the remaining chords
    for chord in array:
        curr_idx = chord.chord_idx
        curr_height = chord.height
        # Append only if chord_idx != i
        if curr_idx != i:
            # Decrease the index if greater than i
            new_idx = curr_idx - 1 if curr_idx > i else curr_idx
            # Decrease the height if greater than the erased chord's height
            new_height = curr_height - 1 if curr_height > height_to_erase else curr_height
            new_chord = ChordForArray(chord_idx=new_idx, sign=chord.sign, height=new_height)
            # Object interning: let's reuse created chords:
            if new_chord not in chord_cache:
                new_array.append(new_chord)
                chord_cache[new_chord] = new_chord
            else:
                new_array.append(chord_cache[new_chord])

    new_clasp = ClaspDiagram.from_array(array=new_array)

    if clasp.alexander.equals(new_clasp.alexander) or clasp.alexander.equals(-new_clasp.alexander):
        return new_clasp, chord_to_erase
    else:
        raise ImplementationError(f"Move C1 failed to produce an isotopic clasp: {type(clasp.alexander)} vs {type(new_clasp.alexander)}.")

# ==================== move -C1: add isolated chord (after a starting point) ====================
def valid_add_isolated_chord(n, after_point, sign, height):
    """
    Checks if the specified chord fits in the clasp diagram.
    """
    if n != 0:
        valid_points = list(range(0, 2*n))
    else:
        valid_points = [-1] # Special case: adding a chord to an unknot (). Add after "point" -1
    if after_point not in valid_points:
        raise ValueError(f"Invalid starting/ending point chosen ({after_point}). Must be in {valid_points}.")
    
    if sign not in ['-', '+']:
        raise ValueError(f"Invalid sign chosen ({sign}). Must be '-' or '+'.")
    
    valid_heights = list(range(1, n+2))
    if height not in valid_heights:
        raise ValueError(f"Invalid height chosen ({height}). Must be in {valid_heights}")
    
def add_isolated_chord(clasp: ClaspDiagram, *, after_point, new_sign, new_height) -> ClaspDiagram:
    """
    Move -C1: Add an isolated chord after the specified starting/ending point.

    Parameters
    ----------
    clasp : ClaspDiagram
        The diagram to apply the move to.
    after_point : int
        Starting/ending point after which to add the new isolated chord.
    sign : str
        Sign of the new chord. Must be '+' or '-'
    height : int
        Height of the new chord.
    
    Returns
    -------
    ClaspDiagram
        New diagram with move applied.

    n is the number of chords in the clasp diagram.

    Time complexity: O(n) or O(nlogn)
    Space complexity: O(n)
    """
    matrix = clasp.matrix
    n = len(matrix)

    # If the following function doesn't raise any errors, the move can be performed.
    valid_add_isolated_chord(n=n, after_point=after_point, sign=new_sign, height=new_height)
    
    new_matrix = []
    new_sp = after_point + 1
    new_ep = after_point + 2
    new_chord = ChordForMatrix(new_sp, new_ep, new_sign, new_height)
 
    # Add the new chord after the specified starting/ending point.
    # For every other chord:
    #   - increase the starting/ending points by two if greater or equal to new_sp,
    #   - increase height by one if greater or equal to new_height.
    for chord in matrix:
        sp, ep, sign, height = astuple(chord)
        if sp >= new_sp:
            sp += 2
        if ep >= new_sp:
            ep += 2
        if height >= new_height:
            height += 1
        new_matrix.append(ChordForMatrix(sp, ep, sign, height)) # Adding the modified chord

        if sp == after_point or ep == after_point:
            new_matrix.append(new_chord)

    # Special case: adding a chord to an unknot ()
    if n == 0:
        new_matrix.append(new_chord)

    new_matrix = sorted(new_matrix, key=lambda x: x.start_point) # Timsort is O(n) for nearly sorted data?
    new_matrix = tuple(new_matrix)
    new_clasp = ClaspDiagram.from_matrix(matrix=new_matrix)

    if clasp.alexander.equals(new_clasp.alexander) or clasp.alexander.equals(-new_clasp.alexander):
        return new_clasp
    else:
        raise ImplementationError("Move -C1 failed to produce an isotopic clasp.")



        

