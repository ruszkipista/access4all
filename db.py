import os
import json
from datetime import datetime

# DB parameters
dbConfig = {}
dbConfig["OS_DATA_PATH"]          = os.environ.get("OS_DATA_PATH", "./static/data/")
dbConfig["FIELDCATALOG_FILENAME"] = os.environ.get("FIELDCATALOG_FILENAME", "fieldcatalog.json")
dbConfig["COLLECTIONS"] = ["question_sets", "interviews"]
QUESTION_SETS  = dbConfig["COLLECTIONS"][0]
INTERVIEWS     = dbConfig["COLLECTIONS"][1]


def get_data_from_json_file(file_name):
    data = None
    with open(file_name, mode='r', encoding="utf-8") as f:
        data = json.loads(f.read())
    return data

fieldcatalog = get_data_from_json_file( os.path.join(dbConfig["OS_DATA_PATH"], 
                                                     dbConfig["FIELDCATALOG_FILENAME"]))


def get_interviews_all():
    file_name = os.path.join(dbConfig["OS_DATA_PATH"], fieldcatalog[INTERVIEWS]["file_name"])
    return get_data_from_json_file(file_name)


def get_question_sets_all():
    file_name = os.path.join(dbConfig["OS_DATA_PATH"], fieldcatalog[QUESTION_SETS]["file_name"])
    return get_data_from_json_file(file_name)


def get_question_set_names():
    questions = get_question_sets_all()
    set_names = []
    for question in questions:
        for row in question["questions"]:
            set_names.append(row["setname"])
    return set_names
