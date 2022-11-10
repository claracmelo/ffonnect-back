import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user,login_required

members = Blueprint('members', 'members')
@members.route('/', methods=['GET'])
@login_required
def members_index():
    result = models.Member.select()
    print('result of member select query')
    print(result)

    current_user_member_dicts = [model_to_dict(member) for member in current_user.members]

    for member_dict in current_user_member_dicts:
        member_dict['relation_id'].pop('password')

    return jsonify({
        'data': current_user_member_dicts,
        'message': f"Successfully found {len(current_user_member_dicts)} members",
        'status': 200
    }), 200

# member create route
# POST /api/v1/members/
#
@members.route('/', methods=['POST'])
@login_required
def create_members():
    payload = request.get_json() # this is like req.body in express
    print(current_user,"current user")
    print(payload)
    new_member = models.Member.create(name=payload['name'],relation=payload["relation"],dob=payload["dob"],status=payload["status"],dod=payload["dod"], relation_id=current_user.id)
    print(new_member) # just print the ID -- check sqlite3 to see

    # name = CharField() #string
    # relationship = CharField() #mom, dad, sis, etc
    # dob = DateField() #date of birth
    # status = BooleanField() #alive? if not, dod field
    # dod = DateField() #date of death
    # relationship_name = CharField() #user

    member_dict = model_to_dict(new_member)
    member_dict['relation_id'].pop('password')
    # owner to user
    return jsonify(
        data=member_dict,
        message='Successfully created member!',
        status=201
    ), 201

# SHOW ROUTE
# GET api/v1/members/<member_id>
# in express it looked something like this
# router.get('/:id')
@members.route('/<id>', methods=['GET'])
@login_required
def get_one_member(id):
    member = models.Member.get_by_id(id)
    print(member)
    return jsonify(
        data = model_to_dict(member),
        message = 'Success!!! 🎉',
        status = 200
    ), 200

# UPDATE ROUTE
# PUT api/v1/members/<member_id>
@members.route('/<id>', methods=["PUT"])
@login_required
def update_member(id):
    payload = request.get_json()
    query = models.Member.update(**payload).where(models.Member.id == id)
    query.execute()
    return jsonify(
        data = model_to_dict(models.Member.get_by_id(id)),
        status=200,
        message='resource updated successfully'
    ), 200


# DELETE ROUTE
# DELETE api/v1/members/<member_id>
@members.route('/<id>', methods=['DELETE'])
@login_required
def delete_member(id):
    query = models.Member.delete().where(models.Member.id == id)
    query.execute()
    return jsonify(
        data= model_to_dict(models.Member.get_by_id(id)),
        message='resource successfully deleted',
        status=200
    ), 200
