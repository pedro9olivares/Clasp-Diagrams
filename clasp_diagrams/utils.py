from clasp_diagrams.objects import ChordForMatrix, ChordForArray

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