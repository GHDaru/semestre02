import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache(allow_output_mutation=True)
def get_data():
    df = pd.read_pickle('itens.pkl')
    product = pd.read_pickle('product.pkl')    
    return df[~df.id_product.isna()], product

df, product = get_data()
df_itens_grouped = df.groupby('nm_product').agg({'id_item':'count'}).sort_values('id_item',ascending=False).reset_index()

qtde_categorias = st.slider("Quantidade de Categorias",1,20,20)


###########################
cols = st.columns([1,1,3])
#######################
cols[0].metric("#Descrições",df.shape[0])
#######################
cols[1].metric("#Categorias",df.id_product.nunique())
#######################
fig, ax = plt.subplots(figsize=(5,5))
ax.set_title("Quantidade de Descrições por Categoria")
#sns.set_theme(style="whitegrid")
sns.barplot(y="nm_product", x="id_item", data=df_itens_grouped.head(int(qtde_categorias)),
            label="Frequencia", ax=ax)

cols[2].pyplot(fig)
#######################
