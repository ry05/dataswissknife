# Explanation of Data Flow through DSK

First, the user **obtains** raw data. This raw data is expected to be in a tabular format and if it is to be used for supervised classification, it should have both descriptors as well as the target feature. The user then **loads** this data onto the DataSwissKnife program. From here, the system-user interaction begins. The first step is for the program to ask the user to **choose a directory** in his or her local system where all the contents and results of the execution of the program will be stored. Once this has been decided, the program **creates a structure** in the user designated directory. After this, the program **starts asking questions** to the user that will be based on what the user wants to do with the data. *For example, the program can ask the user the action he or she would like to take up to deal with missing values in a given feature.*

The program also **provides suggestions** where possible. It **performs corresponding actions on the data** based on the user’s responses. After all data operations(cleaning and preprocessing), the **final outputs are stored** in the project’s directory(chosen earlier by the user) as raw data, cleaned data and preprocessed data. 

The preprocessed data is **passed onto the model** training section. The program also **generates visualizations and reports** from the data provided and also the intermediate outputs.

*NOTE: The auto-generated visualizations are still in rudimentary nature and will be enhanced in the future.*

## Dissecting DSK's Operation

The aim of this section is to dissect the *DataSwissKnife* system and provide low-level details of how each component works. 

For the sample depicted here, the train.csv file of the [Titanic dataset](https://www.kaggle.com/c/titanic/data) has been used.

### Create Structure in the Host’s System
The first action performed is to create a hierarchical directory structure within the user’s computer system. The user can choose the location where he or she wants to place this project structure (as in fig 3). The *ROOT* name or the name of the project has to be set by the user. 

<p align="center"> 
   <img src="https://lh3.googleusercontent.com/UE3-UcERE1-DHq37bS3kJmHsWtAtXbzWF4WNIX3XoFxOXrFwS0FJau_R-KgX9mnTt09iVHlQrm4W7q_AHfrw9me2oAnRvxon9QXMCoFnRlBE2NrCr2ZJ8zfkHgN7e-7HigQ6YCf_">
</p>

<p align="center"> 
    Fig 3. Project Structure in the Host’s System
</p>

The subdirectories are data, visualizations, models and reports. The *data* subdirectory is further divided into *raw*, *clean* and *processed.* Raw has the original copy of the dataset, clean has the cleaned copy and processed has the data that is ready to be passed into an ML model. 
*Visualizations* contain the auto-generated visualizations from data and models has the machine learning models as .pkl files. Finally, *reports* will contain basic, preliminary reports of the data and analysis performed.
The importance of this step is that it makes the results reproducible. This means that the user can access cleaned and preprocessed intermediaries of the dataset, visualizations and basic models at a later stage without having to run this whole program again. 

<p align="center"> 
   <img src="https://lh3.googleusercontent.com/I8-oa_yDuJPaBC4gTXwaheq7e1x7YaJx33Fi2-i_mHxiQVHA4LwiWaArC2HOWAsYGB8nTp-9lVKIFhpXw83_c041y9zZEn4v7VhBPX2BB9nUa3w_T1zPpXaVezeoQva2HQZuBtFo">
</p>

<p align="center"> 
    Fig 4. Choosing the location to place the project directory
</p> 

<p align="center"> 
   <img src="https://lh6.googleusercontent.com/hQtVpAn7on9lDy1kpXd2br72k-tQ-DtojvkxW5Po-wFdhHnjFhl7dRyG7ohsjInuYFkZWuXIoskLMXirBAtPK8SF9SCMnxz8CQxsFncXuiH4zIeGRYa-Z76XpJErX6GJFEgkXg8o">
</p>

<p align="center"> 
    Fig 5. Naming the project directory; The project directory is created in the system and the path is provided
</p> 

### Load Data
After the project structure has been made, the next step is to load the data. As of its first version, DataSwissKnife only supports .csv files. It is expected that the user already has the dataset in his local system. When this dataset is loaded onto the project through DataSwissKnife(DSK), a copy of this is stored in *root/data/raw.*

<p align="center"> 
   <img src="https://lh5.googleusercontent.com/nDtxYf9-R7jCoZS1A4ACkYOmEm52Aem-EmvXxGxl5SB5iTWULyDRwewpFty6SlZaldm7HTuXHnpmpXBF4GkGVarCMDjcJzHSOD9AXPI7G6fvieSydLIzLLkz1VtiAS5Unqo0nNlV">
</p>

<p align="center"> 
    Fig 6. Choosing the dataset from the user's local system
</p> 

<p align="center"> 
   <img src="https://lh6.googleusercontent.com/urBczB1F2-0qwMd1mFzavrE4QuA0RduXjNreV3VUmSxBenXNq-Rvy41mYxRqfPDIcSqCKZ9Wcfq7hM0MQrgc6IIvm4tkHeS-bIqqVnoaqZhnm5DnVSVQAGkTJW3fJ4dpLdFYg6by">
</p>

<p align="center"> 
    Fig 7. Output after loading and renaming the dataset; a preview is generated
</p> 

### Clean Data

This block is concerned with cleaning up the data. A series of questions are asked by DSK and based on user response, the data is cleaned. DSK also performs some preliminary cleaning at the start as soon as it receives the data(without user intervention) and these automated cleaning steps are:

* Rename column names such that there are no spaces in the names and all characters are lowercase
* Remove columns that have only a single value for every instance
* Remove empty columns and rows
* Round of decimal values to 3 decimal places
* Remove duplicate rows
* Remove trailing and leading spaces for values

The other cleaning steps are dealing with missing values and consistency checkers. DSK asks questions to the user, which have one word answers. Based on user responses, cleaning is performed.

<p align="center"> 
   <img src="https://lh5.googleusercontent.com/644QhW3eTM4hO52vEg9MsSjdKkBo7bSw0OXWs1c_OVIEpQoWBW8Nwpy9zo3iBpziByDXI3z8LGkFuJO2MWummAcn4tRP7fooSAiGTVVsf9wkjHI-Uy3eT3zIzm_ydplZCPyCV5Ue">
</p>

<p align="center"> 
    Fig 8. The initiation of Data Cleaning
</p> 

<p align="center"> 
   <img src="https://lh4.googleusercontent.com/9C8BgfyY-2iAJOPqQv8VBrXlr2iTPn1unH-0wFIzpgkcZguxbDbHmdnocee9e6fPcepa3p62EPuxcO18_hV0TwIjRBRmS_ebFVHfe__AIfUSG_-Obci0GRABQkx96zGqyoi_A3zB">
</p>

<p align="center"> 
    Fig 9. Missing value percentages in the data
</p> 

<p align="center"> 
   <img src="https://lh6.googleusercontent.com/azEAhx--cnvQ8eU_Y8SXNvf2ctNHZULlTyHkBvkvKjUmajILGi8pVRClmBQWk5kZWF-H-jdfeoMfKjZXFKRM0eQnWbCucMGZ2n9JdphD7Hbir3FpeuQ46NGS-dS5uackBycn8iJ7">
</p>

<p align="center"> 
    Fig 10. Missing value percentages in the data after removing features with more than 60% as missing values
</p> 

<p align="center"> 
   <img src="https://lh4.googleusercontent.com/U-eDRdzZU5EIzSBxtsvN7hCq5Xj1UhxDvZbEF78cTXBLCIl6HK7QZuHeeri1Gh4-hzDtjcYK0nE2AtNij5Fpr2TK2oToB-RG81ui5ukRmT58f6_99Of0W36xPTxVfLl7CDjC66ir">
</p>

<p align="center"> 
    Fig 11. Performing imputation to fill in the remaining missing values
</p> 

<p align="center"> 
   <img src="https://lh4.googleusercontent.com/bZNeCg7ci0Aa_MFEmRdqh41p5E7YxTvhUB4HWNTU2HNvDSMxgXCodRnJS_KvnUP0c5S_gv1zbcfFEeuYMyurBiCMP03x5uE7RZtp5aZuStHdpJkRm20LxqhbZMl2WhQ35mhfvJjT">
</p>

<p align="center"> 
    Fig 12. All missing values have been dealt with
</p> 

Another step of data cleaning is to check for datatype inconsistencies. A data type inconsistency occurs when a feature is in a datatype that does not facilitate analysis that the user would like to do. An example of this is when a feature like money is encoded as a non-numeric type(i.e object in pandas) because of entries like “50\$”. In such a case, DSK’s datatype inconsistency dealer module will first identify these inconsistencies based on the user’s responses to how he or she would prefer a feature to be (numeric or non-numeric) and checks these against the actual types with which these features have been encoded. After identifying inconsistent features, DSK flags off non-numeric characters. In our example of money, “​\$” is a non-numeric character. DSK flags this off and provides the user with an opportunity to remove these values from the data. After removing “$” symbols, we can see that our money feature can now be converted into numeric type easily. If there are no inconsistencies, then that too is informed to the user (fig 13).

<p align="center"> 
   <img src="https://lh6.googleusercontent.com/Tm4-ivTjG57Qj01II3QPtdT1b3L-3psk8VRGNJzhFDdsW_Ql2Kn3YLktL5xa1zPehUTlblGraoJz_hubCG60g0VIPZhj8k0DwlkkqYpjjXWQ8nGI5A3_EK0QPI_4PAjafsM8mpxH">
</p>

<p align="center"> 
    Fig 13. Datatype consistency management
</p> 

After this step, the clean data is stored in *root/data/clean*

### Preprocess Data
Data preprocessing concerns itself with converting clean data into a format more suited for machine learning modelling. So far, the data has only been a single .csv file with both descriptors and target features together. In preprocessing, a series of steps are performed that convert this single .csv file into train.csv, test.csv(has test data descriptor values) and test_solution.csv(has test data target values). *80% of the original data is maintained as the train set and 20% is maintained as the test set.*

Initially, these 3 files are stored in *root/data/clean*. But after all preprocessing steps, the preprocessed versions of these 3 files are stored in *root/data/processed*. 

<p align="center"> 
   <img src="https://lh4.googleusercontent.com/qNWZV73LJJTLShq7eXZrvsq0oADoe45mHXwq8o1I1Kobv5LpoclNpdFwjEIHpjcOgjEQbLGqf-qXKj5aMDxnW84EgHu46FcC_wAPHJcn6-J61ayldLYXvUU6E2k9vro367ie28_u">
</p>

<p align="center"> 
    Fig 14. Prompts to enter the target
</p> 

Steps performed are

* Automatically detect identifier features(unique for every instance in the dataset) and remove them
* Detect features with more than 70% values as unique and ask the user if he or she wants to keep these values or remove them
* Interact with the user to identify the specific data type for each given feature. 
  * Asks if feature is **ordinal**
    * If response is no
      * If feature is numerical, the feature is of **ratio** type
      * If feature is non-numerical, asks if feature is **interval** type
        * If response is no, feature is **nominal**
        * Else, feature is **interval**
    * Else, feature is **ordinal**

<p align="center"> 
   <img src="https://lh3.googleusercontent.com/FpIquAS3sFIOOV0PfimNolKytNVDf6QqN9afZgk0M3pqCWNFHnvss9bKlEu7uL53xGw8YYWsT4PrrYyft-Ez53_6NQhiSDjaKzo5mfhGJU47s3RXQxm_7pkwdsapcGo81ZiDkBJk">
</p>

<p align="center"> 
    Fig 15. Interact with the user to choose feature types
</p> 

Interact with user to identify the features from which the user will like to remove outliersNormalize features as per user’s requirement. Currently, only one-hot encoding is performed for nominal features. Label encoding will be performed only for ordinal features(if any)

<p align="center"> 
   <img src="https://lh5.googleusercontent.com/YFc-oBKbwMaTlosUIYcVXc-Mwtj3o9F7fgRVNjnPHqUQoNOq96vQV4APdxJ5NvglrF-3120FsPdFuy--E_eIOKU19fn3Aqs9FV3h_uS4OCFd83DyYL4dTekJiKhDh1e6oIolLPrp">
</p>

<p align="center"> 
    Fig 16. Other preprocessing steps with the help of user input
</p> 

### Visualize Data

DSK auto-generates visualizations based on the data it has. Currently, only density plots, box plots and count/frequency plots are generated.

<p align="center"> 
   <img src="https://lh5.googleusercontent.com/vAX2zY3RNHqKfKRdqdMKniLJlt-vQ1_a4SN3JFni_qxVSUibG80wcq8xxvOw8nNdd1wD2ZXETbHCKWWW5JeNJDLX2uPi6sqP2E7PqsDQTCKJBvl0_SH3NPNLFsZKRag87R7E4nHd">
</p>

<p align="center"> 
    Fig 17. Data visualization
</p> 

<p align="center"> 
   <img src="https://lh4.googleusercontent.com/9JbtTTgTTCH5rDOxWD5Dfj63eoC4Y5DmVsAucYuUBAfbQClvxDqNwNd5bjS7mFDfnJ8C3o8HoxVDmG0jWWqElTT-tVgGeN9AsMC8sek971AN4aBF9C_6aGmEwI_AJ357tD9-beBF">
</p>

<p align="center"> 
    Fig 18. Auto-generated plots
</p> 

### Model Data
DSK performs supervised classification. It takes the pre-processed datasets and builds baseline models and evaluates the models using a 10-fold stratified cross validation strategy. The baseline models are built on the following algorithms

* Logistic regression
* Decision Trees
* Random Forests
* K Nearest Neighbours
* Support Vector Machines 

DSK first fits and evaluates on the train.csv file. After it produces the results for the same, the user is provided an option to choose which model he or she would like to store and use on the test.csv file. Based on the user’s choice, a particular model estimator is saved in *root/models*.


<p align="center"> 
   <img src="https://lh3.googleusercontent.com/XFxp9qr3qt1-qxLBB7VrEeCA2zP2dSFHX0LfKilt4jBRGHv3NHFZ1JsHS6MMgmw6fXRjyZOe06IeET7SAMOrwHCa-ev4mtVNUlzwsWn0Llvxjr0F-SYXXW_QnaecuO-qtXHqjMQS">
</p>

<p align="center"> 
    Fig 19. Baseline model results
</p> 

The **Report results** block will be implemented as a part of this project’s future work.

We encourage you to try this out with other datasets and see DSK in action for yourself!
