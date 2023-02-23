from flask import Blueprint, current_app, jsonify
import pywebostv.controls as tv_cntl

input_bp = Blueprint('input', __name__)

@input_bp.route('/input/<key_name>', methods=['PUT'])
def put_input(key_name):
    tv_client = current_app.tv_client
    tv_cntl.InputControl(tv_client).set_input(key_name)
    # users = [
    #     {'name': 'John', 'age': 30},
    #     {'name': 'Jane', 'age': 25},
    #     {'name': 'Bob', 'age': 40}
    # ]
    print(key_name)
    # return jsonify(users)
