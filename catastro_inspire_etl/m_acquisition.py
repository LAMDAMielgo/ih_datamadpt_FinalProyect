import re
from itertools import combinations
from itertools import chain

import pandas as pd
import numpy as np

import geopandas as gpd
import geojson

# ----------------------------------------------------------------------------------------------------------------------

RENAMING_OF_COLS = {'gml_id': 'ID',
                    'localId_part': 'ID_part',
                    'localId_PI': 'ID_pool',
                    'numberOfFloorsAboveGround': 'nFloors_AG',
                    'numberOfFloorsBelowGround': 'nFloors_BG',
                    'heightAboveGround': 'height_AG',
                    'heightBelowGround': 'height_BG',
                    'areaValue': 'area_m2p',
                    'value': 'area_m2c'}

GEOMETRY_COLS = ['geometry', 'pos']


# ------------------------------------------------------------------------------ CHECKING WHICH COLUMNS SHOULD BE PURGED

def str_forUniques(num):
    """
    Return different string depending of unique_len in checking_forUniques
    """
    if num == 0:
        return 'ALL NULLS'
    else:
        return 'Unique items'


def checking_forUniques(gdf):
    """
    input:
    output:
    """
    cols_with_one_element = []

    print(f"\n-------------------- Current Layers in {gdf.name} ------------------------")
    print(f"------------------------------------------------------------------------")

    for i, col in enumerate(gdf.columns.tolist()):
        if (col not in GEOMETRY_COLS):
            unique_len = len(gdf[str(col)].value_counts().tolist())

            if unique_len == 0:
                print(f"{i + 1}. {col}:\t\t\t{unique_len}\t{str_forUniques(unique_len)}")
            elif len(col) <= 12 and unique_len != 0:
                print(f"{i + 1}. {col}:\t\t\t\t\t{unique_len}\t{str_forUniques(unique_len)}")
            elif 12 < len(col) <= 19 and unique_len != 0:
                print(f"{i + 1}. {col}:\t\t\t\t{unique_len}\t{str_forUniques(unique_len)}")
            elif 19 < len(col) <= 28 and unique_len != 0:
                print(f"{i + 1}. {col}:\t\t\t{unique_len}\t{str_forUniques(unique_len)}")
            elif 28 < len(col) <= 36 and unique_len != 0:
                print(f"{i + 1}. {col}:\t\t{unique_len}\t{str_forUniques(unique_len)}")
            elif 36 < len(col) and unique_len != 0:
                print(f"{i + 1}. {col}:\t{unique_len}\t{str_forUniques(unique_len)}")
            else:
                pass

            if (unique_len == 1) or (unique_len == 0):
                cols_with_one_element.append(col)
            else:
                pass
        else:
            pass

    print(f"------------------------------------------------------------------------\n")
    return cols_with_one_element


def droping_DupCols(gdf, drop_cols=True):
    """

    """
    if drop_cols:
        cols_to_drop = checking_forUniques(gdf)

        print(f"-------------- Droping DUPLICATED COLUMNS in {gdf.name} ------------------")
        [print(f'{i + 1}. {col}\v') for i, col in enumerate(cols_to_drop)]  # repr without new line

        gdf.drop(cols_to_drop,
                 axis=1, inplace=True)

        print(f"-- Finished task -----------------------------------------------------\n")
    else:
        pass


# ------------------------------------------------------------------------------ SEPARATE ID_PARTS iF NEEDED

def get_part(x):
    """
    input: col withs IDs_partXX
    output: XX as int
    Get numeric item in partXX from ID_partXX
    """
    part_str = x.split('_')[1]

    if len(re.findall(r"[\.]", part_str)) != 0:
        return int(part_str.split('.')[1])
    elif len(re.findall(r"t", part_str)) != 0:
        return int(part_str.split('t')[1])
    else:
        print(f"Error. Couldnt find anything to split part to")


def get_ID(x):
    """
    input: localID_partXX
    output: localID
    """
    return x.split('_')[0]


