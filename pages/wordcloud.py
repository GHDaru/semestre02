from configparser import Interpolation
import streamlit as st
import pandas as pd
from  wordcloud import WordCloud
from thefuzz import process
import matplotlib.pyplot as plt
from neonlp import NeoNLP
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")


df_item = pd.read_pickle('database.pkl')

NLP = NeoNLP()

df_category = df_item[['id_item','nm_product','nm_item']].groupby('nm_product').agg({'id_item':'count','nm_item':' '.join})

categoria = st.text_input('Categoria', placeholder='Digite o categoria')

category_selected = process.extractOne(categoria,df_category.index)[0]

nuvem = df_category.loc[category_selected,'nm_item']

NLP.build_model([nuvem])

df = pd.DataFrame(NLP.text2vec.transform([nuvem]).toarray().T, index = NLP.text2vec.get_feature_names(), columns = ['freq'])
df = df.sort_values('freq',ascending=False).iloc[:20,:]
df.index.name = 'token'
# Create and generate a word cloud image:
wc = WordCloud(collocations=False).generate(nuvem)

fig, axs = plt.subplots(2,1,figsize=(15,15))
axs.flatten()
axs[0].set_title(category_selected)
axs[0].imshow(wc,interpolation='bilinear') 
axs[0].axis('off')
sns.set_theme(style="whitegrid")

sns.barplot(x="freq", y="token", data=df.reset_index(),
            label="Frequencia", color="b", ax=axs[1])

st.pyplot(fig, {'figsize':(10,10)})





