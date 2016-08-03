# -*- coding: utf-8 -*-
"""
Created on Wed May 18 19:08:46 2016

@author: Tilemachos Bontzorlos

This program is used to classify a list of countries to a tourist theme
using supervised learning. It creates the feature matrices for the training and 
test data. It tests the accuracy of the classifier. Then it classifies the 
countries based on their feature matrices, creates a bar chart for each
country matching and finally it outputs a world map depicted all the tested 
countries colored in the matching tourist theme.
"""

import create_images_feature_matrices as create_matrices
import bar_chart_graph as show_bar
import create_world_map_graph
import numpy as np
import glob
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier

def create_data():
    """
    This function calls the program 'create_images_feature_matrices' to create 
    the train and test data if they have not yet been generated.
    """
    create_matrices.main()

def plot_world_map():
    """
    This function calls the program 'create_world_map_graph', which creates a  
    world map of all tested countries coloured in their corresponding main 
    tourism theme.
    """
    create_world_map_graph.create_world_map()
    
def classify_countries(classifier=0):
    """
    This function loads the training data and trains a machine learning 
    classifier. It then loads the test data for each country and classifies it. 
    Finally, it saves a bar chart of this classification.
    
    Parameters
    ----------
    classifier : parameter to select which classifier to use. 
            Options:
                0 : Random Forest Classifier
                1 : Etremely Randomized Trees Classifier
                2 or other : Voting Classifier with soft voting method 
                            utilizing:
                                1) Random Forest Classifier with weight=2
                                2) Etremely Randomized Trees Classifier with
                                    weight=1.
                                3) Support Vector Machine with weight=2.
    """
    # load the training data
    train_X = np.loadtxt(create_matrices.TRAIN_MATRICES_EXPORT_PATH + 
                                                                'train_X.txt')
    train_y = np.loadtxt(create_matrices.TRAIN_MATRICES_EXPORT_PATH + 
                                                                'train_y.txt')
    
    # load the class labels
    labels_list = []
    counter = 0
    with open(create_matrices.TRAIN_MATRICES_EXPORT_PATH + 'class_themes.txt') as class_labels:
        for label in class_labels:
            labels_list.append(label.replace('\n',''))
            counter += 1
    
    # select classifier
    if classifier == 0:
        clf = RandomForestClassifier(n_estimators = 100)
    elif classifier == 1:
        clf = ExtraTreesClassifier(n_estimators = 100)
    else:
        clf1 = RandomForestClassifier(n_estimators = 30)
        clf2 = ExtraTreesClassifier(n_estimators = 30)
        clf3 = SVC(kernel='rbf', probability=True)
        clf = VotingClassifier(estimators=[('rf', clf1), ('et', clf2), 
                                ('svc', clf3)], voting='soft', weights=[2,1,2])
    
    # train the system
    clf = clf.fit(train_X, train_y)
    
    # read the names of all the test data files
    path = create_matrices.TEST_MATRICES_EXPORT_PATH + '*' #to select all files
    test_files = glob.glob(path)
    
    # dictionary to save the main theme for each country
    country_main_theme_dict = dict()
    
    # for each country in the list load the data predict them and output a graph
    for country_filename in test_files:
        country_name = country_filename.split('/')[1].split('_')[2].replace(
                                                    '.txt', '').capitalize()
        X_test = np.loadtxt(country_filename)
        y_predict = clf.predict(X_test)
        
        # sum the image classes
        country_classification = np.zeros([len(labels_list)])
        for i in y_predict:
            country_classification[i] += 1
            
        # save the main theme of the country to a dictionary
        main_theme_indices = np.argwhere(country_classification == np.amax(
                                                    country_classification))
        if len(main_theme_indices) == 1:
            country_main_theme_dict[country_name] = labels_list[main_theme_indices]
        else:
            # if more than 1 have same probability randomly pick one
            random_selection = np.random.randint(len(main_theme_indices))
            country_main_theme_dict[country_name] = labels_list[random_selection]
            
        # print a simple graph
        show_bar.show_country_bar_chart(country_classification / 100, 
                                                     labels_list, country_name)
        
    with open('country_main_themes.txt', 'w') as main_themes_file:
        for country in country_main_theme_dict:
            main_themes_file.write(country + ':' + 
                                    country_main_theme_dict[country] + '\n')

def test_accuracy(classifier=0):
    """
    This function loads the training data splits them into new training and
    test data and trains a machine learning classifier on the splitted training
    data. It then test the efficiency of the classifier on the splitted test 
    data and prints the result.
    
    Parameters
    ----------
    classifier : parameter to select which classifier to use. 
            Options:
                0 : Random Forest Classifier
                1 : Etremely Randomized Trees Classifier
                2 or other : Voting Classifier with soft voting method 
                            utilizing:
                                1) Random Forest Classifier with weight=2
                                2) Etremely Randomized Trees Classifier with
                                    weight=1.
                                3) Support Vector Machine with weight=2.
    """
    # load the training data
    X = np.loadtxt(create_matrices.TRAIN_MATRICES_EXPORT_PATH + 'train_X.txt')
    y = np.loadtxt(create_matrices.TRAIN_MATRICES_EXPORT_PATH + 'train_y.txt')
    
    # split the data
    X_train, X_test, y_train, y_test = cross_validation.train_test_split( \
    X, y, test_size=0.3, random_state=42)
    
    # train the system
    # select classifier
    if classifier == 0:
        clf = RandomForestClassifier(n_estimators = 100)
    elif classifier == 1:
        clf = ExtraTreesClassifier(n_estimators = 100)
    else:
        clf1 = RandomForestClassifier(n_estimators = 30)
        clf2 = ExtraTreesClassifier(n_estimators = 30)
        clf3 = SVC(kernel='rbf', probability=True)
        clf = VotingClassifier(estimators=[('rf', clf1), ('et', clf2), 
                                ('svc', clf3)], voting='soft', weights=[2,1,2])
                                
    clf = clf.fit(X_train, y_train)
    
    y_predict = clf.predict(X_test)
    
    # verify accuracy
    y_length = len(y_test)
    counter = 0
    for i in range(y_length):
        if y_predict[i] == y_test[i]:
            counter += 1
            
    print "Accuracy: ", counter * 100 / y_length, "%"
    
    
def main():
#    create_data()
#    test_accuracy(classifier=0)
    classify_countries(classifier=0)
    plot_world_map()
    
if __name__ == '__main__':
    main()