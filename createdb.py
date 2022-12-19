import cs50
import csv

# Create database

open("mineralcollection.db", "w").close()
db = cs50.SQL("sqlite:///mineralcollection.db")

sql = "CREATE TABLE minerals (symbol TEXT, name TEXT NOT NULL, chemistry TEXT, elements TEXT, crystal_system TEXT, fleischer TEXT, PRIMARY KEY(symbol))"
db.execute(sql)

# Open csv

with open("minerals.csv", "r") as file:
    # Dict reader
    reader = csv.DictReader(file)

    for row in reader:
        symbol = row['IMA Mineral Symbol']
        name = row['Mineral Name (HTML)']
        chemistry = row['IMA Chemistry (HTML)']
        elements = row['Chemistry Elements']
        crystal_system = row['Crystal Systems']
        fleischer = row['Fleischers Groupname']

        db.execute("INSERT INTO minerals (symbol, name, chemistry, elements, crystal_system, fleischer) VALUES (?, ?, ?, ?, ?, ?)", symbol, name, chemistry, elements, crystal_system, fleischer)
# User table
sql = "CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)"
db.execute(sql)
db.execute("CREATE UNIQUE INDEX usernameidx ON users (username)")

# Specimen table
sql = "CREATE TABLE specimen (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, my_id TEXT, title TEXT, locality TEXT, day INTEGER, month INTEGER, year INTEGER, storage TEXT, timestamp TEXT, thumbnail TEXT)"
db.execute(sql)
db.execute("CREATE UNIQUE INDEX yearidx ON specimen (year)")

# specmin table
sql = "CREATE TABLE specmin (specimen_id INTEGER NOT NULL REFERENCES specimen(id) ON DELETE CASCADE, min_symbol TEXT NOT NULL, FOREIGN KEY(min_symbol) REFERENCES minerals(symbol))"
db.execute(sql)

# tags table
sql = "CREATE TABLE tags (specimen_id INTEGER NOT NULL REFERENCES specimen(id) ON DELETE CASCADE, tag TEXT NOT NULL)"
db.execute(sql)
db.execute("CREATE INDEX tagidx ON tags (tag)")

# images table
sql = "CREATE TABLE images (specimen_id INTEGER NOT NULL REFERENCES specimen(id) ON DELETE CASCADE, file TEXT NOT NULL)"
db.execute(sql)