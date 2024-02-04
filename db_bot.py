import json
import os
import sqlite3
from time import time
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
    dbInitSql = dbInitFile.read()
    dbCursor.executescript(dbInitSql)
    dbInitDataSql = dbInitDataFile.read()
    dbCursor.executescript(dbInitDataSql)

# Open AI Client
def getChatResponse(prompt: str) -> str:
    openAiClient = OpenAI(api_key=config["openaiKey"])

    response = openAiClient.chat.completions.create(
        model=config["openaiModel"],
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

def retrieveSqlFromResponse(response: str) -> str:
    i = response.index("```")
    i = response.index("\n", i)
    j = response.index("```", i+1)
    return response[i:j]

def answerQuestion(prompt: str, log: object) -> str:
    gptResponse = getChatResponse(prompt)
    try:
        sql = retrieveSqlFromResponse(gptResponse)
        log["sql"] = sql
        dbResponse = dbCursor.execute(sql)

        columnNames = [description[0] for description in dbResponse.description]
        responseData = dbResponse.fetchall()
        log["queryResponse"] = str(responseData)

        friendlyPrompt = "The database returned the following response to the question \"" + question + "\":\nHeaders:\n" + str(columnNames) + "\nData: " + str(responseData) + "\nPlease use this data to provide a direct, friendly response (without any other pleasantries) to the question"
        friendlyResponse = getChatResponse(friendlyPrompt)
        log["friendlyresponse"] = friendlyResponse
        log["success"] = True
        return friendlyResponse
    except Exception as e:
        log["success"] = False
        log["error"] = e
        log["gptResponse"] = gptResponse
        return "Could not execute generated sql statement. ChatGPT response:\n" + gptResponse + "\nError:\n" + str(e)

strategies = {
    "zero-shot-given-tables": "The following sql code defines a database: \n```" + dbInitSql + "```\n",
    "zero-shot-given-sample-data": "The following sql code defines some sample data in a database: \n```" + dbInitDataSql + "```\n",
    "zero-shot-given-tables-and-data": "The following sql code defines a database with sample data: \n```" + dbInitSql + "\n\n" + dbInitDataSql + "```\n"
}

questions = [
    "Which vending machines have Coke?", # 1/Building 1, 2/Building 2
    "Which vending machines need to be restocked?", # 1/Building 1, 2/Break room
    "Which of John's starred vending machines have Drinks?", # 1/Building 1, 2/Building 2
    "Which of John's preferred vending machines have Lemonade?" # 2/Building 2
    "Which of Mary's starred vending machines have which of her starred products in stock?", # 3 (Bagel)
    "My coordinates are 40.249828, -111.647139. What vending machine is closest to me?", # 3
    "Who has the greatest quantity of their starred products available in their starred vending machines?",
    "Which machines have only one product type in stock?"
]

results = []

for strategy in strategies:
    print(strategy)
    for question in questions:
        print(question)
        log = {
            "strategy": strategy,
            "question": question
        }
        prompt = strategies[strategy] + "Write a sqlite select statement (please put statement in code block marked by \"```\") to answer the following question:\n" + question
        print(answerQuestion(prompt, log))
        results.append(log)
        print()
    print()

with open(f"response_{time()}.json", "w") as outFile:
    json.dump(results, outFile)

dbCursor.close()
dbConn.close()
