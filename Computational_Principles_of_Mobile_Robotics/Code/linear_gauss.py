import numpy as np
import matplotlib.pyplot as plt

# Distributions Mean and Standard deviation 
mu_one = -4
sig_one = 3
mu_two = 6
sig_two = 3

# Get distributions
distribution_one = np.random.normal(mu_one, sig_one, 10000)
distribution_two = np.random.normal(mu_two, sig_two, 10000)

# Calculate linear combination of Gaussian's
m = mu_one + sig_one**2/(sig_one**2 + sig_two**2) * (mu_two - mu_one)
s = np.sqrt(1/(1/sig_one**2 + 1/sig_two**2))

# Get distribution
distribution_three = np.random.normal(m, s, 10000)

# Arguments for histogram
a = np.hstack([distribution_one, distribution_two, distribution_three])

# Plot histogram of linear combination of Gaussian's
_ = plt.hist(a, bins='auto')  # arguments are passed to np.histogram
plt.title("Linear Combination Of Gaussian's")
plt.show()