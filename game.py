#!/usr/bin/env python3
"""A simple terminal game designed to stay engaging for about 30 minutes."""

from __future__ import annotations

import random
import textwrap

MAP_SIZE = 6
FLOORS = 5
TARGET_RELICS = 3
START_HEALTH = 20


class Player:
    def __init__(self) -> None:
        self.health = START_HEALTH
        self.attack = 4
        self.heal_potions = 3
        self.relics = 0
        self.x = 0
        self.y = 0


class FloorState:
    def __init__(self, floor_number: int) -> None:
        self.floor_number = floor_number
        self.exit = (MAP_SIZE - 1, MAP_SIZE - 1)
        self.relic_positions = set()
        while len(self.relic_positions) < TARGET_RELICS:
            pos = (random.randint(0, MAP_SIZE - 1), random.randint(0, MAP_SIZE - 1))
            if pos not in {(0, 0), self.exit}:
                self.relic_positions.add(pos)

        self.enemy_positions = {}
        enemy_count = 7 + floor_number
        while len(self.enemy_positions) < enemy_count:
            pos = (random.randint(0, MAP_SIZE - 1), random.randint(0, MAP_SIZE - 1))
            if pos in self.relic_positions or pos in {(0, 0), self.exit}:
                continue
            hp = random.randint(5 + floor_number, 8 + floor_number)
            atk = random.randint(2, 3 + floor_number // 2)
            self.enemy_positions[pos] = {"hp": hp, "atk": atk}

        self.visited = {(0, 0)}


INTRO = """
Welcome to RELIC RUNNER.

Your goal: clear 5 dungeon floors.
On each floor, collect 3 relics, then reach the exit.

This is intentionally paced to run around 30 minutes for most players.
Commands: north, south, east, west, look, stats, heal, help, quit
"""


def wrap(text: str) -> str:
    return textwrap.fill(text.strip(), width=78)


def print_map(player: Player, floor: FloorState) -> None:
    print("\nMini-map (V=visited, .=unknown, P=you)")
    for y in range(MAP_SIZE):
        row = []
        for x in range(MAP_SIZE):
            if (x, y) == (player.x, player.y):
                row.append("P")
            elif (x, y) in floor.visited:
                row.append("V")
            else:
                row.append(".")
        print(" ".join(row))


def combat(player: Player, enemy: dict[str, int], floor_number: int) -> bool:
    print(wrap(f"An enemy blocks your way! (HP {enemy['hp']}, ATK {enemy['atk']})"))
    while enemy["hp"] > 0 and player.health > 0:
        cmd = input("Fight action (attack/heal/run): ").strip().lower()
        if cmd == "attack":
            damage = random.randint(max(1, player.attack - 1), player.attack + 2)
            enemy["hp"] -= damage
            print(f"You hit for {damage}. Enemy HP is now {max(0, enemy['hp'])}.")
        elif cmd == "heal":
            if player.heal_potions > 0:
                recovered = random.randint(4, 8)
                player.health = min(START_HEALTH + floor_number * 2, player.health + recovered)
                player.heal_potions -= 1
                print(f"You use a potion and recover {recovered} HP.")
            else:
                print("No potions left.")
                continue
        elif cmd == "run":
            chance = random.random()
            if chance < 0.45:
                print("You escaped!")
                return False
            print("Escape failed!")
        else:
            print("Unknown action.")
            continue

        if enemy["hp"] > 0:
            incoming = random.randint(max(1, enemy["atk"] - 1), enemy["atk"] + 1)
            player.health -= incoming
            print(f"Enemy hits you for {incoming}. Your HP: {max(0, player.health)}")

    if player.health <= 0:
        print("You fall in battle...")
        return False

    print("Enemy defeated!")
    if random.random() < 0.35:
        player.heal_potions += 1
        print("The enemy dropped a healing potion.")
    return True


def handle_tile(player: Player, floor: FloorState) -> bool:
    pos = (player.x, player.y)
    floor.visited.add(pos)

    if pos in floor.enemy_positions:
        enemy = floor.enemy_positions[pos]
        won = combat(player, enemy, floor.floor_number)
        if not won and player.health <= 0:
            return False
        if enemy["hp"] <= 0:
            del floor.enemy_positions[pos]

    if pos in floor.relic_positions:
        floor.relic_positions.remove(pos)
        player.relics += 1
        print(wrap("You found a relic!"))

    if pos == floor.exit:
        if len(floor.relic_positions) == 0:
            print("The exit is active. You can proceed to the next floor.")
            return True
        print(wrap(f"Exit sealed. You still need {len(floor.relic_positions)} relic(s)."))

    event_roll = random.random()
    if event_roll < 0.12:
        gain = random.randint(1, 3)
        player.attack += gain // 2
        print(wrap(f"You discover a sharpened shard. Attack +{gain // 2}."))
    elif event_roll > 0.9:
        trap = random.randint(1, 3)
        player.health -= trap
        print(wrap(f"A trap scratches you for {trap} damage."))
        if player.health <= 0:
            print("You succumb to your wounds.")
            return False

    return True


def move_player(player: Player, cmd: str) -> bool:
    deltas = {
        "north": (0, -1),
        "south": (0, 1),
        "west": (-1, 0),
        "east": (1, 0),
    }
    if cmd not in deltas:
        return False

    dx, dy = deltas[cmd]
    nx = player.x + dx
    ny = player.y + dy
    if not (0 <= nx < MAP_SIZE and 0 <= ny < MAP_SIZE):
        print("You hit a stone wall.")
        return True

    player.x, player.y = nx, ny
    print(f"You move to ({player.x + 1}, {player.y + 1}).")
    return True


def play() -> None:
    print(wrap(INTRO))
    player = Player()

    for floor_number in range(1, FLOORS + 1):
        floor = FloorState(floor_number)
        player.x = 0
        player.y = 0
        print(f"\n=== FLOOR {floor_number}/{FLOORS} ===")

        while True:
            if player.health <= 0:
                print("Game over.")
                return

            cmd = input("\nCommand: ").strip().lower()
            if cmd == "quit":
                print("Thanks for playing.")
                return
            if cmd == "help":
                print("Commands: north, south, east, west, look, stats, heal, help, quit")
                continue
            if cmd == "look":
                print_map(player, floor)
                continue
            if cmd == "stats":
                print(
                    f"HP: {player.health} | ATK: {player.attack} | Potions: {player.heal_potions} | "
                    f"Relics this floor: {TARGET_RELICS - len(floor.relic_positions)}/{TARGET_RELICS}"
                )
                continue
            if cmd == "heal":
                if player.heal_potions > 0:
                    restored = random.randint(4, 7)
                    player.health = min(START_HEALTH + floor_number * 2, player.health + restored)
                    player.heal_potions -= 1
                    print(f"You healed for {restored}. HP is now {player.health}.")
                else:
                    print("No potions left.")
                continue

            moved = move_player(player, cmd)
            if not moved:
                print("Unknown command. Type 'help'.")
                continue

            alive = handle_tile(player, floor)
            if not alive:
                return

            if (player.x, player.y) == floor.exit and len(floor.relic_positions) == 0:
                print("You descend to the next floor...")
                player.heal_potions += 1
                player.health = min(START_HEALTH + floor_number * 2, player.health + 3)
                break

    print("\nYou escaped with all relics. Victory!")


if __name__ == "__main__":
    random.seed()
    play()
