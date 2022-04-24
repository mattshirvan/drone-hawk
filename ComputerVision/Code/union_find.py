from logging import exception


MAX_LAB = 8

def initialize():
    """
    Initializes the parents vector and label count
    """

    label = 0
    
    parent = {i: 0 for i in range(1, MAX_LAB+1)}

    return label, parent

def find(X, parent):
    """
    Finds and returns the parent of input node X
    """

    # The j'th child of parent[j] 
    j = X 

    # Climb tree until parent is found (Root of tree)
    while j != 0 and parent[j] != 0:

        # Get the parent of node j
        j = parent[j]

    return j

def union(X, Y, parent):
    """
    Constructs the union of two sets for union-find algorithm
    """

    # jth node 
    j = find(X, parent)

    # kth node
    k = find(Y, parent)

    # Ensure not same node
    if j != k:
        parent[k] = j

    return parent

def union_find(B, LB = [[]]):
    """
    Compute the connected components of a binary image
    Using the union find data structure
    """

    # Initialize parent and label
    label, parent = initialize()
    

    # Row, Col
    max_row = len(B)
    max_col = len(B[0])

    # Initialize labeled image
    LB = B.copy()

    # Run-Length Encoding data structure
    rle = {}

    # Initialize M
    M = 0

    # First pass
    for L in range(max_row):

        # Initialize all labels on line L to zero
        LB[L] = [0] * max_col

        # Process line L
        for P in range(max_col):
            print(L, P)
            
            # Compenent Found
            if B[L][P] > 0:
                
                # Get prior neighbors
                A = prior_neighbors(L, P)

                # No prior neighbors
                if len(A) == 0:

                    # M = label
                    M = label

                    # Increment label
                    label += 1
                
                else:
                    
                    # Minimum labels value
                    M = min(labels(A, rle))
                    
                # Label the component
                LB[L][P] = label
                print(LB)
                rle[(L, P)] = label

                # Loop through new labels
                for X in labels(A, rle):

                    # Union of two sets    
                    if X != M:
                        parent = union(M, X, parent)
    
    # Pass 2 replaces pass 1 labels with equivalence class labels
    for L in range(max_row):
        for P in range(max_col):

            if B[L][P] > 0:
                LB[L][P] = find(LB[L][P], parent)

    return LB

def prior_neighbors(L, P):
    """
    Get the previous neighbors of a component
    N and W or N NW NE W
    """

    # Actions to check neighbors (N, W)
    actions = [(-1, 0), (0, -1)]

    # Prior Neighbors
    neighbors = []

    # Check prior neighbors, return only valid neighbors
    for action in actions:
        
        # Check prior neighbors
        l, p = (L+action[0], P+action[1])

        # Set boundary conditions
        out_of_bounds = l < 0 or p < 0 

        # Check in bounds
        if not out_of_bounds and bin_img[l][p] > 0:

            # Add valid prior neighbors
            neighbors.append((l, p))

    return neighbors

def labels(A, labeled):
    """
    Return the labels for the prior neighbors
    """

    # Store labels
    labels = []

    # Get each pixel
    for pixel in A:

        # Add the labels
        labels.append(labeled[pixel])

    return labels


if __name__ == "__main__":
    
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

    print(union_find(bin_img))

