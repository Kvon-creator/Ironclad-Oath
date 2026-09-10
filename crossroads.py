#!/usr/bin/env python3
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class Direction(Enum):
    NORTH = (0, -1, "^")
    EAST = (1, 0, ">")
    SOUTH = (0, 1, "v")
    WEST = (-1, 0, "<")

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]

    @property
    def glyph(self) -> str:
        return self.value[2]

    @classmethod
    def from_str(cls, s: str) -> Optional["Direction"]:
        mapping = {"w": cls.NORTH, "d": cls.EAST, "s": cls.SOUTH, "a": cls.WEST}
        return mapping.get(s.strip().lower(), None)


class FacingAngle(Enum):
    FRONT = 1.0
    FLANK = 1.25
    REAR = 1.75


@dataclass
class Unit:
    id_tag: str
    name: str
    faction: str  # "PLAYER" or "ENEMY"
    x: int
    y: int
    facing: Direction
    max_hp: float
    hp: float
    max_fatigue: float
    fatigue: float
    max_poise: float
    poise: float
    base_evasion: float
    attack_power: float
    attack_range: int
    poise_damage: float
    armor_shred: float
    armor: Dict[str, float]
    has_shield: bool = False
    is_spear: bool = False
    is_afflicted: bool = False
    is_staggered: bool = False
    in_shield_wall: bool = False

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    @property
    def is_exhausted(self) -> bool:
        return self.fatigue >= self.max_fatigue

    def get_effective_evasion(self, angle: FacingAngle) -> float:
        if self.is_staggered or angle == FacingAngle.REAR or self.is_exhausted:
            return 0.0
        eva = self.base_evasion
        if angle == FacingAngle.FLANK:
            eva -= 0.25
        return max(0.0, eva)


