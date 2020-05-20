# -*- coding: utf-8 -*-
"""
Main Code File for ADSAML

"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog
import pickle

import load_data as ld
import clean_data as cd
import preprocess_data as prd
import visualize_data as vd
import classification_modelling as cm


#-----Creating the Project Directory in Host System-----#

# Choose the folder
window = tk.Tk()
window.title("Choose the directory")
window.withdraw()
main_dir = filedialog.askdirectory()

# Make root
root_name = input("Enter the name of your project's root directory :")
root_path = os.path.join(main_dir, root_name)
os.mkdir(root_path)

# Make sub-directories within the project directory
data_path = os.path.join(root_path, "data")
os.mkdir(data_path)
visualization_path = os.path.join(root_path, "visualization")
os.mkdir(visualization_path)
models_path = os.path.join(root_path, "models")
os.mkdir(models_path)
reports_path = os.path.join(root_path, "reports")
os.mkdir(reports_path)

# Make sub-directories in data
raw_data_path = os.path.join(data_path, "raw")
os.mkdir(raw_data_path)
clean_data_path = os.path.join(data_path, "clean")
os.mkdir(clean_data_path)
processed_data_path = os.path.join(data_path, "processed")
os.mkdir(processed_data_path)


#-----Global Parameters-----#
 
PROJ_ROOT = root_path
PROJ_DATA = data_path
PROJ_VIZ = visualization_path
PROJ_MODELS = models_path
PROJ_REPORTS = reports_path
PROJ_RAW_DATA = raw_data_path
PROJ_CLEAN_DATA = clean_data_path
PROJ_PROCESSED_DATA = processed_data_path
DATASET_NAME = None


#-----Loading the dataset-----#

# Load the Dataset
window = tk.Tk()
window.title("Choose the dataset to load")
window.withdraw()
dataset_path = filedialog.askopenfilename()

# Convert to Dataframe
try:
    df = pd.read_csv(dataset_path)
    DATASET_NAME = input("Rename this data file(You don't need to specify "
                        "a .csv extension; no spaces allowed.) :")
    raw_data_path = os.path.join(PROJ_RAW_DATA, (DATASET_NAME+".csv"))
    df.to_csv(raw_data_path, index=False)
except:
    print("Error creating dataframe\n")

print("\n\nBRIEF INFORMATION ABOUT THE DATA")
print("--------------------------------\n")
print("Dataset loaded from :", dataset_path)
print("Copy of dataset stored at :", PROJ_RAW_DATA)
print()
print("> Shape of dataset :",df.shape)
print("> Preview of dataset :")
print(df.head().to_markdown())


#-----Cleaning the dataset-----#

print("\n\nCLEANING THE DATASET")
print("--------------------\n")
raw_data_path = os.path.join(PROJ_RAW_DATA, (DATASET_NAME+".csv"))
df = pd.read_csv(raw_data_path)

# clean_data.py in action
dc = cd.DataCleaner(df)
dc.clean_df()
print("> Preview of cleaned dataset :")
print(dc.df.head().to_markdown())

# store cleaned dataset
clean_data_path = os.path.join(PROJ_CLEAN_DATA, (DATASET_NAME+".csv"))
dc.df.to_csv(clean_data_path, index=False)


#-----Allowing the user to choose whether the project is ML-based or not-----#

"""
print("\n\nCHOOSE YOUR FORM OF PROJECT")
print("Choose datatypes for each feature\n"
      "-> Enter the type of project you are working on\n"
      "-> Enter 1 if it involves Supervised Machine Learning\n"
      "-> Enter 2 if it doesnot involve Machine Learning and is purely"
      " analytical\n"
      "-> Default Options: Supervised Machine Learning\n"
     )
choice = input("Your choice:")
if (choice=='2'):
    # something
else:
    # something2
"""

#-----Preprocessing the dataset-----#

print("\n\nPREPROCESSING THE DATASET")
print("-------------------------\n")
df = pd.read_csv(clean_data_path)

# take in the target feature
print("The following features are present in your cleaned dataset: ")
print(list(df.columns))
print("Which feature do you want to be the target feature? If you have no"
      " target feature, enter 'None'")
target = input("Enter Target Feature:")

# split into train and test data (20% test)
if(target!='None'):
    ds = ld.DataSplitter(df, PROJ_CLEAN_DATA)
    ds.train_test_split(target, test_percent=0.20, random_state=42)
    
    # make them dataframes
    train = pd.read_csv(os.path.join(PROJ_CLEAN_DATA,"train.csv"))
    test = pd.read_csv(os.path.join(PROJ_CLEAN_DATA,"test.csv"))
    test_solution = pd.read_csv(os.path.join(PROJ_CLEAN_DATA,"test_solution.csv"))
    
    # use the preprocessor class from preprocess_data.py
    pp = prd.PreProcessor(train, test, test_solution, target)
    (preproc_train, preproc_test, preproc_test_tar) = pp.give_output()
    
    # get data for modelling
    (X_tr, y_tr, X_te, y_te) = pp.towards_ml()
    
    # store preprocessed files
    preproc_train.to_csv((os.path.join(PROJ_PROCESSED_DATA,"train.csv")),
                         index=False)
    preproc_test.to_csv((os.path.join(PROJ_PROCESSED_DATA,"test.csv")),
                         index=False)
    preproc_test_tar.to_csv((os.path.join(PROJ_PROCESSED_DATA,"test_solution.csv")),
                         index=False)
    
    print("Preprocessed datasets have been loaded into path:",
          PROJ_PROCESSED_DATA)
    
else:
    print("No target feature specified. So, no preprocessing performed.\n")
    train = pd.read_csv(clean_data_path)
    # no need to go into preprocessing if there is no target
    pass
    

#-----Auto-generating Visualizations-----#
       
print("\n\nAUTO-GENERATING THE DATASET")
print("-------------------------\n")

# make them dataframes
train = pd.read_csv(os.path.join(PROJ_PROCESSED_DATA,"train.csv"))
test = pd.read_csv(os.path.join(PROJ_PROCESSED_DATA,"test.csv"))
test_solution = pd.read_csv(os.path.join(PROJ_PROCESSED_DATA,"test_solution.csv"))

# use the visualizer class from visualize_data.py
viz = vd.FinalPlotter(train, test, target, pp.give_feat_list(), PROJ_VIZ)
viz.plot_it_all()


#-----Modelling Data-----#
 
print("\n\nMODELLING")
print("-------------------------\n")

bm = cm.Baseline(X_tr, y_tr, X_te, y_te)
model = bm.disp_it()

# store the model as a .pkl file
with open(os.path.join(PROJ_MODELS,'model.pkl'), 'wb') as file:
    pickle.dump(model, file=file)
    
print("Your preffered model has been stored at",
      os.path.join(PROJ_MODELS,'model.pkl'))

"""The End"""