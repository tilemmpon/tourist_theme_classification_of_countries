# Tourist theme classification of countries
author: Tilemachos Bontzorlos
Python version: 2.7.11

## Introduction
This program is able to automatically find the tourism theme of a country 
using supervised machine learning methods, like Random Forests. The dataset 
used were images that can be gathered online (using the Instagram API for 
example).

The images used for the training and testing of the system are not included
in this repository. Unfortunately, the generated training and test feature 
matrices from these images are also not included. However, each user can
generate the feature matrices through the code in this repository using
his own images. In future, I might add the feature matrices but for now the
files are quite big in size (2.2GB).

The features used are RGB values and Histogram of Gradient (HOG) features. 
RGB features contain the information about colour and HOG features encode 
shape information. The preprocessing step is consisted of image resize to
50×50. The size of the RGB features per image equals to 50×50×3=7500. Then 
HOG features with 8 orientations resulting in 288 features per image are
extracted. In total each image contributes to 7788 features. For training 
6000 images (1000 images for each of the 6 themes) classified by theme
through their labels were used. Themes selected are:
* Architecture
* Desert
* Beach
* Wildlife
* Nature
* Winter landscape

For each country up to 100 images that will be used for classifying the 
country were selected.

For the machine learning part the capabilities of *scikit-learn* library
was utilized.

## Example results

Example match of theme for a country:

![](https://github.com/tilemmpon/tourist_theme_classification_of_countries/blob/master/results/random%20forest%20classifer/countries_graphs/graph_Belgium.png)

World map of all tested countries colored in corresponding theme:

![](https://github.com/tilemmpon/tourist_theme_classification_of_countries/blob/master/results/random%20forest%20classifer/world_map.png)

## Dependencies

* Python 2.7
* numpy
* matplotlib
* glob
* sci-kit learn (sklearn)
* PIL
* skimage
* iso3166
* cartopy
* colorsys

## DESCRIPTION OF FILES AND FOLDERS

### FOLDERS

**train\_data** : Contains all the images used for training. It contains
	subfolders which are the labels of the images they contain. For example, 
	all images in folder "beach" are labeled as beach images. The tourist 
	themes selected and as a result the (empty) subfolders contained
	currently are:
	* Architecture
	* Desert
	* Beach
	* Wildlife
	* Nature
	* Winter landscape

**test\_data** : Contains all the images used for classifying the countries. Each s
	ubfolders contains all the images for a country. For example (empty) 
	folder "visit_austria" contains all images for Austria. The code assumes 
	that these subfolders are named in form "visit_X", where X is the 
	official name of the country. WARNING: if the name of the country is not 
	the official then the world map won't be able to color this country 
	(since its using a certain ISO). Example: Russia is officially called 
	"RUSSIAN FEDERATION".

**train\_data\_matrices** : Contains all the data concerning the training.
* **train_X.txt** : the feature matrix of the training images.
* **train_y.txt** : the classification of the training images.
* **class_themes.txt** : the classes. Classification equal to 0 
					corresponds to first entry of this
					file and so on.
	
	All these files are created by "create_images_feature_matrices.py".
	Currently, this folder only contains dummy files for *train_X.txt* and
	*train_y.txt*, however you can generate new feature matrices for training 
	by using your own images and the provided code in this repository.

**test\_data\_matrices** : Contains all the feature matrices for the countries (test 
	data). Example: "test_X_france.txt" contains the features of the images 
	for France. All these files are created by 
	"create_images_feature_matrices.py".
	Currently, it only contains a dummy file, however you can generate new
	feature matrices for countries by using your own images and the provided
	code in this repository.

**countries\_graphs** : In this folders the code outputs the theme matching
	graphs for each country.

**results** : This folder contains some results I have taken.

### FILES

**country\_main\_themes.txt** : Contains the major tourist theme that a country
	has been classified to, for all the tested countries. Example entry:
	"Finland:winterlandscape"

**world\_map.png** : The world map that "create_world_map_graph.py" outputs.

**bar_chart_graph.py** : Helper program that creates a graph showing the 
	theme match of a country.

**create\_images\_feature_matrices.py** : This is a program that creates feature 
	matrices for training and test data images contained in the 
	corresponding folders. The features used  are RGB and HOG features.
	Labels of the training data are the names of the folders that contain 
	these images. Example: images in folder "beach" will be labelled as 
	beach photos.
	For the test data there are no labels. The folder containing the photos 
	defines the country that these photos belong to. Example: images in 
	folder "visit_austria" belong to country Austria. The code in written 
	in the way of assuming that the folders names of countries are "visit_X" 
	where X is the  country name.
	Also, it outputs class_themes.txt that contains all the classes.
	This program can run indepedently.

**create\_world\_map\_graph.py** : This is a program that creates a world map where 
	each tested country is colored to its best matching tourist theme and 
	the rest countries are colored grey.
	This program can run indepedently.

**classify_countries.py** : This program is used to classify a list of countries to 
	a tourist theme using supervised learning. It creates the feature 
	matrices for the training and test data. It tests the accuracy of the 
	classifier. Then it classifies the countries based on their feature 
	matrices, creates a bar chart for each	country matching and finally it 
	outputs a world map depicted all the tested countries colored in the 
	matching tourist theme.
	This program utilizes all the above mentioned scripts to achieve this 
	functionality.
