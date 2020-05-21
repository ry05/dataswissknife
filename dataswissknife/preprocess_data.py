"""
Module Preprocess Data
======================
This module performs the task of preprocessing cleaned up tabular data with user
interaction
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing

class Essentials:
    """
    Performs essential operations in preprocessing 
    > Works on the dataframe only
    > Will be most necessary for the preprocessing stage

      1. Split up the cleaned dataframe into X(descriptors) and y(target)
      2. X and y are to be independently processed
      3. y will only adhere to one kind of preprocessing : Label Encoding (if required)
    """
    
    df = None             # train dataframe
    target = None         # name of target feature
    X = None              # train descriptors
    y = None              # train target
    df_test = None        # test dataframe; user should never see this
    test_target = None    # test target
    numericals = []       # numerical features
    non_numericals = []   # non-numerical features
    ratio = []            # ratio features
    ordinal = []          # ordinal features
    nominal = []          # nominal features
    interval = []         # interval features
    interval_sep = None   # interval sepearator
    
    def __init__(self, dataframe, test_dataframe, test_solution, target):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The train dataframe
            test_dataframe (pandas dataframe): The test dataframe without target
            test_solution (pandas dataframe): The target of test dataframe
            target (str): The target feature
        """

        self.df = dataframe
        self.df_test = test_dataframe
        self.test_target = test_solution
        self.target = target
        if(target!='None'):
            self.X = self.df.drop([self.target], axis=1)
            self.y = self.df[[self.target]]
        else:
            self.X = self.df
            
    def find_cardinality(self, feature):
        """
        Cardinality of a given feature
        
        Parameters:
            feature (str): Feature whose cardinality has to be found
            
        Returns:
            Cardinality of feature
        """
        
        return (len(list(self.df[feature].unique())))
    
    def prompt_id_removal(self):
        """
        Prompts the user to remove features that look like 'id' features
        """
        
        potential_ids = []
        above_70 = []
        
        for feat in self.X.columns:
            uniq_percent = len(self.X[feat].unique()) / (self.X.shape[0])
            if(uniq_percent == 1):
                potential_ids.append(feat)
            elif(uniq_percent > 0.70):
                above_70.append(feat)
            else:
                continue
            
        if(len(potential_ids)==0):
            pass
        elif(len(potential_ids)==1):
            self.X = self.X.drop(potential_ids, axis=1)
            self.df_test = self.df_test.drop(potential_ids, axis=1) 
            print("The feature",potential_ids[0], "has been removed as it",
                  "has been recognized as an identifier feature")
        else:
            self.X = self.X.drop(potential_ids, axis=1)
            self.df_test = self.df_test.drop(potential_ids, axis=1)
            print("The features",','.join(potential_ids), "have been removed",
                  "as they have been recognized as an identifier feature")
        
        for feat in above_70:
            print("Do you wish to remove the feature",feat,
                  "as it has a high unique value percentage(greater than 70%) ?",
                  "\nEnter y for yes, else enter anything")
            ans = input()
            if(ans=='y'):
                self.X = self.X.drop([feat], axis=1)
            else:
                continue        
    
    def df_ftypes(self):
        """
        Returns the feature types i.e (ordinal, nominal, interval, numeric)
        """

        for feat in self.X.columns:
            if(('float' in str(self.X[feat].dtype)) or 
               ('int' in str(self.X[feat].dtype))):
                self.numericals.append(feat)
            else:
                self.non_numericals.append(feat)
                
    def is_interval(self, feat):
        """
        Check if a feature is an interval feature
        
        Parameters:
            feat (str): Feature to check if it's an interval
        """

        print("Is the feature titled ",feat," an interval feature?")
        ans = input()
        if(ans=='y'):
            separator = input("Enter the character used as separator: ")
            self.interval_sep = separator
            self.interval.append(feat)
        else:
            self.nominal.append(feat)
    
    def does_order_matter(self):
        """
        Checks if order matters
        
        Parameters:
            features (list): Features of the dataframe
        """
        
        print("\nDECIDING THE TYPES OF FEATURES >\n")
        
        print("NOTE: Answer the following questions with y/n")
        for feat in (self.X.columns):
            print("Do you wish to encode ",feat," as an ordinal feature?")
            ans = input()
            if(ans=='y'):
                self.ordinal.append(feat)
            else:
                if(feat in self.numericals):
                    self.ratio.append(feat)
                else:
                    self.is_interval(feat)
                            
        
