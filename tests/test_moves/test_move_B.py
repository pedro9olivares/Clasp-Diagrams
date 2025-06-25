from clasp_diagrams.objects import ChordForMatrix, ClaspDiagram
from clasp_diagrams.moves import cyclic_height_shift, inverse_cyclic_height_shift
from clasp_diagrams.generators import random_valid_matrix
from hypothesis import given, settings, strategies as st

# ==================== move B and -B: cyclic height shift ====================
# ==================== Move check ====================
def test_B_expected():
    clasp = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 2),
                                             ChordForMatrix(2, 3, '+', 1),
                                             ChordForMatrix(4, 5, '+', 3),))
    
    expected = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 3),
                                                ChordForMatrix(2, 3, '+', 2),
                                                ChordForMatrix(4, 5, '+', 1),))
    new = cyclic_height_shift(clasp)

    assert new == expected

def test_B_inverse_expected():
    clasp = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 2),
                                             ChordForMatrix(2, 3, '+', 1),
                                             ChordForMatrix(4, 5, '+', 3),))
    
    expected = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 1),
                                                ChordForMatrix(2, 3, '+', 3),
                                                ChordForMatrix(4, 5, '+', 2),))
    new = inverse_cyclic_height_shift(clasp)

    assert new == expected

def test_B_preserves_alpo():
    clasp = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 2),
                                             ChordForMatrix(2, 3, '+', 1),
                                             ChordForMatrix(4, 5, '+', 3),))

    new = cyclic_height_shift(clasp)

    assert clasp.alexander == new.alexander and clasp != new

def test_B_inverse_preserves_alpo():
    clasp = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 2),
                                             ChordForMatrix(2, 3, '+', 1),
                                             ChordForMatrix(4, 5, '+', 3),))

    new = inverse_cyclic_height_shift(clasp)

    assert clasp.alexander == new.alexander and clasp != new

def test_B_and_B_inverse():
    clasp = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 2),
                                             ChordForMatrix(2, 3, '+', 1),
                                             ChordForMatrix(4, 5, '+', 3),))

    intermediate = cyclic_height_shift(clasp)
    new = inverse_cyclic_height_shift(intermediate)

    assert new == clasp

def test_B_and_B_inverse_other_dir():
    clasp = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '+', 2),
                                             ChordForMatrix(2, 3, '+', 1),
                                             ChordForMatrix(4, 5, '+', 3),))

    intermediate = inverse_cyclic_height_shift(clasp)
    new = cyclic_height_shift(intermediate)

    assert new == clasp

def test_B_on_unknot():
    clasp = ClaspDiagram.from_matrix(matrix=())
    new = cyclic_height_shift(clasp)
    assert clasp == new

def test_B_inverse_on_unknot():
    clasp = ClaspDiagram.from_matrix(matrix=())
    new = inverse_cyclic_height_shift(clasp)
    assert clasp == new

@given(st.integers(min_value=2, max_value=6))
@settings(deadline=None)
def test_B_modifies_clasp(n):
    clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(n))
    new = cyclic_height_shift(clasp)

    assert new != clasp

@given(st.integers(min_value=2, max_value=6))
@settings(deadline=None)
def test_B_inverse_modifies_clasp(n):
    clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(n))
    new = inverse_cyclic_height_shift(clasp)

    assert new != clasp