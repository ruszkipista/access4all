import os
import json
from datetime import datetime

# envDB.py should exist only in Development
if os.path.exists("envDB.py"):
    import envDB

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


def get_fields_from_fieldcatalog(collection_name):
    return fieldcatalog[collection_name]['dbfields']


def get_db_field_type_lookup_triples(collection_name, field_names):
    triples = []
    coll_fields = get_fields_from_fieldcatalog(collection_name)
    for field_name in field_names:
        field_def = next(
            (f for f in coll_fields if f['name'] == field_name), '')
        input_type = field_def.get('input_type', None)
        lookup_collection_name = field_def.get('values', None)
        triples.append((field_name, input_type, lookup_collection_name))
    return triples


def convert_field_values_in_interviews(collection_name, records):
    field_names = ['date']
    field_type_lookup_triples = get_db_field_type_lookup_triples(collection_name, field_names)
    for record in records:
        # convert From Date isodatestring to datetime
         for field, type, lookup in field_type_lookup_triples:
            translate_external_to_internal(field, type, lookup, record)
    return records

def translate_external_to_internal(source_field_name, input_type, lookup_collection_name, record):
    external_value = record.get(source_field_name, None)
    internal_value = None

    if input_type == 'date':
        if external_value == '' or external_value is None:
            del record[source_field_name]
        else:
            # convert isodatestring YYYY-MM-DD into datetime object
            internal_value = datetime.fromisoformat(external_value)

    else:
        lookup = get_db_select_field_lookup(lookup_collection_name)
        internal_value = lookup.get(external_value, None)

    if internal_value:
        record[source_field_name] = internal_value        


def get_interviews_all():
    collection_name = INTERVIEWS
    collection_file_name = fieldcatalog[collection_name]["file_name"]
    file_name = os.path.join(dbConfig["OS_DATA_PATH"], collection_file_name)
    records = get_data_from_json_file(file_name)
    convert_field_values_in_interviews(collection_name, records)
    return records


def get_question_sets_all():
    file_name = os.path.join(dbConfig["OS_DATA_PATH"], fieldcatalog[QUESTION_SETS]["file_name"])
    return get_data_from_json_file(file_name)


def get_question_set_names():
    questions = get_question_sets_all()
    set_names = []
    for question in questions:
        for row in question["questions"]:
            set_names.append(row["setname"])
    return list(set(set_names))


def create_form_data_attributes(coll_fieldcat: dict, record: dict, filter_postfix: str):
    attributes = ""
    if coll_fieldcat.get('filter', None):
        for field in coll_fieldcat['fields']:
            if field['name'] in coll_fieldcat['filter']:
                attributes += "data-" + field['name'] + "_" + filter_postfix \
                    + "=" + str(record[field['name']])
    return attributes

    
def get_db_entity_select_field(entity_id, collection_name):
    select_field_name = fieldcatalog[collection_name]['select_field']
    file_name = os.path.join(dbConfig["OS_DATA_PATH"], fieldcatalog[QUESTION_SETS]["file_name"])
    collection = get_data_from_json_file(file_name)
    try:
        entity_old = collection.find(lambda x : x._id==entity_id)
        if entity_old:
            return entity_old[select_field_name]
    except:
        pass
    return ""


def get_db_record_by_id(collection_name, record_id):
    pass


def get_db_entity_name(collection_name):
    pass


def save_record_to_db(request, collection_name, record):
    pass


def delete_db_record(collection_name, record):
    pass