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
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = {
        "members": members
    }
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_member():
    new_member = request.json
    jackson_family.add_member(new_member)
    return jsonify(new_member), 200  

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_family_member(member_id):
    delete_member = jackson_family.delete_member(member_id)
    if not delete_member:
        return jsonify({"msg": "member not found"}), 400
    return jsonify({"done": True}), 200

@app.route('/member/<int:member_id>', methods=['PUT'])
def update_family_member(member_id):
    new_member = request.json
    updated_member = jackson_family.update_member(member_id, new_member)  
    if not updated_member:
        return jsonify({"msg": "member not found"}), 400
    return jsonify({"done": "member updated"}), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    miembro_encontrado = jackson_family.get_member(member_id)
    if not miembro_encontrado:
        return jsonify({"msg": "member not found"}), 400
    return jsonify(miembro_encontrado), 200
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)