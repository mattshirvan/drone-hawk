# Adjacency Matrix
connections = {}
labels = {}

# Size of neighborhood to check
k_neighbors = 2

# Binary Image fig. 3.6 Computer Vision - Shapiro, Stockman
bin_img = [
    [1,1,0,1,1,1,0,1],
    [1,1,0,1,0,1,0,1],
    [1,1,1,1,0,0,0,1],
    [0,0,0,0,0,0,0,1],
    [1,1,1,1,0,1,0,1],
    [0,0,0,1,0,1,0,1],
    [1,1,0,1,0,0,0,1],
    [1,1,0,1,0,1,1,1]
]

# Store max values for boundary check
MAX_ROW = len(bin_img) - 1 
MAX_COL = len(bin_img[0]) - 1

def negate(B):
    """
    Takes a binary image and returns a matrix with -1
    Input: Binary Image (B)
    Output: Labeled Binary Image (LB)
    """

    # Store lengths of matrix
    row_length = len(B)
    col_length = len(B[0])

    # Convert 1's to -1's 
    for i in range(row_length):
        for j in range(col_length):
            
            # Ensure only 1's are converted
            if B[i][j] == 1:
                B[i][j] = -1

    return B

def recusive_connected_components(B = [[]], LB = [[]]):
    """
    Main procedure for recursive connected components
    """

    # Convert Binary Image B into negated LB
    LB = negate(B)

    # Label Count 
    label = 0

    # Call Find Components
    find_components(LB, label)
    print(LB)

def find_components(LB, label):
    """
    Find components in the recursive backtracking search procedure
    """

    # Store lengths of matrix
    row_length = len(LB)
    col_length = len(LB[0])
    
    # Check all the points in the binary image
    for L in range(row_length):
        for P in range(col_length):

            # Check if component is found
            if LB[L][P] == -1:
                label += 1
                
                # Call recursive search procedure
                search(LB, label, L, P)

def search(LB, label, L, P):
    """
    Recursively search for connected components
    """

    # Store labeled component
    LB[L][P] = label

    # Set of neighbors
    Nset = neighbors(L, P)

    # Check if components are connected
    for l, p in Nset:

        # if Connected complete connection
        if LB[l][p] == -1:
            search(LB, label, l, p)

def neighbors(L, P):
    """
    Return the set of neighbors to the point (L,P)
    """

    # Actions to check neighbors (N, S, E, W)
    actions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    # Neighbors
    neighbors = []

    # Check neighbors, return only valid neighbors
    for action in actions:
        
        # Check neighbors
        l, p = (L+action[0], P+action[1])

        # Set boundary conditions
        out_of_bounds = (l < 0 or l > MAX_ROW) or (p < 0 or p > MAX_COL)

        # Check in bounds
        if not out_of_bounds:

            # Add valid neighbors
            neighbors.append((l, p))

    return neighbors

recusive_connected_components(bin_img)
