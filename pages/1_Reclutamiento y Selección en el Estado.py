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
import plotly.express as px 
import plotly.graph_objects as go

st.set_page_config(layout='wide')

# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=200, height=100)
st.image(my_logo)

# Set Page Header
st.header("Reclutamiento y Selección de Personas en el Estado")
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

# define si se ven los ejes Y
visible_y_axis=True
    
#https://framework.digital.gob.cl/colors.html
color_line='#4A4A4A' # gris oscuro
color_line_2='#E0701E'
color_bar='#006FB3'
color_bar_2='#0A132D'
# Asignar colores de acuerdo a una paleta de colores a cada sexo
sexo_color_map = {'Mujeres': 'orange', 'Hombres': 'blue'}  # Mapeo de colores por sexo

df_concursos=pd.read_csv('ADP/df_concursos.csv',sep=';',encoding='utf-8')

unique_niveles = df_concursos['Nivel'].unique()
Nivel = pd.DataFrame({'Nivel': unique_niveles})
nuevo_registro = pd.DataFrame({'Nivel': ['Todos']})
Nivel = pd.concat([nuevo_registro, Nivel])
Nivel = Nivel.reset_index(drop=True)
Nivel = Nivel['Nivel'].tolist()

unique_ministerios = df_concursos['Ministerio'].unique()
Ministerios = pd.DataFrame({'Ministerio': unique_ministerios})
nuevo_registro = pd.DataFrame({'Ministerio': ['Todos']})
Ministerios = pd.concat([nuevo_registro, Ministerios])
Ministerios = Ministerios.reset_index(drop=True)
Ministerios = Ministerios['Ministerio'].tolist()

unique_region = df_concursos['Region'].unique()
Region = pd.DataFrame({'Region': unique_region})
nuevo_registro = pd.DataFrame({'Region': ['Todos']})
Region = pd.concat([nuevo_registro, Region])
Region = Region.reset_index(drop=True)
Region = Region['Region'].tolist()

def select_servicio(df_concursos, option_3):
    if option_3 == 'Todos':
        unique_servicio = df_concursos['Servicio'].unique()
    else:
        unique_servicio = df_concursos.query(f'Ministerio == "{option_3}"')['Servicio'].unique()
    Servicio = pd.DataFrame({'Servicio': unique_servicio})
    nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
    Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()

    return Servicio
    



with st.sidebar:
    a=st.radio('Reclutamiento y Selección: ',['Alta Dirección Pública','Empleo Público','Prácticas Chile'])

if a=='Alta Dirección Pública':
    with st.container():
       st.radio('Seleccionar: ',["Concursos", "Postulaciones","Nombramientos"],horizontal=True)
if a=='Empleo Público':
    with st.container():
       st.radio('Seleccionar: ',["Convocatorias", "Postulaciones","Seleccionados"],horizontal=True)
if a=='Prácticas Chile':
    with st.container():
       st.radio('Seleccionar: ',["Convocatorias", "Postulaciones","Seleccionados"],horizontal=True)


