from clasp_diagrams.objects import ChordForMatrix, ChordForArray
from clasp_diagrams.validators import validate_clasp_array, validate_clasp_matrix
import random

def make_valid_chord_for_matrix(idx: int, start: int, end: int, height: int) -> ChordForMatrix:
    if end < start:
        start, end = end, start
    return ChordForMatrix(
        start_point=start,
        end_point=end,
        sign='+' if idx % 2 == 0 else '-',
        height=height
    )

def random_valid_matrix(n: int) -> tuple[ChordForMatrix]:
    """
    Generates a random but valid tuple (matrix) of n ChordForMatrix instances.

    Time complexity: O(n)
    Space complexity: O(n)
    """
    # Allocate 2n unique positions from 0 to 2n-1
    positions = list(range(2 * n))
    random.shuffle(positions)

    matrix = []
    for i in range(n):
        sp = positions[2 * i]
        ep = positions[2 * i + 1]
        matrix.append(make_valid_chord_for_matrix(i, sp, ep, height=i+1))

    matrix = sorted(matrix, key=lambda x: x.start_point)
    matrix = tuple(matrix)

    validate_clasp_matrix(matrix)

    return matrix 

def random_valid_array(n: int) -> list[ChordForArray]:
    """
    Generates a random but valid list of n ChordForArray instances.
    In total, there are m = 2*n of these instances.

    Time complexity: O(m)? (check if remove affects the complexity)
    Space complexity: O(m)
    """
    m = 2 * n
    array = [None] * m
    start_points_stack = list(range(n, 0, -1))
    end_points = []
    already_created_chords = {}

    for j in range(m):
        if len(end_points) == 0:
            idx = start_points_stack.pop()
            end_points.append(idx)
        else:
            # Choose randomly to pop or to extract an element from end_points list
            s1 = len(start_points_stack)
            s2 = len(end_points)
            rand = random.randint(1, s1+s2)
            if rand < s1:
                idx = start_points_stack.pop()
                end_points.append(idx)
            else:
                idx = random.choice(end_points)
                end_points.remove(idx)

        if idx not in already_created_chords:
            already_created_chords[idx] = ChordForArray(chord_idx=idx, sign='+', height=idx)
            array[j] = already_created_chords[idx]
        else:
            array[j] = already_created_chords[idx]

    validate_clasp_array(array)

    return array