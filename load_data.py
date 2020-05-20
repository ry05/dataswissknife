"""
Module Load Data
================
This module is concerned with all operations that involve loading data onto the
program
"""

import pandas as pd
import os
import sys


class DataLoader:
    """
    Load data from local system 
    
    Attributes:
        datapath (str): The path to the dataset
        dest_dir (str): The path into which the dataset should be loaded
    """
    
    __datapath = None  # path to dataset
    __dest_dir = None  # destination directory path
    df_name = None     # name of the dataframe
    df = None          # dataframe
    
    
    def __init__(self, datapath, dest_dir=None):
        """
        Constructor for the class
        
        Parameters:
            datapath (str): The path to the dataset
            dest_dir (str): The path into which the dataset should be loaded
        """
        
        self.__datapath = datapath
        self.__dest_dir = dest_dir
        
    def name_df(self):
        """Asks the user for the new name to be applied to the dataset"""
        
        self.df_name = input("Rename this data file(You don't need to specify "
                        "a .csv extension; no spaces allowed.) :")
        
    def load(self):
        """Load the dataset from the given path"""
        
        try:
            self.df = pd.read_csv(self.__datapath)
            self.name_df()
            if(self.__dest_dir==None):
                pass
            else:
                self.df.to_csv(self.__dest_dir+"/"+self.df_name+".csv")
        except:
            print("Error creating dataframe\n",
                  "Aborting...\n")
            sys.exit(0)
            
    def load_dataframe(self):
        """Loads data and returns the dataframe"""
        
        self.load()
        return (self.df)

    
class DataSplitter:
    """
    Splits a whole dataset into train and test
    
    Attributes:
        dataframe (pandas dataframe): The main dataframe to be split
        split_data_path (str): The destination path of the split datasets
    """
    
    __df = None  # dataframe to be split up
    __split_data_path = None # path to the directory where split data is stored
    
    def __init__(self, dataframe, split_data_path):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The main dataframe to be split
            split_data_path (str): The destination path of the split datasets
        """
        
        self.__df = dataframe
        self.__split_data_path = split_data_path
        
    def store_split_data(self, train, test, solution):
        """
        Stores split data in appropriate files
        
        Parameters:
            train (pandas dataframe): The training dataframe
            test (pandas dataframe): The testing dataframe
            solution (pandas dataframe): The target feature of the testing set
        """
        
        # Store the files back as train.csv, test.csv and submission.csv
        train.to_csv(os.path.join(self.__split_data_path,"train.csv"),
                     index=False)
        test.to_csv(os.path.join(self.__split_data_path,"test.csv"),
                    index=False)
        solution.to_csv(os.path.join(self.__split_data_path,"test_solution.csv"),
                        index=False)
        
    def train_test_split(self, target, test_percent=0.20, random_state=42):
        """
        Splits a whole dataset(.csv) for ML into train.csv, test.csv and 
        test_solution.csv
        
        Parameters:
            target (str): Target feature in the dataframe
            test_percent (float): Percentage of data to be used as testing set
                                  (Default: 0.20)
            random_state (int): Seed value for reproducibility        
        """
        
        # number of rows for test data
        num_test_rows = round(self.__df.shape[0] * test_percent)
        
        # Split the data into training and testing data
        test = self.__df.sample(n=num_test_rows, random_state=random_state)
        train = self.__df.drop(list(test.index)).reset_index(drop=True)
        test = test.reset_index(drop=True)
        
        # Store Target values of test separately; remove of the main dataframe
        test_target = test[target].values
        test = test.drop(target, axis=1)

        # Make the submission dataframe
        # This is the final values with which we have to
        # compare our predictions on the test dataset
        solution = pd.DataFrame({target:test_target})
        
        self.store_split_data(train, test, solution)
        
        print("DATA HAS BEEN SPLIT INTO\n",
              "> train.csv\n",
              "> test.csv\n",
              "> test_solution.csv\n",
              "Split data available at:\n",
              self.__split_data_path)
        
        
        
        
        