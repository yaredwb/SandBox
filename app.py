import streamlit as st

st.title("My First Streamlit Web App")
st.write("Welcome to this simple Streamlit web application!")

import pandas as pd

df = pd.DataFrame({
    'Column 1': [1, 2, 3, 4],
    'Column 2': [10, 20, 30, 40]
})
st.dataframe(df)

import pydeck as pdk

chart = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
)
st.pydeck_chart(chart)