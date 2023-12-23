from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for, redirect  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"Message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data)
    return {"Message": "Internal server error"}, 500

    

######################################################################
# GET A PICTURE
######################################################################

def pic_by_id(pic_id):
    entry = None
    for pic in data:
        if(pic["id"] == pic_id):
            entry = pic
            break
    return entry

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if not data:     
        return {"Message": "Internal server error"}, 500
    if id-1 < 0:
        return {"Message": f"Picture id:{id} not found"}, 404
    
    entry = pic_by_id(id)
    
    if not entry:
        return {"Message": f"Picture id:{id} not found"}, 404
    return jsonify(entry) 


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    body = request.json

    pic_id = body["id"]
    pic_url = body["pic_url"]
    event_country = body["event_country"]
    event_state = body["event_state"]
    event_city = body["event_city"]
    event_date = body["event_date"]

    if(pic_id < 0):
        return {"Message":"invalid id"}

    if(pic_by_id(pic_id)):
        return {"Message":f"picture with id {pic_id} already present"} , 302
    
    pic_entry_struct = {
        "id":pic_id,
        "pic_url":pic_url,
        "event_country":event_country,
        "event_state":event_state,
        "event_city":event_city,
        "event_date":event_date
    }

    data.append(pic_entry_struct)

    print(pic_id)

    pic_at_id = pic_by_id(pic_id)
    if(pic_at_id != pic_entry_struct):
        print("Invalid Entry")
        return {"Messge":"Error"} , 503

    return jsonify(pic_at_id) , 201
    

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):

    pic_struct = pic_by_id(id)
    if(not pic_struct):
        return {"Message" : f"picture not found"} , 404

    #Extract Data
    picture_data = request.json
    pic_keys = list(picture_data.keys())

    allowed_keys = ["id" , "pic_url" , "event_country" , "event_state" , "event_city" , "event_date"]
    
    #filter data
    for key in pic_keys:
        if not key in allowed_keys:
            picture_data.pop(key)

    pic_index = data.index(pic_struct)
    data[pic_index] = picture_data

    return data[pic_index]



######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pic_struct = pic_by_id(id)
    if(not pic_struct):
        return {"Message" : f"picture not found"} , 404

    pic_index = data.index(pic_struct)
    data.pop(pic_index)

    return "",204
