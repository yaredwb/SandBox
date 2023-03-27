import numpy as np
from scipy.optimize import leastsq

# Define the residuals function
def residuals(params, sigma, theta, phi, z):
    gamma, S1, S2, alpha1, alpha2, lamda, eta = params
    f = gamma * z * np.cos(theta)**2 + 0.5 * np.sin(theta)**2 * (S1 + S2 + (alpha1 + alpha2) * z + (S1 - S2) * np.cos(2*(phi - lamda)) + (alpha1 - alpha2) * z * np.cos(2*(phi - (lamda + eta))))
    return f - sigma**n

# Generate some example measurement data
n = 2
N = 10
sigma_mean = np.random.uniform(0, 1, N)
sigma_std = np.random.uniform(0.01, 0.1, N)
sigma = np.random.normal(sigma_mean, sigma_std)
theta_mean = np.random.uniform(0, np.pi/2, N)
theta_std = np.random.uniform(0.01, 0.1, N)
theta = np.random.normal(theta_mean, theta_std)
phi_mean = np.random.uniform(0, np.pi/2, N)
phi_std = np.random.uniform(0.01, 0.1, N)
phi = np.random.normal(phi_mean, phi_std)
z_mean = np.random.uniform(0, 1, N)
z_std = np.random.uniform(0.01, 0.1, N)
z = np.random.normal(z_mean, z_std)

# Choose an initial guess for the unknown parameters
params0 = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])

# Use the least squares method to find the values of the unknown parameters
params_fit, success = leastsq(residuals, params0, args=(sigma, theta, phi, z))

# Check the optimization result
if success:
    print("Optimization successful!")
else:
    print("Optimization failed!")

# Calculate the Jacobian matrix of the residuals function
def jac(params, sigma, theta, phi, z):
    gamma, S1, S2, alpha1, alpha2, lamda, eta = params
    J = np.zeros((len(sigma), len(params)))
    J[:, 0] = z * np.cos(theta)**2
    J[:, 1] = 0.5 * np.sin(theta)**2
    J[:, 2] = 0.5 * np.sin(theta)**2
    J[:, 3] = z * np.cos(2*(phi - lamda))
    J[:, 4] = z * np.cos(2*(phi - (lamda + eta)))
    J[:, 5] = -np.sin(2*(phi - lamda)) * np.sin(theta)**2
    J[:, 6] = -np.sin(2*(phi - (lamda + eta))) * np.sin(theta)**2
    return J

J = jac(params_fit, sigma, theta, phi, z)

# Calculate the standard deviation of the unknown parameters using the covariance matrix
cov_mat = np.linalg.inv(np.dot(J.T, J))
params_std = np.sqrt(np.diag(cov_mat))

# Print the values of the unknown parameters and their standard deviations
print("Unknown parameters:")
print("gamma =", params_fit[0], "+/-", params_std[0])
print("S1 =", params_fit[1], "+/-", params_std[1])
print("S2 =", params_fit[2], "+/-", params_std[2])
print("alpha1 =", params_fit[3], "+/-", params_std[3])
print("alpha2 =", params_fit[4], "+/-", params_std[4])
print("lamda =", params_fit[5], "+/-", params_std[5])
print("eta =", params_fit[6], "+/-", params_std[6])

# Print the mean and standard deviation values of the residuals of the fit and the unknown parameters
residuals_fit = residuals(params_fit, sigma, theta, phi, z)
print("Residuals of the fit:")
print("Mean =", np.mean(residuals_fit))
