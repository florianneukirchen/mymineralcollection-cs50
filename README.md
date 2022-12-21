# Mymineralcollection
Mymineralcollection is a webapp for mineral collectors using python, flask, and javascript. It is my final project of the [CS50 Introduction to Computer Science](https://www.edx.org/cs50) online course from Harvard / edx. My app allows registered users to manage, browse and search their mineral collection. It uses a database with (almost) all IMA approved minerals (data from from [https://rruff.info/ima/](https://rruff.info/ima/)) to automatically show chemistry, crystal system etc. 

## Requirements
- cs50
- Flask
- Flask-Session
- PIL
- sqlite3

## Create Database
A clean database should be included in the repository.

If the database mineralcollection.db does not exist, it can be created with the script `createdb.py`. A CSV file with mineral data is required that can be downloaded from [https://rruff.info/ima/](https://rruff.info/ima/). Be sure to include "Mineral Name (plain)", "Chrystal Systems", "IMA Chemistry (HTML)", "Chemical Elements", "Fleischers Groupname", "IMA Mineral Symbol" in your export options and save the file as minerals.csv. Note that some newly approved minerals that don't have a offical IMA symbol yet are skipped.

## Database scheme
The database uses 6 tables:
- minerals
- users
- specimen
- specmin
- tags
- images

The specimen table contains the data of the mineral specimen. Since one specimen can contain several minerals, the table specmin is needed to link specimen to minerals. The minerals table contains the mineral data of all approved minerals. It uses the official IMA mineral symbol as primary key, in order to allow updates of the mineral data without breaking database relations.

The database scheme is:

``` sql
CREATE TABLE minerals (
    symbol TEXT, 
    name TEXT NOT NULL, 
    chemistry TEXT, 
    elements TEXT, 
    crystal_system TEXT, 
    fleischer TEXT, P
    RIMARY KEY(symbol));
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, 
    hash TEXT NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE UNIQUE INDEX usernameidx ON users (username);
CREATE TABLE specimen (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    user_id INTEGER NOT NULL, 
    my_id TEXT, 
    title TEXT, 
    locality TEXT, 
    day INTEGER, 
    month INTEGER, 
    year INTEGER, 
    notes TEXT, 
    thumbnail TEXT);
CREATE UNIQUE INDEX yearidx ON specimen (year);
CREATE TABLE specmin (
    specimen_id INTEGER NOT NULL REFERENCES specimen(id) ON DELETE CASCADE, 
    min_symbol TEXT NOT NULL, FOREIGN KEY(min_symbol) REFERENCES minerals(symbol));
CREATE TABLE tags (
    specimen_id INTEGER NOT NULL REFERENCES specimen(id) ON DELETE CASCADE, 
    tag TEXT NOT NULL);
CREATE INDEX tagidx ON tags (tag);
CREATE TABLE images (
    specimen_id INTEGER NOT NULL REFERENCES specimen(id) ON DELETE CASCADE, 
    file TEXT NOT NULL);
```

Note that the columns "thumbnail" is not used in the current version of Mymineralcollection.

## Ideas for improvement
A one week project can't be perfect. Future work could include:
- Port db handling from cs50 to sqlAlchemy. 
- Allow deleting of multiple entries in the table view. I had this kind of working, but it often triggered an exception in flasks session management and even google couldn't give me any clues.
- Print labels for selected specimen.
- Optionally print these labels with QR codes of the URL of the specimen.
