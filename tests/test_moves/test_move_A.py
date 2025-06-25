from clasp_diagrams.objects import ChordForMatrix, ClaspDiagram
from clasp_diagrams.moves import exchange_heights
from clasp_diagrams.generators import random_valid_matrix
from clasp_diagrams.utils import matrix_chords_intersect, consecutive_heights
from hypothesis import given, strategies as st
import pytest
import random

# ==================== move A: exchange_heights ====================
# ==================== Error raising check ====================
def generate_invalid_indices(n: int):
    """
    Generates random indices i, j outside the range [1, ..., n].

    Rejection sampling is used since valid range is normally small (n <= 10 in larger clasps)
    """
    while True:
        i = random.randint(-100, 100)
        if i < 1 or i > n:
            break

    while True:
        j = random.randint(-100, 100)
        if j < 1 or j > n:
            break

    return i, j

def test_A_raises_less_than_two():
    # Error: less than two chords
    matrix = random_valid_matrix(0)
    clasp = ClaspDiagram.from_matrix(matrix=matrix)
    with pytest.raises(ValueError, match="Clasp diagram has less than two chords"):
        exchange_heights(clasp, i=1, j=2)

    matrix = random_valid_matrix(1)
    clasp = ClaspDiagram.from_matrix(matrix=matrix)
    with pytest.raises(ValueError, match="Clasp diagram has less than two chords"):
        exchange_heights(clasp, i=1, j=2)

@given(st.integers(min_value=2, max_value=5))
def test_A_raises_invalid_indices(n):
    # Error: invalid indices
    matrix = random_valid_matrix(n)
    clasp = ClaspDiagram.from_matrix(matrix=matrix)
    i, j = generate_invalid_indices(n)
    with pytest.raises(ValueError, match="out of bounds for diagram"):
        exchange_heights(clasp, i=i, j=j)

def test_A_raises_same_chord_chosen():
    # Error: same chord chosen
    matrix = random_valid_matrix(5)
    clasp = ClaspDiagram.from_matrix(matrix=matrix)
    with pytest.raises(ValueError, match="Chord indices i, j must be different."):
        exchange_heights(clasp, i=3, j=3)

def test_A_raises_intersecting_chords():
    # Error: chosen chords intersect
    matrix = (ChordForMatrix(0, 2, '+', 1),
              ChordForMatrix(1, 3, '-', 2))
    clasp = ClaspDiagram.from_matrix(matrix=matrix)
    with pytest.raises(ValueError, match="intersect."):
        exchange_heights(clasp, i=1, j=2)

def test_A_non_consecutive_heights():
    # Error: non consecutive heights
    matrix = (ChordForMatrix(0, 1, '+', 1),
              ChordForMatrix(2, 3, '-', 2),
              ChordForMatrix(4, 5, '-', 3),
              ChordForMatrix(6, 7, '-', 4))
    clasp = ClaspDiagram.from_matrix(matrix=matrix)
    with pytest.raises(ValueError, match="don't have consecutive heights."):
        exchange_heights(clasp, i=4, j=2)

# ==================== Move check ====================
def test_A_expected():
    # The check passes if the new clasp diagram equals the expected.
    matrix = (ChordForMatrix(0, 5, '-', 1),
              ChordForMatrix(1, 3, '-', 2),
              ChordForMatrix(2, 6, '-', 4),
              ChordForMatrix(4, 7, '-', 3))
    old_clasp = ClaspDiagram.from_matrix(matrix=matrix)
    new_clasp = exchange_heights(clasp=old_clasp, i=4, j=2)

    expected_matrix = (ChordForMatrix(0, 5, '-', 1),
                        ChordForMatrix(1, 3, '-', 3),
                        ChordForMatrix(2, 6, '-', 4),
                        ChordForMatrix(4, 7, '-', 2))
    expected_clasp = ClaspDiagram.from_matrix(matrix=expected_matrix)

    assert new_clasp == expected_clasp

def test_A_preserves_alpo():
    matrix = (ChordForMatrix(0, 5, '-', 1),
              ChordForMatrix(1, 3, '-', 2),
              ChordForMatrix(2, 6, '-', 4),
              ChordForMatrix(4, 7, '-', 3))
    old_clasp = ClaspDiagram.from_matrix(matrix=matrix)
    new_clasp = exchange_heights(clasp=old_clasp, i=2, j=4)
    assert old_clasp.alexander == new_clasp.alexander

def test_A_and_A_inverse():
    matrix = (ChordForMatrix(0, 5, '-', 1),
              ChordForMatrix(1, 3, '-', 2),
              ChordForMatrix(2, 6, '-', 4),
              ChordForMatrix(4, 7, '-', 3))
    old_clasp = ClaspDiagram.from_matrix(matrix=matrix)
    int_clasp = exchange_heights(clasp=old_clasp, i=2, j=4)
    final_clasp = exchange_heights(clasp=int_clasp, i=4, j=2)
    assert final_clasp == old_clasp

def test_A_modifies_clasp():
    for n in range(2, 6): 
        for _ in range(20):
            # Generate a random clasp diagram with enough chords
            matrix = random_valid_matrix(n)
            clasp = ClaspDiagram.from_matrix(matrix=matrix)

            # Try all pairs where i != j to find a valid (i, j)
            pairs = [(i, j) for i in range(1, n + 1) for j in range(1, n + 1) if i != j]

            for i, j in pairs:
                c1 = matrix[i - 1]
                c2 = matrix[j - 1]

                # Skip if chords intersect or aren't consecutive
                if matrix_chords_intersect(c1, c2):
                    continue
                if not consecutive_heights(c1, c2, n):
                    continue

                # Valid move found
                new_clasp = exchange_heights(clasp=clasp, i=i, j=j)
                # Assert that the move actually modifies the clasp
                assert new_clasp != clasp, f"Move A did not modify the clasp at i={i}, j={j}"

            # Note: If no valid moves are found, the test passes silently as intended.


