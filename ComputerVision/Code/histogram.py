from PIL import Image

MAX_VAL  = 256

def histogram(I, H):
    """
    Compute the histogram H of gray-tone image I
    """

    # Length and width
    rows, cols = I.size

    # Get image pixels
    image = I.load()

    # Compute values by accumulation
    for r in range(rows):
        for c in range(cols):

            # Run accumulation
            grayval = image[r,c]
            H[grayval] += 1


    return H

image = Image.open("result_bw.png")
print(histogram(image, [0] * MAX_VAL))
