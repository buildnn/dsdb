# Welcome to `dsdb`

> Dsdb is a [Buildnn](https://www.buildnn.com) open source project.

Tired of having to manage thousands of unstructured .csv outputs for your small Data Science experiments? Would you like to experience a real SQL-like data management of yout datasets with a real database? 

Take a look at what you can do with [Postgres](https://www.pgadmin.org/screenshots/#7).

Give a boost to your data management skills with `DsDb` (**D**ata **S**cience **D**ata**B**ase).


## Idea

The workflow to launch a dockerized `jupyter` server with an underlying db will be like:

```bash
$ docker-compose up
```
And... that's it. We will package db creation with docker (coming very soon, just wait a bit) and hidden integration of dsdb with no hassle.

## Contents

1. [Basic usage of `DsDb`](#Basic_usage_of_DsDb)
2. [Install](#Install)
3. [Connection to a custom DB server](#Connection_to_a_custom_DB_server)



## Basic usage of `DsDb`

Push a table from pandas to postgres with Just:

```python
import dsdb
import pandas as pd

# Load some data or take a DataFrame you analyzed
df = pd.read_csv('my-ugly-file.csv')

with dsdb.DsDbConnect() as con:
    df.to_sql_table('table', con=con)

```
and... that's it.



## Install
```bash
$ pip install git+git@bitbucket.org:buildnn/dsdb.git
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