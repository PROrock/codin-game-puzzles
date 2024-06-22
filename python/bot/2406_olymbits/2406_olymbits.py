import dataclasses
import operator
import sys
from typing import List, Dict


def debug(*s):
    print(*s, file=sys.stderr, flush=True)


@dataclasses.dataclass
class MedalAmounts:
    n_golds: int
    n_silvers: int
    n_bronzes: int

    def compute_score(self):
        return 3*self.n_golds+self.n_silvers


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


@dataclasses.dataclass
class HurdlesGame(Game):
    my_id: int
    runners: List[int] = dataclasses.field(init=False)
    stuns: List[int] = dataclasses.field(init=False)

    hurdle: str = "#"
    spaces_to_action: Dict[int, str] = dataclasses.field(init=False, default_factory=lambda: {
        1: "LEFT",
        # 2: "DOWN",
        2: "UP",  # + jump
        3: "RIGHT",
    })
    stun_penalty: int = 2
    winning_dist_thres: int = 8
    losing_dist_thres: int = 8

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

    def find_preferred_action_for_this_play(self):
        if game.gpu == "GAME_OVER":
            return None

        if self.stuns[self.my_id] > 0:
            return None

        if self.losing_dist_thres >= self.compute_leading_dist() >= self.winning_dist_thres:
            return None

        return self.find_optimal_action_for_this_play()

    def compute_leading_dist(self):
        # todo take stuns into account - stun-aware dist
        # stun_aware_position =
        opponents = self.runners[:self.my_id] + self.runners[self.my_id+1:]
        furthest_opponent = max(opponents)
        return self.runners[self.my_id] - furthest_opponent


def parse_score_info(score_info):
    score_info = score_info.split()
    score_info = score_info[1:]
    medal_amounts = []
    for i in range(nb_games):
        numbers, score_info = score_info[:3], score_info[3:]
        medal_amounts.append(MedalAmounts(*numbers))
    return medal_amounts


def argmin(iter):
    return min(enumerate(iter), key=operator.itemgetter(1))[0]


player_idx = int(input())
nb_games = int(input())
games = [None] * nb_games

# game loop
while True:
    for i in range(3):
        score_info = input()
        if i == player_idx:
            medal_amounts = parse_score_info(score_info)
    for i in range(nb_games):
        inputs = input().split()
        gpu = inputs[0]
        registers = [int(i) for i in inputs[1:]]

        game = HurdlesGame(gpu, registers, player_idx)
        game.update(gpu, registers)
        games[i] = game

    scores = [m.compute_score() for m in medal_amounts]
    min_score_game_idx = argmin(scores)
    action = games[min_score_game_idx].find_optimal_action_for_this_play()
    debug(medal_amounts)
    debug(scores)
    debug(min_score_game_idx)
    print(action)


# multiple games
# naive - get optimal for all and take the most frequent action
# take leading dist into account and ignore totally won and lost games
# return preferred action instead of optimal - return None, if abstaining from decision
