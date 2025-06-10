from clasp_diagrams.objects import ChordForMatrix, ChordForArray, ClaspDiagram

# =============== Chord for matrix creation ===============
a_chord = ChordForMatrix(0, 1, '+', 1)
print(a_chord, end='\n\n')

# =============== Chord for array creation ===============
another_chord = ChordForArray(1, '+', 1)
print(another_chord, end='\n\n')

# =============== Clasp diagram object creation ===============
# Instantiation of a clasp diagram via matrix
trefoil = ClaspDiagram.from_matrix(matrix=(ChordForMatrix(0, 1, '-', 1),
                                           ChordForMatrix(2, 3, '+', 2))
                                    )
print(repr(trefoil))
print(str(trefoil))

unknot = ClaspDiagram.from_matrix(matrix=())
print(repr(unknot))
print(str(unknot))

# Comparisons are done via comparison of the clasp diagram matrix
print(unknot is unknot)
print(unknot is trefoil)

# Instantiation of a clasp diagram via array

