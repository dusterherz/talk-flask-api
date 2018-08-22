from flask import Flask
from flask_restplus import Api
from flask_restplus import Resource, abort, fields, reqparse

app = Flask(__name__)
api = Api(app)

cats = [
    {"name": "brindille", "age": 7, "colors": ['brown', 'grey', 'white']}
]

model = api.model('Cat', {
    'name': fields.String(default="Minet"),
    'age': fields.Integer(default=4),
    'colors': fields.List(fields.String),
})

cat_parser = reqparse.RequestParser()
cat_parser.add_argument('name', type=str, default="Minet")
cat_parser.add_argument('age', type=int, default=3)
cat_parser.add_argument('colors', type=str, action='append', default=[])


class CatResource(Resource):
    @api.marshal_with(model)
    def get(self, cat_name):
        for i, cat in enumerate(cats):
            if cat['name'] == cat_name:
                return cat
        abort(404, message="Cat {} does not exist :(".format(cat_name))


class CatsResource(Resource):
    @api.marshal_with(model, as_list=True)
    def get(self):
        return cats

    @api.marshal_with(model)
    @api.expect(model)
    def post(self):
        parsed_args = cat_parser.parse_args()
        cat = {'name': parsed_args.name,
               'age': parsed_args.age,
               'colors': parsed_args.colors}
        cats.append(cat)
        return cat


api.add_resource(CatsResource, '/api/cats/', endpoint="cats")
api.add_resource(CatResource, '/api/cats/<string:cat_name>', endpoint="cat")


if __name__ == '__main__':
    app.run(debug=True)
