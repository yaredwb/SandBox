import streamlit as st
import numpy as np
import plotly.graph_objs as go

# Define Drucker-Prager yield function
def drucker_prager(sigma_1, sigma_2, sigma_3, c, phi):
    p = (sigma_1 + sigma_2 + sigma_3) / 3
    q = np.sqrt(1.5) * np.sqrt((sigma_1 - sigma_2)**2 + (sigma_2 - sigma_3)**2 + (sigma_3 - sigma_1)**2)
    return q - c - np.sin(phi) * p

# Define function to compute yield surface
def compute_yield_surface(c, phi):
    # Define range of sigma values
    sigma_min = -1.5 * c
    sigma_max = 500
    num_points = 50
    sigma_1_vals = np.linspace(sigma_min, sigma_max, num_points)
    sigma_2_vals = np.linspace(sigma_min, sigma_max, num_points)
    sigma_3_vals = np.linspace(sigma_min, sigma_max, num_points)

    # Compute yield surface
    yield_surface = np.zeros((num_points, num_points, num_points))
    for i, sigma_1 in enumerate(sigma_1_vals):
        for j, sigma_2 in enumerate(sigma_2_vals):
            for k, sigma_3 in enumerate(sigma_3_vals):
                yield_surface[i, j, k] = drucker_prager(sigma_1, sigma_2, sigma_3, c, phi)

    return sigma_1_vals, sigma_2_vals, sigma_3_vals, yield_surface

# Define function to plot 3D yield surface
def plot_3d_yield_surface(sigma_1_vals, sigma_2_vals, sigma_3_vals, yield_surface, c):
    fig = go.Figure(data=go.Volume(
        x=sigma_1_vals,
        y=sigma_2_vals,
        z=sigma_3_vals,
        value=yield_surface,
        isomin=-1.5 * c,
        isomax=500,
        opacity=0.1, # needs to be small to see through all surfaces
        surface_count=21, # needs to be a large number for good volume rendering
        ))
    fig.update_layout(scene=dict(
        xaxis_title='\u03C3_1',
        yaxis_title='\u03C3_2',
        zaxis_title='\u03C3_3',
    ))
    st.plotly_chart(fig)

# Define function to plot 2D yield surface projection
def plot_2d_yield_surface_projection(sigma_1_vals, sigma_2_vals, yield_surface, x_label, y_label):
    fig = go.Figure(data=go.Contour(
        x=sigma_1_vals,
        y=sigma_2_vals,
        z=yield_surface,
        contours=dict(
            coloring='lines',
            showlabels=True,
            labelfont=dict(
                family='Arial',
                size=12,
                color='black'
            )
        ),
        line=dict(
            smoothing=0.85,
            width=1,
            color='black'
        ),
        ))
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        xaxis=dict(
            tickfont=dict(
                family='Arial',
                size=12,
                color='black'
            )
        ),
        yaxis=dict(
            tickfont=dict(
                family='Arial',
                size=12,
                color='black'
            )
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        width=400,
        height=400,
    )
    st.plotly_chart(fig)


# Define main function
def main():
    # Set page layout to wide
    st.set_page_config(layout="wide")
    
    # Define sidebar widgets
    c = st.sidebar.slider('Cohesion (c)', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    phi = st.sidebar.slider('Friction angle (\u03C6)', min_value=0.0, max_value=90.0, value=30.0, step=1.0)

    # Compute yield surface
    sigma_1_vals, sigma_2_vals, sigma_3_vals, yield_surface = compute_yield_surface(c, np.deg2rad(phi))

    # Create grid layout for plots
    col1, col2 = st.columns(2)
    
    with col1:
        plot_3d_yield_surface(sigma_1_vals, sigma_2_vals, sigma_3_vals, yield_surface, c)
        plot_2d_yield_surface_projection(sigma_1_vals, sigma_2_vals, yield_surface, 'Sigma_1', 'Sigma_2')
    
    with col2:
        plot_2d_yield_surface_projection(sigma_1_vals, sigma_3_vals, yield_surface, 'Sigma_1', 'Sigma_3')
        plot_2d_yield_surface_projection(sigma_2_vals, sigma_3_vals, yield_surface, 'Sigma_2', 'Sigma_3')

    # Plot sigma_2-sigma_3 projection
    

if __name__ == '__main__':
    main()