import numpy as np
from scipy.special import erf
import matplotlib.pyplot as plt

# Material properties
k_grout = 1.5       # Thermal conductivity (W/m·K)
rho_grout = 1269    # Density (kg/m³)
cp_grout = 3000     # Specific heat capacity (J/kg·K)
alpha_grout = k_grout / (rho_grout * cp_grout)  # Thermal diffusivity (m²/s)

# Initial and boundary conditions
T_initial = -10.0    # Initial temperature (°C)
T_infinity = 8.0    # Ambient temperature at surface (°C)

# Positions to evaluate (distance from surface, m)
x_positions = np.linspace(0, 0.2, 100)  # Grout layer thickness is 0.2 m

# Times to evaluate (s)
times = [1 * 3600, 6 * 3600, 12 * 3600, 24 * 3600, 48 * 3600]  # Times in seconds

# Function to calculate temperature at position x and time t
def temperature_semi_infinite(T_i, T_inf, x, t, alpha):
    return T_inf + (T_i - T_inf) * erf(x / (2 * np.sqrt(alpha * t)))

# Plot temperature profiles at different times
plt.figure(figsize=(8, 6))

for t in times:
    T_x = temperature_semi_infinite(T_initial, T_infinity, x_positions, t, alpha_grout)
    plt.plot(x_positions, T_x, label=f'Time = {t/3600} hr')

plt.xlabel('Distance from Grout-Rock Interface (m)')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Distribution in Grout Layer Over Time')
plt.legend()
plt.grid(True)
plt.gca().invert_xaxis()  # Invert x-axis to show surface on the left
plt.show()