class CrossroadsGame:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.bloom_tiles = {(1, 3), (1, 4), (2, 3), (2, 4), (2, 5)}
        self.ruin_tiles = {(4, 4), (5, 4)}
        self.turn_count = 1
        self.units: List[Unit] = []
        self._init_units()

    def _init_units(self):
        # Player squad (starts south)
        self.units.append(
            Unit(
                id_tag="P1",
                name="Vanguard Knight",
                faction="PLAYER",
                x=4,
                y=8,
                facing=Direction.NORTH,
                max_hp=45,
                hp=45,
                max_fatigue=30,
                fatigue=0,
                max_poise=40,
                poise=40,
                base_evasion=0.10,
                attack_power=14.0,
                attack_range=1,
                poise_damage=15.0,
                armor_shred=8.0,
                armor={"FRONT": 50.0, "FLANK": 30.0, "REAR": 15.0},
                has_shield=True,
            )
        )
        self.units.append(
            Unit(
                id_tag="P2",
                name="Hedge Halberdier",
                faction="PLAYER",
                x=5,
                y=8,
                facing=Direction.NORTH,
                max_hp=38,
                hp=38,
                max_fatigue=25,
                fatigue=0,
                max_poise=30,
                poise=30,
                base_evasion=0.15,
                attack_power=16.0,
                attack_range=2,
                poise_damage=12.0,
                armor_shred=10.0,
                armor={"FRONT": 35.0, "FLANK": 20.0, "REAR": 10.0},
                is_spear=True,
            )
        )
        self.units.append(
            Unit(
                id_tag="P3",
                name="Outrider Scout",
                faction="PLAYER",
                x=6,
                y=9,
                facing=Direction.NORTH,
                max_hp=28,
                hp=28,
                max_fatigue=20,
                fatigue=0,
                max_poise=18,
                poise=18,
                base_evasion=0.30,
                attack_power=11.0,
                attack_range=3,
                poise_damage=6.0,
                armor_shred=3.0,
                armor={"FRONT": 15.0, "FLANK": 10.0, "REAR": 5.0},
            )
        )

        # Enemy squad (starts north)
        self.units.append(
            Unit(
                id_tag="E1",
                name="Footman A",
                faction="ENEMY",
                x=4,
                y=2,
                facing=Direction.SOUTH,
                max_hp=35,
                hp=35,
                max_fatigue=25,
                fatigue=0,
                max_poise=25,
                poise=25,
                base_evasion=0.15,
                attack_power=12.0,
                attack_range=1,
                poise_damage=10.0,
                armor_shred=6.0,
                armor={"FRONT": 30.0, "FLANK": 20.0, "REAR": 10.0},
                has_shield=True,
            )
        )
        self.units.append(
            Unit(
                id_tag="E2",
                name="Footman B",
                faction="ENEMY",
                x=5,
                y=2,
                facing=Direction.SOUTH,
                max_hp=35,
                hp=35,
                max_fatigue=25,
                fatigue=0,
                max_poise=25,
                poise=25,
                base_evasion=0.15,
                attack_power=12.0,
                attack_range=1,
                poise_damage=10.0,
                armor_shred=6.0,
                armor={"FRONT": 30.0, "FLANK": 20.0, "REAR": 10.0},
                has_shield=True,
            )
        )
        self.units.append(
            Unit(
                id_tag="ET",
                name="Bloom Thrall",
                faction="ENEMY",
                x=1,
                y=2,
                facing=Direction.SOUTH,
                max_hp=55,
                hp=55,
                max_fatigue=40,
                fatigue=0,
                max_poise=60,
                poise=60,
                base_evasion=0.05,
                attack_power=17.0,
                attack_range=1,
                poise_damage=22.0,
                armor_shred=14.0,
                armor={"FRONT": 15.0, "FLANK": 15.0, "REAR": 15.0},
                is_afflicted=True,
            )
        )

    def get_unit_at(self, x: int, y: int) -> Optional[Unit]:
        for u in self.units:
            if u.is_alive and u.x == x and u.y == y:
                return u
        return None

    def update_auras(self):
        for u in self.units:
            u.in_shield_wall = False
            if not u.is_alive or not u.has_shield:
                continue
            # Check adjacent allies
            for d in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
                neighbor = self.get_unit_at(u.x + d.dx, u.y + d.dy)
                if neighbor and neighbor.faction == u.faction and neighbor.has_shield and neighbor.facing == u.facing:
                    u.in_shield_wall = True
                    break

    def determine_relative_facing(self, attacker: Unit, defender: Unit) -> Tuple[FacingAngle, str]:
        dx = attacker.x - defender.x
        dy = attacker.y - defender.y
        # Normalize to dominant axis
        if abs(dx) > abs(dy):
            approach = Direction.EAST if dx > 0 else Direction.WEST
        else:
            approach = Direction.SOUTH if dy > 0 else Direction.NORTH

        def_facing = defender.facing
        if approach == def_facing:
            return FacingAngle.FRONT, "FRONT"
        elif approach.dx == -def_facing.dx and approach.dy == -def_facing.dy:
            return FacingAngle.REAR, "REAR"
        else:
            return FacingAngle.FLANK, "FLANK"

    def execute_combat(self, attacker: Unit, defender: Unit):
        cost = 4.0 if not attacker.is_exhausted else 6.0
        attacker.fatigue = min(attacker.max_fatigue, attacker.fatigue + cost)

        angle, armor_slot = self.determine_relative_facing(attacker, defender)
        print(f"\n>> {attacker.name} strikes {defender.name} from the {angle.name}!")[cite: 2]

        # Shield wall frontal deflection
        if defender.in_shield_wall and angle == FacingAngle.FRONT and attacker.attack_range > 1:
            print(f"[{defender.name}'s Shield Wall deflected all incoming projectile force!]")
            return

        raw_dmg = attacker.attack_power * angle.value[cite: 2]
        armor_val = defender.armor[armor_slot]

        if angle == FacingAngle.REAR:
            unmitigated = raw_dmg * 0.75 + max(0.0, (raw_dmg * 0.25) - armor_val)[cite: 2]
            absorbed = min(armor_val, raw_dmg * 0.25)
        else:
            absorbed = min(armor_val, raw_dmg * 0.65)[cite: 2]
            unmitigated = raw_dmg - absorbed

        # Apply armor break & HP damage
        defender.armor[armor_slot] = max(0.0, defender.armor[armor_slot] - attacker.armor_shred)[cite: 2]
        defender.hp = max(0.0, defender.hp - unmitigated)[cite: 2]

        if not defender.is_afflicted:
            defender.poise = max(0.0, defender.poise - attacker.poise_damage)[cite: 2]
            if defender.poise <= 0.0:
                defender.is_staggered = True[cite: 2]
                print(f"** {defender.name} has been STAGGERED! **"[cite: 2])

        print(f"Result: {unmitigated:.1f} HP damage dealt ({absorbed:.1f} absorbed by {armor_slot} armor).")
        print(f"{defender.name} HP: {defender.hp:.1f}/{defender.max_hp} | {armor_slot} Armor left: {defender.armor[armor_slot]:.1f}")

        if not defender.is_alive:
            print(f"*** {defender.name} has fallen in battle! ***")
            if defender.is_afflicted:
                print(f"Spore Burst: The Thrall detonates, spreading Bloom spores across ({defender.x}, {defender.y})!")[cite: 2]
                self.bloom_tiles.add((defender.x, defender.y))

    def apply_bloom_hazard(self):
        print("\n--- Environmental Phase: Bloom Spore Pulse ---")[cite: 2]
        for u in self.units:
            if u.is_alive and (u.x, u.y) in self.bloom_tiles:
                u.fatigue = min(u.max_fatigue, u.fatigue + 2.0)[cite: 2]
                # Corrode all armor sectors by 5%
                for k in u.armor:
                    u.armor[k] = max(0.0, u.armor[k] * 0.95)[cite: 2]
                print(f"[BLOOM TOXIN] {u.name} at ({u.x},{u.y}) suffers +2 Fatigue and 5% armor corrosion!"[cite: 2])

    def render_map(self):
        print("\n   " + " ".join(f" {x} " for x in range(self.width)))
        for y in range(self.height):
            row_str = f"{y:2d} "
            for x in range(self.width):
                unit = self.get_unit_at(x, y)
                if unit:
                    glyph = f"{unit.id_tag}{unit.facing.glyph}"
                elif (x, y) in self.ruin_tiles:
                    glyph = "###"
                elif (x, y) in self.bloom_tiles:
                    glyph = " % "
                else:
                    glyph = " . "
                row_str += glyph
            print(row_str)
        print("Legend: [P#] Mercenaries | [E#] Imperials | [ET] Bloom Thrall | [ % ] Bloom Spores | [###] Stone Ruins")

    def run_turn(self):
        self.update_auras()
        self.render_map()

        print(f"\n==================== TURN {self.turn_count} (PLAYER PHASE) ====================")
        active_player_units = [u for u in self.units if u.faction == "PLAYER" and u.is_alive]

        for u in active_player_units:
            if u.is_staggered:
                print(f"\n{u.name} is recovering from Stagger and cannot act this turn."[cite: 2])
                u.is_staggered = False
                u.poise = u.max_poise * 0.5
                continue

            print(f"\n--- Controlling {u.name} [{u.id_tag}] at ({u.x}, {u.y}) Facing: {u.facing.name} ---")
            print(f"HP: {u.hp:.1f}/{u.max_hp} | Fatigue: {u.fatigue:.1f}/{u.max_fatigue} | Poise: {u.poise:.1f}/{u.max_poise}")
            print(f"Armor: Front {u.armor['FRONT']:.0f} | Flank {u.armor['FLANK']:.0f} | Rear {u.armor['REAR']:.0f}")
            if u.in_shield_wall:
                print("[ACTIVE FORMATION: Shield Wall Lock]")

            # 1. Movement
            mv = input("Move (W/A/S/D steps, e.g., 'ww' or enter to stay): ").strip().lower()
            for step in mv:
                dx, dy = 0, 0
                if step == "w": dy = -1
                elif step == "s": dy = 1
                elif step == "a": dx = -1
                elif step == "d": dx = 1

                nx, ny = u.x + dx, u.y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and not self.get_unit_at(nx, ny) and (nx, ny) not in self.ruin_tiles:
                    u.x, u.y = nx, ny
                    move_tax = 2.0 if (nx, ny) in self.bloom_tiles else 1.0[cite: 2]
                    u.fatigue = min(u.max_fatigue, u.fatigue + move_tax)

            # 2. Attack check
            targets = []
            for enemy in [e for e in self.units if e.faction == "ENEMY" and e.is_alive]:
                dist = abs(u.x - enemy.x) + abs(u.y - enemy.y)
                if dist <= u.attack_range:
                    targets.append(enemy)

            if targets:
                print("Available targets in range:")
                for idx, t in enumerate(targets):
                    angle, _ = self.determine_relative_facing(u, t)
                    print(f"  [{idx}] {t.name} at ({t.x}, {t.y}) - Vector: {angle.name}")
                pick = input(f"Select target index (0-{len(targets)-1}) or enter to pass: ").strip()
                if pick.isdigit() and int(pick) < len(targets):
                    self.execute_combat(u, targets[int(pick)])
            else:
                print("No targets within weapon range.")

            # 3. Facing choice
            fc = input("Set final facing direction (W=North, D=East, S=South, A=West) [Default keeps current]: ").strip().lower()
            new_dir = Direction.from_str(fc)
            if new_dir:
                u.facing = new_dir

        # Check win condition
        if not any(e.is_alive for e in self.units if e.faction == "ENEMY"):
            self.render_map()
            print("\nVICTORY! All hostiles cleared from the outpost.")
            sys.exit(0)

        # Enemy Phase
        print(f"\n==================== TURN {self.turn_count} (ENEMY PHASE) ====================")
        self.update_auras()
        for enemy in [e for e in self.units if e.faction == "ENEMY" and e.is_alive]:
            if enemy.is_staggered:
                print(f"{enemy.name} is staggered and loses their turn."[cite: 2])
                enemy.is_staggered = False
                enemy.poise = enemy.max_poise * 0.5
                continue

            # Target closest player
            living_players = [p for p in self.units if p.faction == "PLAYER" and p.is_alive]
            if not living_players:
                break
            living_players.sort(key=lambda p: abs(p.x - enemy.x) + abs(p.y - enemy.y))
            target = living_players[0]

            # Step toward target
            step_x = 1 if target.x > enemy.x else (-1 if target.x < enemy.x else 0)
            step_y = 1 if target.y > enemy.y else (-1 if target.y < enemy.y else 0)

            # Prioritize moving on open tiles
            cand_x, cand_y = enemy.x + step_x, enemy.y
            if step_x != 0 and 0 <= cand_x < self.width and not self.get_unit_at(cand_x, enemy.y) and (cand_x, enemy.y) not in self.ruin_tiles:
                enemy.x = cand_x
            else:
                cand_y = enemy.y + step_y
                if step_y != 0 and 0 <= cand_y < self.height and not self.get_unit_at(enemy.x, cand_y) and (enemy.x, cand_y) not in self.ruin_tiles:
                    enemy.y = cand_y

            # Re-orient facing toward the player
            dx, dy = target.x - enemy.x, target.y - enemy.y
            if abs(dx) > abs(dy):
                enemy.facing = Direction.EAST if dx > 0 else Direction.WEST
            elif dy != 0:
                enemy.facing = Direction.SOUTH if dy > 0 else Direction.NORTH

            dist = abs(enemy.x - target.x) + abs(enemy.y - target.y)
            if dist <= enemy.attack_range:
                self.execute_combat(enemy, target)

        # Apply hazards & recover
        self.apply_bloom_hazard()
        for u in self.units:
            if u.is_alive:
                # Slight passive fatigue recovery if not exhausted
                u.fatigue = max(0.0, u.fatigue - 1.0)

        # Check loss condition
        if not any(p.is_alive for p in self.units if p.faction == "PLAYER"):
            self.render_map()
            print("\nDEFEAT: Your mercenary vanguard has perished.")
            sys.exit(0)

        self.turn_count += 1


if __name__ == "__main__":
    game = CrossroadsGame()
    print("Welcome to Ironclad Oath: The Crossroads Outpost Prototype.")
    print("Direct squad movement, protect your unarmored flanks, and watch the Bloom.")
    while True:
        game.run_turn()