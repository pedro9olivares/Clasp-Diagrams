from clasp_diagrams.utils import matrix_chords_intersect, consecutive_heights
from clasp_diagrams.objects import ChordForMatrix
from hypothesis import given
import hypothesis.strategies as st
import pytest

# =============== chords intersect? ===============
# --- Example testing ---
def test_matrix_chords_intersect():
    # No intersection: chord1 ends before chord2 starts
    c1 = ChordForMatrix(start_point=0, end_point=2, sign='+', height=1)
    c2 = ChordForMatrix(start_point=3, end_point=5, sign='-', height=2)
    assert not matrix_chords_intersect(c1, c2)

    # Intersection: chord1 end lies inside chord2
    c1 = ChordForMatrix(start_point=0, end_point=4, sign='+', height=1)
    c2 = ChordForMatrix(start_point=2, end_point=5, sign='-', height=2)
    assert matrix_chords_intersect(c1, c2)

    # Intersection: chord2 starts before chord1, but still intersects
    c1 = ChordForMatrix(start_point=3, end_point=6, sign='+', height=1)
    c2 = ChordForMatrix(start_point=1, end_point=5, sign='-', height=2)
    assert matrix_chords_intersect(c1, c2)

    # No intersection: chord1 completely inside chord2, end point not between
    c1 = ChordForMatrix(start_point=2, end_point=3, sign='+', height=1)
    c2 = ChordForMatrix(start_point=1, end_point=5, sign='-', height=2)
    assert not matrix_chords_intersect(c1, c2)

    # No intersection: identical chords
    c1 = ChordForMatrix(start_point=1, end_point=4, sign='+', height=1)
    c2 = ChordForMatrix(start_point=1, end_point=4, sign='-', height=2)
    assert not matrix_chords_intersect(c1, c2)

# --- Property testing ---
@given(
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=0, max_value=100),
)
def test_matrix_chords_intersect_property(sp1, ep1, sp2, ep2):
    # Ensure distinct points
    if sp1 == ep1:
        ep1 += 1
    if sp2 == ep2:
        ep2 += 1

    # Ensure start <= end for both chords
    start1, end1 = sorted((sp1, ep1))
    start2, end2 = sorted((sp2, ep2))

    c1 = ChordForMatrix(start_point=start1, end_point=end1, sign='+', height=1)
    c2 = ChordForMatrix(start_point=start2, end_point=end2, sign='-', height=2)

    # Ensure c1 starts before c2 (to avoid erroneous expectations)
    if c2.start_point < c1.start_point:
        c1, c2 = c2, c1

    expected = c2.start_point < c1.end_point < c2.end_point
    actual = matrix_chords_intersect(c1, c2)

    assert actual == expected, (
        f"Failed on chords: c1=({c1.start_point},{c1.end_point}) "
        f"c2=({c2.start_point},{c2.end_point}); expected={expected}, actual={actual}"
    )

# =============== consecutive height checks ===============
def test_linear_consecutive_heights():
    n = 2
    c1 = ChordForMatrix(0, 1, '+', 1)
    c2 = ChordForMatrix(2, 3, '-', 2)
    assert consecutive_heights(c1, c2, n)
    assert consecutive_heights(c2, c1, n)

def test_wraparound_consecutive_heights():
    n = 5
    c1 = ChordForMatrix(0, 1, '+', 1)
    c2 = ChordForMatrix(2, 3, '-', 2)
    c3 = ChordForMatrix(4, 5, '+', 3)
    c4 = ChordForMatrix(6, 7, '-', 4)
    c5 = ChordForMatrix(8, 9, '+', 5)
    assert consecutive_heights(c1, c5, n)
    assert consecutive_heights(c5, c1, n)

def test_non_consecutive_heights():
    n = 5
    c1 = ChordForMatrix(0, 1, '+', 1)
    c2 = ChordForMatrix(2, 3, '-', 2)
    c3 = ChordForMatrix(4, 5, '+', 3)
    c4 = ChordForMatrix(6, 7, '-', 4)
    c5 = ChordForMatrix(8, 9, '+', 5)
    assert not consecutive_heights(c1, c4, 5)

def test_invalid_n_negative():
    c1 = ChordForMatrix(0, 1, '+', 1)
    c2 = ChordForMatrix(2, 3, '-', 2)
    with pytest.raises(ValueError):
        consecutive_heights(c1, c2, -5)

# =============== Interval tree testing (skipped, not using interval tree in this version) ===============