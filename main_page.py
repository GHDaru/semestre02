import streamlit as st
import pandas as pd
from  thefuzz import fuzz

df_item = pd.read_pickle('database.pkl')

st.set_page_config(page_title="Saneamento Ativo",
                   page_icon=":bar_chart:",
                   layout="wide")

item = st.text_input('Produto', placeholder='Digite o GTIN ou uma parte do produto')

cols = ['nm_item','gtin','nm_marca','nm_product','nm_manufatura']

df_item.loc[df_item.nm_item_norm.map(lambda x: fuzz.ratio(item, x)).sort_values(ascending = False).index[:15]][cols]


