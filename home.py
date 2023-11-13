import streamlit as st
from streamlit_option_menu import option_menu
# import snowflake.connector
import pandas as pd
from PIL import Image
import plotly.express as px
import numpy as np
# import base64
import time
# import altair as alt
import streamlit.components.v1 as components

st.set_page_config(layout='wide')

# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

#my_logo = add_logo(logo_path="./imagenes/logo.png", width=200, height=100)
#st.sidebar.image(my_logo)
#st.sidebar.header("Configuration")
#st.sidebar.subheader("Servicio Civil.")

# Set Page Header
st.header("Datos Abriertos Servicio Civil")
# Set custom CSS for hr element
st.markdown(
    """
        <style>
            hr {
                margin-top: 0.0rem;
                margin-bottom: 0.5rem;
                height: 3px;
                background-color: #333;
                border: none;
            }
        </style>
    """,
    unsafe_allow_html=True,
)

# Add horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------
df_concursos_eepp_aviso=pd.read_csv('EEPP/df_concursos_eepp_Aviso.csv',sep=";",encoding='utf-8')
df_concursos_eepp_Postulacion=pd.read_csv('EEPP/df_concursos_eepp_Postulacion en linea.csv',sep=";",encoding='utf-8')
df_concursos_eepp=pd.concat([df_concursos_eepp_aviso,df_concursos_eepp_Postulacion])

vacantes = df_concursos_eepp.agg({'Nº de Vacantes':'sum'}).reset_index()
vacantes.iat[0,1]
                           

table_scorecard = """
<div class="ui five small statistics">
      <div class="grey statistic">
        <div class="value">"""+str(vacantes.iat[0,1])+"""</div>
        <div class="grey label">Tables</div>
      </div>

</div>"""

table_scorecard += """<br><br><br><div id="mydiv" class="ui centered cards">"""
