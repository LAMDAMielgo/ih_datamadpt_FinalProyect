# for web
import streamlit as st
import streamlit.components.v1 as components
import webbrowser

#for data
import branca.colormap as cm
from sklearn.preprocessing import StandardScaler
import pandas as pd

# files
from p_acquisition import m_opening_final as m_op_f
from streamlit_graphics import spider_plot as s_pl
from load_css import local_css
#----------------------------------------------------------------------------------------------------------- SET WEB STRUCTURE

st.beta_set_page_config(layout="wide")
c1, c2 = st.beta_columns((1, 4))
local_css("style.css")

#----------------------------------------------------------------------------------------------------------- GLOBAL VARIABLES
GITHUB_REPOSITORY = 'https://github.com/LAMDAMielgo/ih_datamadpt_FinalProyect'

CLEAN_DATA_PATH = 'data/clean'  # three files (there should be only two: catastro and arturo). DIFFERENT SHAPES
LABLD_DATA_PATH = 'data/labelled'  # two files: clusters from catastro and clusters from all data. DIFFERENT SHAPES
MODEL_DATA_PATH = 'data/modelbase'  # one file: data with all columns from arturo and catastro. SHAPE 90.5% of Catastro Data
FINAL_DATA_PATH = 'data/final_streamlit'

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

    'bu_parcel_epsg3857.geojson': 'BU_PARCELS',
}

MADRID_EPSG = 25830
STATE = 42


#---------------------------------------------------------------------------------------------------------- LOAD FINAL GDF

@st.cache(allow_output_mutation=True)
def load_data():
    bu_parcel = m_op_f.getting_final_geoframes(FINAL_DATA_PATH)
    # NOTES sobre data perdida
    # Principalmente no ha cogido El pardo, la zona de Barajas y solares vacíos dl sur
    return bu_parcel

bu_parcel = load_data()

#---------------------------------------------------------------------------------------------------------- BASE COLORS

LinearCMAP = cm.LinearColormap(CUSTOM_CPal, index = [i/len(CUSTOM_CPal) for i in range(0, len(CUSTOM_CPal))])
CPAL = [LinearCMAP(i/len(bu_parcel)) for i in range(0, len(bu_parcel))]

CUSTOM_CPal = ['#F2BF6C',
              "#F5E6CB","#F4DCC7","#F4D3C3","#F3C9C0","#F3C0BC","#F2B6B8","#F2ADB4","#F1A3B1",
              "#F19AAD","#F090A9","#E387A6","#D57DA3","#C874A1","#BB6A9E","#AD619B","#A05798",
              "#934E96","#854493","#783B90","#6A318D","#5D288A","#501E88","#421585","#350B82"][::-1]

st.markdown("""<style>
            .reportview-container {
                background-image: linear-gradient(#eee, #eee);
                color: #000000;
                text-align: center;
            }</style>""", unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------------- C1
with c1:

    st.markdown("<pre class='highlight_title'><span class= 'bold'><span class='title'> U Q O </span><br>"
                "<span class= 'subtitle'> urban  quality  operational  tool <br>"
                "~</span></span><br>"
                "<span class= 'subtitle'> likeability of urban morphology based <br> on an <span class= 'bold'>open citizen survey</span></span></pre>"
                , unsafe_allow_html=True)

    st.markdown("<pre class='highlight_text'>"
                "<span class='cuerpo'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, <br>"
                "sed do eiusmod tempor incididunt ut labore et dolore magna <br>"
                "aliqua. Ut enim ad minim veniam, quis nostrud exercitation <br>"
                "ullamco laboris nisi ut aliquip ex ea commodo consequat. <br>"
                "Duis aute irure dolor in reprehenderit in voluptate velit <br>"
                "esse cillum dolore eu fugiat nulla pariatur. Excepteur <br>"
                "sint occaecat cupidatat non proident, sunt in culpa qui <br>"
                "officia deserunt mollit anim id est laborum</span></span></pre>"
                , unsafe_allow_html=True)

    st.markdown("<div class='legend' style='position: relative; width: 500px; height: 20px;'>", unsafe_allow_html=True)

    st.write(LinearCMAP) # this doesnt work, add a html gradient here

    "Filter Controls"
    cluster_value = st.slider("Sidebar to filter layers", 0, 10)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    row = 2
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    cluster_all = bu_parcel.groupby('cluster_build').describe()[
        ['n_BuildingUnits', 'n_Dwellings', 'nFloors_AG', 'nFloors_BG', 'area_m2c', 'area_m2p']].T

    values_to_hold = ['50%', 'min', 'max']
    tables_to_spider_plot = [
        pd.DataFrame(StandardScaler().fit_transform(cluster_all.iloc[cluster_all.index.isin([val], level=1)].T)) for val
        in values_to_hold]

    s_pl.make_spider_plot(table=tables_to_spider_plot[0],
                     table_min=tables_to_spider_plot[1],
                     table_max=tables_to_spider_plot[2],
                     row = cluster_value,
                     title=f'Group {cluster_value + 1}',
                     color=color_palette[0:88:20],
                     alpha=[0.25, 0.5, 0.75])

    if st.button("+"):
        webbrowser.open_new_tab(GITHUB_REPOSITORY)

#-----------------------------------------------------------------------------------------------------------

st.sidebar.markdown('Credits Here')

with c2:

    HtmlFile = open("notebooks/tryout.html", 'r', encoding='utf-8')
    components.html(HtmlFile.read(),
                    width=2000,
                    height=950,
                    scrolling=False)

    my_expander = st.beta_expander("//////////////////////////////////////////////////////////////////////")
    with my_expander:
        st.markdown(
            "<pre class='highlight_text'>"
                "<span class= 'bold'>"
                    "<span class='subtitle'> WHICH PARAMETERS MOST IMPACT ON QUAKITY? </span>"
            "</pre>", unsafe_allow_html=True)

#-----------------------------------------------------------------------------------------------------------
