# API/modules/db_tools.py

## import libraries
-   sqlalchemy
-   own data 
-   loguru
-   os

## Create Database

Define path
Define engine and give it the path
Create sessionmaker with engine

## Functions use in main file

###### Functions to access db session with result from sessionmaker

###### Read Database
```
Read Database():
    Open session:
        select rows from database
        change format to fit needed format
        return selection
```

###### Read id in Database
```
Read id in Database():
    Open session:
        select ids in rows from database
        change format to fit needed format
        return selection
```

###### Add row into Database
```
Add row in Database():
    Open session:
        Create object type Row
        Add object to session
        Commit session
        Get row with injected data from database
        return row with injected data
```

###### Create Database if needed
```
Create Database():
    If database exist:
        Show message that say database exist
    Else:
        Show message that say database not found
        Create tables from database files
        Create sessionmaker from engine define at the beginning
        Show message show path of db and explain creation
```

