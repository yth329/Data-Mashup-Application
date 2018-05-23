from flask import Flask, jsonify, request
from flask_restful import reqparse
import requests
import os
import pandas as pd
import pymongo
import json
from mongoengine import StringField, IntField, Document, EmbeddedDocument, ListField, EmbeddedDocumentField

app = Flask(__name__)

mng_client = pymongo.MongoClient(host='mongodb://LlZzYy:LlZzYy@ds231090.mlab.com:31090/project')
mng_db = mng_client['project']

def import_content(file, collection):
    collection_name = collection
    db_cm = mng_db[collection_name]
    data = pd.read_csv(file, encoding = "ISO-8859-1")
    data_json = json.loads(data.to_json(orient='records'))

    db_cm.remove()
    db_cm.insert(data_json)

def get_post_args(arg_names, arg_types):
    parser = reqparse.RequestParser()
    for i in range(len(arg_names)):
        parser.add_argument(arg_names[i], type=arg_types[i])
    return parser.parse_args()

@app.route("/gun_shot/detailed_gunshot", methods=['GET'])
def get_detailed_ones():
    args = get_post_args(['date', 'state', 'city_or_county', 'n_injured', 'n_killed'], [str, str, str, int, int])
    args_json = request.get_json()
    print(args_json)
    query = {}

    for key, value in args.items():
        if value != None:
            query[key] = value
    db_cm = mng_db['detailed_gunshot']
    t = db_cm.find(query)
    result = []
    for doc in t:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    #print(result)
    if result == []:
        return 'Not Found', 404
    return jsonify(result), 200

@app.route("/gun_shot/mass_gunshot", methods=['GET'])
def get_mass_ones():
    args = get_post_args(['Location', 'Date', 'Fatalities', 'Injured'], [str, str,  int, int])
    print(args)
    query = {}

    for key, value in args.items():
        if value != None:
            query[key] = value
    db_cm = mng_db['mass_gunshot']
    t = db_cm.find(query)
    result = []
    for doc in t:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    #print(result)
    if result == []:
        return 'Not Found', 404
    return jsonify(result), 200

#get_detailed_ones()
app.run()
#if __name__ == '__main__':
#    import_content('Mass Shootings Dataset Ver 5.csv', 'mass_gunshot')
#    import_content('gun-violence-data_01-2013_03-2018.csv', 'detailed_gunshot')
