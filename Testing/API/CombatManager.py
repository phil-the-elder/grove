from collections import deque
from random import random, randint

class OutcomePicker:
    """ Class designed to allow for rapid outcome picking for combat actions given an array of probability values
    :int attacker: attacker creature id
    :int target: target creature id
    :str method: attack method (valid options: melee, ranged, magic)
    :list w: list of probability values for all possible outcomes
    :return: None
    """
    def __init__(self, attacker: int, target: int, method: str, w: list):
        self.attacker = attacker
        self.target = target
        self.method = method
        width = len(w)
        scale = width / sum(w)
        input_probs = [1] * width
        probs = [1] * width
        alias = [None] * width
        bigs = deque()
        smalls = deque()
        for i, p in enumerate(w):
            input_probs[i] = p * scale
            if input_probs[i] < 1:
                smalls.append(i)
            else:
                bigs.append(i)
        while smalls and bigs:
            small_idx = smalls.pop()
            large_idx = bigs[-1]
            probs[small_idx] = input_probs[small_idx]
            alias[small_idx] = large_idx
            input_probs[large_idx] = input_probs[large_idx] + input_probs[small_idx] - 1
            if input_probs[large_idx] < 1:
                smalls.append(bigs.pop())
        self.probs = probs
        self.alias = alias
        self.range = width - 1

    def pick(self):
        """ Picks a result given the weighted lists
        :return: list index
        """
        idx = randint(0, self.range)
        return idx if random() <= self.probs[idx] else self.alias[idx]
            