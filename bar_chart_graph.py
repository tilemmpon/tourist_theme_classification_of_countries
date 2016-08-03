# -*- coding: utf-8 -*-
"""
Created on Wed May 18 19:08:46 2016

@author: Tilemachos Bontzorlos

This is a helper script that contains a function to create a bar chart for an
input country that shows its matching classification to the tourist themes.
"""

import numpy as np
import matplotlib.pyplot as plt

# folder that the graphs will be saves
GRAPH_FOLDER = 'countries_graphs/'

def autolabel(rects, ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%0.2f' % height, ha='center', va='bottom')


def show_country_bar_chart(country_classification, labels_list, country):
    """
    Creates a bar chart of a country matching of the tourist themes.
    
    Parameters
    ----------
    country_classification : Location of file to load.
    
    labels_list : numpy array of the sum of images classified in each theme.
    
    country : name of the country.
    """
    N = len(country_classification)
    ind = np.arange(N) # the x locations for the groups
    width = 0.35       # the width of the bars
    fig, ax = plt.subplots()
    rects = ax.bar(ind, country_classification, width, color='b')
    
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Percentage of match')
    ax.set_title('Theme match of ' + country.capitalize())
    ax.set_xticks(ind - width / 2)
    ax.set_xticklabels(labels_list, rotation=45)
    
    axes = plt.gca()
    axes.set_ylim([0, min(1, max(country_classification) + 0.2)])
    
    autolabel(rects, ax)
#    plt.show()
    plt.savefig(GRAPH_FOLDER + 'graph_' + country + '.png', 
                                                        bbox_inches='tight')