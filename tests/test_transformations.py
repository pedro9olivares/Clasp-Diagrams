from hypothesis import given, strategies as st
from clasp_diagrams.objects import ChordForMatrix, ChordForArray
from clasp_diagrams.transformations import transform_matrix_to_array
from clasp_diagrams.validators import validate_clasp_array

def make_valid_chord_for_matrix(idx: int, start: int, end: int, height: int) -> ChordForMatrix:
    return ChordForMatrix(
        start_point=start,
        end_point=end,
        sign='+' if idx % 2 == 0 else '-',
        height=height
    )

@given(st.integers(min_value=1, max_value=100))
def test_transform_matrix_to_array_produces_valid_array(n):
    """
    Generates a valid matrix of n ChordForMatrix instances and verifies that the
    transform_matrix_to_array function produces a valid array.
    """

    # Allocate 2n unique positions from 0 to 2n-1
    positions = list(range(2 * n))
    import random
    random.shuffle(positions)

    matrix = []
    for i in range(n):
        sp = positions[2 * i]
        ep = positions[2 * i + 1]
        matrix.append(make_valid_chord_for_matrix(i, sp, ep, height=i + 1))

    matrix = tuple(matrix)
    array = transform_matrix_to_array(matrix)

    # Ensure output is a valid clasp array
    validate_clasp_array(array)

    # Check that the array has exactly 2n elements
    assert len(array) == 2 * n

    # All elements should be instances of ChordForArray
    assert all(isinstance(c, ChordForArray) for c in array)
