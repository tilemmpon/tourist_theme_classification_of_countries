# -*- coding: utf-8 -*-
"""
Created on Tue May 17 18:20:02 2016

@author: Tilemachos Bontzorlos

This is a program that creates feature matrices for training and test data 
images contained in the corresponding folders. The features used  are RGB and 
HOG features.

Labels of the training data are the names of the folders that contain these
images. Example: images in folder "beach" will be labelled as beach photos.

For the test data there are no labels. The folder containing the photos defines
the country that these photos belong to. Example: images in folder 
"visit_austria" belong to country Austria. The code in written in the way of
assuming that the folders names of countries are "visit_X" where X is the
 country name.
"""

import numpy as np
import glob
from PIL import Image
from skimage.feature import hog

# size to resize images
IMAGE_SIZE = 50

# data paths
TRAIN_DATA_PATH = 'train_data/*'
TEST_DATA_PATH = 'test_data/*'

# paths to export deature matrices
TRAIN_MATRICES_EXPORT_PATH = 'train_data_matrices/'
TEST_MATRICES_EXPORT_PATH = 'test_data_matrices/'

def create_train_data():
    """
    Loads the train images and creates the features matrices required for the 
    training. Exports the train_X and train_y in seperate txt files.
    """
    # get folder names for the train data (themes)
    path = TRAIN_DATA_PATH
    folders = glob.glob(path)
    
    # create a dictionary with the theme and the corresponding class number
    # also create a reverse list in python with class numbers + corresponding 
    # class
    themes_dict = dict()
    class_themes = dict()
    for i in range(len(folders)):
        theme = folders[i].split('/')[1]
        themes_dict[theme] = i
        class_themes[i] = theme
        
    # get the filenames of images in every theme and save them in a dictionary
    filenames = dict()
    for i in range(len(folders)):
        filenames[folders[i].split('/')[1]] = glob.glob(folders[i] + '/*')
        
        
    # count number of images to create numpy array
    file_counter = 0
    for theme in filenames:
        file_counter += len(filenames[theme])
        
    # get sample hog features for an image to know the hog features matrix size
    file_temp = filenames[filenames.keys()[0]][0]
    hog_features_size = len(hog(np.array(Image.open(file_temp)\
            .convert('L').resize([IMAGE_SIZE,IMAGE_SIZE])), orientations=8))
        
    # create numpy array for the features and class array
    features_array = np.zeros([file_counter, IMAGE_SIZE * IMAGE_SIZE * 3 + 
                                                            hog_features_size])
    class_array = np.zeros([file_counter])
    
    # Load each image, resize, flatten and save it in a list. Also, in a 
    # seperate list save the class of each image. HOG features are also added.
    counter = 0
    for theme in filenames:
        for file_ in filenames[theme]:
            image_orig = Image.open(file_).resize([IMAGE_SIZE,IMAGE_SIZE])
            image = np.array(image_orig)
            features_array[counter, :IMAGE_SIZE * IMAGE_SIZE * 3] = \
                                                        image.flatten()[:]
            features_array[counter, IMAGE_SIZE * IMAGE_SIZE * 3:] = \
                hog(np.array(image_orig.convert('L').resize([IMAGE_SIZE,
                                                 IMAGE_SIZE])), orientations=8)
            class_array[counter] = themes_dict[file_.split('/')[1]]
            counter += 1
            
    # save the feature arrays to files
    np.savetxt(TRAIN_MATRICES_EXPORT_PATH + 'train_X.txt', features_array)
    np.savetxt(TRAIN_MATRICES_EXPORT_PATH + 'train_y.txt', class_array)
    
    # save class themes to file
    with open(TRAIN_MATRICES_EXPORT_PATH + 'class_themes.txt', 'w') as class_file:
        for i in range(len(class_themes.keys())):
            class_file.write(class_themes[i] + '\n')
    


def create_test_data():
    """
    For every country loads the test images and creates a feature matrix to
    test using any ML approach. Exports a train_x_<country name>.txt file with
    these features for every country.
    """
    # get folder names for the test data (countries)
    path = TEST_DATA_PATH
    folders = glob.glob(path)
    
    # create a dictinary with countries and a list of the filenames of all its 
    # images
    countries_dict = dict()
    for i in range(len(folders)):
        countries_dict[folders[i].split('/')[1].split('_')[1]] = glob.glob(
                                                            folders[i] + '/*')
        
    # get sample hog features for an image to know the hog features matrix size
    file_temp = countries_dict[countries_dict.keys()[0]][0]
    hog_features_size = len(hog(np.array(Image.open(file_temp)\
            .convert('L').resize([IMAGE_SIZE,IMAGE_SIZE])), orientations=8))    
    
    # for every country create a feature matrix and save it
    for country in countries_dict:
        # create an array to store all features
        country_features = np.zeros([len(countries_dict[country]),\
            IMAGE_SIZE * IMAGE_SIZE * 3 + hog_features_size])
        
        # for every country fill the features array 
        counter = 0
        for file_ in countries_dict[country]:
            image_orig = Image.open(file_).resize([IMAGE_SIZE,IMAGE_SIZE])
            image = np.array(image_orig)
            country_features[counter, :IMAGE_SIZE * IMAGE_SIZE * 3] = \
                                                            image.flatten()[:]
            country_features[counter, IMAGE_SIZE * IMAGE_SIZE * 3:] = \
                hog(np.array(image_orig.convert('L').resize([IMAGE_SIZE,
                                             IMAGE_SIZE])), orientations=8)
            counter += 1
        
        # save the array to file
        np.savetxt(TEST_MATRICES_EXPORT_PATH + 'test_X_' + country + '.txt', 
                                                           country_features)

def main():
    create_train_data()
    create_test_data()

if __name__ == '__main__':
    main()