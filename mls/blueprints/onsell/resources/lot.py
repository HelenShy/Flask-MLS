from flask import jsonify
from flask_restplus import Resource, reqparse, Namespace

from flask_jwt_extended import (jwt_required, get_jwt_identity, get_raw_jwt, current_user)

from mls.blueprints.onsell.models import Lot, LotSchema
from flask_jwt_extended import get_jwt_identity, current_user


ns = Namespace('lots', description='API for single lot')

# Parsers
parser = reqparse.RequestParser()
parser.add_argument('type', type=str, help='', required=True, location='form')
parser.add_argument('description', type=str, help='', required=False, location='form')
parser.add_argument('square', type=int, help='', required=False, location='form')
parser.add_argument('qty_rooms', type=int, help='', required=False, location='form')
parser.add_argument('parking', type=bool, help='', required=False, location='form')
parser.add_argument('garageSpaces', type=int, help='', required=False, location='form')
parser.add_argument('year_built', type=int, help='', required=False, location='form')
parser.add_argument('price', type=int, help='', required=False, location='form')
parser.add_argument('status', type=str, help='', required=False, location='form')


lot_schema = LotSchema()
lots_schema = LotSchema(many=True)


@ns.route('')
class UserLot(Resource):
    @jwt_required
    @ns.expect(parser)
    def post(self):
        data = parser.parse_args()
        new_lot = Lot()
        from mls.blueprints.auth.models import User
        current_user = User.find_by_username(get_jwt_identity())
        new_lot.agent_id = current_user.id
        for k, v in data.items():
            if bool(v):
                setattr(new_lot, k, v)
        try:
            new_lot.save()
            return {'message': 'Lot #{} was saved successfully'.format(new_lot.id)}
        except:
            return {'message': 'Something went wrong'}, 500

    def get(self):
        all_lots = Lot.all()
        result = lots_schema.dump(all_lots)
        return jsonify(result.data)


@ns.route('/<int:_id>')
class UserLotById(Resource):
    response = {
        'error': {
            'message': 'Lot does not exist'
        }
    }

    def get(self, _id):
        lot = Lot.find_by_id(_id=_id)
        if lot:
            return LotSchema().dump(lot)
        else:
            return jsonify(self.response), 500

    @jwt_required
    @ns.expect(parser)
    def put(self, _id):
        data = parser.parse_args()
        lot = Lot.query.filter_by(id=_id, agent_id=current_user.id).first()
        if not lot:
            return jsonify(self.response), 404
        for k, v in data.items():
            if bool(v):
                setattr(lot, k, v)
        try:
            lot.save()
            return {'message': 'Lot #{}  was edited successfully'.format(lot.id)}
        except:
            return jsonify(self.response), 500

    @jwt_required
    def delete(self, _id):
        lot = Lot.query.filter_by(id=_id, agent_id=current_user.id).first()
        if not lot:
            return jsonify(self.response), 404
        try:
            lot.delete()
            return {'message': 'Lot #{}  was deleted'.format(str(_id))}
        except:
            return jsonify(self.response), 500

