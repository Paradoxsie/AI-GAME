#!/usr/bin/env python3
"""Boredom Quest: a lightweight terminal game designed for ~30 minutes of play.

The player survives a sequence of mini-events over 30 in-game days.
Each day has a quick choice and small narrative outcome.
"""

from __future__ import annotations

import random
import textwrap

TOTAL_DAYS = 30
START_ENERGY = 6
START_MORALE = 6
START_SUPPLIES = 6


def wrap(text: str) -> str:
    return "\n".join(textwrap.wrap(text, width=78))


def print_intro() -> None:
    print("=" * 78)
    print("BOREDOM QUEST: 30 Days to Stay Busy")
    print("=" * 78)
    print(
        wrap(
            "You are trapped in a tiny outpost with one mission: make it through "
            "30 days without running out of Energy, Morale, or Supplies. "
            "Each day you choose one action. Survive all 30 days to win."
        )
    )
    print("\nHow to play: type 1, 2, or 3 each day.")
    print("Goal: finish Day 30 with all stats above 0.\n")


def day_event(day: int) -> tuple[str, list[dict]]:
    prompts = [
        "A cold wind shakes the outpost walls.",
        "Your radio catches a brief static signal.",
        "The pantry smells... questionable.",
        "You wake up from a weird dream about sandwiches.",
        "The generator coughs and flickers.",
        "A long silence settles over the snow.",
        "You find an old notebook with blank pages.",
        "You hear something scratching outside.",
    ]

    options = [
        {
            "label": "Repair and maintain the outpost",
            "effects": {"energy": -2, "morale": -1, "supplies": +2},
            "result": "You fix leaks and sort supplies. It is exhausting but useful.",
        },
        {
            "label": "Create something fun (journal, song, game)",
            "effects": {"energy": -1, "morale": +2, "supplies": -1},
            "result": "You make a tiny masterpiece. Spirits rise.",
        },
        {
            "label": "Forage outside for rare resources",
            "effects": {"energy": -2, "morale": +1, "supplies": +1},
            "result": "The trip is risky, but you return with useful scraps.",
        },
    ]

    random.shuffle(options)

    if day % 7 == 0:
        prompts.append("A weekly storm arrives, pushing all systems to the limit.")
        for option in options:
            option["effects"]["energy"] -= 1

    if day % 10 == 0:
        prompts.append("You receive a care package! Supplies feel less scarce today.")
        options[0]["effects"]["supplies"] += 1
        options[1]["effects"]["supplies"] += 1
        options[2]["effects"]["supplies"] += 1

    return random.choice(prompts), options


def clamp(value: int) -> int:
    return max(0, min(12, value))


def print_stats(energy: int, morale: int, supplies: int) -> None:
    print(f"Stats -> Energy: {energy:2d} | Morale: {morale:2d} | Supplies: {supplies:2d}")


def apply_decay(day: int, energy: int, morale: int, supplies: int) -> tuple[int, int, int]:
    # Time itself creates pressure.
    supplies -= 1
    if day % 5 == 0:
        morale -= 1
    if day % 6 == 0:
        energy -= 1
    return energy, morale, supplies


def main() -> None:
    random.seed()
    print_intro()

    energy = START_ENERGY
    morale = START_MORALE
    supplies = START_SUPPLIES

    for day in range(1, TOTAL_DAYS + 1):
        print("\n" + "-" * 78)
        print(f"Day {day}/{TOTAL_DAYS}")
        print_stats(energy, morale, supplies)

        prompt, options = day_event(day)
        print(wrap(prompt))

        for idx, option in enumerate(options, start=1):
            print(f"  {idx}) {option['label']}")

        choice = None
        while choice not in {"1", "2", "3"}:
            choice = input("Choose your action [1-3]: ").strip()

        selected = options[int(choice) - 1]
        energy = clamp(energy + selected["effects"]["energy"])
        morale = clamp(morale + selected["effects"]["morale"])
        supplies = clamp(supplies + selected["effects"]["supplies"])

        print(wrap(selected["result"]))

        energy, morale, supplies = apply_decay(day, energy, morale, supplies)
        energy, morale, supplies = clamp(energy), clamp(morale), clamp(supplies)

        if energy == 0 or morale == 0 or supplies == 0:
            print("\nYou could not keep the routine together.")
            print_stats(energy, morale, supplies)
            print("Game Over. You lasted", day, "days.")
            return

    print("\n" + "=" * 78)
    print("You made it through all 30 days. Boredom defeated.")
    print_stats(energy, morale, supplies)
    print("Victory!")


if __name__ == "__main__":
    main()
