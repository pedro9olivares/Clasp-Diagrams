from clasp_diagrams.objects import ChordForMatrix, ChordForArray

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
    array = [None] * (2 * n)

    # Create the chords for the array and fill it.
    for i, chord_for_matrix in enumerate(matrix):
        chord_for_array = ChordForArray(chord_idx=i+1, 
                                        sign=chord_for_matrix.sign,
                                        height=chord_for_matrix.height)
        sp, ep = chord_for_matrix.start_point, chord_for_matrix.end_point
        array[sp], array[ep] = chord_for_array, chord_for_array

    return array