def separate_parts(gdf, cols=['']):
    """
    If it is a geodf with ID_partXX then both parts are separated in different cols
    This is necessary to be able to join gdfs
    """
    print(f"-------------- Checking for COLS to separate in {gdf.name} --------------")
    assert type(cols) == list

    c = 0
    for col in cols:
        if (len(re.findall(r"_", gdf[col].tolist()[0])) != 0) and col in gdf.columns.tolist():

            print(f"{c + 1}. {col}\t\t Dropped")
            splited_col_name = re.split(r"_", gdf[col].tolist()[0])
            part_title = re.findall(r"\D+", splited_col_name[1])

            gdf[col + f'_{part_title[0]}'] = gdf[col].apply(get_part).astype(dtype='int64')
            gdf[col] = gdf[col].apply(get_ID)
            c += 1
        else:
            print(f"No columns to separate")

    print(f"-- Finished task -----------------------------------------------------\n")


# ------------------------------------------------------------------------------ DATETIME OPERATIONS

def get_year(strng):
    """
    Input:  string
    Output: year as string

    Note_____________________________________________________________
    Pandas requires years to be inside the bound of 1677 - 2262
    To use pandas Timestamp it is need to defined custom Stamp Period
    String operations seems easier in this case
    """
    first_w = strng.split('T')[0]
    return first_w.split('-')[0]


def getYearOfConstruction(gdf, life_span_col='beginLifespanVersion', drop_col=True):
    """
    Cleaning Datetime and datetime columns if needed
    """
    indicator_of_datetime = ['end', 'begin', 'Lifespan']

    print(f"-- Getting YEAR OF CONSTRUCTION in {gdf.name} --------------------------")

    if life_span_col in gdf.columns.tolist():
        gdf['yearOfConstruction'] = gdf[life_span_col].apply(get_year)

        if drop_col:
            print(f"Dropping col {drop_col}: \t{life_span_col}")
            gdf.drop(life_span_col, axis=1, inplace=True)

            for col in gdf.columns:
                if len(re.findall("end", col)) != 0 or \
                        len(re.findall("Lifespan", col)) != 0 or \
                        len(re.findall("begin", col)) != 0:
                    print(f"\t\t Dropping too col {drop_col}: \t{col}")
                    gdf.drop(col, axis=1, inplace=True)

        else:
            print(f"Dropping col {drop_col}: \t{life_span_col}")

    print(f"-- Finished task -----------------------------------------------------\n")


# ------------------------------------------------------------------------------ DROPPING DUPLICATED COLUMNS

def check_allTrue(gdf, col1, col2):
    """
    Esta función se usa en ....
    """
    print(f"-- Checking if PAIRS are ALL TRUE {gdf.name} ---------------")

    # hay columnas que son alturas y otras num de plantas. Con multiplicar x3 se arregla
    if False not in gdf.apply(lambda x: (x[col1] == x[col2]) or (x[col1] == 3 * x[col2]) or (3 * x[col1] == x[col2]),
                              axis=1).value_counts().index.tolist():

        print(f"All True --\n-- Droping {col2}")
        gdf.drop([col2], axis=1, inplace=True)
    else:
        print(f"Pass \tThere are inequalities between columns")


def checking_forIdenCols(gdf, drop_cols=True):
    """
    Note_____________________________________________________________
    Same unique elements are an indication that they give the same
    (or nearly) the same information, therefore to simply ddbb
    all columns that give the same info are purged
    """
    print(f"------------- Checking for SAME LEN COLS in {gdf.name} -----------------")

    # 1 // creating vars for search
    cols = [col for col in gdf.columns.tolist() if (col not in GEOMETRY_COLS)]
    len_unique_cols = [len(gdf[col].value_counts().tolist()) for col in cols]
    equal_cols, del_cols = [], []

    # 2 // creating pairs of columns that are suspect of giving the same information
    for tup_len, tup_col in zip(list(combinations(len_unique_cols, 2)), list(combinations(cols, 2))):
        if tup_len[0] == tup_len[1]:
            equal_cols.append([tup_col[0], tup_col[1]])
        else:
            pass

    # 3 // if True, drop columns that are equal, evaluating if all rows are the same
    if drop_cols and len(equal_cols) != 0:
        for pair in equal_cols:

            if pair[1] not in del_cols:
                gdf.drop(pair[1], axis=1, inplace=True)
                del_cols.append(pair.pop(1))
            else:
                pass

        print(f"1. Deleted   columns: ")  # repr without new line
        [print(f'\t\t\t{i + 1}. {col} \v') for i, col in enumerate(del_cols)];
        print('\n')

        print(f"2. Remaining columns: ")  # repr without new line
        [print(f'\t\t\t{i + 1}. {col} \v') for i, col in enumerate(list(chain.from_iterable(equal_cols)))]

    # 4 // printing columns that remain after purging
    elif len(equal_cols) == 0:
        print('List to return is empty')
    else:
        print(f"Remaining columns: \n")  # repr without new line
        [print(f'\t\t\t{i + 1}. {col} \v') for i, col in enumerate(list(chain.from_iterable(equal_cols)))]

    print(f"-- Finished task -----------------------------------------------------\n")
    return list(chain.from_iterable(equal_cols))


