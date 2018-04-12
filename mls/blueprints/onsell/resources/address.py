from flask import jsonify
from flask_restplus import Resource, reqparse, Namespace

from flask_jwt_extended import (jwt_required, get_jwt_identity, get_raw_jwt, current_user)

from mls.blueprints.onsell.models import Address, AddressSchema, Lot


ns = Namespace('address', description='API for lots geo location')
ns_address = Namespace('address', description='API for lots addresses')

parser_address = reqparse.RequestParser()
# parser_address.add_argument('id', type=int, help='', required=False, location='form')
parser_address.add_argument('city', type=str, help='', required=False, location='form')
parser_address.add_argument('street', type=str, help='', required=False, location='form')
parser_address.add_argument('house_number', type=int, help='', required=False, location='form')


@ns.route('')
class LotAddress(Resource):
    response = {
        'error': {
            'message': 'Lot does not exist'
        }
    }

    def get(self, _id):
        lot = Lot.query.filter_by(id=_id)
        if not lot:
            return jsonify(self.response), 404
        address = Address.find_by_lot_id(lot_id=_id)
        if not address:
            return {'message': 'Lot #{} does not have geo location yet.'.format(_id)}
        result = AddressSchema().dump(address)
        return jsonify(result.data)

    @jwt_required
    @ns.expect(parser_address)
    def post(self, _id):
        lot = Lot.query.filter_by(id=_id, agent_id=current_user.id)
        if not lot:
            return jsonify(self.response), 404
        data = parser_address.parse_args()
        address = Address.find_by_lot_id(lot_id=int(_id))
        if address:
            return {'message': 'Address for lot #{} already exists'.format(_id)}, 500
        new_address = Address()
        for k, v in data.items():
            #if bool(v):
            setattr(new_address, k, v)
        new_address.lot_id = _id
        try:
            new_address.save()
            return {'message': 'Address for lot #{} was added'.format(_id)}, 200
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    @ns.expect(parser_address)
    def put(self, _id):
        lot = Lot.query.filter_by(id=_id, agent_id=current_user.id)
        if not lot:
            return jsonify(self.response), 404
        data = parser_address.parse_args()
        address = Address.find_by_lot_id(lot_id=int(_id))
        if address:
            for k, v in data.items():
                if bool(v):
                    setattr(address, k, v)
            try:
                address.save()
                return {'message': 'Address for lot #{} was changed'.format(_id)}, 200
            except:
                return {'message': 'Something went wrong'}, 500
        else:
            return {'message': 'Lot #{} does not have address yet.'.format(_id)}, 404

    @jwt_required
    def delete(self, _id):
        lot = Lot.query.filter_by(id=_id, agent_id=current_user.id)
        if not lot:
            return jsonify(self.response), 404
        address = Address.find_by_lot_id(lot_id=int(_id))
        if address:
            try:
                address.delete()
                return {'message': 'Address for lot #{} was removed successfully'.format(_id)}
            except:
                return {'message': 'Something went wrong'}, 500
        else:
            return {'message': 'Lot #{} does not have address yet.'.format(_id)}, 404


@ns_address.route('')
class AllAddresses(Resource):
    def get(self):
        all_addresses = Address.all()
        result = AddressSchema.dump(all_addresses)
        return jsonify(result.data)
