from clasp_diagrams.utils import matrix_chords_intersect
from clasp_diagrams.objects import ChordForMatrix
from hypothesis import given
import hypothesis.strategies as st

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