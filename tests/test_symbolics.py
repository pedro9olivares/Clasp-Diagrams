from hypothesis import given, strategies as st
from clasp_diagrams.symbolics import get_l_matrix
from clasp_diagrams.objects import ClaspDiagram, ChordForMatrix
from clasp_diagrams.utils import matrix_chords_intersect
import numpy as np
import sympy as sp

# Only the testing of the generation of the L-matrix and alexander polynomial is performed.
# This is because the L-matrix is the only non-trivial matrix to be generated, and because
# the alexander polynomial sits at the end of all symbolic calculations.
# It uses the SD-matrix, which in turn uses the LE-matrix, so testing the alexander polynomial implicitly tests all previous matrices.

# =============== symbolics.py standalone testing ===============
def test_get_l_matrix1():
    clasp_matrix = (ChordForMatrix(0, 3, '+', 3),
                    ChordForMatrix(1, 5, '+', 2),
                    ChordForMatrix(2, 4, '+', 1))
    
    expected_l_matrix = np.array([[0,1,1],
                                  [0,0,0],
                                  [0,0,0]])
    
    calculated_l_matrix = get_l_matrix(clasp_matrix=clasp_matrix)
    #print(f"Calculated L matrix: \n{calculated_l_matrix}")
    
    assert np.array_equal(expected_l_matrix, calculated_l_matrix), f"L matrix mismatch: {calculated_l_matrix} != {expected_l_matrix}"

def test_get_l_matrix2():
    clasp_matrix = (ChordForMatrix(0, 3, '+', 1),
                    ChordForMatrix(1, 5, '+', 2),
                    ChordForMatrix(2, 4, '+', 3))
    
    expected_l_matrix = np.array([[0,0,0],
                                  [-1,0,0],
                                  [-1,0,0]])
    
    calculated_l_matrix = get_l_matrix(clasp_matrix=clasp_matrix)
    #print(f"Calculated L matrix: \n{calculated_l_matrix}")
    
    assert np.array_equal(expected_l_matrix, calculated_l_matrix), f"L matrix mismatch: {calculated_l_matrix} != {expected_l_matrix}"

def test_get_alexander_polynomial():
    t = sp.symbols('t')
    alpo_unknot = sp.Integer(1)
    alpo_3_1 = 1 - t + t**2
    alpo_4_1 = 1 - 3*t + t**2
    alpo_5_1 = 1 - t + t**2 - t**3 + t**4
    alpo_5_2 = 2 - 3*t + 2*t**2
    alpo_6_1 = 2 - 5*t + 2*t**2
    alpo_6_2 = 1 - 3*t + 3*t**2 - 3*t**3 + t**4

    # Caveat: instead of testing get_alexander_polynomial(), we test ClaspDiagram.alexander
    unknot = ClaspDiagram.from_matrix(matrix=())
    cd_3_1 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 2, '+', 2),
                                              ChordForMatrix(1, 3, '+', 1)))
    cd_4_1 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 2, '-', 2),
                                              ChordForMatrix(1, 3, '+', 1)))
    cd_5_1 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 3, '+', 3),
                                              ChordForMatrix(1, 4, '+', 2),
                                              ChordForMatrix(2, 5, '+', 1)))
    cd_5_2 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 3, '+', 3),
                                              ChordForMatrix(1, 5, '+', 1),
                                              ChordForMatrix(2, 4, '+', 2)))
    cd_6_1 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 3, '-', 3),
                                              ChordForMatrix(1, 5, '+', 2),
                                              ChordForMatrix(2, 4, '+', 1)))
    cd_6_2 = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 3, '-', 3),
                                              ChordForMatrix(1, 4, '+', 2),
                                              ChordForMatrix(2, 5, '+', 1)))
    
    # Equality is tested up to sign
    assert sp.simplify(unknot.alexander - alpo_unknot) == 0 or sp.simplify(-1 * unknot.alexander - alpo_unknot) == 0
    assert sp.simplify(cd_3_1.alexander - alpo_3_1) == 0 or sp.simplify(-1 * cd_3_1.alexander - alpo_3_1) == 0
    assert sp.simplify(cd_4_1.alexander - alpo_4_1) == 0 or sp.simplify(-1 * cd_4_1.alexander - alpo_4_1) == 0
    assert sp.simplify(cd_5_1.alexander - alpo_5_1) == 0 or sp.simplify(-1 * cd_5_1.alexander - alpo_5_1) == 0
    assert sp.simplify(cd_5_2.alexander - alpo_5_2) == 0 or sp.simplify(-1 * cd_5_2.alexander - alpo_5_2) == 0
    assert sp.simplify(cd_6_1.alexander - alpo_6_1) == 0 or sp.simplify(-1 * cd_6_1.alexander - alpo_6_1) == 0
    assert sp.simplify(cd_6_2.alexander - alpo_6_2) == 0 or sp.simplify(-1 * cd_6_2.alexander - alpo_6_2) == 0
    