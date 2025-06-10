from clasp_diagrams.objects import ChordForMatrix, ChordForArray
from collections import Counter

def validate_clasp_matrix(matrix: tuple[ChordForMatrix]) -> None:
    """
    Validates the proposed tuple of ChordForMatrix instances.
    Raises errors if something's off, else just returns.

    n is the number of ChordForMatrix instances.
    Time complexity: O(n)
    Space complexity: O(n)
    """
    # first, None & type checking
    if matrix is None:
        raise ValueError("matrix argument is None")
    if not isinstance(matrix, tuple):
        raise TypeError("matrix argument must be a tuple of ChordForMatrix instances")
    if not all(isinstance(chord, ChordForMatrix) for chord in matrix):
        raise TypeError("All elements of the tuple matrix must be of type ChordForMatrix")
    
    # content checking follows
    
    # height validation: all heights must uniquely go from 1 to n, non-repeating
    # time complexity is O(n), space is O(n)
    n = len(matrix)
    heights = [chord.height for chord in matrix] # O(n)
    if set(heights) != set(range(1, n + 1)):
        raise ValueError(f"The heights are invalid: {heights}")

    # sign validation: signs must be either '+' or '-'
    # end_point validation: all end_points must be strictly greater than the starting points
    # start_point validation: all start_points must strictly increase vertically on the first column
    # time complexity is O(n), space is O(1)
    previous_start_point = -1
    for chord in matrix:
        if chord.sign not in ('+', '-'):
            raise ValueError(f"Invalid sign encountered in {chord}")
        if chord.end_point <= chord.start_point:
            raise ValueError(f"Invalid start and endpoint in {chord}")
        if chord.start_point <= previous_start_point:
            raise ValueError(f"Invalid order of the start points: {previous_start_point} and {chord.start_point}")
        else:
            previous_start_point = chord.start_point

    # start_point and end_point validation: all points go from 0 to 2n-1 uniquely
    # time complexity is O(n), space complexity is O(n)
    points = []
    for chord in matrix:
        points.append(chord.start_point)
        points.append(chord.end_point)
    actual_points = set(points)
    expected_points = set(range(2 * n))
    if actual_points != expected_points:
        raise ValueError(f"Invalid start/end points: {actual_points - expected_points} (expected: 0 to {2 * n - 1})")

def validate_clasp_array(array: list[ChordForArray]) -> None:
    """
    Validates the proposed list of ChordForArray instances.
    Raises errors if something's off, else just returns.

    m is the number of ChordForArray instances.
    Time complexity: O(m)
    Space complexity: O(m)
    """
    # first, None, type and even list checking
    if array is None:
        raise ValueError("array argument is None")
    if not isinstance(array, list):
        raise TypeError("array argument must be a list of ChordForArray instances")
    if not all(isinstance(chord, ChordForArray) for chord in array):
        raise TypeError("All elements of the list must be of type ChordForArray")
    if len(array) % 2 != 0:
        raise ValueError("Array must contain an even number of ChordForArray instances.")
    
    # content checking follows
    
    # double occurrence validation: all instances of ChordForArray must appear exactly twice in the list.
    # they must reference the same chord in memory (hence the id() usage). Not to confuse with the attribute chord_idx.
    # time complexity is O(m), space is O(m)
    chord_id_counts = Counter(id(chord) for chord in array)
    id_to_obj = {id(chord): chord for chord in array}

    invalid_chords = [
        id_to_obj[chord_id]
        for chord_id, count in chord_id_counts.items()
        if count != 2
        ]
    
    if invalid_chords:
        raise ValueError(f"Some ChordForArray objects do not appear exactly twice (they might not the be the same object in memory): {invalid_chords}")

    # sign validation: signs must be either '+' or '-'
    # id validation: check that all chord_idxs are in the range [1, m//2]
    # height validation: check that all chord_idxs are in the range [1, m//2],
    # (No need to check that chord_idxs or heights appear exactly twice; that was handled earlier with object identity)
    m = len(array)
    unique_chords = set()

    for chord in array:
        unique_chords.add(chord)

    for chord in unique_chords:
        if chord.sign not in ('+', '-'):
            raise ValueError(f"Invalid sign encountered in {chord}")
        if not (1 <= chord.chord_idx <= m//2):
            raise ValueError(f"Invalid chord_idx encountered in {chord}. Expected in [1, {m//2}]")
        if not (1 <= chord.height <= m//2):
            raise ValueError(f"Invalid height encountered in {chord}. Expected in [1, {m//2}]")

    