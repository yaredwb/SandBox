import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title of the app
st.title("Data Analysis App")

# Sidebar for data generation settings
st.sidebar.header("Data Settings")
num_rows = st.sidebar.slider("Number of rows:", min_value=50, max_value=500, value=100)
num_cols = st.sidebar.slider("Number of columns:", min_value=1, max_value=10, value=9)

# Generate random data
df = pd.DataFrame(np.random.randn(num_rows, num_cols), columns=[f"Column {i+1}" for i in range(num_cols)])

# Display the dataframe in the app
st.write("### Generated Data Preview:")
st.dataframe(df)

# Sidebar for column selection for histogram
column_to_plot = st.sidebar.selectbox("Choose a column to plot:", df.columns)

# Plot histogram
st.write(f"### Histogram of {column_to_plot}")
fig, ax = plt.subplots()
ax.hist(df[column_to_plot], bins=30, edgecolor='black')
ax.set_xlabel(column_to_plot)
ax.set_ylabel('Frequency')
st.pyplot(fig)