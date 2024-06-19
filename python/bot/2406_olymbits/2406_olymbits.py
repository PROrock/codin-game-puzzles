import dataclasses
import sys
from typing import List, Dict


def debug(*s):
    print(*s, file=sys.stderr, flush=True)


@dataclasses.dataclass
class Game:
    gpu: str
    registers: List[int]   # 7? game-specific registers

    def update(self, gpu, registers):
        self.gpu = gpu
        self.registers = registers
        self.post_update()

    def post_update(self):
        raise NotImplementedError()

    def find_optimal_action_for_this_play(self):
        raise NotImplementedError()


class HurdlesGame(Game):
    my_id: int
    runners: List[int]
    stuns: List[int]

    hurdle: str = "#"
    spaces_to_action: Dict[int, str] = {
        1: "LEFT",
        2: "DOWN",
        # 2: "UP", # + jump
        3: "RIGHT",
    }

    def post_update(self):
        self.runners = self.registers[:3]
        self.stuns = self.registers[3:6]

    def find_optimal_action_for_this_play(self):
        if game.gpu == "GAME_OVER":
            return "DOWN"

        my_position = self.runners[self.my_id]
        nearest_hurdle = self.gpu.find(self.hurdle, my_position + 1)
        distance_to_hurdle = -1 if nearest_hurdle == -1 else (nearest_hurdle - my_position)
        if distance_to_hurdle == 1:
            return "UP"
        return self.spaces_to_action.get(distance_to_hurdle-1, "RIGHT")


# todo handle game over
# todo parse code

game = HurdlesGame()
game.update()
game.find_optimal_action_for_this_play()
