# -*- coding: utf-8 -*-
"""
Main Code File for DataSwissKnife

CHANGES TO BE MADE
------------------
1. Add Authors on the README
2. Learn how to maintain a change log and maintain one for DSK
3. Structure the questions asked
    > Example: Your Choice[Y/N]
    > Default option appears first
    > Write this when you start the program
    > Give users an idea of what to expect
4. Use tqdm to depict progress for data viz. and operations that require long 
   waits
"""

import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog
import pickle

from colorama import Fore, Back, Style, init
from termcolor import colored
init()

import load_data as ld
import clean_data as cd
import preprocess_data as prd
import visualize_data as vd
import classification_modelling as cm


#-----Print the Welcome-----#
print(colored((r"""
 ____        _        ____          _         _  __      _  __      
|  _ \  __ _| |_ __ _/ ___|_      _(_)___ ___| |/ /_ __ (_)/ _| ___ 
| | | |/ _` | __/ _` \___ \ \ /\ / / / __/ __| ' /| '_ \| | |_ / _ \
| |_| | (_| | || (_| |___) \ V  V /| \__ \__ \ . \| | | | |  _|  __/
|____/ \__,_|\__\__,_|____/ \_/\_/ |_|___/___/_|\_\_| |_|_|_|  \___|

A Handy Little Tool for your Data Science Operations            
"""),
    'white'))

print(colored(
        'Authors: Ramshankar Yadhunath, Srikanth Srivenkata, Arvind Sudheer', 
              'white', 'on_red')
)


#-----Creating the Project Directory in Host System-----#

print(r""" 
  __               _       _                      _                        __                           
 (_ _|_  _  ._    / \ o   /  ._ _   _. _|_  _    |_) ._ _  o  _   _ _|_   (_ _|_ ._     _ _|_     ._ _  
 __) |_ (/_ |_)   \_/ o   \_ | (/_ (_|  |_ (/_   |   | (_) | (/_ (_  |_   __) |_ | |_| (_  |_ |_| | (/_ 
            |                                             _|                                            
 Create the structure of your project in your local system
""")
print(colored('INSTRUCTIONS :', 'white', 'on_blue'))
print("1. Choose a directory in your system in which you want the project structure to be built\n"
      "2. Enter the name of your project's root directory\n")

print("Please wait a moment while the 'Choose Folder' dialog opens...\n")

# Choose the folder
dir_window = tk.Tk()
dir_window.title("Choose the directory")
dir_window.withdraw()
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

# outputs
print()
print(colored('OUTPUTS :', 'white', 'on_green'))
print("The project structure has been created in", root_path)


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

print(r""" 
  __                      _                                         
 (_ _|_  _  ._    /| o   | \  _. _|_  _.   |   _   _.  _| o ._   _  
 __) |_ (/_ |_)    | o   |_/ (_|  |_ (_|   |_ (_) (_| (_| | | | (_| 
            |                                                    _| 
 Load the dataset for the project from your local system
""")
print(colored('INSTRUCTIONS :', 'white', 'on_blue'))
print("1. Choose the .csv dataset from your system\n"
      "2. Rename your dataset\n")

print("Please wait a moment while the 'Choose Dataset' dialog opens...\n")

# Load the Dataset
data_window = tk.Tk()
data_window.title("Choose the dataset to load")
data_window.withdraw()
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
    
# outputs
print()
print(colored('OUTPUTS :', 'white', 'on_green'))
print(colored('Brief information about the data', 'blue', 'on_white'))
print("Copy of dataset stored at:", PROJ_RAW_DATA)
print("Number of rows in the dataset:",df.shape[0])
print("Number of columns in the dataset:",df.shape[1])
print("Preview of dataset:")
print(df.head().to_markdown())


#-----Cleaning the dataset-----#

print(r""" 
  __              _       _                 _                         
 (_ _|_  _  ._     ) o   | \  _. _|_  _.   /  |  _   _. ._  o ._   _  
 __) |_ (/_ |_)   /_ o   |_/ (_|  |_ (_|   \_ | (/_ (_| | | | | | (_| 
            |                                                      _| 
 Clean the dataset and rid it of values that affect its credibility
""")
print(colored('INSTRUCTIONS :', 'white', 'on_blue'))
print("1. Answer the questions asked by the system to clean up the data\n")

raw_data_path = os.path.join(PROJ_RAW_DATA, (DATASET_NAME+".csv"))
df = pd.read_csv(raw_data_path)

# clean_data.py in action
dc = cd.DataCleaner(df)
dc.clean_df()
print("Preview of cleaned dataset :")
print(dc.df.head().to_markdown())

