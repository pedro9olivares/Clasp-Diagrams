from hypothesis import given, strategies as st
from clasp_diagrams.objects import ChordForMatrix, ChordForArray
from clasp_diagrams.transformations import transform_matrix_to_array, transform_array_to_matrix
from clasp_diagrams.validators import validate_clasp_array, validate_clasp_matrix
from clasp_diagrams.generators import random_valid_matrix, random_valid_array


@given(st.integers(min_value=1, max_value=100))
def test_transform_matrix_to_array_produces_valid_array(n):
    """
    Generates a valid matrix of n ChordForMatrix instances and verifies that the
    transform_matrix_to_array function produces a valid array.
    """
    print(f"Testing with n={n}")

    matrix = random_valid_matrix(n)

    array = transform_matrix_to_array(matrix)
    
    # Ensure output is a valid clasp array
    validate_clasp_array(array)

    # Check that the array has exactly 2n elements
    assert len(array) == 2 * n

    # All elements should be instances of ChordForArray
    assert all(isinstance(c, ChordForArray) for c in array)


@given(st.integers(min_value=1, max_value=100))
def test_transform_array_to_matrix_produces_valid_matrix(n):
    """
    Generates a valid array of n ChordForArray instances and verifies that the
    transform_array_to_matrix function produces a valid matrix.
    """
    print(f"Testing with n={n}")
    
    array = random_valid_array(n)

    matrix = transform_array_to_matrix(array)

    # Ensure output is a valid clasp matrix
    validate_clasp_matrix(matrix)

    # Check size
    assert len(matrix) == n

    # All elements should be instances of ChordForMatrix
    assert all(isinstance(c, ChordForMatrix) for c in matrix)
