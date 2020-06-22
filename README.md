# DataSwissKnife

A Handy Little Tool for your Data Science Operations

<p align="center"> 
   <img src="img/dsk_logo.png">
</p>

## Description
*Are you a data science beginner who wishes you had access to a tool that would help you watch data science in action **without writing code**? Or are you someone who understands the importance of data in your business, **but lack the technical grounding to code**? Or are you an expert-level researcher or data scientist who just wishes to do some preliminary analysis or build baseline models **without having to spend time writing code**?* 

If you fall into any of these categories, the DataSwissKnife project(abbreviated as DSK) will be of help to you. DSK is software that has been built with the purpose of aiding anybody who is familiar with necessary domain knowledge to do preliminary data science. The term **"domain knowledge"** signifies the relevant information a given user has with respect to the dataset he or she is analysing. The kinds of information a user needs to know about their the concerned dataset include:

* What is the data about? Why is the data being analysed?
* What features does the dataset contain? What are the expected data types of these features(i.e numerical or non-numerical)?
* Does the dataset contain outliers? If yes, which features do you think would contain outliers?
* And more...

DSK lets users load a raw block of tabular data onto it and by asking relevant questions about the kind of work the user wants to do with the data; DSK performs the operations of **data cleaning**, **pre-processing**, **auto-generating visualizations** and even some **preliminary baseline modelling**. *DSK only makes use of these question-response interactions with the user and thus helps users perform preliminary data science without having to write any code to do so.*

Fig. 1 describes how DSK works. 

<p align="center"> 
   <img src="img/dsk_block_diagram.png">
</p>

<p align="center"> 
    Fig 1. DSK Block Diagram
</p>

### Background - Why is this important?

There is no doubt that data science is one field that has recently seen a surge in the number of people who want to work in it. From school students to experienced professionals, everybody is trying to figure a way to enter this mercurial field born out of the confluence of multiple disciplines. However, it is no secret that like all fields, getting into data science and being able to leverage data science abilities for your business is not an overnight job. It takes time to learn and apply these concepts. This time space might be further extended if individuals lack the technical expertise to readily analyse data. The problem with this extended time space is that it *delays the ability of a person to see how impactful data science can be for his or her work.* 

In fig. 2, the different consumers of data science have been broadly categorized. 

<p align="center"> 
   <img src="img/data_science_consumers.JPG">
</p>

<p align="center"> 
    Fig 2. Consumers of Data Science
</p>

#### Beginners

**Who:** Individuals who are beginners in data science and are only interested in learning. They are not looking to solve a complete problem yet. Can be further classified into students and professionals looking to make a career transition.

**Main Problem:** They need to know too much of theory before being able to start real analysis or develop models.

#### Non-Data Technicals
**Who:** Individuals who do not have a background in technical knowledge for data science, but are eagerly looking forward to using it for improving their businesses or for other purposes. They have the necessary domain knowledge they require.

**Main Problem:** They do not have the expertise to write code and neither do they have a lot of time to spare for learning how to write code.

#### Data Technicals

**Who:** Individuals with complete in-depth understanding of data science. They might be working professionals or working in academia. They know how to write code and are technically sound.

**Main Problem:** Data cleaning, generating preliminary baseline models, creating basic reports etc. becomes time-consuming and rather cumbersome. They will appreciate it if provided with a mechanism to automate these tasks(if not completely, at least partially).

### The Idea of DSK as a Solution

The gravity of the problem statement at hand calls for a new approach to data science. If data science has to be made simpler and easier for quickly generating essential results(without having to write code), full or partial control has to be transferred from the hands of the user to the system itself. In other words, *the system has to be automated.* Therefore, DSK is an attempt at setting the foundations for a system that will work in automated fashion to help users perform preliminary data science operations without writing code. Currently, DSK is prototypical and will be scaled to a full product in the future iterations of this project.

## Usage 

### Suggestion
It is recommended you download and run this project within a virtual environment, in order to ensure that the package installs do not tamper with the versions present in your system. The following links will help you learn why and how to use virtual environments in python.  
* http://www.python.education/2017/10/setting-up-virtual-environment-in-python.html (For Windows users)
* https://realpython.com/python-virtual-environments-a-primer/

### Instructions to run the tool

1. Download or clone this repository onto your local system

2. Extract the repository's contents

3. Navigate to the repository via the command line

4. Run the following command to install all necessary dependencies

   ```bash
   pip install -r requirements.txt
   ```

5. Run the following command to start the tool 

   ```bash
   python dataswissknife/main_code.py
   ```

   To avoid warnings being displayed, run with

   ```bash
   python -W ignore dataswissknife/main_code.py
   ```

6. The tool should start in your command line. Follow the prompts.

## Caveat 

While DSK will help with some very basic operations, we do not make a claim that DSK can replace efficient ways of learning and using data science i.e by writing code. Therefore, if you are a data science aspirant, we strongly urge you to continue learning your concepts and use DSK as a tool to help you generate some quick results.

## Support
DSK is a project that our team has worked on as a part of our final year project in our CSE undergraduate degree. Since we are making an attempt to deal with making data science more accessible and easy for everyone, we would strongly encourage the community's support in making DSK better and more user friendly with every future version.

In case of queries, suggestions or concerns, please feel free to reach me at *yadramshankar@gmail.com*

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) 
