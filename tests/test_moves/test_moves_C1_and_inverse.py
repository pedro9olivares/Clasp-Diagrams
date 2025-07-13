from clasp_diagrams.moves import erase_isolated_chord, add_isolated_chord
from clasp_diagrams.objects import ClaspDiagram, ChordForMatrix
from clasp_diagrams.generators import random_valid_matrix
from hypothesis import given, settings, strategies as st
import pytest
import random

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

def test_non_immediate_close_raises():
    clasp = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0,2,'+',1),
                                             ChordForMatrix(1,5,'+',2),
                                             ChordForMatrix(3,4,'+',3),
                                             ChordForMatrix(6,9,'+',4),
                                             ChordForMatrix(7,8,'+',5)))
    
    with pytest.raises(ValueError, match="does not close immediately."):
        erase_isolated_chord(clasp, i=4)

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
        add_isolated_chord(clasp, after_point=-2, new_sign='+', new_height=1)
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
    clasp_1 = ClaspDiagram.from_matrix(matrix=())
    expected_1 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 1),))

    clasp_2 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 3, '+', 1),
                                               ChordForMatrix(1, 2, '+', 2)))
    expected_2 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 5, '+', 1), 
                                                  ChordForMatrix(1, 4, '+', 3),
                                                  ChordForMatrix(2, 3, '+', 2))) # added this one
    
    clasp_3 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 3, '+', 1),
                                               ChordForMatrix(1, 5, '+', 2),
                                               ChordForMatrix(2, 4, '+', 3)))
    expected_3 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 3, '+', 1),
                                                  ChordForMatrix(1, 5, '+', 2),
                                                  ChordForMatrix(2, 4, '+', 3),
                                                  ChordForMatrix(6, 7, '+', 4))) # added this one
    
    assert expected_1 == add_isolated_chord(clasp_1, after_point=-1, new_sign='+', new_height=1)[0]
    assert expected_2 == add_isolated_chord(clasp_2, after_point=1, new_sign='+', new_height=2)[0]
    assert expected_3 == add_isolated_chord(clasp_3, after_point=5, new_sign='+', new_height=4)[0]

def test_C1_inverse_preserves_alpo():
    clasp = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 3, '+', 1),
                                               ChordForMatrix(1, 5, '+', 2),
                                               ChordForMatrix(2, 4, '+', 3)))
    for i in range(6):  # Points 0 through 5
        new_clasp, chord_idx = add_isolated_chord(clasp, after_point=i, new_sign='+', new_height=4)
        assert (
            clasp.alexander.equals(new_clasp.alexander)
            or clasp.alexander.equals(-new_clasp.alexander)
        )

def test_C1_inverse_on_unknot():
    unknot = ClaspDiagram.from_matrix(matrix=())
    new_clasp, chord_idx = add_isolated_chord(unknot, after_point=-1, new_sign='+', new_height=1)
    expected = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 1),))
    assert new_clasp == expected

def test_C1_inverse_on_heights():
    clasp = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 3, '+', 1),
                                               ChordForMatrix(1, 5, '+', 2),
                                               ChordForMatrix(2, 4, '+', 3)))
    for i in range(1, 5):  # Heights 1 through 5
        new_clasp, chord_idx = add_isolated_chord(clasp, after_point=1, new_sign='+', new_height=i)
        if i == 1:
            expected = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 5, '+', 2),
                                                        ChordForMatrix(1, 7, '+', 3),
                                                        ChordForMatrix(2, 3, '+', i),
                                                        ChordForMatrix(4, 6, '+', 4)))
        elif i == 2:
            expected = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 5, '+', 1),
                                                        ChordForMatrix(1, 7, '+', 3),
                                                        ChordForMatrix(2, 3, '+', i),
                                                        ChordForMatrix(4, 6, '+', 4)))
        elif i == 3:
            expected = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 5, '+', 1),
                                                        ChordForMatrix(1, 7, '+', 2),
                                                        ChordForMatrix(2, 3, '+', i),
                                                        ChordForMatrix(4, 6, '+', 4)))
        elif i == 4:
            expected = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 5, '+', 1),
                                                        ChordForMatrix(1, 7, '+', 2),
                                                        ChordForMatrix(2, 3, '+', i),
                                                        ChordForMatrix(4, 6, '+', 3)))

        assert new_clasp == expected

@given(st.integers(min_value=1, max_value=5))
@settings(deadline=None)
def test_C1_inverse_modifies_clasp(n):
    clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(n))
    for i in range(0, 2*n):
        new_clasp, chord_idx = add_isolated_chord(clasp, after_point=i, new_sign='+', new_height=1)
        assert clasp != new_clasp
        #print(f"\n Went from {clasp} to {new_clasp}")

# ==================== Revertibility checks: C1 + (-C1) or -C1 + C1 ====================
successful = 0
@given(st.integers(min_value=1, max_value=7))
@settings(deadline=None)
def test_C1_then_C1_inverse(n):
    global successful
    # For n chords, let's do 20 different random generations
    for _ in range(20):
        clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(n))
        for i in range(1, n + 1):
            try:
                new_clasp, erased = erase_isolated_chord(clasp, i=i)
                rev_idx = erased.start_point - 1

                # Edge case: wrap around handling
                reverse_points = False
                if erased.start_point == 0 and erased.end_point == 2*n - 1:
                    reverse_points = True

                recovered, chord_idx = add_isolated_chord(new_clasp,
                                            after_point=rev_idx,
                                            new_sign=erased.sign,
                                            new_height=erased.height,
                                            reverse_points=reverse_points)
                
                assert clasp == recovered, f"Failed on erasing chord_idx {i}: {clasp.matrix[i-1]}, used rev_idx={rev_idx}"
                successful += 1
            except ValueError as ve:
                # Careful here, visually check that only ValueErrors like "... is not isolated" or 
                # "... does not close immediately" occur. No others allowed
                #print('\n',ve)
                continue  # Not all i are isolated
    #print(f"successful recoveries (C1 then -C1): {successful}")

@given(st.integers(min_value=1, max_value=5))
@settings(deadline=None)
def test_C1_inverse_then_C1(n):
    for _ in range(20):
        clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(n))
        for after_point in range(-1, 2*n):
            new_clasp, chord_idx  = add_isolated_chord(clasp, after_point=after_point, new_sign='+', new_height=random.randint(1, n+1))
            recovered = erase_isolated_chord(new_clasp, i=chord_idx)
            assert clasp == recovered[0]

    new_clasp, chord_idx = add_isolated_chord(clasp, after_point=-1, new_sign='+', new_height=random.randint(1, n+1), reverse_points=True)
    recovered = erase_isolated_chord(new_clasp, i=1)
    assert clasp == recovered[0]

