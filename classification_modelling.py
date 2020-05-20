"""
Module Classification Modelling
===============================
This module is concerned with classification tasks in machine learning
"""

import pandas as pd

# eval metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score

# modelling
from sklearn import linear_model, tree, ensemble, neighbors, svm
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_validate


class Baseline:
    """
    Performances of sklearn classifiers with default arguments
    """
    
    # baseline models
    baseline_models = {
        "logistic regression":
            linear_model.LogisticRegression(random_state=42),
        "decision tree":
            tree.DecisionTreeClassifier(random_state=42),
        "random forest":
            ensemble.RandomForestClassifier(random_state=42),
        "k nearest neighbours":
            neighbors.KNeighborsClassifier(),
        "support vector machine":
            svm.SVC(random_state=42),
        "gradient boosting classifier":
            ensemble.GradientBoostingClassifier(random_state=42)
    }
        
    X_tr = None          # Train descriptors
    y_tr = None          # Train target
    X_te = None          # Test desciptors
    y_te = None          # Test target
    
    SEED = 42            # seed value for cross validation
    
    model_df = None      # dataframe with model informations post training
    model_names = []
    acc = []
    f1 = []
    prec = []
    rec = []
    fit_times = []
    score_times = []
    estimators = []      # model estimators
                
    
    def __init__(self, X_train, y_train, X_test, y_test):
        """
        Constructor for the class
        
        Parameters:
            X_train: Train dataset descriptors
            y_train: Train dataset target
        """
        
        self.X_tr= X_train
        self.y_tr = y_train
        self.X_te= X_test
        self.y_te = y_test
        
    def train_it(self):
        """Train the algorithms"""
        
        # cross validation folds
        cv_folds = 10
        
        # initialising empty lists for storing model related info
        
        for model in self.baseline_models:
            self.model_names.append(model)
            kfold = StratifiedKFold(n_splits=cv_folds, random_state=self.SEED)
            cv_results = cross_validate(self.baseline_models[model], self.X_tr, self.y_tr, cv=kfold,
                                        scoring=('accuracy', 'f1_micro', 'precision_micro',
                                                 'recall_micro'),
                                        return_estimator=True)
            # update model info
            self.acc.append(cv_results['test_accuracy'].mean())
            self.f1.append(cv_results['test_f1_micro'].mean())
            self.prec.append(cv_results['test_precision_micro'].mean())
            self.rec.append(cv_results['test_recall_micro'].mean())
            #roc_auc.append(cv_results['roc_auc'].mean())
            self.fit_times.append(cv_results['fit_time'].mean())
            self.score_times.append(cv_results['score_time'].mean())
            self.estimators.append(cv_results['estimator'][0])
            
        # make the dataframe
        self.model_df = pd.DataFrame({
                'Name of Model':self.model_names,
                'Accuracy':self.acc,
                'Precision':self.prec,
                'Recall':self.rec,
                'Time to fit model':self.fit_times,
                'Time to predict on test split':self.score_times
        })
               
    def choose_model(self):
        """
        Choose the model
        """
        
        ind = int(input("Enter the index of the model that you prefer to "
                        "use on the test data:"))
        model = self.estimators[ind]
        preds = model.predict(self.X_te)
        acc_score = accuracy_score(self.y_te, preds)
        
        print("Model Accuracy on Train Data:", self.acc[ind])
        print("Model Accuracy on Test Data:", acc_score)
        
        if(self.acc[ind] > acc_score):
            print("Train accuracy is greater than Test accuracy. Therefore,",
                  "there is a chance of overfitting")
            
        return model
    
    def disp_it(self):
        """
        Display the models
        """
        
        self.train_it()
        
        print('Simple Model Accuracies with Cross Validation(K=10):\n')
        print(self.model_df.head())
        
        # provide option for user to choose preferred model
        # use that to train
        model = self.choose_model()
        
        # return the model
        return model
        