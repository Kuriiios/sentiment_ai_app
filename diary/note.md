## Application

1 - Conception
2 - Developement / Research (notebooks)
3 - Production (code and test)
4 - Monitoring
##### Developement / Research (notebooks)
  - eda of database
  - discover nltk
  - creating routes
  - creation of modules

##### Production (code and test)
  - Setup of app
  - creating pages

# Step of project
- create working directory
- create files
  - venv (virtual environment with libraries)
  - env
  - README.md
  - requirements.txt
  - .gitignore
- separation of architecture
  - folders
    - API
    - API_IA
    - APP
  - layer of architecture
    - slice by modules
    - slice by models
    - slice by data

## Logic and steps
**APP**
-   import libraries
-   load env variable
-   create pages
    - root
        - ping the api ex:`Hello Word`
        - transaction get with route`'/'`
    - insert
      - form to insert data
      - transaction post with route `'/insert'`
      - catching exceptions
    - display
      - display dataframe with all data from database
      - transaction get with route `'/read'`
      - catching exceptions
    - search
      - options for retriving method (random, by id, by id mine) 
      - transaction get with route (`'/read/random'`, `'/read/{id}'`, `'/read_ids', '/read/{id}'`) 
      - return quote
      - display analyze button
        - retriving and formating quote
        - transaction post with route `'/analyse_sentiment'` 
        - return sentiment
          - display polarities
          - display compound

**API**
- import libraries
- load env variable
- define pydantic models
- define logs
- create api
    - define routes
      - main route -get 
        - hello word
      - insert route - post 
        - generate Class object
        - write object in database
        - query object to database
        - return object
      - read route -get
        - read all database
        - return list comprehension of rows
      - read id route -get
        - read all id database
        - return list comprehension of rows
      - read per id -get
        - read all database
        - select only row with id
        - return content of row
- logic launch APP
  - initalize database
    - create database if not exist
  
**Default Model**
```
Decorator / HTML requests / Response Model
Function / Request Model
    Try
        Call db_tools function
        Log infos/sucess
        return result of function 
    Exception
        Log error
        Raise HTTPException
    Finally
        Close every temporary Session
```


**API_IA**
- import libraries
- load env variable
- define pydantic models
- define logs
- create api
    - define routes
      - main route -get 
        - hello word
      - analyse sentiment route - post 
        - analyse text with SIA
        - return sentiment dict
- logic launch APP
  
**Default Model**
```
Decorator / HTML requests / Response Model
Function / Request Model
    Try
        Call db_tools function
        Log infos/sucess
        return result of function 
    Exception
        Log error
        Raise HTTPException
    Finally
        Close every temporary Session
```

**test**
- test backend api ia
  - import libraries
  - test analyse sentiment
    - create exemple of quote
    - create exemple of SIA output
    - compare result of SIA and output of function
- test backend api
  - import libraries
  - test root
    - compare output of root function status code with return from server
  - test read
    - compare output of read function status code with return from server
- test backend orm
  - import libraries
  - create fixtures
    - create function for test engines
    - create function for test of setup of database
      - create tables
    - create function for test db session
      - 

## Architecture
```
mon_projet/
├── API
│   ├── __init__.py
│   ├── logs
│   │   └── main.log
│   ├── modules
│   │   ├── __init__.py
│   │   └── db_tools.py
│   ├── data
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── models.py
│   │   └── quotes_db.db
│   └── main.py
├── API_AI
│   ├── logs
│   │   └── sentiment_api.log
│   └── sentiment_api.py
├── APP
│   ├── app.py
│   └── pages
│       ├── 0_insérer.py
│       ├── 1_Afficher.py
│       └── 2_search.py
├── DEV
│   └── dev.ipynb
├── tests
│   ├── test_backend_api.py
│   ├── test_backend_orm.py
│   └── test_initiation.py
├── README.md
├── .env
├── .venv
└── .gitignore
```