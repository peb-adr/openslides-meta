#!/bin/python3

from json import dump, load
from yaml import safe_load
import sys


MODELS_FILENAME = 'models.yml'
MODELS = {}
D1 = {}
D2 = {}
DIFF = []


def check_field(collection, model_id, field_name):
    global D1, D2, DIFF

    info(f"check_field: {collection}/{model_id}/{field_name} ...")

    # To be very explicit we will now look at all known field types distinctly,
    # although in most cases '==' equality should suffice.

    field_type = MODELS[collection][field_name]['type']
    field_value_d1 = D1[collection][model_id][field_name]
    field_value_d2 = D2[collection][model_id][field_name]

    # assume not equal until proven otherwise
    is_equal = False

    if field_type == 'boolean':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'color':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'decimal(6)':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'float':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'generic-relation':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'generic-relation-list':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'HTMLPermissive':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'HTMLStrict':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'JSON':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'number':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'number[]':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'relation':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'relation-list':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'string':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'string[]':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'text':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'text[]':
        is_equal = field_value_d1 == field_value_d2
    elif field_type == 'timestamp':
        is_equal = field_value_d1 == field_value_d2

    if not is_equal:
        DIFF += [f"{collection}/{model_id}/{field_name} of type {field_type} differs."]
        DIFF += [f"  D1: {field_value_d1}"]
        DIFF += [f"  D2: {field_value_d2}"]


def check_model(collection, model_id):
    global D1, D2, DIFF

    info(f"check_model: {collection}/{model_id} ...")

    # This check is redundantly done before in check_collection and should
    # therefore never be possible to fail.
    assert model_id in D1[collection].keys() 
    if model_id not in D2[collection].keys():
        DIFF += [f"{collection}/{model_id} exists in D1 but not in D2"]
        return

    field_names_d1 = D1[collection][model_id].keys()
    field_names_d2 = D2[collection][model_id].keys()

    for field_name in field_names_d1:
        if field_name not in field_names_d2:
            DIFF += [f"{collection}/{model_id}/{field_name} exists in D1 but not in D2"]
            continue

        check_field(collection, model_id, field_name)


def check_collection(collection):
    global D1, D2, DIFF

    if collection not in D1.keys() and collection not in D2.keys():
        info(f"check_collection: skipping {collection}, does not exist in both D1 and D2 ...")
        return

    info(f"check_collection: {collection} ...")

    model_ids_d1 = D1[collection].keys()
    model_ids_d2 = D2[collection].keys()

    for model_id in model_ids_d1:
        if model_id not in model_ids_d2:
            DIFF += [f"{collection}/{model_id} exists in D1 but not in D2"]
            continue

        check_model(collection, model_id)


def check_all():
    for collection in MODELS.keys():
        if collection == '_meta':
            continue
        check_collection(collection)


def load_models():
    global MODELS

    with open(MODELS_FILENAME, 'r') as f:
        MODELS = safe_load(f)


def load_input():
    global D1, D2

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    with open(filename1) as f1:
        D1 = load(f1)
    with open(filename2) as f2:
        D2 = load(f2)


def print_diff():
    print('\n'.join(DIFF))


def info(s):
    #print(f"INFO: {s}")
    pass


def main():
    load_models()
    load_input()

    #print(MODELS['_meta'])
    #print(D1['action_worker']['1']['name'])
    #check_collection('action_worker')
    check_all()
    print_diff()


if __name__ == '__main__':
    main()
