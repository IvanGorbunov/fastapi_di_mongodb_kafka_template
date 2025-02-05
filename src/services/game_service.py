import random
from typing import List

class GameService:

    def __init__(self, spidey_names: List[str], my_name: str, kafka_service):
        self.spidey_names = spidey_names
        self.my_name = my_name
        self.kafka_service = kafka_service

        self.mapping_place = {
            3: "name is the Winner!!!",
            2: "name is the Second Place!!!",
            1: "name is the Third Place!!!",
        }

    def spidey_random(self, spidey_list: List) -> List:
        random.shuffle(spidey_list)
        return spidey_list

    async def play_turn(self, finalists: List):
        spidey_order = self.spidey_random(finalists)
        await self.kafka_service.send_message(spidey_order)

    def check_spidey(self, finalists: List) -> bool:
        return self.my_name == finalists[0]

    async def process_turn(self, msg):
        finalists = msg
        is_my_turn = self.check_spidey(finalists)

        if is_my_turn:
            print(self.mapping_place[len(finalists)].replace('name', self.my_name))

            if len(finalists) > 1:
                finalists.pop(0)
                await self.play_turn(finalists)
