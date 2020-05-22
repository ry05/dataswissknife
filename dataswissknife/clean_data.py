"""
Module Clean Data
=================
This module performs the task of cleaning raw tabular data with user
interaction
"""

import pandas as pd
import sys
import itertools
import re

from colorama import Fore, Back, Style, init
from termcolor import colored
init()

class Initiator:
    """
    Initiates the data cleaning operation by loading data
    
    Attributes:
        dataframe (pandas dataframe): The dataframe to be cleaned
    """
    
    df = None     # the dataframe       
    num_rows = 0  # number of rows
    num_cols = 0  # number of columns
    
    def __init__(self, dataframe):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The dataframe to be cleaned
        """
        
        self.df = dataframe
           
    def init_rows_cols(self):
        """Initialises rows and columns"""
        
        self.num_rows = self.df.shape[0]
        self.num_cols = self.df.shape[1]
    
    def preview_df(self):
        """Display the first 5 rows of the dataframe"""
        
        self.init_rows_cols()
        print("\nDataset Preview >\n")
        print(self.df.head().to_markdown())


class ColumnCleaner(Initiator):
    """ Cleans Columns in Data """

    def __init__(self, dataframe, round_to=3):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The dataframe to be cleaned
            round_to (int): Number of decimals to round of float values to
        """
        
        super(ColumnCleaner, self).__init__(dataframe)
        self.round_to = round_to

    def rename_cols(self):
        """Rename Column Names"""
        
        new_col_list = []
        for c in (self.df.columns):
            new_col_list.append(c.replace(" ","_").lower().replace("\n","_").
                                strip())
        self.df.columns = new_col_list

    def cardinality(self, feature):
        """
        Find cardinality of a given feature
        
        Parameters:
            feature (str): The name of the feature
        
        Returns:
            int: The cardinality of the feature in the dataframe
        """

        return (len(self.df[feature].unique()))
    
    def rem_const_cols(self):
        """Remove columns with a single constant value"""

        const_cols = []
        for c in (self.df.columns):
          if(self.cardinality(c) == 1):
            const_cols.append(c)

        self.df = self.df.drop(const_cols, axis=1)

    def is_col_empty(self, feature):
        """
        Check if a given column is empty
        
        Parameters:
            feature (str): The name of the feature
        
        Returns:
            bool: True if column is empty, else False
        """
        
        return ((self.df[feature].isna().sum()) == self.num_rows)

    def rem_empty_cols(self):
        """Removes columns with only NaNs"""

        self.df = self.df.dropna(axis=1, how='all')

    def round_float_cols(self):
      """Rounds elements to given number of places"""

      for c in (self.df.columns):
        if("float" in str(self.df[c].dtype)):
          self.df[c] = round(self.df[c], self.round_to)


class RowCleaner(Initiator):
    """ Cleans Rows in Data """
    
    def __init__(self, dataframe):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The dataframe to be cleaned
        """
        
        super(RowCleaner, self).__init__(dataframe)

    def rem_empty_rows(self):
        """Remove empty rows"""

        self.df = self.df.dropna(axis=0, how='all')

    def rem_dupli_rows(self):
        """Remove duplicate rows"""

        self.df = self.df.drop_duplicates()


class ValueCleaner(Initiator):
    """ Clean values """

    def __init__(self, dataframe):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The dataframe to be cleaned
        """
        
        super(ValueCleaner, self).__init__(dataframe)

    def rem_space(self):
        """Remove trailing and leading whitespaces"""
         
        for col in self.df.columns:
            try: # to make it work only for str columns
                self.df[col] = self.df[col].str.strip()
            except:
              continue


