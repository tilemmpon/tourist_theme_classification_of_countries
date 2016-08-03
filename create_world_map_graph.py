# -*- coding: utf-8 -*-
"""
Created on Thu May 19 21:57:43 2016

@author: Tilemachos Bontzorlos

This is a program that creates a world map where each tested country is colored
to its best matching tourist theme and the rest countries are colored grey.

REQUIREMENTS: cartopy, iso3166 python packages must be installed.
"""

#==============================================================================
# Solution includes code adaptation from:
# http://gis.stackexchange.com/questions/88209/python-mapping-in-matplotlib-cartopy-color-one-country
# http://stackoverflow.com/questions/35423366/change-map-boundary-color-in-cartopy
#==============================================================================

import iso3166
import matplotlib.pyplot as plt
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import numpy as np
import colorsys
import matplotlib.patches as mpatches
import create_images_feature_matrices as create_matrices

#==============================================================================
# code from: http://stackoverflow.com/questions/470690/how-to-automatically-generate-n-distinct-colors
#==============================================================================
def get_colors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors
#==============================================================================

def create_world_map():
    """
    This function reads all the data for the countries concerning the main
    tourist theme (from file). It creates a world map of the tested countries 
    colored to each theme's color.
    """
    # read the dictionary with the countries and the main theme
    countries_theme_dict = dict()
    with open('country_main_themes.txt') as main_themes_file:
        for entry in main_themes_file:
            country, theme = entry.replace('\n', '').split(':')
            countries_theme_dict[country] = theme
    
    # read all the themes list
    themes_list = []
    counter = 0
    with open(create_matrices.TRAIN_MATRICES_EXPORT_PATH + 'class_themes.txt')\
                                                            as class_labels:
        for theme in class_labels:
            themes_list.append(theme.replace('\n',''))
            counter += 1
    
    # get unique color for each theme
    color_list = get_colors(len(themes_list))
    
    # map each color to the theme string
    theme_color = dict()
    for i in range(len(themes_list)):
        theme_color[themes_list[i]] = color_list[i]
        
    # create a mapping between country name and its ISO 3-digit code
    countries_name_dict = dict()
    for country in countries_theme_dict:
        # filter out any name mismatch
        try:
            country_code = iso3166.countries_by_name[country.upper()][2]
            countries_name_dict[country_code] = country
        except KeyError:
#            print country
            pass
    
    # create the world map
    fig = plt.Figure()
    fig.set_canvas(plt.gcf().canvas)
    
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cartopy.feature.LAND, linewidth=0.5, edgecolor='white')
    ax.add_feature(cartopy.feature.OCEAN)
    ax.set_extent([-150,60,-25,60])
    
    shpf = shpreader.natural_earth(resolution='110m', category='cultural', 
                                                   name='admin_0_countries')
    
    reader = shpreader.Reader(shpf)
    countries = reader.records()
    
    for country in countries:
        if country.attributes['adm0_a3'] in countries_name_dict.keys():
            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor=theme_color[
                                  countries_theme_dict[
                                      countries_name_dict[
                                          country.attributes['adm0_a3']]]],
                              linewidth=0.5, edgecolor='white', 
                              label=country.attributes['adm0_a3'])
        else:
            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor=(0.3,0.3,0.3),
                              linewidth=0.5, edgecolor='white', 
                              label=country.attributes['adm0_a3'])
    
    plt.title('World map of countries colored in main tourist theme')
    
    # === create the legend ===
    # create list with rectangle colors for the legend
    legend_color_list = []
    for color in  color_list:
        temp = mpatches.Rectangle((0, 0), 1, 1, facecolor=color)
        legend_color_list.append(temp)
    legend_color_list.append(mpatches.Rectangle((0, 0), 1, 1, 
                                                facecolor=(0.3,0.3,0.3)))
    
    # create labels for the legend
    legend_labels_list = []
    for theme in themes_list:
        legend_labels_list.append(theme)
    legend_labels_list.append('not tested')
        
    ncol = 4
    plt.legend(legend_color_list, legend_labels_list,
                   loc='lower left', bbox_to_anchor=(0.025, -0.3), 
                    fancybox=True, prop={'size':6}, ncol=ncol)              
    
    # save figure to file
    fig.savefig("world_map.png", format='png', dpi=200, bbox_inches='tight')
    
def main():
    create_world_map()
    
if __name__ == '__main__':
    main()