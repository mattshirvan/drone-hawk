import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd

def ransac_fit(X, y, data, max_iterations = 100, select_points = 10, min_consensus_size = 10, consensus = 0.05):

    # Best Model
    best_model = {}

    # Best error
    best_error = np.inf

    # Run through max iterations k = log(1 - p) / log(1 - w^n)
    for _ in range(max_iterations):

        # Randomly select subset of data set 
        #points = random.sample(data, select_points)
        points = np.random.default_rng().permutation(data)

        # Initial inliers
        maybe_inliers = points[: select_points]

        # First model fit
        maybe_model = fit(X[maybe_inliers], y[maybe_inliers])

        # Set threshold
        thresholded = squared_error_loss(y[points][select_points :], predict(X[points][select_points :], maybe_model)) < consensus

        # Get the inliers ids
        inlier_ids = points[select_points :][np.flatnonzero(thresholded).flatten()]

        # Compare against minimum consensus 
        if inlier_ids.size > min_consensus_size:

            # Get the inlier points 
            inlier_points = np.hstack([maybe_inliers, inlier_ids])

            # Fit for best model
            best_model = fit(X[inlier_points], y[inlier_points])

            # Get current error
            this_error = mean_squared_error(y[inlier_points], predict(X[inlier_points], best_model))

            # If a reduction in error
            if this_error < best_error:

                # Set new error
                best_error = this_error

                # Set new model
                best_model = maybe_model

    return best_model

def fit(X: np.ndarray, y: np.ndarray):
    """
    Fit data points
    """
    r, _ = X.shape
    X = np.hstack([np.ones((r, 1)), X])
    params = np.linalg.inv(X.T @ X) @ X.T @ y
    return params

def predict( X: np.ndarray, params = None):
    """
    Run prediction on data points
    """
    r, _ = X.shape
    X = np.hstack([np.ones((r, 1)), X])
    return X @ params

def squared_error_loss(true_value, predicted_value):
    """
    Squared error loss
    """

    return (true_value - predicted_value) ** 2

def mean_squared_error(true_value, predicted_value):
    """
    Mean Squared Error (MSE)
    """

    return np.sum(squared_error_loss(true_value, predicted_value)) / true_value.shape[0]


if __name__ == "__main__":

    # Dataset (replace with any points)
    X = np.array(
         [-0.848,-0.800,-0.704,-0.632,-0.488,-0.472,-0.368,-0.336,-0.280,
         -0.200,-0.00800,-0.0840,0.0240,0.100,0.124,0.148,0.232,0.236,0.324,
         0.356,0.368,0.440,0.512,0.548,0.660,0.640,0.712,0.752,0.776,0.880,
         0.920,0.944,-0.108,-0.168,-0.720,-0.784,-0.224,-0.604,-0.740,-0.0440,
         0.388,-0.0200,0.752,0.416,-0.0800,-0.348,0.988,0.776,0.680,0.880,-0.816,
         -0.424,-0.932,0.272,-0.556,-0.568,-0.600,-0.716,-0.796,-0.880,-0.972,
         -0.916,0.816,0.892,0.956,0.980,0.988,0.992,0.00400]).reshape(-1,1)
          
    y = np.array(
        [-0.917,-0.833,-0.801,-0.665,-0.605,-0.545,-0.509,-0.433,-0.397,
        -0.281,-0.205,-0.169,-0.0531,-0.0651,0.0349,0.0829,0.0589,0.175,
        0.179,0.191,0.259,0.287,0.359,0.395,0.483,0.539,0.543,0.603,0.667,
        0.679,0.751,0.803,-0.265,-0.341,0.111,-0.113,0.547,0.791,0.551,0.347,
        0.975,0.943,-0.249,-0.769,-0.625,-0.861,-0.749,-0.945,-0.493,0.163,
        -0.469,0.0669,0.891,0.623,-0.609,-0.677,-0.721,-0.745,-0.885,-0.897,
        -0.969,-0.949,0.707,0.783,0.859,0.979,0.811,0.891,-0.137]).reshape(-1,1)

    # Ransac
    regressor = ransac_fit(X, y, X.shape[0])

    # Linear regression
    fitted = fit(X, y)

    # Set up plot
    plt.style.use("seaborn-darkgrid")
    fig, ax = plt.subplots(1, 1)
    ax.set_box_aspect(1)

    # Scatter points
    plt.scatter(X, y)

    # Create regression line
    line = np.linspace(-1, 1, num=150).reshape(-1, 1)

    # Plot and display results
    plt.plot(line, predict(line, regressor), c="peru")
    plt.show()