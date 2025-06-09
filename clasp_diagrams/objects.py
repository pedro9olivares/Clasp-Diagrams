import numpy as np
import sympy as sp
from collections import namedtuple

# Represents a chord with start/end points and properties for matrix computations.
ChordForMatrix = namedtuple('ChordForMatrix', ['start_point', 'end_point', 'sign', 'height'])

# Represents a chord by index with associated properties for array computations.
ChordForArray = namedtuple('ChordForArray', ['chord_idx', 'sign', 'height'])

class ClaspDiagram:
    """
    Represents a clasp diagram and stores various chord representations and algebraic invariants.

    Attributes:
        matrix (list[ChordForMatrix] | None): 
            A list of ChordForMatrix instances, which contain geometric data (start and end points).
        
        array (list[ChordForArray] | None): 
            A list of ChordForArray instances, used for fast numerical computations.

        clasp_word (list[int] | None): 
            A grammatical representation of the clasp diagram.

        e_matrix (sp.Matrix | None): 
            The E-matrix used in symbolic computations.
        
        l_matrix (sp.Matrix | None): 
            The L-matrix used in symbolic computations.
        
        le_matrix (sp.Matrix): 
            The sum of L and E matrices.
        
        sd_matrix (sp.Matrix): 
            A symbolic matrix used for obtaining the alexander polynomial.
        
        alexander (sp.Expr): 
            The Alexander polynomial of the associated knot.
    """

    def __init__(self, *, matrix=None, array=None, calculate_word=False):
        if (matrix is None) == (array is None):
            raise ValueError("Exactly one of `matrix` or `array` must be provided.")
    
        self.matrix = matrix
        self.array = array

        if array is None:
            self.array = self.derive_array_from_matrix()
        elif matrix is None:
            self.matrix = self.derive_matrix_from_array()

        # TODO: (Postpone) generate these attributes
        self.e_matrix = None
        self.l_matrix = None
        self.le_matrix = None
        self.sd_matrix = None
        self.alexander = None

        if calculate_word:
            self.clasp_word = self.generate_clasp_word()
        else:
            self.clasp_word = None

    @classmethod
    def from_matrix(cls, matrix):
        """
        Factory method to create a Clasp from a matrix of chords.
        """
        # TODO: Think if this is really necessary: Add matrix validation for clasp diagram object creation
        return cls(matrix=matrix)
    
    @classmethod
    def from_array(cls, array):
        """
        Factory method to create a Clasp from an array of chords.
        """
        # TODO: Think if this is really necessary: Add array validation for clasp diagram object creation
        return cls(array=array)
    
    def derive_array_from_matrix(self):
        # TODO: Do this derivation (matrix → array)
        raise NotImplementedError("Implement matrix → array conversion.")
    
    def derive_matrix_from_array(self):
        # TODO: Do this derivation (array → matrix)
        raise NotImplementedError("Implement array → matrix conversion.")
    
    def generate_clasp_word(self):
        # TODO: (Postpone) Generate clasp word (algorithm is almost already done)
        raise NotImplementedError("Implement generation of clasp word.")
    
    def __repr__(self):
        return (
            f"{self.__class__.__name__}(\n"
            f"  matrix={self.matrix},\n"
            f"  array={self.array},\n"
            f"  clasp_word={self.clasp_word},\n"
            f"  e_matrix={self.e_matrix},\n"
            f"  l_matrix={self.l_matrix},\n"
            f"  le_matrix={self.le_matrix},\n"
            f"  sd_matrix={self.sd_matrix},\n"
            f"  alexander={self.alexander}\n"
            f")")
    
    def __str__(self):
        matrix_str = "\n".join(
            f"[{chord.start_point}, {chord.end_point}, {chord.sign}, {chord.height}]"
            for chord in self.matrix
        )
        return (
            f"Clasp Diagram object\n"
            f"{matrix_str}"
            f"Alexander polynomial = {self.alexander}"
        )
    
    def __eq__(self, other):
        # TODO: Check equality between two clasp diagrams. They are the same if their matrices match.
        raise NotImplementedError("Implement __eq__")
    
    def __hash__(self):
        # TODO: Hash the matrix.
        raise NotImplementedError("Implement __hash__")
         