class ProcessRatios(Essentials):
    """Performs preprocessing operations on ratio features"""
       
    def __init__(self, dataframe, test_dataframe, test_solution, target):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The train dataframe
            test_dataframe (pandas dataframe): The test dataframe without target
            test_solution (pandas dataframe): The target of test dataframe
            target (str): The target feature
        """
        
        super(ProcessRatios, self).__init__(dataframe, test_dataframe,
             test_solution, target)
      
    def to_rem_outliers(self, feat):
        """
        Asks user whether to remove outliers from a feature or not

        Parameters:
            feat (str): Feature to be asked for
            
        Returns:
            Boolean status
        """

        print("Do you wish to remove outliers in the feature titled",feat,"?")
        ans = input("Enter your choice (y or n). Anything else will default to"
                    " y. ")
        if(ans=='n'):
            return False
        else:
          return True 
    
    def outlier_rem(self, feat):
        """
        Removes outliers from ratio features using the IQR outlier removal
        method

        Parameters:
            feat (str): Feature whose outlier has to be removed
        """
        
        # finding inter-quartile range
        Q1 = self.X[[feat]].quantile(0.25)
        Q3 = self.X[[feat]].quantile(0.75)
        IQR = Q3 - Q1
        
        # fitting on train
        self.X[[feat]] = self.X[[feat]][~((self.X[[feat]] < (Q1 - 1.5 * IQR))|
                (self.X[[feat]] > (Q3 + 1.5 * IQR))).any(axis=1)]
        self.X = self.X.dropna()
        
        '''
        don't remove any data from test
        # for test
        self.df_test[self.ratio] = self.df_test[self.ratio][~((self.df_test[self.ratio] < (Q1 - 1.5 * IQR))|
                (self.df_test[self.ratio] > (Q3 + 1.5 * IQR))).any(axis=1)]
        self.df_test = self.df_test.dropna()
        '''
        
    def minmaxscale(self, feat):
        """
        Performs Min-Max Scaling
        
        Parameters:
            feat (str): Feature to be scaled
        """
        
        # fitting on train
        arr = self.X[feat].values
        min_val = np.amin(arr)
        max_val = np.amax(arr)

        if(min_val!=max_val):
            den = max_val-min_val
            self.X[feat] = (arr-min_val)/den

            # for test
            arr_test = self.df_test[feat].values
            self.df_test[feat] = (arr_test-min_val)/den

        else:
            pass    
        
    def to_scale(self):
        """
        Asks user whether to scale a given ratio feature or not

        Parameters:
            feat (str): Feature to be asked for
            
        Returns:
            Boolean status
        """
        
        print("Do you wish to scale(normalize) the numerical features?")
        ans = input("Enter your choice (y or n). Anything else will default to"
                    " y. ")
        if(ans=='n'):
            return False
        else:
          return True  
    
    def outlier_removal(self):
        """
        Scales ratio features
        """
        
        print("\nREMOVING OUTLIERS >\n")
        
        for feat in self.ratio:
            if(self.to_rem_outliers(feat)):
                self.outlier_rem(feat)
            else:
                print("\nNot removing outliers",feat,"as per your request")
    
    def ratio_scaling(self):
        """
        Scales ratio features
        """
        
        print("\nNORMALIZING NUMERICAL FEATURES >\n")
        
        if(self.to_scale()):
            for feat in self.ratio:
                self.minmaxscale(feat)
        else:
            print("\nNot scaling features as per your request")
       

class ProcessOrdinals(Essentials):
    """Performs preprocessing operations on ordinal features"""
    
    order_dict = {}           # order for ordinal features
    
    def __init__(self, dataframe, test_dataframe, test_solution, target):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The train dataframe
            test_dataframe (pandas dataframe): The test dataframe without target
            test_solution (pandas dataframe): The target of test dataframe
            target (str): The target feature
        """
        
        super(ProcessOrdinals, self).__init__(dataframe, test_dataframe,
             test_solution, target)
        
    def take_order(self, feat):
        """
        Take user input about order of values in ordinal features
        
        Parameters:
            feat (str): Feature that is under consideration
            
        Returns:
            list: order of labels
        """
        # pick order only for categorical features
        print("The unique values in ",feat, "is =>",
              list(self.X[feat].unique())
              )
        
        print("Feature",feat)
        order = input("Enter these values in order(separate with comma) => ")
        order = order.split(',')
        return order
        
    def encode_with_order(self):
        """
        Encodes ordinal features with a given order
        """
        
        print("\nORDINAL ENCODING >\n")
        
        for feat in self.ordinal:
            
            # find order
            order = self.take_order(feat)
            labels = list(range(len(order)))
            self.order_dict[feat] = dict(zip(order, labels))
            
            # label encode train
            self.X.replace(self.order_dict[feat], inplace=True)
            
            # label encode test
            # Assumption: No new category exists in the test set
            self.df_test.replace(self.order_dict[feat], inplace=True)
 
           
