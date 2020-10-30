# for web
import streamlit as st
import streamlit.components.v1 as components

import webbrowser

# for data
import pandas as pd
from sklearn.preprocessing import StandardScaler

# for viz
import branca.colormap as cm

# files
from p_acquisition import m_opening_final as m_op_f
from streamlit_graphics import spider_plot as s_pl
from streamlit_graphics import main_map as map
from streamlit_front import load_css as load

# ----------------------------------------------------------------------------------------------------------- SET WEB STRUCTURE

st.beta_set_page_config(layout="wide")
c1, c2 = st.beta_columns((1, 4))
load.local_css("streamlit_front/style.css")

# ----------------------------------------------------------------------------------------------------------- GLOBAL VARIABLES
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


# ---------------------------------------------------------------------------------------------------------- LOAD FINAL GDF

@st.cache(allow_output_mutation=True)
def load_data():
    bu_parcel = m_op_f.getting_final_geoframes(FINAL_DATA_PATH)
    # NOTES sobre data perdida
    # Principalmente no ha cogido El pardo, la zona de Barajas y solares vacíos dl sur
    return bu_parcel


bu_parcel = load_data()

# ---------------------------------------------------------------------------------------------------------- BASE COLORS
CUSTOM_CPal = ['#F2BF6C',
               "#F5E6CB", "#F4DCC7", "#F4D3C3", "#F3C9C0", "#F3C0BC", "#F2B6B8", "#F2ADB4", "#F1A3B1",
               "#F19AAD", "#F090A9", "#E387A6", "#D57DA3", "#C874A1", "#BB6A9E", "#AD619B", "#A05798",
               "#934E96", "#854493", "#783B90", "#6A318D", "#5D288A", "#501E88", "#421585", "#350B82"][::-1]

LinearCMAP = cm.LinearColormap(CUSTOM_CPal, index=[i / len(CUSTOM_CPal) for i in range(0, len(CUSTOM_CPal))])
CPAL = [LinearCMAP(i / len(bu_parcel)) for i in range(0, len(bu_parcel))]

st.markdown("""<style>
            .reportview-container {
                background-image: linear-gradient(#eee, #eee);
                color: #000000;
                text-align: center;
            }</style>""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------------- C1
with c1:
    st.markdown("<pre class='highlight_title'>"
                "<span class= 'bold'><span class='title'> ·UQO· </span><br>"
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

    st.markdown(f"<span class='cuerpo'>URBAN QUALITY MAP KEY<br></span>"
                f"<div class='legend' style='position: static; height: 20px;'>"
                f"<span class='bold'> - {45 * '&nbsp;'} -> {45 * '&nbsp;'} + </span><br><br>"
                "<br><span class='cuerpo'>FILTER CONTROLS<br> ~ <br>"
                "To better understand the final clusterization, you can select two <br>"
                "options: by types of urban morphology (stablish through Catastro's data <br>"
                "clusterization or Mayority Use</span>", unsafe_allow_html=True)


    # FILTERS FOR MAP IN HERE
    uses_to_show = st.selectbox(f"MAIN CLUSTER USE", ('all', 'residential', 'terciary'))  # Change this
    morpho_cluster = st.slider("URBAN MORPHOLOGY CLUSTERS", 0, 12)

    # !!!!!!!
    cluster_all = bu_parcel.groupby('cluster_build').describe()[
        ['n_BuildingUnits', 'n_Dwellings', 'nFloors_AG', 'nFloors_BG', 'area_m2c', 'area_m2p']].T

    values_to_hold = ['50%', 'min', 'max']
    tables_to_spider_plot = [pd.DataFrame(StandardScaler() \
                                          .fit_transform(cluster_all \
                                                         .iloc[cluster_all.index \
                                                         .isin([val], level=1)].T)) for val in values_to_hold]

    s_pl.make_spider_plot(table=tables_to_spider_plot[0],
                          table_min=tables_to_spider_plot[1],
                          table_max=tables_to_spider_plot[2],
                          row=morpho_cluster,
                          title=f'Group {morpho_cluster + 1}',
                          color=['#350B82', '#f63366', '#F19AAD'],
                          # CAP[0:88:20]
                          # Selected three colors because of control
                          alpha=[0.25, 0.30, 0.45])

# -----------------------------------------------------------------------------------------------------------
# SIDEBAR
st.markdown("""<style>
            .sidebar .sidebar-content {
                background-image: linear-gradient(25deg, hsla(344, 92%, 58%, 1) 5%, hsla(1, 72%, 87%, 1) 100%);
                color: white;
            }</style>""", unsafe_allow_html=True)

st.sidebar.markdown("<span class= 'bold'> CREDITS <br>~<br><br><br>"
                    "Este proyecto ha sido posible gracias al proyecto <span class='bold'>[ARTURO](arutor) </span><br> realizado por: <br></span>"
                    "300000kms<br>con<br>cotec_c<br>para<br>#Imperidble_03<br><br><br><br>", unsafe_allow_html=True)


st.sidebar.markdown(":metal:<br>Puedes obtener<br>el dataset de entrenamiento<br>"
                    "<span class='bold'> [aqui](http://www.atnight.ws/_imperdible/out/votes.json) </span>" , unsafe_allow_html=True)
st.sidebar.markdown("Última actualización:<br>30/07/2020", unsafe_allow_html=True)

st.sidebar.markdown(":metal:<br>Participa<br><br>![](http://arturo.300000kms.net/img/qr.png)<br> "
                    "la ciudad es tuya<br><br><br><br><br><br>", unsafe_allow_html=True)



if st.sidebar.button("+"):
    webbrowser.open_new_tab(GITHUB_REPOSITORY)

# -----------------------------------------------------------------------------------------------------------
# GET MAP FROM HTML DOCUMENT
if uses_to_show == 'all':   gdf_to_show = bu_parcel
elif uses_to_show == 'terciary':    filtr = (bu_parcel['currentUse'] != 'residential'); gdf_to_show = bu_parcel[filtr]
elif uses_to_show == 'residential': filtr = (bu_parcel['currentUse'] == uses_to_show); gdf_to_show = bu_parcel[filtr]
else:   print("Error in uses filter")

map.get_main_map(gfd=gdf_to_show,
                 center_location=[40.4168, -3.7038],
                 tile='CartoDB PositronNoLabels',
                 color_palette=CPAL)

with c2:
    HtmlFile = open("streamlit_graphics/map_to_render.html", 'r', encoding='utf-8')
    components.html(HtmlFile.read(),
                    width=2000,
                    height=950,
                    scrolling=False)

    my_expander = st.beta_expander(f"{296 * '/'}  WHICH URBANPARAMETERS MOST IMPACT ON QUALITY?")
    with my_expander:
        st.markdown(
            "<pre class='highlight_text'>"
            "<span class= 'bold'>"
            "<span class='bold'> Here more text and tables </span>"
            "</pre>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------------------------
