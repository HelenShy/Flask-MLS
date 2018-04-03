from flask import Flask, Blueprint
from flask_restplus import Api, Resource

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)

ns = api.namespace('ns_hello', description='...')


@ns.route('/hello')
class HiWorld(Resource):
    def get(self):
        return {'hi': 'world'}
