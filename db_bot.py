import json
import os
import sqlite3
from openai import OpenAI

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

# Open AI Client
def getChatResponse(prompt: str):
    openAiClient = OpenAI(api_key=config["openaiKey"])

    response = openAiClient.chat.completions.create(
        model=config["openaiModel"],
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

# prompt = input("Enter prompt:\n")
prompt = "Write the numbers 1-10, separated by commas"
print(getChatResponse(prompt))
