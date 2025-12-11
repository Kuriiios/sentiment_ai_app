# API/main.py

## import libraries
-   fastapi
-   uvicorn
-   pandas
-   pydantic
-   loguru
-   os
-   dotenv
-   typing
-   random
-   own modules

## define variables

- Load environment variables

- Create DTOs

- Create FastApi app

- Log PATHs

- Define logs

## FastApi Routes

#### Default Model
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
#### Routes
- [Root response of API call](#default-model)

- [Call function to insert data into database](#default-model)

- [Call function to read every rows of database](#default-model)

- [Call function to read every id in rows of database](#default-model)

- [Call function to read row with defined id in database](#default-model)

- [Call function to read a random row with randomly generate id in database](#default-model)

## Define uvicorn parameters
-   port
-   url
## Run Uvicorn APP
-   route
-   host
-   port
-   extra parameters