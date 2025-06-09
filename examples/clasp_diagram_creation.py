from clasp_diagrams.objects import ChordForMatrix, ChordForArray, ClaspDiagram

# =============== Chord for matrix creation ===============
a_chord = ChordForMatrix(0, 1, '+', 1)
print(a_chord, end='\n\n')

# =============== Chord for array creation ===============
another_chord = ChordForArray(1, '+', 1)
print(another_chord, end='\n\n')

# =============== Clasp diagram object creation ===============
# Instantiation of a clasp diagram via matrix
unknot = ClaspDiagram.from_matrix([])
print(repr(unknot))
print(str(unknot))

trefoil = ClaspDiagram.from_matrix([ChordForMatrix(0, 2, '+', 2),
                                    ChordForMatrix(1, 3, '+', 1)])
print(repr(trefoil))
print(str(trefoil))

# Comparisons are done via comparison of the clasp diagram matrix
print(unknot is unknot)
print(unknot is trefoil)


# Instantiation of a clasp diagram via array

