import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

today = date.today()
#sns.set_style('whitegrid')
style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1
dpi = 1000
plt.rcParams['font.size'] = 13
#plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
plt.rcParams['axes.titlesize'] = plt.rcParams['font.size']
plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['figure.figsize'] = 8, 8



st.sidebar.markdown('# COVID-19 Data and Reporting')
st.sidebar.markdown('## **EpiCenter for Disease Dynamics**') 
st.sidebar.markdown('**School of Veterinary Medicine   UC Davis**') 
st.sidebar.markdown("## Key COVID-19 Metrics")
st.sidebar.markdown("COVID-Local provides basic key metrics against which to assess pandemic response and progress toward reopening. See more at https://www.covidlocal.org/metrics/")
st.sidebar.markdown('For additional information  please contact *epicenter@ucdavis.edu*  https://ohi.vetmed.ucdavis.edu/centers/epicenter-disease-dynamics')
st.markdown('## Select counties of interest')
