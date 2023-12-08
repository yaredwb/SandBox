import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title of the app
st.title("Trigonometric Function Plotter")

# Dropdown menu for selecting a trigonometric function
option = st.selectbox(
    'Which trigonometric function would you like to plot?',
    ('Sine', 'Cosine', 'Tangent'))

# Generate a range of x values
x = np.linspace(-2 * np.pi, 2 * np.pi, 400)

# Plot the selected trigonometric function
if option == 'Sine':
    y = np.sin(x)
    plt.title("Sine Function")
elif option == 'Cosine':
    y = np.cos(x)
    plt.title("Cosine Function")
else:
    y = np.tan(x)
    plt.title("Tangent Function")

# Handle the discontinuity in the tangent function
if option == 'Tangent':
    plt.ylim(-10, 10)

# Plot the function
plt.figure(figsize=(3, 1.5))
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel(option)
plt.grid(True, which='both', linestyle='--')
st.pyplot(plt, clear_figure=True, use_container_width=False)
