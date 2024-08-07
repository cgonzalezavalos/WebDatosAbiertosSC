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
import pyarrow.parquet as pq

st.set_page_config(layout='wide',
                   initial_sidebar_state="collapsed")                                #collapsed expanded


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

remote_css(
    "https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css")
local_css("style.css")

# This function sets the logo and company name inside the sidebar

# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=150, height=150)
st.image(my_logo)


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

# Set Page Header
st.title("Datos Abiertos Servicio Civil")

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
tiempo_actualizacion=3600

@st.cache_data(ttl=tiempo_actualizacion)
def df_conc_eepp():
    df_conc_ep = pd.read_parquet('datos/df_concursos_eepp.parquet')
    return df_conc_ep

@st.cache_data(ttl=tiempo_actualizacion)
def df_conc_adp():
    df_conc = pd.read_parquet('datos/df_concursos.parquet')
    return df_conc


@st.cache_data(ttl=tiempo_actualizacion)
def df_selec_pch():
    df_sel_pch = pq.read_table('datos/df_postulaciones_pch.parquet')
    df_sel_pch=df_sel_pch.drop_columns(['FechaNacimiento', 'FechaPostulacion'])
    df_sel_pch = df_sel_pch.to_pandas(timestamp_as_object=False)
    return df_sel_pch

@st.cache_data(ttl=tiempo_actualizacion)
def df_selec_dee():
    #df_sel_dee = pd.read_csv('datos/tblConcursos.csv', sep=';')
    df_sel_dee=pd.read_parquet('datos/df_concursos_dee.parquet')
    return df_sel_dee






df_concursos_eepp=df_conc_eepp()
df_concursos_adp=df_conc_adp()
df_seleccionados_pch=df_selec_pch()
df_seleccionados_deem=df_selec_dee()

vacantes = df_concursos_eepp['Vacantes'].sum()
postulaciones=df_concursos_eepp['Total_Postulaciones'].sum()
concursos_adp=df_concursos_adp.CD_Concurso.count()
nombrados_adp=df_concursos_adp.query("Estado=='Nombrado'").CD_Concurso.count()

# Realiza el conteo de valores en la columna 'EstadoPost'
seleccionados_pch = df_seleccionados_pch['EstadoPost'].value_counts().reset_index()
seleccionados_pch = seleccionados_pch.loc[seleccionados_pch['EstadoPost'] == "Seleccionado", 'count'].values[0]

seleccionados_deem=df_seleccionados_deem[df_seleccionados_deem['Estado'] == "Nombrado"].agg('count').values[0]
sel_dee = (df_seleccionados_deem['idConcurso'][df_seleccionados_deem['Estado'] == 'Nombrado']).count()

st.write(sel_dee)

with st.container():
    col1,col2,col3,col4,col5,col6=st.columns(6,gap='small')
    with col1:
        #image = Image.open('imagenes/job_application.jpg')
        image=add_logo(logo_path="./imagenes/job_application.jpg", width=150, height=150)
        st.image(image)
        valor_col1=f"{postulaciones:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col1}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total postulaciones portal Empleos Públicos</h2>", unsafe_allow_html=True)
    with col2:
        #image = Image.open('imagenes/job_offer.png')
        image=add_logo(logo_path="./imagenes/job_offer.png", width=150, height=150)
        st.image(image)
        #valor_col2=f"{vacantes.iat[0,1]:,}".replace(",", ".")
        valor_col2=f"{vacantes:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col2}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total vacantes ofrecidas portal Empleos Públicos</h2>", unsafe_allow_html=True)
    with col3:
        #image = Image.open('imagenes/mannager_selection.png')
        image=add_logo(logo_path="./imagenes/mannager_selection.png", width=150, height=150)
        st.image(image)
        valor_col3=f"{concursos_adp:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col3}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total concursos de Alta Dirección Pública</h2>", unsafe_allow_html=True)
    with col4:
        #image = Image.open('imagenes/adp_nombrado.PNG')
        image=add_logo(logo_path="./imagenes/adp_nombrado.PNG", width=150, height=150)
        st.image(image)
        valor_col4=f"{nombrados_adp:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col4}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total nombramientos en Alta Dirección Pública</h2>", unsafe_allow_html=True)
    with col5:
        #image = Image.open('imagenes/Directores.png')
        image=add_logo(logo_path="./imagenes/Directores.png", width=150, height=150)
        st.image(image)
        valor_col5=f"{seleccionados_pch:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col5}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Personas seleccionadas en Prácticas Chile</h2>", unsafe_allow_html=True)
    with col6:
        #image = Image.open('imagenes/trainee.PNG')
        image=add_logo(logo_path="./imagenes/trainee.PNG", width=150, height=150)
        st.image(image)
        valor_col6=f"{seleccionados_deem:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col6}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Personas seleccionadas en Directores para Chile</h2>", unsafe_allow_html=True)


#st.dataframe(df_seleccionados_pch.head(10))



with st.container():
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("<hr>", unsafe_allow_html=True)
    texto_home="""El Servicio civil pone a disposición de la ciuaddanía esta plataforma de Datos Abiertos, como una forma de rendir cuentas a la sociedad civil y generar un diálogo horizontal y transparente."""
    st.markdown(f"<h1 style='text-align: center; '><strong>{texto_home}</strong></h1>", unsafe_allow_html=True) #color: grey;

#image = Image.open('./imagenes/datosabiertos.png')
#st.image(image, width=1000)
with st.container():
    texto_foot_1="""¿Qué son los Datos Abiertos?"""
    texto_foot_2="""Los datos abiertos son datos que pueden ser utilizados, reutilizados y redistribuidos libremente por cualquier persona, y que se encuentran sujetos, cuando más, al requerimiento de atribución y de compartirse de la misma manera en que aparecen. """
    texto_foot_3="""¿Por qué son importantes?"""
    texto_foot_4="""Los datos abiertos son importantes porque permiten a la ciudadanía acceder a información pública de forma libre y gratuita, y a los organismos públicos mejorar la calidad de los servicios que prestan, la toma de decisiones y la rendición de cuentas."""
    with st.expander(texto_foot_1):
        st.write(texto_foot_2, unsafe_allow_html=False)
        st.write(texto_foot_3, unsafe_allow_html=False)
        st.write(texto_foot_4, unsafe_allow_html=False)     
    texto_foot_5="""Morandé 115, P.9, Santiago, Chile. Fono(56 2) 2873 4400"""
    st.caption(texto_foot_5, unsafe_allow_html=False, help=None)  



    
    

