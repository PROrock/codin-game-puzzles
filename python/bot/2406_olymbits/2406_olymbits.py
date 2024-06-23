import math
import operator
import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

START_BALANCING_TURN = 70
ACTIONS = ["UP", "RIGHT", "DOWN", "LEFT"]


def debug(*s):
    print(*s, file=sys.stderr, flush=True)

def signum(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0


@dataclass
class MedalAmounts:
    n_golds: int
    n_silvers: int
    n_bronzes: int

    def compute_score(self):
        return 3*self.n_golds+self.n_silvers


@dataclass
class Game:
    my_id: int
    gpu: str = ""

    def update(self, gpu, registers):
        self.gpu = gpu
        self.post_update(registers)

    def post_update(self, registers):
        raise NotImplementedError()

    def find_optimal_action_for_this_play(self):
        raise NotImplementedError()

    def find_preferred_action_for_this_play(self):
        raise NotImplementedError()


@dataclass
class DummyGame(Game):
    def post_update(self, registers):
        pass  # dummy impl

    def find_optimal_action_for_this_play(self):
        return "LEFT"

    def find_preferred_action_for_this_play(self):
        return None


@dataclass
class HurdlesGame(Game):
    runners: List[int] = field(init=False)
    stuns: List[int] = field(init=False)

    hurdle: str = "#"
    spaces_to_action: Dict[int, str] = field(init=False, repr=False, default_factory=lambda: {
        1: "LEFT",
        2: "DOWN",
        # 2: "UP",  # + jump
        3: "RIGHT",
    })
    stun_penalty: int = 2
    winning_dist_thres: int = 8
    losing_dist_thres: int = 8

    def post_update(self, registers):
        self.runners = registers[:3]
        self.stuns = registers[3:6]

    def find_optimal_action_for_this_play(self):
        if game.gpu == "GAME_OVER":
            return "DOWN"

        distance_to_hurdle = self._get_distance_to_hurdle()
        if distance_to_hurdle == 1:
            return "UP"
        return self.spaces_to_action.get(distance_to_hurdle-1, "RIGHT")

    def _get_distance_to_hurdle(self):
        my_position = self.runners[self.my_id]
        nearest_hurdle = self.gpu.find(self.hurdle, my_position + 1)
        distance_to_hurdle = -1 if nearest_hurdle == -1 else (nearest_hurdle - my_position)
        return distance_to_hurdle

    def find_preferred_action_for_this_play(self):
        if game.gpu == "GAME_OVER":
            return None

        if self.stuns[self.my_id] > 0:
            return None

        if self._get_distance_to_hurdle()-1 > 3:
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


class Vect:
    """Immutable 2D vector"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def l2_norm(self):
        """
        XXX: Consider using math.hypot(*coordinates) or math.dist(p, q), which is probably faster.
        See https://docs.python.org/3/library/math.html#math.dist
        For timing guide, see https://stackoverflow.com/a/24105845/2127340
        """
        return math.sqrt(self.x**2 + self.y**2)

    def __bool__(self):
        return True

    def __repr__(self):
        return f"V({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Vect((self.x + other.x), (self.y + other.y))
    def __sub__(self, other):
        return Vect((self.x - other.x), (self.y - other.y))
    def __mul__(self, multiplier):
        return Vect(self.x * multiplier, self.y * multiplier)
    # right multiplication to support 2 * p
    __rmul__ = __mul__
    def __neg__(self):
        return Vect(-self.x, -self.y)


@dataclass
class ArcheryGame(Game):
    coordinates: List[Vect] = field(init=False)
    bulls_eye: Vect = Vect(0, 0)
    diff_signs_to_action: Dict[Tuple[bool, int], str] = field(init=False, repr=False, default_factory=lambda: {
        (True, 1): "LEFT",
        (True, -1): "RIGHT",
        (False, 1): "UP",
        (False, -1): "DOWN",
    })

    @property
    def my_coordinates(self):
        return self.coordinates[self.my_id]

    def post_update(self, registers):
        self.coordinates = [Vect(x,y) for x, y in zip(registers[:5:2], registers[1:6:2])]

    def find_optimal_action_for_this_play(self):
        if game.gpu == "GAME_OVER":
            return None
        # current_wind = int(game.gpu[0])
        diff_to_bulls_eye = self.my_coordinates - self.bulls_eye
        x_is_farther = abs(diff_to_bulls_eye.x) > abs(diff_to_bulls_eye.y)
        debug(x_is_farther, diff_to_bulls_eye)
        return self.diff_signs_to_action.get((x_is_farther, signum(diff_to_bulls_eye.x) if x_is_farther else signum(diff_to_bulls_eye.y)))

    def find_preferred_action_for_this_play(self):
        if game.gpu == "GAME_OVER":
            return None
        return self.find_optimal_action_for_this_play()


@dataclass
class DivingGame(Game):
    points: List[int] = field(init=False)
    combos: List[int] = field(init=False)
    letter_to_action: Dict[str, str] = field(init=False, repr=False, default_factory=lambda: {a[0]: a for a in ACTIONS})

    def post_update(self, registers):
        self.points = registers[:3]
        self.combos = registers[3:6]

    def find_optimal_action_for_this_play(self):
        if game.gpu == "GAME_OVER":
            return None
        current_letter = game.gpu[0]
        return self.letter_to_action[current_letter]

    def find_preferred_action_for_this_play(self):
        if game.gpu == "GAME_OVER":
            return None
        return self.find_optimal_action_for_this_play()


def parse_score_info(score_info):
    score_info = [int(i) for i in score_info.split()]
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
games: List[Game] = [HurdlesGame(player_idx), ArcheryGame(player_idx), DummyGame(player_idx), DivingGame(player_idx)]
medal_amounts = []
i_turn = 0

while True:
    for i in range(3):
        score_info = input()
        if i == player_idx:
            medal_amounts = parse_score_info(score_info)
    for i in range(nb_games):
        inputs = input().split()
        gpu = inputs[0]
        registers = [int(i) for i in inputs[1:]]

        game = games[i]
        game.update(gpu, registers)


    debug(games)
    debug(medal_amounts)
    debug([g.find_optimal_action_for_this_play() for g in games])
    actions = [g.find_preferred_action_for_this_play() for g in games]
    debug(actions)

    if i_turn < START_BALANCING_TURN:
        filtered_actions = [a for a in actions if a is not None]
        action = None
        if len(filtered_actions):
            action = Counter(filtered_actions).most_common(1)[0][0]
        if action is None:
            action = "UP"
    else:
        scores = [m.compute_score() for m in medal_amounts]
        min_score_game_idx = argmin(scores)
        action = games[min_score_game_idx].find_optimal_action_for_this_play()
        if action is None:
            action = "DOWN"
        debug(scores)
        debug(min_score_game_idx)

    print(action)
    i_turn += 1