if a=='Alta Dirección Pública':
    with st.container():
        col1,col2,col3,col4=st.columns(4,gap="large")
        with col1:
           option_1 = st.selectbox('Nivel Jerárquico',Nivel)
        with col2:
           option_2 = st.selectbox('Región',Region)
        with col3:
           option_3 = st.selectbox('Ministerio',Ministerios)
        with col4:
           option_4 = st.selectbox('Servicio',select_servicio(df_concursos,option_3))

    # para 4 variables que toman 2 valores las combinaciones son 16

    if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos': #1
        publicaciones=df_concursos.groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1').groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1=='Todos' and option_2!='Todos' and option_3=='Todos'and option_4=='Todos': #2
        publicaciones=df_concursos[(df_concursos.Region==option_2)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Region==option_2)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1=='Todos' and option_2!='Todos' and option_3!='Todos' and option_4=='Todos': #3
        publicaciones=df_concursos[(df_concursos.Region==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()    
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Region==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()    
    if option_1=='Todos' and option_2!='Todos' and option_3!='Todos' and option_4!='Todos': #4
        publicaciones=df_concursos[(df_concursos.Region==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()    
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Region==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()    
    if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos': #5
        publicaciones=df_concursos[(df_concursos.Nivel==option_1)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1!='Todos' and option_2!='Todos' and option_3=='Todos' and option_4=='Todos': #6
        publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Region==option_2)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region==option_2)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1!='Todos' and option_2!='Todos' and option_3!='Todos' and option_4=='Todos': #7
        publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Region==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1!='Todos' and option_2!='Todos' and option_3!='Todos' and option_4!='Todos': #8
        publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Region==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos': #9
        publicaciones=df_concursos[(df_concursos.Ministerio==option_3)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos': #10
        publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4!='Todos': #11
        publicaciones=df_concursos[(df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1!='Todos' and option_2!='Todos' and option_3=='Todos' and option_4!='Todos': #12
        publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Region==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos': #13
        publicaciones=df_concursos[(df_concursos.Ministerio==option_3)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1=='Todos' and option_2!='Todos' and option_3=='Todos' and option_4!='Todos': #14
        publicaciones=df_concursos[(df_concursos.Region==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Region==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4!='Todos': #15
        publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
    if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos': #16
        publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
        Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()

    publicaciones=publicaciones.rename(columns={'CD_Concurso': 'Concursos'})
    Nominas=Nominas.rename(columns={'CD_Concurso': 'Concursos'})
    
    # grafico Convocatorias por Año
    graf1=px.bar(publicaciones,x='Year_Convocatoria',y='Concursos',title='<b>Evolución de convocatorias a cargos ADP por año</b>',color_discrete_sequence=[color_bar]).\
                 update_yaxes(visible=visible_y_axis,title_text=None).\
                      update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf1.update_layout(yaxis_tickformat='.0f')

    # grafico nominas por Año
    graf2=px.bar(Nominas,x='Year_Nomina',y='Concursos',title='<b>Evolución de nóminas enviadas a la autoridad por concursos a cargos ADP por año</b>',color_discrete_sequence=[color_bar]).\
                 update_yaxes(visible=visible_y_axis,title_text=None).\
                      update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf2.update_layout(yaxis_tickformat='.0f')
    

    with st.container():
        col1,col2=st.columns(2,gap='small')
        with col1:    
            st.plotly_chart(graf1,use_container_width=True)
        with col2:
            st.plotly_chart(graf2,use_container_width=True)
    
#----------------------------------------------------------------------------------------------------------------------
if a=='Empleo Público':
    
    df_postulaciones=pd.read_csv('EEPP/postulaciones_x_año.csv',encoding='utf-8')    
    df_postulaciones_sexo=pd.read_csv('EEPP/porcentaje_postulaciones_sexo_e.csv',sep=";")
    df_postulaciones_promedio=pd.read_csv('EEPP/Postulacion_Promedio_x_Año.csv')
    df_convocatorias=pd.read_csv('EEPP/Convocatorias_x_año.csv')
    df_vacantes=pd.read_csv('EEPP/Vacantes.csv')
    df_ConvEnLinea=pd.read_csv('EEPP/ConvEnLineaxAño.csv',sep=";")
    
    date='31 de Marzo de 2023'
    
    st.title('Estadísticas Portal Empleos Públicos')
    st.subheader(date)
    
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Evolución de Postulaciones por Año
    graf1=px.line(df_postulaciones,x='año',y='postulaciones',title='<b>Evolución de postulaciones por año</b>').\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf1.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
    graf1.update_layout(yaxis_tickformat='.0f')
    #----------------------------------------------------------------------------------------------------------------------------
    #grafico 2: Distribución de Postulaciones por Sexo
    # Create separate DataFrames for "Mujeres" and "Hombres"
    df_mujeres = df_postulaciones_sexo[df_postulaciones_sexo.Sexo == 'Mujeres']
    df_hombres = df_postulaciones_sexo[df_postulaciones_sexo.Sexo == 'Hombres']
    
    # Create the line plot using Plotly Express
    graf2 = px.line(
        title='<b>Evolución de postulaciones por año y sexo</b>',
        labels={'year': 'Año', 'Porcentaje': 'Porcentaje'},  # Customize axis labels
    )
    
    # Cambiar el formato del eje y a porcentaje (0.1 se mostrará como 10%)
    graf2.update_layout(yaxis_tickformat='.0%')
    
    # Add lines for "Mujeres" and "Hombres"
    graf2.add_trace(
        go.Scatter(x=df_mujeres['year'], y=df_mujeres['Porcentaje'], mode='lines+markers',line_shape='spline',marker=dict(size=8), name='Mujeres',line_color=sexo_color_map['Mujeres'])
    )
    graf2.add_trace(go.Scatter(x=df_hombres['year'], y=df_hombres['Porcentaje'], mode='lines+markers',line_shape='spline',marker=dict(size=8), name='Hombres',line_color=sexo_color_map['Hombres']))
    
    # Actualizar la ubicación de la leyenda
    graf2.update_layout(
        legend=dict(x=0.5, xanchor='center', y=-0.2, yanchor='top', traceorder='normal', itemsizing='trace')  # Ubicar debajo del eje x en dos columnas
    )
    
    # actualiza el eje x para nostrar todas las etiquetas de años
    graf2.update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Postulación Promedio por Año
    graf3=px.line(df_postulaciones_promedio,x='Año',y='Tasa Postulación Promedio - Concursos en Línea',title='<b>Evolución de postulaciones promedio por convocatoria por año</b>').\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    
    graf3.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Convocatorias por Año
    graf4=px.bar(df_convocatorias,x='Año',y='Convocatorias',title='<b>Evolución de convocatorias por año</b>',color_discrete_sequence=[color_bar]).\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf4.update_layout(yaxis_tickformat='.0f')
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Vacantes Concursadas por Año
    graf5=px.bar(df_vacantes,x='Año',y='Vacantes',title='<b>Evolución de vacantes ofrecidas por año</b>',color_discrete_sequence=[color_bar]).\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf5.update_layout(yaxis_tickformat='.0f')
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Porcentaje de Convocatorias en Linea por Año
    graf6=px.line(df_ConvEnLinea,x='year',y='Porcentaje Convocatorias Postulacion en Linea',title='<b>Evolución de convocatorias en línea por año</b>').\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    
    graf6.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_bar)
    graf6.update_layout(yaxis_tickformat='.0%')
    #----------------------------------------------------------------------------------------------------------------------------
    
    col1,col2,col3=st.columns(3,gap='small')
    with col1:
        st.plotly_chart(graf1,use_container_width=True)
    with col2:
        st.plotly_chart(graf2,use_container_width=True)
    with col3:
        st.plotly_chart(graf4,use_container_width=True)
    
    
    col4, col5, col6=st.columns(3,gap='small')
    with col4:
            st.plotly_chart(graf3,use_container_width=True)
    with col5:
            st.plotly_chart(graf5,use_container_width=True)
    with col6:
            st.plotly_chart(graf6,use_container_width=True)

#----------------------------------------------------------------------------------------------------------------------

if a=='Prácticas Chile':

    df_postulaciones=pd.read_csv('PCH/postulaciones_x_año.csv',encoding='utf-8')    
    df_convocatorias=pd.read_csv('PCH/Convocatorias_x_año.csv')
    #df_seleccionados=pd.read_csv('PCH/Seleccionado_x_año.csv',sep=";",encoding='utf-8')
    df_seleccionados=pd.read_excel('PCH/Seleccionado_x_año.xlsx')
    
    date='31 de Marzo de 2023'
    
    st.title('Estadísticas Portal Prácticas Chile')
    st.subheader(date)
    # markdown style
    
    st.markdown("""
    <style>
    .normal-font {
        font-size:30px;
        fott-type:roboto
    }
    </style>
    """, unsafe_allow_html=True)
    
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Evolución de Postulaciones por Año
    graf1=px.line(df_postulaciones,x='año',y='Postulaciones',title='<b>Evolución de postulaciones por año</b>').\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1)
    graf1.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
    graf1.update_layout(yaxis_tickformat='.0f')
    #----------------------------------------------------------------------------------------------------------------------------
    
    # grafico Convocatorias por Año
    graf2=px.bar(df_convocatorias,x='Año',y='Convocatorias',title='<b>Evolución de convocatorias por año</b>',color_discrete_sequence=[color_bar]).\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1)
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Seleccionados por Año
    # Create the line plot
    graf3 = px.line(df_seleccionados, x='year', y='Seleccionados', title='<b>Evolución de cantidad estudiantes seleccionados/as por año</b>')\
        .update_yaxes(visible=visible_y_axis, title_text=None)\
        .update_xaxes(title_text=None,tickmode='linear', dtick=1)
    
    graf3.update_traces(mode='lines+markers', marker=dict(size=8), line_shape='spline', line_color=color_line)
    #----------------------------------------------------------------------------------------------------------------------------
    
    
    col1,col2,col3=st.columns(3,gap='small')
    with col1:
        st.markdown('<p class="normal-font">Prácticas Chile es un programa gestionado por el Servicio Civil, que busca promover y atraer talento joven al Estado, y que permite a estudiantes de carreras universitarias y técnicas realizar sus prácticas en ministerios y servicios públicos, poniendo al servicio del país sus conocimientos y habilidades. </p>', unsafe_allow_html=True)
    with col2:
        st.plotly_chart(graf1,use_container_width=True)
    with col3:
        st.plotly_chart(graf2,use_container_width=True)
    
    
    col4, col5=st.columns(2,gap='small')
    with col4:
            st.plotly_chart(graf3,use_container_width=True)
    with col4:
            st.text('')
        
