from flask import Blueprint
from flask_restplus import Api
from .lot import ns as ns_lot
from .geo import ns as ns_lot_geo, ns_geo
from .address import ns as ns_lot_address, ns_address
from .photo import ns as ns_photos

onsell_blueprint = Blueprint('onsell', __name__, url_prefix='/api/onsell')
onsell_api = Api(onsell_blueprint)


onsell_api.add_namespace(ns_lot, path='/lots')
onsell_api.add_namespace(ns_lot_geo, path='/lots/<int:_id>/geo')
onsell_api.add_namespace(ns_geo, path='/geo')
onsell_api.add_namespace(ns_lot_address, path='/lots/<int:_id>/address')
onsell_api.add_namespace(ns_address, path='/address')
onsell_api.add_namespace(ns_photos, path='/lots/<int:_id>/photos')
