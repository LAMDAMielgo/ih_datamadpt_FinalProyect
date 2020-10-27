# Dependencies
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import re

from p_acquisition import m_opening_final as m_op_f
from load_css import local_css
#----------------------------------------------------------------------------------------------------------- GLOBAL VARIABLES

CLEAN_DATA_PATH = 'data/clean'  # three files (there should be only two: catastro and arturo). DIFFERENT SHAPES
LABLD_DATA_PATH = 'data/labelled'  # two files: clusters from catastro and clusters from all data. DIFFERENT SHAPES
MODEL_DATA_PATH = 'data/modelbase'  # one file: data with all columns from arturo and catastro. SHAPE 90.5% of Catastro Data

NAMES_DICT = {

    'cadastralparcel.geojson': 'CAD_PA',
    'otherconstruction.geojson': 'O_CONS',
    'buildingpart.geojson': 'P_BU',
    'building.geojson': 'BU',
    'cadastralzoning.geojson': 'CAD_ZO',
    '28900.geojson': 'MAD',

    'building_points.geojson': 'BU_POINTS',
    'arturo.geojson': 'ARTURO_DF',
    'building_polygs.geojson': 'BU_POLYGONS',
    'building_parcls.geojson': 'BU_PARCELS',
}

MADRID_EPSG = 25830
STATE = 42

#-----------------------------------------------------------------------------------------------------------

@st.cache(allow_output_mutation=True)
def load_data():
    # OPENING LABELS FROM CLUSTERS
    all_labels, catastro_labels = m_op_f.opening_csv_in_path(LABLD_DATA_PATH)
    # OPENING GEO DATA FRAMES FOR THE THREE TYPES OF GEOMETRIES
    bu_points, bu_polygs, bu_parcel = m_op_f.getting_final_geoframes(CLEAN_DATA_PATH, MODEL_DATA_PATH,
                                                                     gdfs_labels=[all_labels, catastro_labels])
    # NOTES sobre data perdida
    # Principalmente no ha cogido El pardo, la zona de Barajas y solares vacíos dl sur
    return bu_points, bu_polygs, bu_parcel


local_css("style.css")
#sbu_points, bu_polygs, bu_parcel = load_data()

#-----------------------------------------------------------------------------------------------------------
# all sidebar text
# st.sidebar.markdown("![](https://wallpaperaccess.com/full/55235.jpg)") image for title
st.sidebar.title("\t\t\tURBAN  PAISAGE ")
st.sidebar.title("\t\t\tQUALITY INDEX")
st.sidebar.title("----------------------------")
st.sidebar.markdown("")


st.sidebar.markdown("------------------------------------------------------")
st.sidebar.markdown("Why measure this?")
st.sidebar.markdown("La ")
slider_01 = st.sidebar.slider("Sidebar to filter layers", 0, 10)

t = "<div>Hello there my <span class='highlight blue'>name <span class='bold'>yo</span> </span> is <span class='highlight red'>Fanilo <span class='bold'>Name</span></span></div>"
st.markdown(t, unsafe_allow_html=True)

st.sidebar.markdown("------------------------------------------------------")
st.sidebar.markdown(":: Puedes obtener el [dataset de entrenamiento](http://www.atnight.ws/_imperdible/out/votes.json) como parte del experiemento de ![](http://arturo.300000kms.net/img/logos/300000kms.png) con ![](http://arturo.300000kms.net/img/logos/cotec_t.png) para #Imperidble_03")
st.sidebar.markdown("Última actualización:  30/07/2020") # bold
st.sidebar.markdown(":metal:  Participa ![](http://arturo.300000kms.net/img/qr.png) la ciudad es tuya")



#-----------------------------------------------------------------------------------------------------------
st.markdown("/////////////////////////////////////////////////////////////////////////////////////////")
st.markdown("¿CÓMO SON LAS CONJUNTOS MÁS HABITABLES?")

# main vizualization: Madrid
fig, ax = plt.subplots()

# All layers
"""
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
bu_parcel.plot(column = 'cluster_all', cmap = 'flare', figsize = (25,25),
               legend = False, edgecolor="face", linewidth=0.01, ax = ax)
ax.set_xticks([]); ax.set_yticks([])

st.pyplot(fig)"""

st.markdown("/////////////////////////////////////////////////////////////////////////////////////////")
st.markdown("¿CÓMO SON LAS CONJUNTOS MÁS HABITABLES?")



