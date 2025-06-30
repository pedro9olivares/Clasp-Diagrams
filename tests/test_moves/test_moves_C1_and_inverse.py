from clasp_diagrams.moves import add_isolated_chord, erase_isolated_chord
from clasp_diagrams.objects import ClaspDiagram, ChordForMatrix
from clasp_diagrams.generators import random_valid_matrix
from hypothesis import given, settings, strategies as st

# ==================== move C1: erase isolated chord ====================
# ==================== Error raising checks ====================
# TODO

# ==================== Move check ====================
def test_C1_expected():
    raise NotImplementedError()

def test_C1_preserves_alpo():
    raise NotImplementedError()

def test_C1_on_unknot():
    raise NotImplementedError()

def test_C1_modifies_clasp():
    raise NotImplementedError()

# ==================== move -C1: add isolated chord ====================
# ==================== Error raising checks ====================
# TODO

# ==================== Move check ====================
def test_C1_inverse_expected():
    raise NotImplementedError()

def test_C1_inverse_preserves_alpo():
    raise NotImplementedError()

def test_C1_inverse_on_unknot():
    raise NotImplementedError()

def test_C1_inverse_modifies_clasp():
    raise NotImplementedError()


# ==================== C1 + (-C1): Revertibility checks ====================
def test_C1_and_C1_inverse():
    raise NotImplementedError()

def test_C1_inverse_and_C1():
    raise NotImplementedError()

@given(st.integers(min_value=1, max_value=6))
@settings(deadline=None)
def test_C1_C1_inverse_property(n):
    clasp = ClaspDiagram.from_matrix(matrix=random_valid_matrix(n))
    for i in range(1, n + 1):
        try:
            new_clasp, erased = erase_isolated_chord(clasp, i=i)
            recovered = add_isolated_chord(new_clasp,
                                           after_point=erased.start_point - 1,
                                           new_sign=erased.sign,
                                           new_height=erased.height)
            assert recovered == clasp
            print("Success.")
        except ValueError:
            continue  # Not all i are isolated