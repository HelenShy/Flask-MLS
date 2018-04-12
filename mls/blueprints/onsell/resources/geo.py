from flask import jsonify
from flask_restplus import Resource, reqparse, Namespace
from flask_jwt_extended import (jwt_required, get_jwt_identity, get_raw_jwt, current_user)

from mls.blueprints.onsell.models import Geo, GeoSchema, Lot

ns = Namespace('geo', description='API for lots geo location')
ns_geo = Namespace('geo', description='API for lots geo location')

parser_geo = reqparse.RequestParser()
parser_geo.add_argument('lat', type=int, help='', required=False, location='form')
parser_geo.add_argument('lng', type=int, help='', required=False, location='form')


@ns.route('')
class LotGeo(Resource):
    response = {
        'error': {
            'message': 'Lot does not exist'
        }
    }

    def get(self, _id):
        lot = Lot.query.filter_by(id=_id)
        if not lot:
            return jsonify(self.response), 404
        geo = Geo.find_by_lot_id(lot_id=_id)
        if not geo:
            return {'message': 'Lot #{} does not have geo location yet.'.format(_id)}
        result = GeoSchema().dump(geo)
        return jsonify(result.data)

    @jwt_required
    @ns.expect(parser_geo)
    def post(self, _id):
        lot = Lot.query.filter_by(id=_id, agent_id=current_user.id)
        if not lot:
            return jsonify(self.response), 404
        data = parser_geo.parse_args()
        geo = Geo.find_by_lot_id(lot_id=int(_id))
        if geo:
            return {'message': 'Geo location for lot #{} already exists'.format(_id)}, 500
        new_geo = Geo()
        for k, v in data.items():
            if bool(v):
                setattr(new_geo, k, v)
        new_geo.lot_id = _id
        try:
            new_geo.save()
            return {'message': 'Geo location for lot #{} was added'.format(_id)}, 200
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    @ns.expect(parser_geo)
    def put(self, _id):
        lot = Lot.query.filter_by(id=_id, agent_id=current_user.id)
        if not lot:
            return jsonify(self.response), 404
        data = parser_geo.parse_args()
        geo = Geo.find_by_lot_id(lot_id=int(_id))
        if geo:
            for k, v in data.items():
                #if bool(v):
                setattr(geo, k, v)
            try:
                geo.save()
                return {'message': 'Geo location for lot #{} was changed'.format(_id)}, 200
            except:
                return {'message': 'Something went wrong'}, 500
        else:
            return {'message': 'Lot #{} does not have geo location yet.'.format(_id)}, 404

    @jwt_required
    def delete(self, _id):
        lot = Lot.query.filter_by(id=_id, agent_id=current_user.id)
        if not lot:
            return jsonify(self.response), 404
        geo = Geo.find_by_lot_id(lot_id=int(_id))
        if geo:
            try:
                geo.delete()
                return {'message': 'Geo location for lot #{} was removed successfully'.format(_id)}
            except:
                return {'message': 'Something went wrong'}, 500
        else:
            return {'message': 'Lot #{} does not have geo location yet.'.format(_id)}, 404


@ns_geo.route('')
class AllGeo(Resource):
    def get(self):
        all_geo = Geo.all()
        result = GeoSchema(many=True).dump(all_geo)
        return jsonify(result.data)

