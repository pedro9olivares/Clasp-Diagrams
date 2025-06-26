import pytest
from clasp_diagrams.objects import ChordForMatrix, ChordForArray, ClaspDiagram
from clasp_diagrams.generators import random_valid_matrix, random_valid_array
from hypothesis import given, settings, strategies as st

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


# --- Happy path, as of now max_chords are 10 (max_value) ---
@given(st.integers(min_value=0, max_value=10))
@settings(deadline=None)
def test_creation_from_matrix(n):
    matrix = random_valid_matrix(n)
    clasp = ClaspDiagram.from_matrix(matrix=matrix)
    assert clasp.matrix == matrix


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

def test_validate_chord_idx_raises2():
    chord1 = ChordForArray(2, '+', 2)
    chord2 = ChordForArray(1, '+', 1)
    arr = [chord1, chord1, chord2, chord2]
    with pytest.raises(ValueError, match="Invalid ordering of chord idxs:"):
        ClaspDiagram.from_array(arr)


# --- Happy path, as of now max_chords are 10 (max_value) ---
@given(st.integers(min_value=0, max_value=10))
@settings(deadline=None)
def test_creation_from_array(n):
    array = random_valid_array(n)
    clasp = ClaspDiagram.from_array(array=array)
    assert clasp.array == array

# =============== ClaspDiagram hashability validation ===============
@given(st.integers(min_value=0, max_value=10))
@settings(deadline=None)
def test_clasp_diagram_from_matrix_is_hashable(n):
    matrix = random_valid_matrix(n)
    clasp = ClaspDiagram.from_matrix(matrix=matrix)
    clasp_set = {clasp}
    assert clasp in clasp_set

@given(st.integers(min_value=0, max_value=10))
@settings(deadline=None)
def test_clasp_diagram_from_array_is_hashable(n):
    array = random_valid_array(n)
    clasp = ClaspDiagram.from_array(array=array)
    clasp_set = {clasp}
    assert clasp in clasp_set

# =============== Random creation validation ===============
@given(st.integers(min_value=0, max_value=500))
def test_random_valid_matrix(n):
    random_valid_matrix(n)

@given(st.integers(min_value=0, max_value=500))
def test_random_valid_array(n):
    random_valid_array(n)

# =============== Move delegator ===============
def test_move_delegator_raises_error():
    clasp = ClaspDiagram.from_array(array=random_valid_array(3))
    with pytest.raises(ValueError, match="Invalid move_num"):
        clasp.move(move_num=-99, i=1, j=2)

def test_move_delegator_on_arbitrary_move():
    clasp = ClaspDiagram.from_array(array=random_valid_array(3))

    int_clasp = clasp.move(move_num=2, i=None, j=None)
    final_clasp = int_clasp.move(move_num=-2, i=None, j=None)

    assert clasp == final_clasp

