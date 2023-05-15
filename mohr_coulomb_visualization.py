import streamlit as st
import numpy as np
import plotly.graph_objects as go

def drucker_prager(sigma_1, sigma_2, sigma_3, A, B):
    p = (sigma_1 + sigma_2 + sigma_3) / 3.0
    q = np.sqrt(1.5 * ((sigma_1 - sigma_2)**2 + (sigma_2 - sigma_3)**2 + (sigma_3 - sigma_1)**2))
    return q - 2.0 * A * p - B * q

def main():
    st.title("Drucker-Prager Yield Surface")

    A, B = st.sidebar.slider("Material Parameters", 0.0, 1.0, (0.5, 0.5), 0.1)

    s_range = np.linspace(-100, 100, 100)
    X, Y, Z = np.meshgrid(s_range, s_range, s_range)

    F = drucker_prager(X, Y, Z, A, B)

    fig = go.Figure(data=go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=F.flatten(),
        isomin=np.min(F),
        isomax=np.max(F),
        opacity=0.1,
        surface_count=10,
    ))
    fig.update_layout(scene=dict(xaxis_title="sigma_1", yaxis_title="sigma_2", zaxis_title="sigma_3"))
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
