import os
import json
from flask import g
from datetime import datetime

class Result:
    def __init__(self, record={}, messages=[]):
        self.record = record
        self.messages = messages

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


def get_next_id(collection):
    id = 0
    for rec in collection:
        if id < rec["_id"]:
            id = rec["_id"]
    return id + 1


def create_record(collection_name, record):
    collection = get_collection(collection_name)
    record["_id"] = get_next_id(collection)
    collection.append(record)
    update_collection(collection_name, collection)
    return record


def update_record(collection_name, record_old, record_new):
    collection = get_collection(collection_name)
    for rec, index in enumerate(collection):
        if rec["_id"] == record_old["_id"]:
            record_new["_id"] = record_old["_id"]
            collection[index] = record_new
            break
    update_collection(collection_name, collection)


def save_record_from_form_to_db(request, collection_name, record_old):
    messages = []
    coll_fieldcatalog = fieldcatalog[collection_name]
    fields = [field['name'] for field in coll_fieldcatalog['dbfields']]
    record_new = {f: request.form.get(f) for f in fields
                  if request.form.get(f, None) is not None and
                  request.form.get(f) != record_old.get(f, None)}

    for field in coll_fieldcatalog['dbfields']:
        field_input_type = field.get('input_type', None)
        if not field_input_type:
            continue
        field_name = field['name']
        field_values = field.get('values', None)
        # convert date value to datetime object
        if field_input_type == 'date':
            record_new[field_name] = request.form.get(field_name, None)
            translate_external_to_internal(field_name, field_input_type, field_values, record_new)
        # store foreign key from select-option
        elif field_input_type == 'select':
            field_value = record_new.get(field_name, None)
            if field_value:
                # convert foreign key to integer
                record_new[field_name] = int(field_value)
        # store check box as boolean
        elif field_input_type == 'checkbox':
            record_new[field_name] = True if record_new.get(field_name, 'off') == 'on' else False

    if not record_new:
        messages.append(
            (f"Did not {'update' if record_old else 'add'} record", "error"))
    else:
        if record_old:
            try:
                update_record(collection_name, record_old, record_new)
                messages.append(
                    (f"Successfully updated one {get_entity_name(collection_name)} record", "success"))
                record_new = {}
            except:
                messages.append((f"Error in update operation!", "danger"))
        else:
            try:
                record_new = create_record(collection_name, record_new)
                # create empty record - this clears the input fields, because the update was OK
                record_new = {}
                messages.append(
                    (f"Successfully added one {get_entity_name(collection_name)} record", "success"))
            except:
                messages.append((f"Error in addition operation!", "danger"))

    return Result(record_new, messages)
