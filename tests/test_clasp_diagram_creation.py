import pytest
from clasp_diagrams.objects import ChordForMatrix, ChordForArray, ClaspDiagram

def make_valid_matrix(n):
    return tuple(
        ChordForMatrix(
            start_point=2*i,
            end_point=2*i + 1,
            sign='+' if i % 2 == 0 else '-',
            height=i+1,
        )
        for i in range(n)
    )

# =============== chord hashability validation ===============
def test_chord_for_matrix_is_hashable():
    chord = ChordForMatrix(0, 1, '+', 1)
    chord_set = {chord}
    assert chord in chord_set

def test_chord_for_array_is_hashable():
    chord = ChordForArray(1, '+', 1)
    chord_set = {chord}
    assert chord in chord_set

# =============== from_matrix() basic creation validation ===============
# --- tuple of ChordForMatrix validation ---
def test_none_matrix_raises_value_error():
    with pytest.raises(ValueError, match="matrix argument is None"):
        ClaspDiagram.from_matrix(matrix=None)

def test_non_tuple_matrix_raises_type_error():
    with pytest.raises(TypeError, match="matrix argument must be a tuple of ChordForMatrix instances"):
        ClaspDiagram.from_matrix(matrix=[1, 2, 3])  # (passing list instead of tuple)

def test_non_chord_element_raises_type_error():
    bad_matrix = (1, 2, 3)
    with pytest.raises(TypeError, match="All elements of the tuple matrix must be of type ChordForMatrix"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

# --- Height validation ---
def test_non_unique_heights_raises_value_error():
    bad_matrix = (
        ChordForMatrix(0, 1, '+', 1),
        ChordForMatrix(2, 3, '-', 5)
    )
    with pytest.raises(ValueError, match=r"The heights are invalid"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

# --- Sign validation ---
def test_invalid_sign_raises_value_error():
    bad_matrix = (
        ChordForMatrix(0, 1, 'x', 1),
    )
    with pytest.raises(ValueError, match=r"Invalid sign encountered in"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

# --- End point validation ---
def test_invalid_end_point_raises_value_error():
    bad_matrix = (
        ChordForMatrix(1, 1, '+', 1),
    )
    with pytest.raises(ValueError, match=r"Invalid start and endpoint in"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

# --- Start point order validation ---
def test_start_points_not_strictly_increasing_raises_value_error():
    bad_matrix = (
        ChordForMatrix(1, 2, '-', 2),
        ChordForMatrix(0, 3, '+', 1),
    )
    with pytest.raises(ValueError, match=r"Invalid order of the start points:"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

# --- Start and end points in range [0, 2n-1] validation ---
def test_invalid_points_raises_value_error():
    bad_matrix = (
        ChordForMatrix(0, 1, '+', 1),
        ChordForMatrix(4, 5, '-', 2)
    )
    with pytest.raises(ValueError, match=r"Invalid start/end points"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

# --- Happy path ---
def test_valid_matrix_creates_clasp_diagram():
    matrix = make_valid_matrix(4)
    clasp = ClaspDiagram.from_matrix(matrix=matrix)
    assert clasp.matrix == matrix

# TODO: =============== ClaspDiagram hashability validation ===============



