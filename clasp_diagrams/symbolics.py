from clasp_diagrams.objects import ChordForMatrix, ChordForArray
import sympy as sp
import numpy as np

def get_e_matrix(clasp_matrix: tuple[ChordForMatrix]) -> np.matrix:
    """
    """
    raise NotImplementedError("Doing...")

def get_l_matrix(clasp_matrix: tuple[ChordForMatrix]) -> np.matrix:
    """
    """
    raise NotImplementedError("Doing...")

def get_le_matrix(e_matrix: np.matrix, l_matrix: np.matrix) -> sp.Matrix:
    """
    """
    raise NotImplementedError("Doing...")

def get_sd_matrix(le_matrix: sp.Matrix) -> sp.Matrix:
    """
    """
    raise NotImplementedError("Doing...")

def get_alexander_polynomial(sd_matrix: sp.Matrix) -> sp.Expr:
    """
    """
    raise NotImplementedError("Doing...")