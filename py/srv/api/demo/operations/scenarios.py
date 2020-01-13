import pickle

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from py.srv.api.demo.models.scenarios import DemoScenarioInputDTO
from py.srv.api.exceptions import SimpleException
from py.srv.database import db_session
from py.srv.database.models.condition import ConditionMdl
from py.srv.database.models.device import DeviceMdl
from py.srv.database.models.instructions import InstructionMdl, InstructionParamsMdl, InstructionTypeEnum
from py.srv.database.models.scenario import ScenarioMdl
from py.srv.database.models.trigger import TriggerMdl


@db_session
def get_all_scenarios(session):
    return ScenarioMdl.get_all(session=session)


@db_session
def delete_scenarios(scenarios, session):
    for num, item in enumerate(scenarios):
        try:
            delete_scenario(item=item, session=session)
        except UnmappedInstanceError as e:
            raise SimpleException('Item #{} not found. Stopping'.format(num))
    session.commit()


@db_session
def delete_scenario(item, session):
    scenario = ScenarioMdl.get_by_uuid(uuid=item, session=session)
    session.delete(scenario)
    session.flush()
    return scenario

@db_session
def add_scenarios(scenarios, session):
    res = list()
    for num, item in enumerate(scenarios):
        try:
            res.append(add_scenario(item=item, session=session))
        except IntegrityError as e:
            raise SimpleException('Duplicate on #{} in sequence. Stopping'.format(num))
    session.commit()
    return res


@db_session
def add_scenario(item, session):
    model = DemoScenarioInputDTO(item)

    scenario = ScenarioMdl(name=model.name,
                           description=model.description)
    for item in model.triggers:
        trigger = TriggerMdl(comment=item.comment,
                             parameter=item.parameter,
                             device_uuid=DeviceMdl.get_device_with_name(name=item.device,
                                                                        session=session).uuid)
        scenario.triggers.append(trigger)
    for item in model.conditions:
        condition = ConditionMdl(condition_type=item.type,
                                 source_dev_uuid=DeviceMdl.get_device_with_name(name=item.source_device,
                                                                                session=session).uuid,
                                 source_parameter=item.source_parameter,
                                 target_dev_uuid=DeviceMdl.get_device_with_name(name=item.target_device,
                                                                                session=session).uuid,
                                 target_parameter=item.target_parameter)
        scenario.conditions.append(condition)
    for item in model.instructions:
        instruction = InstructionMdl(order=item.order, instruction_type=item.type)
        for sub in item.parameters.items():
            param = InstructionParamsMdl(name=sub[0], pickle_value=pickle.dumps(sub[1]))
            if instruction.instruction_type == InstructionTypeEnum.SetValue \
                    and param.name in ['source', 'target']:
                param.pickle_value = pickle.dumps(DeviceMdl.get_device_with_name(sub[1]).uuid)
            instruction.parameters.append(param)
        scenario.instructions.append(instruction)

    session.add(scenario)
    session.flush()
    return scenario
