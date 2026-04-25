from __future__ import annotations

import random
from collections import defaultdict


class MarkovStyleModel:
    def __init__(self, order: int = 3) -> None:
        if order < 1:
            raise ValueError("order must be >= 1")
        self.order = order
        self.chain: dict[str, list[str]] = defaultdict(list)

    def fit(self, text: str) -> "MarkovStyleModel":
        text = text.replace("\n", "。")
        if len(text) <= self.order:
            return self
        for i in range(len(text) - self.order):
            key = text[i : i + self.order]
            value = text[i + self.order]
            self.chain[key].append(value)
        return self

    def generate(self, target_chars: int = 3500, seed: str | None = None) -> str:
        if not self.chain:
            return ""
        rng = random.Random()
        keys = list(self.chain.keys())
        current = seed if seed in self.chain else rng.choice(keys)
        out = list(current)
        while len(out) < target_chars:
            options = self.chain.get(current)
            if not options:
                current = rng.choice(keys)
                out.extend(current)
                continue
            nxt = rng.choice(options)
            out.append(nxt)
            current = "".join(out[-self.order :])
        return "".join(out[:target_chars])
