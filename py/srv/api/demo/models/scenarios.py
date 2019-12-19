from py.srv.database.models.condition import ConditionTypeEnum
from py.srv.database.models.instructions import InstructionTypeEnum
from py.srv.database.models.scenario import ScenarioMdl


class DemoScenarioDTO:
    def __init__(self, scenario: ScenarioMdl):
        self.uuid = scenario.uuid
        self.description = scenario.description
        self.name = scenario.name

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': self.name,
            'description': self.description
        }


class DemoScenarioTriggerDTO:
    def __init__(self, info):
        self.device = info['device']
        self.parameter = info['parameter']
        self.comment = info['comment']


class DemoScenarioConditionDTO:
    def __init__(self, info):
        self.type = ConditionTypeEnum[info['type']]
        self.source_device = info['source']['device']
        self.source_parameter = info['source']['parameter']
        self.target_device = info['target']['device']
        self.target_parameter = info['target']['parameter']


class DemoScenarioInstructionDTO:
    def __init__(self, info):
        self.order = info['order']
        self.type = InstructionTypeEnum[info['type']]
        self.parameters = {x['name']: x['value'] for x in info['parameters']}


class DemoScenarioInputDTO:
    def __init__(self, info):
        self.name = info['name']
        self.description = info['description']
        self.triggers = [DemoScenarioTriggerDTO(x) for x in info['triggers']]
        self.conditions = [DemoScenarioConditionDTO(x) for x in info['conditions']]
        self.instructions = [DemoScenarioInstructionDTO(x) for x in info['instructions']]