import os
import json
from flask import g
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


def get_collection(collection_name):
    collection_file_name = fieldcatalog[collection_name]["file_name"]
    file_name = os.path.join(dbConfig["OS_DATA_PATH"], collection_file_name)
    records = get_data_from_json_file(file_name)
    convert_field_values_in_collection(collection_name, records)
    return records


def get_interviews_all():
    return get_collection(INTERVIEWS)


def get_question_sets_all():
    return get_collection(QUESTION_SETS)


fieldcatalog = get_data_from_json_file( os.path.join(dbConfig["OS_DATA_PATH"], 
                                                     dbConfig["FIELDCATALOG_FILENAME"]))


def get_fields_from_fieldcatalog(collection_name):
    return fieldcatalog[collection_name]['dbfields']


def get_lookup_ext_to_int(collection_name):
    if not getattr(g, "_ext_to_int_lookups", None):
        g._ext_to_int_lookups = {}
    records = getattr(g._ext_to_int_lookups, collection_name, None)
    if records is None:
        coll = get_collection(collection_name)
        if coll:
            coll_fieldcatalog = fieldcatalog[collection_name]
            select_field = coll_fieldcatalog.get('select_field', None)
            if select_field:
                records = {c[select_field]: c['_id'] for c in coll}
            else:
                records = {}
            g._ext_to_int_lookups[collection_name] = records
    return records


def get_lookup_int_to_ext(collection_name):
    if not getattr(g, "_int_to_ext_lookups", None):
        g._int_to_ext_lookups = {}
    records = getattr(g._int_to_ext_lookups, collection_name, None)
    if records is None:
        coll = get_collection(collection_name)
        if coll:
            coll_fieldcatalog = fieldcatalog[collection_name]
            select_field = coll_fieldcatalog.get('select_field', None)
            if select_field:
                records = {c['_id'] : c[select_field] for c in coll}
            else:
                records = {}
            g._int_to_ext_lookups[collection_name] = records
    return records


def get_question_set_names():
    set_names_dict = get_lookup_int_to_ext(QUESTION_SETS)
    set_names = set_names_dict.values()
    return set_names


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


def convert_field_values_in_collection(collection_name, records):
    field_names = fieldcatalog[collection_name].get("convert_fields", None)
    if field_names:
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
        lookup_table = get_lookup_ext_to_int(lookup_collection_name)
        internal_value = lookup_table.get(external_value, None)

    if internal_value:
        record[source_field_name] = internal_value        


def create_form_data_attributes(coll_fieldcat: dict, record: dict, filter_postfix: str):
    attributes = ""
    if coll_fieldcat.get('filter', None):
        for field in coll_fieldcat['fields']:
            if field['name'] in coll_fieldcat['filter']:
                attributes += "data-" + field['name'] + "_" + filter_postfix \
                    + "=" + str(record[field['name']])
    return attributes

    
def get_foreign_value(entity_id, collection_name):
    lookup = get_lookup_int_to_ext(collection_name)
    return lookup.get(entity_id, "")


def get_record_by_id(collection_name, record_id):
    coll = get_collection(collection_name)
    return next((rec for rec in coll if rec["_id"]==record_id), None)


def get_entity_name(collection_name):
    coll_fieldcatalog = fieldcatalog[collection_name]
    return coll_fieldcatalog["entity_name"]


def save_record_to_db(request, collection_name, record):
    pass


def delete_db_record(collection_name, record):
    pass