class MissingValueDealer(Initiator):
    """ Deal with Missing Values """

    __operations = []        # list of operations to be performed
    __perform_missing = True # by default, assume that missing values exist
    __feature_dict = {}      # dictionary of features according to num vs non-num

    def __init__(self, dataframe):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The dataframe to be cleaned
        """
        
        super(MissingValueDealer, self).__init__(dataframe)

    def disp_miss_percent(self):
        """
        Display missing value percentages in the dataset
        """
        
        cols = []
        miss_val_percent = []
        
        for feat in self.df.columns:
            cols.append(feat)
            miss_val_percent.append(
                    self.df[feat].isna().sum() / self.df.shape[0]
            )
            
        d = pd.DataFrame({'Name of Feature':cols,
             'Percentage of Missing Values':miss_val_percent
             })
            
        print("Missing Value Percentages in the Dataset")
        print(d.to_markdown())
        
    def missing_exists(self):
        """
        Checks if missing values exist
        
        Returns:
            bool: True if missing values exist in the dataframe, else False
        """

        return (self.df.isna().any().any())

    def feature_types(self):
        """Segregate features based on datatypes stored"""
        num = []
        non_num = []
        for col in self.df.columns:
            datype = str(self.df[col].dtype)
            if(("int" in datype) or ("float" in datype)):
                num.append(col)
            else:
                non_num.append(col)

        self.__feature_dict['numeric'] = num
        self.__feature_dict['non-numeric'] = non_num
                
    def mean_impute(self, feature):
        """
        Impute all missing values in the feature with the mean of non-missing
        values
        
        Parameters:
            feature (str): The name of the feature
        """
        
        self.df[feature].fillna(self.df[feature].mean(), inplace=True)

    def median_impute(self, feature):
        """
        Impute all missing values in the feature with the median of non-missing
        values
        
        Parameters:
            feature (str): The name of the feature
        """
        
        self.df[feature].fillna(self.df[feature].median(), inplace=True)

    def mode_impute(self, feature):
        """
        Impute all missing values in the feature with the mode of non-missing
        values
        
        Parameters:
            feature (str): The name of the feature
        """
        
        mode = self.df[feature].mode()[0] # choose lowest mode
        self.df[feature].fillna(mode, inplace=True)
    
    def numeric_impute(self, feature):
        """
        Impute missing values in a numeric feature
        
        Parameters:
            feature (str): The name of the feature
        """
        
        print(colored('Choose method for imputing missing values in numerical features >',
                      'red','on_white'))
        print(colored("-> Enter 1 for 'Imputing with Mean'",
                      'white'))
        print(colored("-> Enter 2 for 'Imputing with Median'",
                      'white'))
        print(colored("-> Enter 3 for 'Imputing with Mode'",
                      'white'))
        print()
        method = input("Your Choice: ")
        
        if(method == '1'):
            self.mean_impute(feature)
        elif(method=='2'):
            self.median_impute(feature)
        elif(method=='3'):
            self.mode_impute(feature)
        else:
            print("Faulty Choice. Please stick to the options provided.")
            self.numeric_impute(feature)
    
    def non_numeric_impute(self, feature):
        """
        Impute missing values in a non-numeric feature
        
        Parameters:
            feature (str): The name of the feature
        """
        
        mode = self.df[feature].mode()[0] # choose lowest mode
        self.df[feature].fillna(mode, inplace=True)
    
    def custom_impute(self, feature):
        """
        Impute missing values with custom, user-defined values
        
        Parameters:
            feature (str): The name of the feature
        """

        if(feature in self.__feature_dict['numeric']):
            value = float(input("Enter Value(Numeric) to Impute with :"))
        else:
            value = input("Enter Value(Non-numeric) to Impute with :")

        self.df[feature].fillna(value, inplace=True)
    
    def impute(self, feature):
        """
        Impute missing values in the feature based on user-interactions
        
        Parameters:
            feature (str): The name of the feature
        """

        print("Imputation For ", feature, " :")
        print()
        print(colored('Choose method for imputing values >',
                      'red','on_white'))
        print(colored("-> Enter 1 for 'Statistical Imputation'",
                      'white'))
        print(colored("-> Enter 2 for 'Custom Imputation'",
                      'white'))
        print()
        print(colored('Warnings >',
                      'red','on_white'))
        print(colored("[!] 'Statistical Imputation' can be 'Overgeneralized'",
                      'yellow'))
        print(colored("[!] 'Custom Imputation' can be 'Time Consuming'",
                      'yellow'))
        print()
        method = input("Your Choice: ")
        
        if(method == '1'):
            if(feature in self.__feature_dict['numeric']):
                print("Performing Numeric Imputation...")
                self.numeric_impute(feature)
            else:
                print("Performing Non-numeric Imputation...")
                self.non_numeric_impute(feature)
        elif(method == '2'):
            print("Initiating Custom Imputation...")
            self.custom_impute(feature)

    def start_imputation(self):
        """Initiate the process of imputation on the dataframe"""

        for col in self.df.columns:
            if(self.df[col].isna().any().any()):
                self.impute(col)
   
    def choose_option(self):
        """Ask user for their choice of method to deal"""
        
        self.disp_miss_percent()
        
        print(colored('MISSING VALUE HANDLING',
                      'red','on_white'))
        print()
        print(colored('Choose method to deal with missing values >',
                      'red','on_white'))
        print(colored("-> Enter 1 for 'Removing' rows with atleast one missing value ",
                      'white'))
        print(colored("-> Enter 2 for 'Imputing' missing values",
                      'white'))
        print(colored("-> Enter 3 for 'Removing' columns with more than 60% missing values",
                      'white'))
        print(colored("-> Enter 4 for 'Quitting' this action",
                      'white'))
        print()
        print(colored("Warnings >", 'red', 'on_white'))
        print(colored("[!] 'Removing rows' can cause 'Data Loss'",
                      'yellow'))
        print(colored("[!] 'Imputing' missing values can cause 'Data Mutation'",
                      'yellow'))
        print(colored("[!] 'Removing columns' can cause 'Data Loss'",
                      'yellow'))
        print()
        choice = input("Your Choice: ")
                
        if(choice=='4'):
            print("Quitting 'MISSING VALUE HANDLING' as per your request...")
            pass
        elif(choice=='3'):
            print("Removing columns with more than 60% as missing values")
            min_non_na = (0.4 * (self.df.shape[0]))
            self.df = self.df.dropna(axis=1, thresh=min_non_na)
            print(colored("Preview of dataframe after this operation >",
                          'red', 'on_white'))
            print(self.df.head().to_markdown())
            print()
            self.choose_option()
        elif(choice=='2'):
            print("Imputing Missing Values as per your request...")
            self.start_imputation()
            self.choose_option()
        else:
            print("Removing rows with atleast one missing value")
            self.df = self.df.dropna(how='any', axis=0)
            print(colored("Preview of dataframe after this operation >",
                          'red', 'on_white'))
            print(self.df.head().to_markdown())
            print() 
            self.choose_option()

    def deal_missing(self):
        """Checks if missing operation is to be performed or not"""

        self.feature_types()

        if(self.missing_exists()):
            self.choose_option()
        else:
            print()
            print(colored('There are no missing values in the loaded dataframe.', 'green'))
            print()
            pass


class ConsistencyChecker(Initiator):
    """Checks for and rectifies consistency-based issues with data"""

    __type_dict = {}   # datatype dictionary
    __mismatches = []  # features that have a type mismatch (only false non-num)
    __symbol_list = [] # list of non-numeric symbols
    __symbol_dict = {} # non-numeric symbols dictionary

    def __init__(self, dataframe):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The dataframe to be cleaned
        """
        
        super(ConsistencyChecker, self).__init__(dataframe)

    def choose_dtype(self, feature):
        """
        Asks the user to choose potential datatypes for each feature based on
        the user's domain expertise
        
        Parameters:
            feature (str): The name of the feature
        """

        datype = input("Choose data type for " + feature + " : ")
        
        if(datype=='1'):
            self.__type_dict[feature] = 'numeric'
        elif(datype=='2'):
            self.__type_dict[feature] = 'non-numeric'
        else:
            print("\nUnknown Option. Re-enter your option.\n")
            self.choose_dtype(feature)
            
        print()
    
    def make_dtype_dict(self):
        """Make the data type dictionary for the features of the dataframe"""

        print(colored('Choose datatypes for each of the features >',
                      'red','on_white'))
        print("-> Enter the best suited data type for a given feature\n"
              "-> Enter 1 for features that have to be 'numeric'\n"
              "-> Enter 2 for features that have to be 'non-numeric'\n"
              )
        for col in self.df.columns:
            self.choose_dtype(col)

    def add_to_mismatches(self, feature):
        """
        Adds mismatched features to a common list
        
        Parameters:
            feature (str): The name of the feature
        """

        if(not(feature in self.__mismatches)):
            self.__mismatches.append(feature)
    
    def check_mismatch(self):
        """Identifies mismatches of data types"""

        for col in self.df.columns:
            datype = str(self.df[col].dtype)
            if(('int' in datype) or ('float' in datype)):
                if(self.__type_dict[col] == 'non-numeric'):
                    pass
            else:
                if(self.__type_dict[col] == 'numeric'):
                    self.add_to_mismatches(col)
                pass

    def disp_mismatches(self):
        """Displays the mismatches"""
        
        print(colored("\nOnly those features that are non-numeric as per the dataset "
                  "but, have to be numeric according to the user are considered "
                  "at this stage.",
                      'yellow'))
        print()
        
        if(len(self.__mismatches)!=0):
            print(colored('There are datatype mismatches!\n',
                      'white','on_red'))
            print("The following features' datatypes do not match with "
                  "the types you have provided with :\n", self.__mismatches)
        else:
            print(colored('There are no datatype mismatches!\n',
                      'white','on_green'))
    
    def make_symbol_list(self, feature):
        """
        Makes a list of non-numeric characters appearing in a feature
        
        Parameters:
            feature (str): The name of the feature
            
        Returns:
            list: List of non-numeric symbols
        """
        
        symbols = []
        for i in range(len(feature)):
            if(not(feature[i].isdigit()) and (feature[i]!='.') and
               (not(feature[i] in self.__symbol_list))):
                self.__symbol_list.append(feature[i])
                symbols.append(feature[i])
        return symbols
    
    def find_symbols(self, feature):
        """
        Identify non-numeric symbols in a feature that is not supposed to have
        any
        
        Parameters:
            feature (str): The name of the feature
        """

        symbols = (self.df[feature].apply(self.make_symbol_list))
        symbols = list(itertools.chain.from_iterable(symbols))
        self.__symbol_dict[feature] = symbols
        print("\nNon-numeric Symbols in "+feature+ " :", symbols)

    def disp_symbols(self):
        """Display all non-numeric symbols in all features"""

        for col in self.__mismatches:
            self.find_symbols(col)

    def rem_symbols(self, feature):
        """
        Remove non-numeric symbols in a feature and make it numeric
        
        Parameters:
            feature (str): The name of the feature
        """

        rem = re.compile('|'.join(map(re.escape, self.__symbol_dict[feature])))
        self.df[feature] = [float(rem.sub('', text)) for text in self.df[feature]]

    def ignore(self, feature):
        """
        Ignore a particular feature from the mismatches list
        
        Parameters:
            feature (str): The name of the feature
        """

        pass

    def rem_feature(self, feature):
        """
        Remove the feature from the dataframe
        
        Parameters:
            feature (str): The name of the feature
        """

        self.df = self.df.drop([feature], axis=1)

    def user_rectification(self, feature):
        """
        Ask the user about the necessary action to undertake with each
        mismatched feature
        
        Parameters:
            feature (str): The name of the feature
        """

        print("\nSelect your choice of dealing with inconsistencies in",
              feature, "\n")
        
        choice = input("-> Enter 1 for 'Ignoring' the feature\n"
              "-> Enter 2 for 'Removing non-numeric symbols' in the feature\n"
              "-> Enter 3 for 'Removing the feature'\n"
              "\nWARNINGS :\n"
              "[!] 'Removing the feature' leads to data loss\n"
              "Your Choice : ")
        
        if(choice=='1'):
            self.ignore(feature)
        elif(choice=='2'):
            self.rem_symbols(feature)
        elif(choice=='3'):
            self.rem_feature(feature)
        else:
            self.rectify_mismatches(feature)

    def rectify_mismatches(self):
        """Rectifies Mismatches with the help of user input"""

        for col in self.__mismatches:
            self.user_rectification(col)

    def establish_consistency(self):
        """Check and establish consistency in the dataframe"""
        
        print(colored('MANAGING DATATYPE INCONSISTENCIES',
                      'red','on_white'))
        print()

        print("-> A datatype inconsistency occurs when columns are stored as ",
              "datatypes that does not support the user's requirement\n",
              "-> We consider only those features that the user expects to be ",
              "numeric, but are non-numeric in the dataset",
              "-> Example : A 'money' column needs to be numeric for better "
              "analysis\n",
              "-> Follow the prompts to rid the dataframe of datatype "
              "inconsistencies or mismatches\n")
        
        # choose datatypes
        self.make_dtype_dict()
        
        if(len(self.__mismatches)!=0):
            # check and display mismatches; display non-numeric symbols
            print("\nDatatype Inconsistencies :\n")
            self.check_mismatch()
            self.disp_mismatches()
            self.disp_symbols()
    
            # user options
            self.rectify_mismatches()
        else:
            print(colored('There are no datatype mismatches!\n',
                      'white','on_green'))

            
class DataCleaner(ColumnCleaner, RowCleaner, ValueCleaner, MissingValueDealer,
                  ConsistencyChecker):
    """Performs the operation of data cleaning"""

    def __init__(self, dataframe):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The dataframe to be cleaned
        """
        
        super(DataCleaner, self).__init__(dataframe)

    def clean_df(self):
        """Complete cleaning of the dataframe"""

        # do we allow the user to select what options he wants to enforce?
        # this can be done in the GUI implementation

        self.rename_cols()            # renames column names
        self.rem_empty_rows()         # removes empty rows
        self.rem_empty_cols()         # removes empty columns
        self.rem_dupli_rows()         # removes duplicate rows
        self.rem_space()              # removes trailing and leading spaces
        print("\n> Preview of dataframe after preliminary cleaning ops:")
        print(self.df.head().to_markdown())
        print()
        self.deal_missing()           # deal with missing values
        self.rem_const_cols()         # removes constant columns
        self.round_float_cols()       # rounds float columns
        self.establish_consistency()

    def disp_clean_df(self):
        """Display preview of cleaned dataset"""

        self.clean_df()
        print("\nPreview of Cleaned Dataset >\n")
        print(self.df.head().to_markdown())  

     

      

    
    
        
    
        
    
        
    

