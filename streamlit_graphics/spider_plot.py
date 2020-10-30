from math import pi
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

sns.set_style("darkgrid", {"axes.facecolor": ".9"})

def make_spider_plot(table, table_min, table_max, row, title, color, alpha):
    """
    Make custom polar plot for every label
    """
    # number of variable
    categories = table.columns.tolist()
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # first value to close the circular graph

    ########
    fig = plt.figure(figsize=(5, 5))
    ax = plt.subplot(1, 1, 1, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='white', size=0)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([10, 20, 30], ["10", "20", "30"], color="grey", size=7)
    plt.ylim(-2.5, 5.00)

    #######
    # We are going to plot the first line of the data frame.
    values = table.loc[row].values.flatten().tolist();
    values += values[:1]  # first value to close the circular graph

    values_min = table_min.loc[row].values.flatten().tolist();
    values_min += values[:1]
    values_max = table_max.loc[row].values.flatten().tolist();
    values_max += values[:1]

    # Plot data
    ax.fill(angles, values_min, color=color[0], alpha=alpha[0], linewidth=0.)  # Fill area
    ax.fill(angles, values, color=color[1], alpha=alpha[1], linewidth=0.)  # Fill area
    ax.fill(angles, values_max, color=color[1], alpha=alpha[2], linewidth=0.)  # Fill area

    #######
    plt.subplots_adjust(hspace=5)
    fig.patch.set_visible(False)
    st.pyplot(fig)