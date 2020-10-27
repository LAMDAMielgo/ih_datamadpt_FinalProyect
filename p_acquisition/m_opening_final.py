# for data
from os import listdir
from os.path import isfile, join
from functools import reduce
import re
import streamlit as st
import pandas as pd
import numpy as np

# for geospatial
import geopandas as gpd
import geojson

import seaborn as sns



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

#----------------------------------------------------------------------------------------------------------- GLOBAL VARIABLES

def opening_csv_in_path(path):
    """
    INPUT:   path where the csv files are saved
    OUTPUT:  a dataframe for each file loaded in memory
    """
    ends = '.csv'  # type of file to open
    print(f"\n-- Opening {ends} in {path}---------------------------------------------------------------")
    files = [f for f in listdir(LABLD_DATA_PATH) if isfile(join(LABLD_DATA_PATH, f))]

    for file in files:
        if file.endswith(ends):
            opened_file = pd.read_csv(f"{path}/{file}", index_col='ID')
            print(
                f"\t{file.split('.')[0]} \tOPENED \t\tMemory Usage:\t{np.round(opened_file.memory_usage().sum() / 1000000, 2)} Mb \tShape: {opened_file.shape}")
            yield opened_file


def adding_labels(gdf, labels):
    """
    This definition adds the labels at the end of the GeoDataFrame
    input: gdf.shape(rows, cols)
    output: gdf.shape(rows, cols + catastro labels + all_labels)
    """
    # catastro labels -- 13 labels for only catastro information
    # all_labels ------- 87 labels for all information available (arturo + catastro)
    list_of_gdfs = [gdf] + labels
    return reduce(lambda left, right: pd.merge(left, right, on='ID', how='left'), list_of_gdfs)


def getting_final_geoframes(geometries_path, dataframe_path, gdfs_labels):
    """
    INPUT:
    OUTPUT:
    """
    # List with necessary files
    all_data_file = [f for f in listdir(dataframe_path) if isfile(join(dataframe_path, f)) and re.findall('all_data',
                                                                                                          f)]  # change as merging_all_data final file is name
    print(
        f"\n-- Opening {len(all_data_file)} files in {dataframe_path} --------------------------------------------------------------")

    # Constructing a GeoDataFrame since it does not work like pandas
    all_cols_df = gpd.read_file(f"{dataframe_path}/{all_data_file[0]}").set_index('ID').set_crs(epsg=MADRID_EPSG,
                                                                                                allow_override=True)
    df_cols = [col for col in all_cols_df.columns if col != 'geometry']
    print(
        f"\t{all_data_file[0].split('.')[0]} \tOPENED \t\tMemory Usage:\t{np.round(all_cols_df.memory_usage().sum() / 1000000, 2)} Mb \t\tShape: {all_cols_df.shape}")

    geom_bu_files = [f for f in listdir(geometries_path) if isfile(join(geometries_path, f)) and re.findall('building',
                                                                                                            f)]  # only retrieves files names with 'building' in them
    print(
        f"\n-- Opening {len(geom_bu_files)} files in {geometries_path} --------------------------------------------------------------")

    for file in geom_bu_files:
        # Constructing a GeoDatFrame and giving them a name
        # Note: yield directly from gpd.read_files doesnt work like in pandas, returns constructor
        geom_file = gpd.read_file(f"{CLEAN_DATA_PATH}/{file}").set_index('ID')
        geom_file.name = NAMES_DICT[file]

        # Final GeoDataFrame to retrieve
        geom_file = gpd.GeoDataFrame(all_cols_df[df_cols],
                                     geometry=geom_file['geometry']).set_crs(epsg=MADRID_EPSG, allow_override=True)
        # revise with def adding_labels
        geom_file = adding_labels(gdf=geom_file,
                                  labels=gdfs_labels)
        print(
            f"\t{file.split('.')[0]} \tOPENED \tMemory Usage:\t{np.round(geom_file.memory_usage().sum() / 1000000, 2)} Mb \t\tShape: {geom_file.shape}")
        yield geom_file