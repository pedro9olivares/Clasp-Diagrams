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

# =============== creation via matrix validation ===============
# --- Creation validation ---
def test_none_matrix_raises_value_error():
    with pytest.raises(ValueError, match="matrix argument is None"):
        ClaspDiagram.from_matrix(matrix=None)

def test_non_tuple_matrix_raises_type_error():
    with pytest.raises(TypeError, match="matrix argument must be a tuple of ChordForMatrix instances"):
        ClaspDiagram.from_matrix(matrix=[1, 2, 3])  # (passing list instead of tuple)

def test_non_chord_element_raises_type_error_from_matrix():
    bad_matrix = (1, 2, 3)
    with pytest.raises(TypeError, match="All elements of the tuple matrix must be of type ChordForMatrix"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

# --- Height validation ---
def test_non_unique_heights_raises_value_error():
    bad_matrix = (
        ChordForMatrix(0, 1, '+', 1),
        ChordForMatrix(2, 3, '-', 5)
    )
    with pytest.raises(ValueError, match="The heights are invalid"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

# --- Sign validation ---
def test_invalid_sign_raises_value_error():
    bad_matrix = (
        ChordForMatrix(0, 1, 'x', 1),
    )
    with pytest.raises(ValueError, match="Invalid sign encountered in"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

# --- End point validation ---
def test_invalid_end_point_raises_value_error():
    bad_matrix = (
        ChordForMatrix(1, 1, '+', 1),
    )
    with pytest.raises(ValueError, match="Invalid start and endpoint in"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

# --- Start point order validation ---
def test_start_points_not_strictly_increasing_raises_value_error():
    bad_matrix = (
        ChordForMatrix(1, 2, '-', 2),
        ChordForMatrix(0, 3, '+', 1),
    )
    with pytest.raises(ValueError, match="Invalid order of the start points:"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

# --- Start and end points in range [0, 2n-1] validation ---
def test_invalid_points_raises_value_error():
    bad_matrix = (
        ChordForMatrix(0, 1, '+', 1),
        ChordForMatrix(4, 5, '-', 2)
    )
    with pytest.raises(ValueError, match="Invalid start/end points"):
        ClaspDiagram.from_matrix(matrix=bad_matrix)

"""
TODO: test this
# --- Happy path ---
def test_happy_path_from_matrix():
    matrix = make_valid_matrix(4)
    clasp = ClaspDiagram.from_matrix(matrix=matrix)
    assert clasp.matrix == matrix
 """

# =============== creation via array validation ===============
# --- Creation validation ---
def test_none_array_raises_value_error():
    with pytest.raises(ValueError, match="array argument is None"):
        ClaspDiagram.from_array(array=None)

def test_non_list_raises_type_error():
    with pytest.raises(TypeError, match="array argument must be a list of ChordForArray instances"):
        ClaspDiagram.from_array(array=(1, 2, 3))  # (passing tuple instead of list)

def test_non_chord_element_raises_type_error_from_array():
    bad_array = [1, 2, 3]
    with pytest.raises(TypeError, match="All elements of the list must be of type ChordForArray"):
        ClaspDiagram.from_array(array=bad_array)

def test_validate_odd_length_raises_value_error():
    with pytest.raises(ValueError, match="Array must contain an even number of ChordForArray instances."):
        ClaspDiagram.from_array([ChordForArray(1, '+', 1)])

# --- Content validation ---
def test_validate_non_double_occurrence_raises():
    chord1 = ChordForArray(1, '+', 2)
    chord2 = ChordForArray(2, '+', 1)
    arr = [chord1, chord2, chord1, ChordForArray(2, '+', 1)]  # chord2 is not the same object in memory
    with pytest.raises(ValueError, match="do not appear exactly twice"):
        ClaspDiagram.from_array(arr)

def test_validate_sign_raises():
    chord1 = ChordForArray(1, '*', 2)
    chord2 = ChordForArray(2, '+', 1)
    arr = [chord1, chord1, chord2, chord2]
    with pytest.raises(ValueError, match="Invalid sign encountered"):
        ClaspDiagram.from_array(arr)

def test_validate_chord_idx_raises():
    chord1 = ChordForArray(2, '+', 2)
    chord2 = ChordForArray(3, '+', 1)
    arr = [chord1, chord1, chord2, chord2]
    with pytest.raises(ValueError, match="Invalid chord_idx encountered"):
        ClaspDiagram.from_array(arr)

def test_validate_height_raises():
    chord1 = ChordForArray(1, '+', 3)
    chord2 = ChordForArray(2, '+', 1)
    arr = [chord1, chord1, chord2, chord2]
    with pytest.raises(ValueError, match="Invalid height encountered"):
        ClaspDiagram.from_array(arr)

"""
TODO: test this
def test_happy_path_from_array():
    chord1 = make_chord(sign='+', chord_idx=1, height=1)
    chord2 = make_chord(sign='-', chord_idx=2, height=2)
    arr = [chord1, chord1, chord2, chord2]
    # Should not raise
    validate_clasp_array(arr)
"""

# TODO: =============== ClaspDiagram hashability validation ===============


# TODO: =============== Random creation validation =============== (with hypothesis)
