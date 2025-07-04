from clasp_diagrams.moves import erase_isolated_chord, add_isolated_chord
from clasp_diagrams.objects import ClaspDiagram, ChordForMatrix
from clasp_diagrams.generators import random_valid_matrix
from hypothesis import given, settings, strategies as st
import pytest

# ==================== move C1: erase isolated chord ====================
# ==================== Error raising checks ====================
def test_less_than_one_chord_raises():
    unknot = ClaspDiagram.from_matrix(matrix=())
    with pytest.raises(ValueError, match="Clasp diagram needs to have at least one chord."):
        erase_isolated_chord(unknot, i=-1)

def test_invalid_chord_idx_raises():
    clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(3))
    with pytest.raises(ValueError, match="Invalid chord index chosen"):
        erase_isolated_chord(clasp, i=0)
    with pytest.raises(ValueError, match="Invalid chord index chosen"):
        erase_isolated_chord(clasp, i=4)

def test_non_isolated_chord_raises():
    clasp = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 2, '+', 1),
                                             ChordForMatrix(1, 3, '-', 2)))
    with pytest.raises(ValueError, match="is not isolated."):
        erase_isolated_chord(clasp, i=1)
    with pytest.raises(ValueError, match="is not isolated."):
        erase_isolated_chord(clasp, i=2)

# ==================== Move check ====================
def test_C1_expected():
    clasp_1 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 1),))
    expected_1 = ClaspDiagram.from_matrix(matrix=())

    clasp_2 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 1),
                                               ChordForMatrix(2, 3, '-', 2)))
    expected_2 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '-', 1),)) # erased chord 1

    clasp_3 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 4, '+', 1),
                                               ChordForMatrix(1, 2, '-', 2),
                                               ChordForMatrix(3, 6, '+', 3),
                                               ChordForMatrix(5, 7, '-', 4)))
    expected_3 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 2, '+', 1),
                                                  ChordForMatrix(1, 4, '+', 2),
                                                  ChordForMatrix(3, 5, '-', 3),)) # erased chord 2
    
    assert erase_isolated_chord(clasp_1, i=1)[0] == expected_1
    assert erase_isolated_chord(clasp_2, i=1)[0] == expected_2
    assert erase_isolated_chord(clasp_3, i=2)[0] == expected_3
    
def test_C1_preserves_alpo():
    clasp = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 4, '+', 1),
                                            ChordForMatrix(1, 2, '-', 2),
                                            ChordForMatrix(3, 6, '+', 4),
                                            ChordForMatrix(5, 7, '+', 3)))
    modified = erase_isolated_chord(clasp, i=2)[0]

    expected = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 2, '+', 1),
                                                  ChordForMatrix(1, 4, '+', 3),
                                                  ChordForMatrix(3, 5, '+', 2),)) # erased chord 2
    
    assert modified.alexander == expected.alexander
    
def test_C1_on_unknot():
    unknot = ClaspDiagram.from_matrix(matrix=())
    with pytest.raises(ValueError, match="Clasp diagram needs to have at least one chord."):
        erase_isolated_chord(unknot, i=-1)

@given(st.integers(min_value=1, max_value=6))
@settings(deadline=None)
def test_C1_modifies_clasp(n):
    clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(n))
    for i in range(1, n + 1):
        try:
            new_clasp, erased = erase_isolated_chord(clasp, i=i)
            assert new_clasp != clasp
            #print(f"\n Went from {clasp} to {new_clasp}")
        except ValueError as ve:
            # Careful here, printing is done so that no other value errors different than 
            # "ChordForMatrix(...) with chord index i is not isolated." are silently catched.
            #print('\n',ve)
            continue  # Not all i are isolated
    
# ==================== move -C1: add isolated chord ====================
# ==================== Error raising checks ====================
def test_invalid_after_point_raises():
    clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(3))
    with pytest.raises(ValueError, match="Invalid starting/ending point chosen"):
        add_isolated_chord(clasp, after_point=-1, new_sign='+', new_height=1)
    with pytest.raises(ValueError, match="Invalid starting/ending point chosen"):
        add_isolated_chord(clasp, after_point=6, new_sign='+', new_height=1)

def test_invalid_sign_raises():
    clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(3))
    with pytest.raises(ValueError, match="Invalid sign chosen"):
        add_isolated_chord(clasp, after_point=5, new_sign=1, new_height=4)
    with pytest.raises(ValueError, match="Invalid sign chosen"):
        add_isolated_chord(clasp, after_point=5, new_sign='2e', new_height=4)

def test_invalid_height_raises():
    clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(3))
    with pytest.raises(ValueError, match="Invalid height chosen"):
        add_isolated_chord(clasp, after_point=5, new_sign='+', new_height=5)
    with pytest.raises(ValueError, match="Invalid height chosen"):
        add_isolated_chord(clasp, after_point=5, new_sign='+', new_height=0)

# ==================== Move check ====================
def test_C1_inverse_expected():
    raise NotImplementedError()

def test_C1_inverse_preserves_alpo():
    raise NotImplementedError()

def test_C1_inverse_on_unknot():
    raise NotImplementedError()

def test_C1_inverse_on_interesting_heights():
    raise NotImplementedError()

def test_C1_inverse_modifies_clasp():
    raise NotImplementedError()


# ==================== Revertibility checks: C1 + (-C1) or -C1 + C1 ====================
def test_C1_and_C1_inverse():
    raise NotImplementedError()

def test_C1_inverse_and_C1():
    raise NotImplementedError()

@given(st.integers(min_value=1, max_value=6))
@settings(deadline=None)
def test_C1_C1_inverse_property(n):
    raise NotImplementedError()
    """
    clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(n))
    for i in range(1, n + 1):
        try:
            new_clasp, erased = erase_isolated_chord(clasp, i=i)
            recovered = add_isolated_chord(new_clasp,
                                           after_point=erased.start_point - 1,
                                           new_sign=erased.sign,
                                           new_height=erased.height)
            print("\nOriginal: ",clasp,"\n")
            print("\nInt step: ",new_clasp,"\n")
            print("\nRecovered: ",recovered,"\n")
            assert recovered == clasp
        except ValueError as ve:
            print('\n',ve)
            continue  # Not all i are isolated
    """