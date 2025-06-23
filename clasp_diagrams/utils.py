from clasp_diagrams.objects import ChordForMatrix, ChordForArray
from intervaltree import IntervalTree

def matrix_chords_intersect(chord1: ChordForMatrix, chord2: ChordForMatrix) -> bool:
    """
    Checks whether two chords intersect on the circle.
    Done by checking if the end_point of the chord with the smaller start_point 
    lies between the other chord's start_point and end_point.

    Time complexity: O(1)
    Space complexity: O(1)
    """
    if chord2.start_point < chord1.start_point:
        chord1, chord2 = chord2, chord1
    
    return chord2.start_point < chord1.end_point < chord2.end_point

def array_chords_intersect(array: list[ChordForArray], chord1: ChordForArray, chord2: ChordForArray) -> bool:
    raise NotImplementedError("This method has O(n) complexity. Use instead matrix_chords_intersect.")

def consecutive_heights(chord1: ChordForMatrix, chord2: ChordForMatrix, n: int) -> bool:
    """
    Checks if two chords have consecutive heights, modulo n.

    Time complexity: O(1)
    Space complexity: O(1)
    """
    if n < 2:
        raise ValueError(f"Invalid n={n} for consecutive_heights check.") 

    h1 = chord1.height
    h2 = chord2.height

    return (h1 - h2) % n in (1, n-1)

def get_interval_tree(clasp_matrix: tuple[ChordForMatrix])-> IntervalTree:
    """
    Constructs an interval tree where each chord is represented as [start_point, end_point).
    The tree allows efficient queries of overlapping chords.

    Time complexity: O(nlogn)
    Space complexity: O(n)
    """
    tree = IntervalTree()
    for chord in clasp_matrix:
        # Insert interval [start, end) -> chord
        # We use +1 because IntervalTree treats [start, end)
        tree[chord.start_point : chord.end_point + 1] = chord
    return tree