# ------------------------------------------------------------------------------ UNIFY ID LAYERS IF GML_ID IS DROPPED

def get_strPoint(x):
    """
    Returns last part of Cadastral ID in gml_id inside shorten_localID
    """
    return x.split('.')[-1]


def shorten_localID(gdf, cols_to_shorten=['gml_id']):
    """
    If localId is dropped in favor of gml_id
    Then, namespace part is purged of name
    """
    print(f"------- Checking for ID col to shorten in {gdf.name} -------------------")

    shorted_localID = np.vectorize(get_strPoint)
    for col_ID in cols_to_shorten:
        if col_ID in gdf.columns.tolist():
            print(f'Shortening columns: {col_ID}')
            gdf[col_ID] = shorted_localID(gdf[col_ID])

        else:
            print(f'Nothing to shorten')

    print(f"-- Finished task -----------------------------------------------------\n")


# ------------------------------------------------------------------------------ RENAME COLUMNS

def rename_cols(gdf):
    """
    If col not in dict, then pass.
    This is used to unify all geojson
    """
    print(f"--------------- Renaming cols in {gdf.name} ----------------------------")

    dict_cols_to_rename = RENAMING_OF_COLS  # dict
    cols_to_rename = [col for col in gdf.columns.tolist() if col in dict_cols_to_rename.keys()]

    gdf.rename(columns=dict_cols_to_rename, inplace=True)  # before: after

    print(f"1. Initial name: ")  # repr without new line
    [print(f'\t\t\t{i + 1}. {col} \v') for i, col in enumerate(cols_to_rename)]

    print(f"2. Final name: ")  # repr without new line
    [print(f'\t\t\t{i + 1}. {dict_cols_to_rename[col]} \v') for i, col in enumerate(cols_to_rename)]

    print(f"-- Finished task -----------------------------------------------------\n")


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------ PIPELINE COLUMNS
# ------------------------------------------------------------------------------

def rawData_infoCleaning(gdf,
                         drop_cols=True,
                         cols_to_separate=['localId', 'gml_id'],
                         datetime_col='beginLifespanVersion'):
    """
    Pipeline towards clearer data
    """
    print(f"Initiating cleaning pipeline -----------------------------------------\n")

    # -- 1 -- SEARCHING FOR COLS WITHOUT DATA IN {gdf.name} -----------------------
    droping_DupCols(gdf, drop_cols=drop_cols)
    # -- 2 -- SEARCHING FOR UNIQUE COLS {gdf.name} --------------------------------
    checking_forUniques(gdf)
    # -- 3 -- SEARCHING FOR COLS TO SEPARATE {gdf.name} ---------------------------
    separate_parts(gdf=gdf, cols=cols_to_separate)
    # -- 4 -- SEARCHING FOR DUPLICATED INFO {gdf.name} ----------------------------
    checking_forIdenCols(gdf, drop_cols=drop_cols)
    # -- 5 -- REFORMATTING DATA IN {gdf.name} -------------------------------------
    getYearOfConstruction(gdf, life_span_col=datetime_col, drop_col=drop_cols)
    shorten_localID(gdf)
    # -- 6 -- RENAMING INFORMATION IN {gdf.name} ----------------------------------
    rename_cols(gdf)

    print(f"Closing cleaning pipeline --------------------------------------------\n")
