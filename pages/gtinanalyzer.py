import streamlit as st
import pandas as pd
from  thefuzz import fuzz

from neodatabases import *

@st.cache(allow_output_mutation=True)
def get_rdw():    
    return rdw_list_azure()

rdw_list = get_rdw()

df_item = pd.read_pickle('database.pkl')

item = st.text_input('Produto', placeholder='Digite o GTIN')
col1,col2 = st.columns(2)
col1.metric("GTINS",0,0)

#cdm_list = cdm_list_azure()

bignum = st.write(rdw_list)

if item != '':
    st.write(item)

    my_bar = st.progress(0)
    df_all = pd.DataFrame()
    for ind, rdw in enumerate(rdw_list):        
        my_bar.progress((ind+1)/len(rdw_list))
        with connect_azure_sqldw() as cnx:
            SQL = f"""
            SELECT id_item, nm_item, cd_ean from {rdw}.dim_item
            where cd_ean like '%{item}%'
            """
            try:
                df_temp = pd.read_sql(SQL, cnx)
                df_temp.loc[:,'varejo'] = rdw
            except:
                pass
            #st.write(df_temp)
            df_all = df_all.append(df_temp)
            #st.write(df_all)
        df_all.to_csv(f'n{item}.csv')
        col1.metric(f"GTINS{rdw}",df_all.shape[0],df_temp.shape[0])        
    st.write(df_all)
    df_all.to_csv(f'n{item}.csv')

#st.write(cdm_list)

