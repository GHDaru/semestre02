import streamlit as st
import pandas as pd

@st.cache(allow_output_mutation=True)
def get_data():
    df = pd.read_pickle('itens.pkl')
    product = pd.read_pickle('product.pkl')    
    return df, product

df, product = get_data()

left, center, right = st.columns(3)

left.dataframe(df)
center.dataframe(product)


