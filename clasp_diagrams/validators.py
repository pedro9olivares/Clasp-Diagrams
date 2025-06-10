from clasp_diagrams.objects import ChordForMatrix

def validate_clasp_matrix(matrix: tuple[ChordForMatrix]) -> None:
    """
    Validates the proposed tuple of ChordForMatrix instances.
    Raises errors if something's off, else just returns.

    n is the number of ChordForMatrix instances.
    Time complexity: O(n)
    Space complexity: O(n)
    """
    # first, type & None checking
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

