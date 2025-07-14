from __future__ import annotations
from pydantic.dataclasses import dataclass

# TODO: (Eventually) add mirrors!

# Represents a chord with start/end points and properties for matrix computations.
@dataclass(frozen=True)
class ChordForMatrix:
    start_point: int
    end_point: int
    sign: str
    height: int

# Represents a chord by index with associated properties for array computations.
@dataclass(frozen=True)
class ChordForArray:
    chord_idx: int
    sign: str
    height: int

# Represents a clasp diagram, our main object.
class ClaspDiagram:
    """
    Represents a clasp diagram and stores various chord representations and algebraic invariants.

    Attributes:
        matrix (tuple[ChordForMatrix] | None): 
            A tuple of ChordForMatrix instances, which contain geometric data (start and end points).
        
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

    def __init__(self, *, matrix=None, array=None, calculate_symbolics=True, calculate_word=False):
        if (matrix is None) == (array is None):
            raise ValueError("Exactly one of `matrix` or `array` must be provided.")
    
        self.matrix = matrix
        self.array = array

        if array is None:
            self.array = self.derive_array_from_matrix()
        elif matrix is None:
            self.matrix = self.derive_matrix_from_array()

        if calculate_symbolics:
            from . import symbolics
            self.e_matrix = symbolics.get_e_matrix(clasp_matrix=self.matrix)
            self.l_matrix = symbolics.get_l_matrix(clasp_matrix=self.matrix)
            self.le_matrix = symbolics.get_le_matrix(e_matrix=self.e_matrix,
                                                    l_matrix=self.l_matrix)
            self.sd_matrix = symbolics.get_sd_matrix(le_matrix=self.le_matrix)
            self.alexander = symbolics.get_alexander_polynomial(sd_matrix=self.sd_matrix)

        if calculate_word:
            self.clasp_word = self.generate_clasp_word()
        else:
            self.clasp_word = None

    @classmethod
    def from_matrix(cls, *, matrix):
        """
        Factory method to create a Clasp from a tuple of ChordForMatrix instances.
        n is the number of ChordForMatrix instances.

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        from clasp_diagrams.validators import validate_clasp_matrix
        validate_clasp_matrix(matrix) # O(n) time, O(n) space
        return cls(matrix=matrix)
    
    @classmethod
    def from_array(cls, array):
        """
        Factory method to create a Clasp from an array of chords.
        m is the number of ChordForArray instances.

        Time Complexity: O(m)
        Space Complexity: O(m)
        """
        from clasp_diagrams.validators import validate_clasp_array
        validate_clasp_array(array) # O(m) time, O(m) space
        return cls(array=array)
    
    def derive_array_from_matrix(self):
        from clasp_diagrams.transformations import transform_matrix_to_array
        from clasp_diagrams.validators import validate_clasp_array

        array = transform_matrix_to_array(self.matrix) # O(n) time, O(n) space
        validate_clasp_array(array) # O(m) time, O(m) space

        return array
    
    def derive_matrix_from_array(self):
        from clasp_diagrams.transformations import transform_array_to_matrix
        from clasp_diagrams.validators import validate_clasp_matrix

        matrix = transform_array_to_matrix(self.array)
        validate_clasp_matrix(matrix)

        return matrix
    
    def generate_clasp_word(self):
        # TODO: (Postpone) Generate clasp word (algorithm is almost already done)
        raise NotImplementedError("Implement generation of clasp word.")
    
    def __repr__(self):
    #    return (
    #        f"{self.__class__.__name__}(\n"
    #        f"  matrix={self.matrix},\n"
    #        f"  array={self.array},\n"
    #        f"  clasp_word={self.clasp_word},\n"
    #        f"  e_matrix={self.e_matrix},\n"
    #        f"  l_matrix={self.l_matrix},\n"
    #        f"  le_matrix={self.le_matrix},\n"
    #        f"  sd_matrix={self.sd_matrix},\n"
    #        f"  alexander={self.alexander}\n"
    #        f")")
        if len(self.matrix) == 0:
                matrix_str = "[]"
        else:
            matrix_str = "\n".join(
                f"[{chord.start_point}, {chord.end_point}, {chord.sign}, {chord.height}]"
                for chord in self.matrix
            )

        return (
            f"Clasp Diagram object\n"
            f"{matrix_str}\n"
            f"Alexander polynomial = {self.alexander}"
        )
    
    def __str__(self):
        if len(self.matrix) == 0:
            matrix_str = "[]"
        else:
            matrix_str = "\n".join(
                f"[{chord.start_point}, {chord.end_point}, {chord.sign}, {chord.height}]"
                for chord in self.matrix
            )

        return (
            f"Clasp Diagram object\n"
            f"{matrix_str}\n"
            f"Alexander polynomial = {self.alexander}"
        )
    
    def __eq__(self, other):
        """
        Checks equality between two clasp diagrams. They are the same if their matrices match.
        """
        if not isinstance(other, ClaspDiagram):
            return NotImplemented
        return self.matrix == other.matrix
    
    def __hash__(self):
        """
        Hashes a clasp diagram via a hashing of the matrix, which is a tuple of namedtuples.
        """
        return hash(self.matrix)
         
    def move(self, *, move_num, **kwargs) -> ClaspDiagram:
        """
        Applies a move to the clasp diagram, delegated by move number.
        Chord indexes are 1-indexed.
        Start/end points are 0-indexed.

        Usage:
        - Move A (and its inverse -A): use `move_num=1`. Requires keyword arguments `i` and `j` (chord indices).
        - Move B: use `move_num=2`. No additional arguments required.
        - Move -B: use `move_num=-2`. No additional arguments required.
        - Move C1: use `move_num=3`. Requires keyword argument `i`, the index of the chord to erase.
        - Move -C1: use `move_num=-3`. Requires keyword arguments:
            - `after_point`: int — the point after which to insert the new chord.
            - `new_sign`: '+' or '-' — the sign of the new chord.
            - `new_height`: int — the height of the new chord.
            - `reverse_points`: bool, optional — whether to use a wrapped point insertion (default: False).

        Parameters
        ----------
        move_num : int
            The move identifier.
        **kwargs :
            Keyword arguments required for the specific move.

        Returns
        -------
        ClaspDiagram
            The result of applying the move.
        """
        import clasp_diagrams.moves as moves
        MOVES = {
                1: moves.exchange_heights,
                2: moves.cyclic_height_shift,
                -2: moves.inverse_cyclic_height_shift,
                3: moves.erase_isolated_chord,
                -3: moves.add_isolated_chord,
                }
        
        try:
            move = MOVES[move_num]
        except KeyError:
            allowed = ', '.join(f"{k}: {v.__name__}" for k, v in MOVES.items())
            raise ValueError(f"Invalid move_num={move_num}. Must be one of: {allowed}")
        
        return move(clasp=self, **kwargs)
    
    def move_help(move_num: int) -> str:
        import clasp_diagrams.moves as moves
        MOVES = {
            1: moves.exchange_heights,
            2: moves.cyclic_height_shift,
            -2: moves.inverse_cyclic_height_shift,
            3: moves.erase_isolated_chord,
            -3: moves.add_isolated_chord,
        }
        try:
            return MOVES[move_num].__doc__
        except KeyError:
            return f"No such move: {move_num}."