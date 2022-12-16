import streamlit as st
import streamlit.components.v1 as components

st.title('Formula of Normal Distribution')

st.sidebar.header('Formula')

st.latex(r'f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}')

components.iframe('https://www.desmos.com/calculator/f4ilbq4dzo?embed')

#components.html('<iframe src="https://www.desmos.com/calculator/r3tmpguuqa?embed" width="500" height="300" style="border: 1px solid #ccc" frameborder=0></iframe>', height=300)
