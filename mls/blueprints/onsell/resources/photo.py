from flask import jsonify
from flask_restplus import Resource, reqparse, Namespace
from flask_jwt_extended import (jwt_required, get_jwt_identity, get_raw_jwt, current_user)
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os

from mls.blueprints.onsell.models import Photo, PhotoSchema, Lot

ns = Namespace('photos', description='API for lot`s photos')

parser_photo = reqparse.RequestParser()
parser_photo.add_argument('file', location='files', type=FileStorage)


@ns.route('')
class LotPhotos(Resource):
    response = {
        'error': {
            'message': 'Lot does not exist'
        }
    }

    def get(self, _id):
        lot = Lot.query.filter_by(id=_id)
        if not lot:
            return jsonify(self.response), 404
        photos = Photo.query.filter_by(lot_id=_id).all()
        if len(photos) == 0:
            return {'message': 'Lot #{} does not have loaded photos yet.'.format(_id)}
        result = PhotoSchema().dump(photos)
        return jsonify(result.data)

    @jwt_required
    @ns.expect(parser_photo)
    def post(self, _id):
        lot = Lot.query.filter_by(id=_id, agent_id=current_user.id)
        if not lot:
            return jsonify(self.response), 404
        data = parser_photo.parse_args()
        file = data['file']
        if file and Photo.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            photo_path = os.path.join(str(_id) + '-' + filename)
            file.save(photo_path)
            new_photo = Photo(lot_id=_id, photo_path=photo_path)
            new_photo.save()
            return {'message': 'Photo was saved succesfully'}
        else:
            return {'message': 'Loading error. Check file extension.'}, 404

    @jwt_required
    @ns.expect(parser_photo)
    def delete(self, _id):
        lot = Lot.query.filter_by(id=_id, agent_id=current_user.id)
        if not lot:
            return jsonify(self.response), 404
        photos = Photo.find_by_lot_id(lot_id=int(_id))
        if len(photos) == 0:
            return {'message': 'Lot #{} does not have loaded photos.'.format(_id)}
        try:
            for photo_id in [x.id for x in photos]:
                photo = Photo.find_by_id(photo_id)
                os.remove(os.path.join(photo.photo_path))
                photo.delete()
                return {'message': 'Photos for lot #{} were removed successfully'.format(_id)}
        except:
            return {'message': 'Something went wrong'}, 500


@ns.route('/<int:photo_id>')
class LotPhoto(Resource):
    @jwt_required
    def delete(self, _id, photo_id):
        photos = Photo.find_by_lot_id(lot_id=int(_id))
        if len(photos) == 0:
            return {'message': 'Lot #{} does not have loaded photos.'.format(_id)}
        if photo_id in [x.id for x in photos]:
            photo = Photo.find_by_id(photo_id)
            try:
                os.remove(os.path.join(photo.photo_path))
                photo.delete()
                return {'message': 'Photo was removed successfully'}
            except:
                return {'message': 'Something went wrong'}, 500
        else:
            return {'message': 'Photo was not found'}, 404

    def get(self, _id, photo_id):
        lot = Lot.query.filter_by(id=_id)
        if not lot:
            return jsonify(self.response), 404
        photo = Photo.query.filter_by(lot_id=_id, id=photo_id).first()
        if not photo:
            return {'message': 'Photo does not exist'}
        result = PhotoSchema().dump(photo)
        return jsonify(result.data)
