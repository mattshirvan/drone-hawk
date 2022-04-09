# Adjacency Matrix
connections = {}
labels = {}

# Size of neighborhood to check
k_neighbors = 2

# External and Interal corner coordinates
E = []
I = []

# Binary Image fig. 1.3 Computer Vision - Shapiro, Stockman
bin_img = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,1,1,1,1,0,0,1,1,0,0,1],
    [1,0,0,0,1,1,1,1,1,1,0,1,1,0,0,1],
    [1,1,1,1,1,0,0,1,1,1,0,0,1,1,0,1],
    [1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,1],
    [1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

def create_adjacency_matrix(r, c):
    """
    Create the adjanceny matrix with coordinates as key
    Key: Vertex, Value: Edges
    G(V, E)
    """

    for i in range(r*c):
        
        row = i // c
        col = i % c

        connections[(row, col)] = []

# Define Interal and External Corners
icorners = ["0001", "0010", "0100", "1000"]
ecorners = ["0111", "1101", "1011", "1110"]

def count_holes(M):
    """
    Returns count of holes in binary image
    """

    # Length and Width of Binary Image M
    length = len(M)
    width = len(M[0])

    # Creates Adjancency Matrix for Binary Image M
    create_adjacency_matrix(length, width)

    # Count for External and Interal corners 
    external = 0
    inside = 0

    # Int procedure Count_Holes(M)
    for x,y in connections:

        # Store patterns in neighborhood
        val = ""

        # Keep track of edges
        row = 0; col = 0

        # Check neighborhood
        for i in range(k_neighbors):
            for j in range(k_neighbors):

                row = i + x 
                col = j + y

                # If in bounds add to pattern 
                if row < length and col < width:
                    val += str(M[row][col])
                    connections[(x, y)].append((row, col))

        # Interal corner
        if val in icorners:
            inside += 1
            labels[(x, y)] = "i"
        
        # External corner
        elif val in ecorners:
            external += 1
            labels[(x, y)] = "e"

    print((external-inside)/4)
    return (external-inside)/4

count_holes(bin_img)
