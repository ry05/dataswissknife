"""
Module Visualize Data
======================
This module performs the task of automatically generating basic visualizations
to aid in Exploratory Data Analysis(EDA)

Notes:
    > There are two ways to plot data:
        - With target feature
        - Without target feature
        
    > Set a theme for plots
    > Set figsize
    > Save the visualizations as .png files in a given location
    > Use plt.subplots() for all visualizations
    
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns

__all__ = [
  'main_code',
  'clean_data',
  'load_data',
  'preprocess_data',
  'classification_modelling',
  'visualize_data',
  'log_tracker',
]

from dataswissknife import preprocess_data as prd

plt.style.use('bmh')

class Initiator:
    """
    Initiates the visualization procedure
    """
    
    train_df = None       # train dataframe(descriptors+target) 
    test_df = None        # test dataframe(only descriptors)
    target = None         # target feature; string
    numericals = []       # numerical features
    non_numericals = []   # non-numerical features
    ratio = []            # ratio features
    ordinal = []          # ordinal features
    nominal = []          # nominal features
    interval = []         # interval features
    interval_sep = None   # interval sepearator
    output_loc = None     # location of outputs
    plotsize = None       # size of plots
    
    def __init__(self, train_df, test_df, target, feature_list, output_loc):
        """
        Constructor for the class
        
        Parameters:
            train_df (pandas dataframe): The train dataframe
            test_df (pandas dataframe): The test dataframe without target
            target (str): The target feature
            feature_list (tuple of lists): The different types of features in
                                           the dataset
            output_loc (str): Output location of the plots
        """
        
        self.train_df = train_df
        self.test_df = test_df
        self.target = target
        
        # the order of features from feature_list should correspond to the
        # order in PreProcessor.give_output() in preprocess_data.py
        self.numericals = feature_list[0]
        self.non_numericals = feature_list[1]
        self.ratio = feature_list[2]
        self.ordinal = feature_list[3]
        self.nominal = feature_list[4]
        self.interval = feature_list[5]
        self.interval_sep = feature_list[6]    # this is a character, not list
        
        self.output_loc = output_loc        
        self.plotsize = (8,6)         # default size of plots
        
    def max_cardinality(self, feature):
        """
        Maximum cardinality of a given feature across train and test datasets
        
        Parameters:
            feature (str): Feature whose cardinality has to be found
            
        Returns:
            Maximum of the cardinality of feature across train and test
            features
        """
        
        tr_card = len(list(self.train_df[feature].unique()))
        te_card = len(list(self.test_df[feature].unique()))
        
        return (max(tr_card, te_card))
        

class TrainTestCompare(Initiator):
    """Compare Data Distributions between train and test"""
    
    def __init__(self, train_df, test_df, target, feature_list, output_loc):
        """
        Constructor for the class
        
        Parameters:
            train_df (pandas dataframe): The train dataframe
            test_df (pandas dataframe): The test dataframe without target
            target (str): The target feature
            feature_list (tuple of lists): The different types of features in
                                           the dataset
        """
        
        super(TrainTestCompare, self).__init__(train_df, test_df, target,
             feature_list, output_loc)
        
    def compare_numericals(self):
        """
        Plots density plots to compare between the distribution of numerical
        descriptor features in train and test datasets
        """
        
        for feat in self.numericals:
            fig, axs = plt.subplots(1,1, figsize=(10,6))
            sns.kdeplot(self.train_df[feat], color='green', label='Train Data', 
                        shade=True, ax=axs)
            sns.kdeplot(self.test_df[feat], color='red', label='Test Data', 
                        shade=True, ax=axs)
            # label and save the plot
            fig.suptitle("Train-test distribution comparison of "+feat,
                         fontsize=20)
            figname = feat+'_train_test_compare.png'
            plt.savefig(os.path.join(self.output_loc,figname))
            #plt.show()
    
    def compare_non_numericals(self):
        """
        Plots countplots to compare between the distribution of non-numerical
        descriptor features in train and test datasets
        """
        
        card_overload = []   # features that have a cardinality of 13 and above
        
        for feat in self.non_numericals:
            
            try:
                if(self.max_cardinality(feat)<13):
                    fig, axs = plt.subplots(2,1, figsize=(20,10))
                    sns.countplot(data=self.train_df, x=feat, ax=axs[0])
                    sns.countplot(data=self.test_df, x=feat, ax=axs[1])
                    # label and save the plot
                    fig.suptitle("Train-test distribution comparison of "+feat,
                                 fontsize=20)
                    figname = feat+'_train_test_compare.png'
                    plt.savefig(os.path.join(self.output_loc,figname))
                    #plt.show()
                else:
                    card_overload.append(feat)
                
            except:
                continue
        
        if(len(card_overload)!=0):
            print("The following features have cardinalities > 12 and hence have",
                  "not been plotted. You may do so separately.")
            print(card_overload)
        else:
            pass
        

class RelWithLabels(Initiator):
    """Plots multiple features based on the target labels"""
    
    def __init__(self, train_df, test_df, target, feature_list, output_loc):
        """
        Constructor for the class
        
        Parameters:
            train_df (pandas dataframe): The train dataframe
            test_df (pandas dataframe): The test dataframe without target
            target (str): The target feature
            feature_list (tuple of lists): The different types of features in
                                           the dataset
        """
        
        super(RelWithLabels, self).__init__(train_df, test_df, target,
             feature_list, output_loc)
        
    def box_comp(self):
        """
        Plots box plots to compare numerical features
        """
        
        for feat in self.numericals:
            fig, axs = plt.subplots(1,1, figsize=(10,6))
            sns.boxplot(data=self.train_df, x=self.target, y=feat)
            # label and save the plot
            fig.suptitle("Box plot of "+feat,
                         fontsize=20)
            figname = feat+'_box_with_labels.png'
            plt.savefig(os.path.join(self.output_loc,figname))
            #plt.show()
            
    
class FinalPlotter(TrainTestCompare, RelWithLabels):
    """
    Final class to generate the plots
    [All data used are preprocessed data]
    """
    
    def __init__(self, train_df, test_df, target, feature_list, output_loc):
        """
        Constructor for the class
        
        Parameters:
            train_df (pandas dataframe): The train dataframe
            test_df (pandas dataframe): The test dataframe without target
            target (str): The target feature
            feature_list (tuple of lists): The different types of features in
                                           the dataset
        """
        
        super(FinalPlotter, self).__init__(train_df, test_df, target,
             feature_list, output_loc)
        
    def corr(self):
        """
        Seaborn pairplot
        """
        try:
            # train data
            sns.pairplot(self.train_df)
            figname = 'train_pairplot.png'
            plt.savefig(os.path.join(self.output_loc,figname))
            # test data
            sns.pairplot(self.test_df)
            figname = 'test_pairplot.png'
            plt.savefig(os.path.join(self.output_loc,figname))
        except:
            pass
    
    def plot_it_all(self):
        
        print("Commencing generation of plots...")
        self.compare_numericals()
        self.compare_non_numericals()
        self.box_comp()
        print("Finished generating all plots. You can view them at",
              self.output_loc)
        self.corr()
    
        

