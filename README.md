# Welcome to `dsdb`

> Dsdb is a [Buildnn](https://www.buildnn.com) open source project.

Tired of having to manage thousands of unstructured .csv outputs for your small Data Science experiments? Would you like to experience a real SQL-like data management of yout datasets with a real database? 

Take a look at what you can do with [Postgres](https://www.pgadmin.org/screenshots/#7).

Give a boost to your data management skills with `DsDb` (**D**ata **S**cience **D**ata**B**ase).

## Contents

1. [Basic usage of `DsDb`](#markdown-header-basic-usage-of-dsdb)
2. [Quickstart with docker-compose](#markdown-header-quickstart-using-docker-compose)
3. [Pip Installation](#markdown-header-pip-installation)
4. [Connection to a custom DB server](#markdown-header-connection_to_a_custom_db_server)

## Basic usage of `DsDb`

Push a table from pandas to postgres with Just:

```python
from dsdb import DsDbConnect
import pandas as pd

# Load some data or take a DataFrame you analyzed
df = pd.read_csv('my-ugly-file.csv')

with DsDbConnect() as con:
    df.to_sql_table('table', con=con, if_exist='append')

```
and... that's it.


## Quickstart using docker-compose

The following workflow launches a dockerized `jupyter` server with an underlying db.
Firs, retrieve our pre-made `docker-compose.yml` file: 
```bash
$ cd my-project-dir
$ wget https://bitbucket.org/buildnn/dsdb/raw/23b3ff150ef9cd2398e6098eeba2a7d912983f7e/docker-compose.yml
$ wget https://bitbucket.org/buildnn/dsdb/raw/8088845bc9d96f60bcd9398d61609c82b8fb09bb/notebooks/dsdb_test.ipynb
$ touch .env
```

open the `.env` file and place the following text, filling the `{text under curly brackets}` as suggested:

```
# content of .env file
DSDB_USER=datascientist  # you can change this value
DSDB_PASSWORD={your password}
DSDB_DB=dsdb  # you can change this value

POSTGRES_USER=admin  # you can change this value
POSTGRES_PASSWORD={your db password}
POSTGRES_DB=mydb  # you can change this value

PGADMIN_DEFAULT_EMAIL={your email}
PGADMIN_DEFAULT_PASSWORD={another different password}
```
And then start the game
```
$ docker-compose up
```

And... **that should be it**.

Visit:
* `https://localhost:8888` to see jupyter
* `https://localhost:5050` to visit the pgadmin panel (use the credentials in .env)


## Pip Installation

To pip-install this repo:
```bash
$ pip install git+https://bitbucket.org/buildnn/dsdb.git
```

## Connection to a custom DB server 

`dsdb.DsDbConnect` uses a `DsDb`
object to connect to your db. It loads some
**environment variables** and uses them to perform
the connection. these are
* `DSDB_USER`: your username in the DB
* `DSDB_PASSWORD`: your password to access the DB
* `DSDB_DB`: The name of the DB 
* `DSDB_HOST`: The address of the DB server
* `DSDB_DRIVER`: The driver. E.g. `'postgres+psycopg2'` for a standard postgres. 

The following is a quick way to create
them directly inside yout python script:

```python
import os

os.environ['DSDB_USER'] = 'myuser'
# prompt a password input (never write pass explicitly!)
os.environ['DSDB_PASSWORD'] = input('password:')
os.environ['DSDB_DB'] = 'mydb'
os.environ['DSDB_HOST'] = 'localhost:5432'  # server address
os.environ['DSDB_DRIVER'] = 'postgres+psycopg2'

...
``` 

another option is to create a custom `dsdb.DsDb` object
to pass to `dsdb.DsDbConnect`:

```python
import dsdb

db = dsdb.DsDb(
    usr='myuser',
    pwd=input('password:'),
    db='mydb',
    host='localhost:5432',   # server address
    driver='postgres+psycopg2',
)
with dsdb.DsDbConnect(db=db) as con:
    df.to_sql_table('table', con=con)
...
``` 