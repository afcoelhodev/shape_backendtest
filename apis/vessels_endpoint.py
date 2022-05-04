from flask import Blueprint, request, jsonify, Response
from sqlalchemy import func, extract, and_
import json

from apis.models.vessel import vessel
from apis.models.model import db


vessels_blueprint = Blueprint('vessels', __name__)


@vessels_blueprint.route('/list_vessel', methods=['GET'])
def get_vessel():
    """Return all vessels registered
        ---
        responses:
          200:
            description: returns OK if the list is correctly generates
          400:
            description: returns ERROR if the request has been done wrong
    """

    list_vessel = vessel.query.all()
    list_vessel_formatted = [vessel_item.formatted() for vessel_item in list_vessel]

    return jsonify({
        'vessels': list_vessel_formatted,
        'total': len(list_vessel),
        'message': 'OK',
        'status': 200
    })


@vessels_blueprint.route('/insert_vessel', methods=['POST'])
def insert_vessel():
    """Insert a new vessel
        ---
        parameters:
            - name: code
              in: body
              type: string
              required: true
        responses:
          201:
            description: returns OK if the vessel was correctly inserted
          400:
            description: returns MISSING_PARAMETER if the vessel code is not sent
          400:
            description: returns WRONG_FORMAT if any parameter are sent in the wrong format
          409:
            description: returns FAIL if the vessel code is already in the system
    """

    body_response = request.get_json()
    code = body_response.get("code")

    if len(code) != 5:
        return {'message': 'MISSING_PARAMETER'}, 400
    else:
        if code[0:2].isalpha() is False or code[2:5].isnumeric() is False:
            return {'message': 'WRONG_FORMAT'}, 400
        else:
            check_vessel = vessel.query.filter_by(code=code).first()
            if check_vessel == code:
                return {'message': 'FAIL'}, 409
            else:
                new_vessel = vessel(
                    code=code
                )
                db.session.add(new_vessel)
                db.session.commit()

                return jsonify({
                    'id': new_vessel.id,
                    'code': new_vessel.code,
                    'message': 'OK'
                }), 201
