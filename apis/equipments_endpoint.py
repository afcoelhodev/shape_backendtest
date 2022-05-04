from flask import Blueprint, request, jsonify, Response
from sqlalchemy import func, extract, and_

from apis.models.equipment import equipment
from apis.models.vessel import vessel
from apis.models.model import db
import json


equipments_blueprint = Blueprint('equipments', __name__)


@equipments_blueprint.route('/insert_equipment', methods=['POST'])
def insert_equipment():
    """Insert a new equipment
        ---
        parameters:
            - name: vessel_code
              in: body
              type: string
              required: true
            - name: code
              in: body
              type: string
              required: true
            - name: name
              in: body
              type: string
              required: true
            - name: location
              in: body
              type: string
              required: true
        responses:
          201:
            description: returns OK if the equipment was correctly inserted
          400:
            description: returns MISSING_PARAMETER if any parameter is not sent
          400:
            description: returns WRONG_FORMAT if any parameter are sent in the wrong format
          409:
            description: returns REPEATED_CODE if the equipment code is already in the system
          409:
            description: returns NO_VESSEL if the vessel code is not already in the system
    """

    try:
        body = request.get_json()

        new_equipment = equipment(
            vessel_id=body['vessel_id'],
            name=body['name'],
            code=body['code'],
            location=body['location'],
        )

        equipment.insert(new_equipment)

        return jsonify({
            'id': new_equipment.id,
            'vessel_id': new_equipment.vessel_id,
            'name': new_equipment.name,
            'code': new_equipment.code,
            'location': new_equipment.location,
            'active': new_equipment.active,
            'message': 'OK'
        }), 201


    except Exception as err:
        if err == KeyError:
            return {'message': 'MISSING_PARAMETER or WRONG_FORMAT'}, 400
        else:
            return {'message': 'NO_VESSEL or REPEATED_CODE'}, 409


@equipments_blueprint.route('/update_equipment_status', methods=['PUT'])
def update_equipment_status():
    """Set an equipment or a list of those to inactive
        ---
        parameters:
            - name: code
              in: body
              type: string
              required: true
        responses:
          201:
            description: returns OK if the equipments were correctly updated
          400:
            description: returns MISSING_PARAMETER if any parameter is not sent
          400:
            description: returns WRONG_FORMAT if any parameter are sent in the wrong format
          409:
            description: returns NO_CODE if the equipment code is not already in the system
    """

    body = request.get_json()
    equipment_to_update = body['equipment']

    try:
        for equipment_item in equipment_to_update:
            equipment_selected = equipment.query.filter_by(code=equipment_item).first()
            equipment_selected.active = False

            equipment.update(equipment_selected)

            return jsonify({
                'id': equipment_selected.id,
                'vessel_id': equipment_selected.vessel_id,
                'name': equipment_selected.name,
                'code': equipment_selected.code,
                'location': equipment_selected.location,
                'active': equipment_selected.active,
                'message': 'OK'
            }), 201

    except Exception as err:
        if err == KeyError:
            return {'message': 'MISSING PARAMETER or WRONG FORMAT'}, 400
        else:
            return {'message': 'NO_CODE RESULT'}, 409


@equipments_blueprint.route('/active_equipments/<vessel_id>', methods=['GET'])
def active_equipment(vessel_id):
    """Return the list of active equipments of a vessel
        ---
        parameters:
            - name: vessel_id
              in: query
              type: string
              required: true
        responses:
          200:
            description: returns a json with equipments key and a list of equipments
          400:
            description: returns MISSING_PARAMETER if the vessel_code is not sent
          400:
            description: returns WRONG_FORMAT if any parameter are sent in the wrong format
          409:
            description: returns NO_VESSEL if the vessel is not already in the system
    """

    active_equipment = equipment.query.filter_by(vessel_id=vessel_id)
    active_equipment_formatted = [active_equipment_item.formatted() for active_equipment_item in active_equipment]
    list_active_equipment = []

    for item in active_equipment_formatted:
        if item['active'] == True:
            list_active_equipment.append(item)
        else:
            pass

    return Response(json.dumps(list_active_equipment)), 200


@equipments_blueprint.route('/all_equipments', methods=['GET'])
def get_equipments():
    """Return the list of equipments of a vessel
         ---
         responses:
           200:
             description: returns a json with vessels key and a list of equipments
           400:
             description: returns ERROR if the request has been done wrong
    """

    list_equipments = equipment.query.all()
    list_equipments_formatted = [equipment_item.formatted() for equipment_item in list_equipments]
    all_equipments = []

    for item in list_equipments_formatted:
        vessel_get = vessel.query.filter_by(id=item['vessel_id']).first()
        vessel_get_formatted = vessel_get.formatted()
        all_equipments.append(
            {f"{item['name']}": f"{vessel_get_formatted['code']}"}
        )

    return Response(json.dumps(all_equipments)), 200
