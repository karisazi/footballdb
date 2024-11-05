# FootballDB

This is footballdb! A package for converting your football match report PDF to a well structured database.


## Goals
Tired of sifting through PDF match reports for key stats? FootballDB is the lightweight package that converts your football reports into structured databases effortlessly. You don’t need to find and type information manually—FootballDB automatically reads all the details from your PDFs. Perfect for enhancing football data management, FootballDB lets you organize and access game insights with ease!


## 🚀 Quick Start

## Run footballdb with three inputs: file_directory, database username, and password

```python
from footballdb import extract_football_to_db

# your path to file football pdf directories 
path = 'D:/signup/upw/footbal/football_docs' 

# extract data from directories to your local database
extract_football_to_db(path=path, db_user='root', db_password='root')

```