import json
import os
import sqlite3

# Load configuration file
with open("config.json") as configFile:
    config = json.load(configFile)

# Remove previous database
dbName = config["dbName"]
if os.path.exists(dbName):
    os.remove(dbName)

# Create database and load data
dbConn = sqlite3.connect(dbName)
dbCursor = dbConn.cursor()
with (
    open("db_init.sql") as dbInitFile,
    open("db_init_data.sql") as dbInitDataFile
):
    dbCursor.executescript(dbInitFile.read())
    dbCursor.executescript(dbInitDataFile.read())


print("End")