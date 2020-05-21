"""
from colorama import init
init()
start = "\033[1;31m"
end = "\033[0;0m"
print ("File is: " + start + "<placeholder>" + end)
"""

from colorama import Fore, Back, Style, init
from termcolor import colored
init()
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')

# then use Termcolor for all colored text output
print(colored('Hello, World!', 'white', 'on_red'))

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


print(r""" 
  __               _       _                      _                        __                           
 (_ _|_  _  ._    / \ o   /  ._ _   _. _|_  _    |_) ._ _  o  _   _ _|_   (_ _|_ ._     _ _|_     ._ _  
 __) |_ (/_ |_)   \_/ o   \_ | (/_ (_|  |_ (/_   |   | (_) | (/_ (_  |_   __) |_ | |_| (_  |_ |_| | (/_ 
            |                                             _|                                            
 Create the structure of your project in your local system
""")
print(colored('Instructions :', 'white', 'on_blue'))
print("1. Choose a directory in your system in which you want the project structure to be built\n",
      "2. Enter the name of your project's root directory\n")

print()
print(colored('Outputs :', 'white', 'on_green'))

 
print(r""" 
  __                      _                                         
 (_ _|_  _  ._    /| o   | \  _. _|_  _.   |   _   _.  _| o ._   _  
 __) |_ (/_ |_)    | o   |_/ (_|  |_ (_|   |_ (_) (_| (_| | | | (_| 
            |                                                    _| 
 Load the dataset for the project
""")
print(colored('Instructions :', 'white', 'on_blue'))
print("1. Choose the .csv dataset from your system\n"
      "2. Rename your dataset\n")

print()
print(colored('Outputs :', 'white', 'on_green'))

print(r""" 
  __              _       _                 _                         
 (_ _|_  _  ._     ) o   | \  _. _|_  _.   /  |  _   _. ._  o ._   _  
 __) |_ (/_ |_)   /_ o   |_/ (_|  |_ (_|   \_ | (/_ (_| | | | | | (_| 
            |                                                      _| 
 """)

print(r""" 
  __              _       _                 _                                         
 (_ _|_  _  ._    _) o   | \  _. _|_  _.   |_) ._ _  ._  ._ _   _  _   _  _ o ._   _  
 __) |_ (/_ |_)   _) o   |_/ (_|  |_ (_|   |   | (/_ |_) | (_) (_ (/_ _> _> | | | (_| 
            |                                        |                             _| 
 """)


print(r""" 
  __                        _                                                           
 (_ _|_  _  ._    |_|_ o   | \  _. _|_  _.   \  / o  _      _. | o _   _. _|_ o  _  ._  
 __) |_ (/_ |_)     |  o   |_/ (_|  |_ (_|    \/  | _> |_| (_| | | /_ (_|  |_ | (_) | | 
            |                                                                           
 """)

print(r""" 
  __               _                                     
 (_ _|_  _  ._    |_  o   |\/|  _   _|  _  | | o ._   _  
 __) |_ (/_ |_)    _) o   |  | (_) (_| (/_ | | | | | (_| 
            |                                         _|    
 """)

print("Message Format:\n")
print("Welcome =>",colored('Welcome Message', 'cyan'))
print("Operation Headings =>",colored('OPERATION SUBHEADING', 'blue', 'on_white'))
print("Operation Headings =>",colored('OPERATION HEADING', 'blue', 'on_cyan'))
print("Error =>",colored('Error Message', 'white', 'on_red'))
print("3.",colored("train.csv", 'cyan'),"contains both descriptor and target features")
print("4.",colored("test.csv", 'cyan'),"contains only descriptor features")
print("5.",colored("test_solution.csv", 'cyan'),"contains only target features of"
      "",colored("test.csv", 'cyan'))


