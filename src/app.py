"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    members = jackson_family.get_all_members()
    response_body = {
        
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):

    member = jackson_family.get_member(member_id)
    return jsonify(member), 200

@app.route('/add_member', methods=['POST'])
def adding_members():

    # this is how you can use the Family datastructure by calling its methods
    request_body = request.get_json()
    result = jackson_family.add_member(request_body["first_name"], request_body["age"], request_body["lucky_numbers"])
    return jsonify(result), 200

@app.route('/del_member/<int:member_id>', methods=['DELETE'])
def del_members(member_id):

    # this is how you can use the Family datastructure by calling its methods
    result = jackson_family.delete_member(member_id)
    
    return jsonify(result), 200

@app.route('/upd_member/<int:member_id>', methods=['PUT'])
def upd_members(member_id):

    # this is how you can use the Family datastructure by calling its methods
    request_body = request.get_json()
    result = jackson_family.update_member(id = member_id, new_name = request_body["first_name"], new_age = request_body["age"], new_luckynum = request_body["lucky_numbers"])
    
    return jsonify(result), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)