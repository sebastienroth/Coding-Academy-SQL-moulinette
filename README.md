# CODING MOULINETTE SQL

Python Moulinette: SQL Days 1 and 2 in coding_academy

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
1. Clone the repository
2. You can now execute the script using ``python3 sql-mouli.py``

or 

2. `chmod +x sql-mouli.py` and execute `./sql-mouli.py <reference_folder> <tested_folder>`

## Usage

`./sql-mouli.py <reference_folder> <tested_folder>`

### To test all the projects: !!Not Tested:

`./sql-mouli.py <folder_de_rendu>`

    rammassage/
        project1/
            ...
        project2/
            ...
        project3/
            ...
        project4/
            ...


### Prerequisites

This script will make call to `mysql -u root --password=root coding -e "sql_statement"`

MySQL must be installed and configured, you need to add the sql database, `coding.sql` to your mysql databases

`mysql -u <username> -p < coding.sql` if tested on localhost

This script works with python3 you can download it and install it. 
```
https://www.python.org/downloads/
```
This script use os, sys, difflib and subprocess python modules


## Authors

* **Julien Aldon** - *Initial work* - [Julien Aldon](https://github.com/JulienAldon) for coding-academy.

