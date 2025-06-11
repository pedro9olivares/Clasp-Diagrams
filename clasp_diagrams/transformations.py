from clasp_diagrams.objects import ChordForMatrix, ChordForArray
from collections import defaultdict

def transform_matrix_to_array(matrix: tuple[ChordForMatrix]) -> list[ChordForArray]:
    """
    Transforms a clasp matrix into a clasp array (list).
    The result is not validated.

    n is the number of ChordForMatrix instances
    Time complexity: O(n)
    Space complexity: O(n)
    """
    # Create the array
    n = len(matrix)

    if n == 0:
        return []

    array = [None] * (2 * n)

    # Create the chords for the array and fill it.
    for i, chord_for_matrix in enumerate(matrix):
        chord_for_array = ChordForArray(chord_idx=i+1, 
                                        sign=chord_for_matrix.sign,
                                        height=chord_for_matrix.height)
        sp, ep = chord_for_matrix.start_point, chord_for_matrix.end_point
        array[sp], array[ep] = chord_for_array, chord_for_array

    return array

def transform_array_to_matrix(array: list[ChordForArray]) -> tuple[ChordForMatrix]:
    """
    Transforms a clasp array into a clasp matrix (tuple).
    The result is not validated.

    m is the number of ChordForArray instances
    Time complexity: O(m)
    Space complexity: O(m)
    """
    m = len(array)
    n = m // 2

    if m == 0:
        return ()

    # First, extract all chord info into a dictionary
    chords_dict = defaultdict(list)

    for point, chord in enumerate(array):
        idx = chord.chord_idx # idx - 1 tells us the "row" of the matrix
        sign = chord.sign
        height = chord.height
        
        if len(chords_dict[idx]) == 0:
            # Case 1: we're seeing the chord for the first time.
            start_point = point
            chords_dict[idx] += [start_point, sign, height]
        else:
            # Case 2: we're seeing the chord for the second time.
            end_point = point
            chords_dict[idx].append(end_point)
    
    # Then, create the tuple
    matrix = [None] * n
    for idx, chord_data in chords_dict.items():
        sp, sign, height, ep = chord_data
        matrix[idx - 1] = ChordForMatrix(start_point=sp, end_point=ep, sign=sign, height=height)

    return tuple(matrix)


