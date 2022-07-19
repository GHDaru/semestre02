import streamlit as st
import pandas as pd

file = st.file_uploader("Arquivo")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:     
     # Can be used wherever a "file-like" object is accepted:
     dataframe = pd.read_csv(uploaded_file)
     st.write(dataframe)
     
     dataframe.to_csv('temp.csv', index=False)     


