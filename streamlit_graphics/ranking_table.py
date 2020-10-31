import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from plotly.subplots import make_subplots

import pandas as pd

#----------------------------------------------------------------------------------------------------

MAP_SAVE_PATH = 'streamlit_graphics/'

def  ranking_table(gdf, col_to_filtr, linearcolormap):
    """
    gdf:
    col_to_filtr:
    """
    print(
        f"\n-- Rendering Main Table ----------------------------------------------------------------------------------------------")
    # corr table
    corr_matrix = gdf.corr()['value'].sort_values(ascending = False)
    cols_for_table = [col for col in corr_matrix.index.tolist()[2:] if col != 'cluster_all']

    # tables to show table
    rank_by_value_df = pd.DataFrame(corr_matrix[cols_for_table].where(lambda x : x>0).dropna())
    df_to_box_plot = pd.DataFrame(StandardScaler().fit_transform(gdf.groupby(col_to_filtr).mean()[rank_by_value_df.T.columns]),
                                 columns = rank_by_value_df.T.columns)
    CPAL_rank = [linearcolormap(i / len(rank_by_value_df)) for i in range(0, len(rank_by_value_df))]
    ###########################################################


    fig = make_subplots(rows = 2, cols = 1)

    # fig 1
    for i,col in enumerate(df_to_box_plot.columns.tolist()):
        fig.add_trace(go.Box(y = df_to_box_plot[col], name = f"{col}", marker_color = CPAL_rank[i]),
                      row = 1, col = 1)

    fig.add_trace(go.Bar(x = rank_by_value_df.index,
                         y = rank_by_value_df['value'],
                         marker_color = CPAL_rank),
                  row = 2, col = 1)

    fig.layout.update(showlegend=False)
    fig.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',})

    fig.update_yaxes(visible=False, showticklabels=False, row = 1, col = 1)
    fig.update_xaxes(visible=False, showticklabels=False, row = 1, col = 1)
    fig.update_xaxes(tickangle=270,
                     tickfont=dict(family='Courier New, monospace', color='black', size=16),
                     row = 2, col = 1)
    fig.update_layout(width=2200, height= 850)
    print(
        f"\t RANK TABLE \tRENDERED --------------------------------------------------------------------------------")
    fig.write_html(f'{MAP_SAVE_PATH}ranking_fig.html')