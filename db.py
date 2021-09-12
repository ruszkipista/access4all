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
dbConfig["FIELDCATALOG"]          = "fieldcatalog"
dbConfig["FILE_NAME"]             = "file_name"
dbConfig["FIELDCATALOG_FILENAME"] = os.environ.get("FIELDCATALOG_FILENAME", "fieldcatalog.json")
dbConfig["COLLECTIONS"] = ["question_sets", "interviews"]
QUESTION_SETS  = dbConfig["COLLECTIONS"][0]
INTERVIEWS     = dbConfig["COLLECTIONS"][1]

# 1st assignment for bootstrapping
fieldcatalog = {
    dbConfig["FIELDCATALOG"]:{
        dbConfig["FILE_NAME"]: dbConfig["FIELDCATALOG_FILENAME"]
    }
}

def get_collection_file_path(collection_name):
    file_name = fieldcatalog[collection_name][dbConfig["FILE_NAME"]]
    return os.path.join(dbConfig["OS_DATA_PATH"], file_name)


def get_data_from_json_file(file_name):
    data = None
    with open(file_name, mode='r', encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


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


# EXTERNAL -> INTERNAL
def translate_external_to_internal(source_field_name, input_type, lookup_collection_name, record):
    external_value = record.get(source_field_name, None)
    internal_value = None

    if input_type == 'auto_increment':
        internal_value = int(external_value)
        

    elif input_type == 'date':
        if external_value == '' or external_value is None:
            del record[source_field_name]
        else:
            # convert isodatestring YYYY-MM-DD into datetime object
            internal_value = datetime.fromisoformat(external_value)

    else:
        lookup_table = get_lookup_int_to_ext(lookup_collection_name)
        internal_value = lookup_table.get(external_value, None)

    if internal_value:
        record[source_field_name] = internal_value        


def convert_field_values_ext_to_int_in_collection(collection_name, records):
    field_names = fieldcatalog[collection_name].get("convert_fields", None)
    if field_names:
        field_type_lookup_triples = get_db_field_type_lookup_triples(collection_name, field_names)
        for record in records:
            for field, type, lookup in field_type_lookup_triples:
                translate_external_to_internal(field, type, lookup, record)
    return records


# INTERNAL -> EXTERNAL
def translate_internal_to_external(source_field_name, input_type, lookup_collection_name, record):
    internal_value = record.get(source_field_name, None)
    external_value = None

    if input_type == 'auto_increment':
        external_value = str(internal_value)

    elif input_type == 'date':
        # convert isodatestring YYYY-MM-DD into datetime object
        external_value = datetime.isoformat(internal_value)

    else:
        lookup_table = get_lookup_int_to_ext(lookup_collection_name)
        external_value = lookup_table.get(internal_value, None)

    if external_value:
        record[source_field_name] = external_value


def convert_field_values_int_to_ext_in_collection(collection_name, records):
    field_names = fieldcatalog[collection_name].get("convert_fields", None)
    print(field_names)
    if field_names:
        field_type_lookup_triples = get_db_field_type_lookup_triples(collection_name, field_names)
        for record in records:
            for field, type, lookup in field_type_lookup_triples:
                translate_internal_to_external(field, type, lookup, record)
    return records


def get_collection(collection_name):
    collection_file_name = get_collection_file_path(collection_name)
    records = get_data_from_json_file(collection_file_name)
    converted_records = convert_field_values_ext_to_int_in_collection(collection_name, records)
    return converted_records


# 2nd assignment for real
fieldcatalog = get_collection(dbConfig["FIELDCATALOG"])


def get_buffered_collections():
    return [coll for coll, fcat in fieldcatalog.items() if fcat.get('buffer_lookup', None)]


def get_interviews_all():
    return get_collection(INTERVIEWS)


def get_question_sets_all():
    return get_collection(QUESTION_SETS)


def get_fields_from_fieldcatalog(collection_name):
    return fieldcatalog[collection_name]['dbfields']


def get_viewfields(collection_name):
    coll_catalog = fieldcatalog[collection_name]
    viewfields = coll_catalog.get("viewfields", None)
    if viewfields:
        # convert list to set
        viewfields = set(viewfields)
    return viewfields


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

  
def get_foreign_value(entity_id, collection_name):
    lookup = get_lookup_int_to_ext(collection_name)
    return lookup.get(entity_id, "")


def get_record_by_id(collection_name, record_id):
    coll = get_collection(collection_name)
    return next((rec for rec in coll if rec["_id"]==record_id), None)


def get_entity_name(collection_name):
    coll_fieldcatalog = fieldcatalog[collection_name]
    return coll_fieldcatalog["entity_name"]


def delete_record(collection_name, record):
    record_id = record.get("_id",None)
    if not record_id:
        return
    collection = get_collection(collection_name)
    collection_new = [ r for r in collection if r.get("_id",None) != record_id ]
    update_collection(collection_name, collection_new)


def update_collection(collection_name, records):
    file_name = get_collection_file_path(collection_name)
    converted_records = convert_field_values_int_to_ext_in_collection(collection_name, records)
    save_data_to_json_file(file_name, converted_records)


def save_data_to_json_file(file_name, data):
    with open(file_name, mode='w', encoding="utf-8") as f:
        f.write(json.dumps(data))


def save_record_from_request_to_db(request, collection_name, record):
    pass
