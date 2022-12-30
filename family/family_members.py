from flask import Blueprint, abort, jsonify, request
from main.householdDB import HouseholdDB

family_members_table = Blueprint("family_members_table", __name__,
                          static_folder="static", template_folder="templates")

@family_members_table.route('/<int:username>')
def find_by_username(username):
    return jsonify(HouseholdDB.find_by_username(username))

@family_members_table.route('/', methods=['GET', 'POST'])
def create_family_member():
    if not request.json:
        abort(400)
    family_members = {
        'Username': request.json['Username'],
        'Password': request.json['Password'],
        'Balance': request.json['Balance'],
        'Debt' : request.json['Debt']
    }
    values = (family_members['Username'], family_members['Password'], family_members['Balance'], family_members['Debt'])
    new_user = HouseholdDB.create_family_members(values)
    family_members['Username'] = new_user
    return jsonify(family_members)

@family_members_table.route('/<int:Username>', methods=['PUT'])
def update_family_members(username):
    found_user = HouseholdDB.find_by_username(username)
    if not found_user:
        abort(404)
    if not request.json:
        abort(400)
    if 'Username' in request.json:
        found_user['Username'] = request.json['Username']
    values = (found_user['Username'])
    HouseholdDB.update_family_members(values)
    return jsonify(found_user)

@family_members_table.route('/<int:Username>', methods=['DELETE'])
def delete_family_members(username):
    HouseholdDB.delete_patient(username)
    return jsonify({'Done': True})