from flask_restful import reqparse, Resource

from py.srv.api.demo.models.scenarios import DemoScenarioDTO
from py.srv.api.demo.operations.scenarios import get_all_scenarios, add_scenarios, delete_scenarios
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session

parser = reqparse.RequestParser()
parser.add_argument('scenarios', type=list, location='json', required=True)


class Scenarios(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        return [DemoScenarioDTO(x).as_json() for x in get_all_scenarios(session=session)]

    @abort_on_exc
    @db_session
    def put(self, session):
        args = parser.parse_args()
        return [DemoScenarioDTO(x).as_json() for x in add_scenarios(scenarios=args['scenarios'], session=session)]

    @abort_on_exc
    @db_session
    def delete(self, session):
        args = parser.parse_args()
        delete_scenarios(scenarios=args['scenarios'], session=session)
