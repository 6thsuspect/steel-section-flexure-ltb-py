import streamlit as st
from i_section import calculate_i_section

st.title("I-Section Calculator")

D = st.number_input("Overall Depth (mm)", value=600.0)
B = st.number_input("Flange Width (mm)", value=250.0)
tf = st.number_input("Flange Thickness (mm)", value=20.0)
tw = st.number_input("Web Thickness (mm)", value=12.0)

if st.button("Calculate"):
    result = calculate_i_section(D, B, tf, tw)

    st.metric("Area", f"{result['area']:.2f} mm²")
    st.metric("Ix", f"{result['Ix']:.2e} mm⁴")
    st.metric("Iy", f"{result['Iy']:.2e} mm⁴")