# store cleaned dataset
clean_data_path = os.path.join(PROJ_CLEAN_DATA, (DATASET_NAME+".csv"))
dc.df.to_csv(clean_data_path, index=False)

# outputs
print()
print(colored('OUTPUTS :', 'white', 'on_green'))
print("The cleaned data has been loaded in", clean_data_path)

# does the user wish to continue?
print(colored('\nDo you wish to continue to Data Preprocessing?', 'green'))
ch = input("Enter your choice[Y/N]: ")
if(ch.upper()=='N'):
    print("\nTerminating DataSwissKnife as per your request.\n"
          "Project Stored at",PROJ_ROOT)
    sys.exit(0)


#-----Preprocessing the dataset-----#

print(r""" 
  __              _       _                 _                                         
 (_ _|_  _  ._    _) o   | \  _. _|_  _.   |_) ._ _  ._  ._ _   _  _   _  _ o ._   _  
 __) |_ (/_ |_)   _) o   |_/ (_|  |_ (_|   |   | (/_ |_) | (_) (_ (/_ _> _> | | | (_| 
            |                                        |                             _| 
 Convert the cleaned data into a format more suitable for Machine Learning
""")
print(colored('INSTRUCTIONS :', 'white', 'on_blue'))
print("1. Answer the questions asked by the system to preprocess the data\n")

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
       
else:
    print("No target feature specified. So, no preprocessing performed.\n")
    train = pd.read_csv(clean_data_path)
    # no need to go into preprocessing if there is no target
    pass
   
# outputs
print()
print(colored('OUTPUTS :', 'white', 'on_green'))
print("1. The preprocessed data has been loaded in", PROJ_PROCESSED_DATA)
print("2.",PROJ_PROCESSED_DATA," has train.csv, test.csv and test_solution.csv")
print("3.",colored("train.csv", 'cyan'),"contains both descriptor and target features")
print("4.",colored("test.csv", 'cyan'),"contains only descriptor features")
print("5.",colored("test_solution.csv", 'cyan'),"contains only target features of"
      "",colored("test.csv", 'cyan'))

# does the user wish to continue?
print(colored('\nDo you wish to continue to auto-generating Data Visualizations?', 'green'))
ch = input("Enter your choice[Y/N]: ")
if(ch.upper()=='N'):
    print("\nTerminating DataSwissKnife as per your request.\n"
          "Project Stored at",PROJ_ROOT)
    sys.exit(0)


#-----Auto-generating Visualizations-----#
       
print(r""" 
  __                        _                                                           
 (_ _|_  _  ._    |_|_ o   | \  _. _|_  _.   \  / o  _      _. | o _   _. _|_ o  _  ._  
 __) |_ (/_ |_)     |  o   |_/ (_|  |_ (_|    \/  | _> |_| (_| | | /_ (_|  |_ | (_) | | 
            |                                                                           
 Generate visualizations from the data. Will be auto-generated by this module.
""")

# make them dataframes
train = pd.read_csv(os.path.join(PROJ_CLEAN_DATA,"train.csv"))
test = pd.read_csv(os.path.join(PROJ_CLEAN_DATA,"test.csv"))
test_solution = pd.read_csv(os.path.join(PROJ_CLEAN_DATA,"test_solution.csv"))

# use the visualizer class from visualize_data.py
viz = vd.FinalPlotter(train, test, target, pp.give_feat_list(), PROJ_VIZ)
viz.plot_it_all()

# outputs
print()
print(colored('OUTPUTS :', 'white', 'on_green'))
print("The auto-generated visualizations are stored in", PROJ_VIZ)

# does the user wish to continue?
print(colored('\nDo you wish to continue to Modelling?', 'green'))
ch = input("Enter your choice[Y/N]: ")
if(ch.upper()=='N'):
    print("\nTerminating DataSwissKnife as per your request.\n"
          "Project Stored at",PROJ_ROOT)
    sys.exit(0)
    
    
#-----Modelling Data-----#
 
print(r""" 
  __               _                                     
 (_ _|_  _  ._    |_  o   |\/|  _   _|  _  | | o ._   _  
 __) |_ (/_ |_)    _) o   |  | (_) (_| (/_ | | | | | (_| 
            |                                         _|    
 Build baseline predictive models for supervised classification 
""")

bm = cm.Baseline(X_tr, y_tr, X_te, y_te)
model = bm.disp_it()

# store the model as a .pkl file
with open(os.path.join(PROJ_MODELS,'model.pkl'), 'wb') as file:
    pickle.dump(model, file=file)
 
# outputs
print()
print(colored('OUTPUTS :', 'white', 'on_green'))
print("Your preffered model has been stored at",
      os.path.join(PROJ_MODELS,'model.pkl'))
print()
print("\nProject Stored at",PROJ_ROOT)

"""The End"""