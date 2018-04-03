from flask import Flask
from flask_restplus import Resource, Api


def create_app():
    app = Flask(__name__)
    api = Api(app)

    @api.route('/hello')
    class HelloWorld(Resource):
        def get(self):
            return {'hello': 'world'}
    return app



# if __name__ == '__main__':
#     app.run(debug=True)