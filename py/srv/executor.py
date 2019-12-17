from queue import Queue
from threading import Thread

from py.srv.database import db_session
from py.srv.database.models.scenario import ScenarioMdl
from py.srv.database.models.trigger import TriggerMdl


class ScenarioExecutorSrv:
    def __init__(self, redis):
        self.q = Queue()
        self.workers = dict()
        redis.subscribe(self.on_update)

    @db_session
    def on_update(self, uuid, key_values, session):
        keys = key_values.keys()
        triggers = TriggerMdl.get_by_parameters(uuid=uuid, parameters=keys, session=session)
        scenarios = set([x.scenario for x in triggers])
        if len(scenarios) == 0:
            return
        for scenario in scenarios:
            self.q.put(scenario.uuid)

        while not self.q.empty():
            task = self.q.get()
            if task in self.workers.keys():
                self.q.put(task)
            else:
                self.workers[task] = Thread(target=self.process_scenario,
                                            kwargs={'item': task})
                self.workers[task].start()

    @db_session
    def process_scenario(self, item, session):
        scenario = ScenarioMdl.get_by_uuid(uuid=item, session=session)

        conditions = scenario.conditions
        for condition in conditions:
            if not condition.is_met():
                del (self.workers[item])
                return

        instructions = sorted(scenario.instructions, key=lambda x: x.order)
        for instruction in instructions:
            instruction.execute(session=session)
        del (self.workers[item])