class ProcessNominals(Essentials):
    """Performs preprocessing operations on nominal features"""
       
    def __init__(self, dataframe, test_dataframe, test_solution, target):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The train dataframe
            test_dataframe (pandas dataframe): The test dataframe without target
            test_solution (pandas dataframe): The target of test dataframe
            target (str): The target feature
        """
        
        super(ProcessNominals, self).__init__(dataframe, test_dataframe,
             test_solution, target)
        
    def one_hot_encode(self):
        """
        One hot encodes the features
        """
        
        print("\nONE HOT ENCODING NOMINAL FEATURES >\n")
        
        # one-hot encode train
        self.X = pd.get_dummies(self.X, columns=self.nominal)
        
        # one-hot encode test
        # Assumption: No new category exists in the test set
        self.df_test = pd.get_dummies(self.df_test, columns=self.nominal)
 
       
class ProcessIntervals(Essentials):
    """Performs preprocessing operations on interval features"""
        
    def __init__(self, dataframe, test_dataframe, test_solution, target):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The train dataframe
            test_dataframe (pandas dataframe): The test dataframe without target
            test_solution (pandas dataframe): The target of test dataframe
            target (str): The target feature
        """
        
        super(ProcessIntervals, self).__init__(dataframe, test_dataframe,
             test_solution, target)
        
    def mean_interval(self, x):
        """
        Just an apply function
        """
        
        l = x.split(self.interval_sep)
        return ((int(l[0]) + int(l[1]))/2)
    
    def mean_encode_intervals(self):
        """
        Mean encodes intervals
        """
        
        print("\nMEAN ENCODING INTERVALS >\n")
        
        for feat in self.interval:
            # mean-encode train
            self.X[feat] = self.X[feat].apply(self.mean_interval)
            # mean-encode test
            self.df_test[feat] = self.df_test[feat].apply(self.mean_interval)
      
        
class ProcessTarget(Essentials):
    """Performs preprocessing operations on target feature"""
    
    def __init__(self, dataframe, test_dataframe, test_solution, target):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The train dataframe
            test_dataframe (pandas dataframe): The test dataframe without target
            test_solution (pandas dataframe): The target of test dataframe
            target (str): The target feature
        """
        
        super(ProcessTarget, self).__init__(dataframe, test_dataframe,
             test_solution, target)
        
    def encode_target(self):
        """Encode target"""
        
        try:
            # Create a label (category) encoder object
            le = preprocessing.LabelEncoder()
            # Fit the encoder to the pandas column
            le.fit(self.y[self.target])

            # encode test target
            self.test_target[self.target] = le.transform(self.test_target[self.target])
        
            # encode train target
            self.y[self.target] = le.transform(self.y[self.target])
            
        except:
            # hope code never enters in here
            print("TEST TARGET HAS CLASSES NOT SEEN IN TRAIN DATA...\n",
                  "Currently, there is no support for this")
            pass

class PreProcessor(ProcessRatios, ProcessNominals, ProcessOrdinals,
                   ProcessIntervals, ProcessTarget):
    """ Main preprocessing class """
    
    final_train = None

    def __init__(self, dataframe, test_dataframe, test_solution, target):
        """
        Constructor for the class
        
        Parameters:
            dataframe (pandas dataframe): The train dataframe
            test_dataframe (pandas dataframe): The test dataframe without target
            test_solution (pandas dataframe): The target of test dataframe
            target (str): The target feature
        """

        super(PreProcessor, self).__init__(dataframe, test_dataframe,
             test_solution, target)
    
    def preprocess_data(self):
        """Preprocess data in steps"""
        
        self.prompt_id_removal()
        self.df_ftypes()                # categorize into types of features
        self.does_order_matter()
        self.outlier_removal()
        self.ratio_scaling()
        self.encode_with_order()
        self.one_hot_encode()
        self.mean_encode_intervals()
        self.encode_target()
        
    def make_final_train(self):
      """Make the final train dataframe"""

      self.final_train = pd.concat([self.X,self.y], axis=1, join='inner')

    def disp_preprocessed_data(self):
        """Display preprocessed dataframe"""
       
        self.preprocess_data()
        self.make_final_train()
        
        print("\nPreview of Preprocessed Train Dataset >\n")
        print(self.final_train.head().to_markdown())
        
        print("\nPreview of Preprocessed Test Dataset >\n")
        print(self.df_test.head().to_markdown())
        
        print("\nPreview of Preprocessed Test Target Labels >\n")
        print(self.test_target.head().to_markdown())
        
    def update_feat_lists(self):
        """
        Update the feature types' lists
        -----
        It's important as one-hot encoding changes the names of features
        """
        
        self.non_numericals = list(set(self.final_train.columns) -
                                   set(self.numericals))
        self.nominal = list(set(self.final_train.columns) -
                            set(self.ratio + self.ordinal + self.interval))
    
    def give_feat_list(self):
        """
        Return the different feature types in the data
        Used for visualize data.py
        """
        
        self.update_feat_lists()
        
        return (self.numericals, self.non_numericals, self.ratio, 
                self.ordinal, self.nominal,  self.interval, self.interval_sep)
    
    def towards_ml(self):
        """
        Prepares and sends output for the ML part
        """
        
        X_tr = self.final_train.drop([self.target], axis=1)
        y_tr = self.final_train[self.target]
        X_te = self.df_test
        y_te = self.test_target
        
        return (X_tr, y_tr, X_te, y_te)
        
    def give_output(self):
        """
        Provide output dataframes
        
        Returns:
            > Final train data with descriptors and target
            > Test sample with no target
            > Test sample's target
            All are dataframes
        """
        
        # perform preprocessing
        self.preprocess_data()
        self.make_final_train()
        
        # return dataframes as outputs
        tr = self.final_train
        te = self.df_test
        tt = self.test_target
        
        return (tr,te,tt)