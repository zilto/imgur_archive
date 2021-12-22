import json

with open(".api_secrets.json") as f:
    AUTH = json.load(f)
STORAGE_DIRPATH = "D:/.coding/projects/imgur_storage/"
LOGS_FILEPATH = STORAGE_DIRPATH + "scraping_logs.json"
DBNAME = "db_imgur.sqlite"