#!/usr/bin/env python3
import sys
from dataclasses import dataclass, field
from enum import Enum, auto
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


class UnitState(Enum):
    READY = auto()
    EXHAUSTED = auto()
    DONE = auto()


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
    in_spear_hedge: bool = False

    # Turn action flags
    has_moved: bool = False
    has_acted: bool = False
    state: UnitState = UnitState.READY

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    @property
    def is_exhausted(self) -> bool:
        return self.fatigue >= self.max_fatigue

    def reset_turn(self):
        self.has_moved = False
        self.has_acted = False
        self.state = UnitState.READY

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
        # Player squad (South)
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

        # Enemy squad (North)
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
            u.in_spear_hedge = False
            if not u.is_alive:
                continue

            for d in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
                neighbor = self.get_unit_at(u.x + d.dx, u.y + d.dy)
                if neighbor and neighbor.faction == u.faction and neighbor.is_alive:
                    if u.has_shield and neighbor.has_shield and neighbor.facing == u.facing:
                        u.in_shield_wall = True
                    if u.is_spear and neighbor.is_spear and neighbor.facing == u.facing:
                        u.in_spear_hedge = True

    def determine_relative_facing(self, attacker: Unit, defender: Unit) -> Tuple[FacingAngle, str]:
        dx = attacker.x - defender.x
        dy = attacker.y - defender.y
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

    def execute_combat(self, attacker: Unit, defender: Unit, is_opportunity: bool = False):
        if not is_opportunity:
            cost = 4.0 if not attacker.is_exhausted else 6.0
            attacker.fatigue = min(attacker.max_fatigue, attacker.fatigue + cost)

        angle, armor_slot = self.determine_relative_facing(attacker, defender)
        tag = "[OPPORTUNITY STRIKE] " if is_opportunity else ""
        print(f"\n>> {tag}{attacker.name} strikes {defender.name} from the {angle.name}!")

        # Shield Wall frontal ranged immunity
        if defender.in_shield_wall and angle == FacingAngle.FRONT and attacker.attack_range > 1:
            print(f"[{defender.name}'s Shield Wall deflected all incoming projectile force!]")
            return

        raw_dmg = attacker.attack_power * angle.value
        armor_val = defender.armor[armor_slot]

        if angle == FacingAngle.REAR:
            unmitigated = raw_dmg * 0.75 + max(0.0, (raw_dmg * 0.25) - armor_val)
            absorbed = min(armor_val, raw_dmg * 0.25)
        else:
            absorbed = min(armor_val, raw_dmg * 0.65)
            unmitigated = raw_dmg - absorbed

        defender.armor[armor_slot] = max(0.0, defender.armor[armor_slot] - attacker.armor_shred)
        defender.hp = max(0.0, defender.hp - unmitigated)

        if not defender.is_afflicted:
            defender.poise = max(0.0, defender.poise - attacker.poise_damage)
            if defender.poise <= 0.0:
                defender.is_staggered = True
                print(f"** {defender.name} has been STAGGERED! **")

        print(f"Result: {unmitigated:.1f} HP damage dealt ({absorbed:.1f} absorbed by {armor_slot} armor).")
        print(f"{defender.name} HP: {defender.hp:.1f}/{defender.max_hp} | {armor_slot} Armor left: {defender.armor[armor_slot]:.1f}")

        if not defender.is_alive:
            print(f"*** {defender.name} has fallen in battle! ***")
            if defender.is_afflicted:
                print(f"[SPORE BURST] Bloom Thrall bursts across ({defender.x}, {defender.y})!")
                self.bloom_tiles.add((defender.x, defender.y))

    def check_zoc_trigger(self, mover: Unit, from_x: int, from_y: int) -> bool:
        """Triggers attacks of opportunity if unit disengages from an enemy frontal tile."""
        for enemy in self.units:
            if enemy.is_alive and enemy.faction != mover.faction and not enemy.is_staggered:
                front_x = enemy.x + enemy.facing.dx
                front_y = enemy.y + enemy.facing.dy
                if (from_x, from_y) == (front_x, front_y):
                    print(f"\n[!] Disengagement detected! {mover.name} breaks out of {enemy.name}'s Frontal Zone of Control!")
                    self.execute_combat(enemy, mover, is_opportunity=True)
                    if not mover.is_alive:
                        return False
        return True

    def check_spear_hedge_reaction(self, mover: Unit, to_x: int, to_y: int) -> bool:
        """Spear hedge units interrupt enemies advancing directly toward their front."""
        for enemy in self.units:
            if enemy.is_alive and enemy.faction != mover.faction and enemy.in_spear_hedge and not enemy.is_staggered:
                f_x = enemy.x + enemy.facing.dx
                f_y = enemy.y + enemy.facing.dy
                if (to_x, to_y) == (f_x, f_y):
                    print(f"\n[!] Spear Hedge Activated! {enemy.name} executes an intercepting brace!")
                    self.execute_combat(enemy, mover, is_opportunity=True)
                    if mover.is_staggered or not mover.is_alive:
                        print(f"Movement halted by Spear Hedge thrust!")
                        return False
        return True

    def apply_bloom_hazard(self):
        print("\n--- Environmental Phase: Bloom Spore Pulse ---")
        for u in self.units:
            if u.is_alive and (u.x, u.y) in self.bloom_tiles:
                u.fatigue = min(u.max_fatigue, u.fatigue + 2.0)
                for k in u.armor:
                    u.armor[k] = max(0.0, u.armor[k] * 0.95)
                print(f"[BLOOM TOXIN] {u.name} at ({u.x},{u.y}) suffers +2 Fatigue and 5% armor corrosion!")

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
        print("Legend: [P#] Mercenaries | [E#] Imperials | [ET] Bloom Thrall | [ % ] Bloom Spores | [###] Ruins")

    def _execute_player_move(self, u: Unit):
        if u.has_moved:
            print("[This unit has already moved this turn.]")
            return

        valid_keys = {"w", "a", "s", "d"}
        while True:
            mv = input("Move sequence (W/A/S/D steps, e.g., 'ww' or Enter to cancel): ").strip().lower()
            if not mv:
                return

            if any(char not in valid_keys for char in mv):
                print("[Invalid characters. Use only W, A, S, or D.]")
                continue

            sim_x, sim_y = u.x, u.y
            accumulated_fatigue = 0.0
            steps = []
            valid_path = True

            for step in mv:
                dx, dy = 0, 0
                if step == "w": dy = -1
                elif step == "s": dy = 1
                elif step == "a": dx = -1
                elif step == "d": dx = 1

                nx, ny = sim_x + dx, sim_y + dy

                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    print(f"[Move error: Step '{step}' would leave map boundaries.]")
                    valid_path = False
                    break

                occupant = self.get_unit_at(nx, ny)
                if occupant and occupant != u:
                    print(f"[Move error: Tile ({nx}, {ny}) blocked by {occupant.name}.]")
                    valid_path = False
                    break

                if (nx, ny) in self.ruin_tiles:
                    print(f"[Move error: Blocked by Stone Ruins at ({nx}, {ny}).]")
                    valid_path = False
                    break

                steps.append((sim_x, sim_y, nx, ny))
                sim_x, sim_y = nx, ny
                accumulated_fatigue += 2.0 if (nx, ny) in self.bloom_tiles else 1.0

            if valid_path:
                # Step-by-step resolution for ZoC checks
                for ox, oy, nx, ny in steps:
                    if not self.check_zoc_trigger(u, ox, oy):
                        return
                    if not self.check_spear_hedge_reaction(u, nx, ny):
                        return
                    u.x, u.y = nx, ny

                u.fatigue = min(u.max_fatigue, u.fatigue + accumulated_fatigue)
                u.has_moved = True
                print(f"{u.name} moved to ({u.x}, {u.y}). Fatigue accrued: +{accumulated_fatigue:.1f}")
                self.update_auras()
                break

    def _execute_player_attack(self, u: Unit):
        if u.has_acted:
            print("[This unit has already acted this turn.]")
            return

        targets = []
        for enemy in [e for e in self.units if e.faction == "ENEMY" and e.is_alive]:
            dist = abs(u.x - enemy.x) + abs(u.y - enemy.y)
            if dist <= u.attack_range:
                targets.append(enemy)

        if not targets:
            print("[No enemy targets in weapon range.]")
            return

        print("Targets in range:")
        for idx, t in enumerate(targets):
            angle, _ = self.determine_relative_facing(u, t)
            print(f"  [{idx}] {t.name} at ({t.x}, {t.y}) - Vector: {angle.name}")

        while True:
            pick = input(f"Select target index (0-{len(targets)-1}) or Enter to cancel: ").strip()
            if pick == "":
                return
            if pick.isdigit() and 0 <= int(pick) < len(targets):
                self.execute_combat(u, targets[int(pick)])
                u.has_acted = True
                break
            print("[Invalid index selection.]")

    def _execute_unit_menu(self, u: Unit):
        while u.state != UnitState.DONE and u.is_alive:
            print(f"\n--- {u.name} [{u.id_tag}] at ({u.x}, {u.y}) | Facing: {u.facing.name} ---")
            print(f"HP: {u.hp:.1f}/{u.max_hp} | Fatigue: {u.fatigue:.1f}/{u.max_fatigue} | Poise: {u.poise:.1f}/{u.max_poise}")
            print(f"Armor: Front {u.armor['FRONT']:.0f} | Flank {u.armor['FLANK']:.0f} | Rear {u.armor['REAR']:.0f}")
            flags = []
            if u.has_moved: flags.append("MOVED")
            if u.has_acted: flags.append("ACTED")
            if u.in_shield_wall: flags.append("SHIELD-WALL")
            if u.in_spear_hedge: flags.append("SPEAR-HEDGE")
            print(f"Status: {', '.join(flags) if flags else 'READY'}")

            print("[M] Move  |  [A] Attack  |  [R] Rest (+3 Stamina)  |  [F] Orient & Finish  |  [B] Back")
            cmd = input("Action: ").strip().lower()

            if cmd == "m":
                self._execute_player_move(u)
                self.render_map()
            elif cmd == "a":
                self._execute_player_attack(u)
            elif cmd == "r":
                if u.has_acted:
                    print("[Already acted this turn.]")
                else:
                    u.fatigue = max(0.0, u.fatigue - 3.0)
                    u.has_acted = True
                    print(f"{u.name} catches their breath. Fatigue recovered: -3.0.")
            elif cmd == "f":
                fc = input("Set final facing (W=North, D=East, S=South, A=West) [Enter keeps current]: ").strip().lower()
                new_dir = Direction.from_str(fc)
                if new_dir:
                    u.facing = new_dir
                u.state = UnitState.DONE
                print(f"{u.name} locks stance facing {u.facing.name}. Activation complete.")
                break
            elif cmd == "b":
                break
            else:
                print("[Invalid choice. Select M, A, R, F, or B.]")

    def run_turn(self):
        self.update_auras()
        for u in self.units:
            if u.faction == "PLAYER":
                u.reset_turn()

        while True:
            self.render_map()
            active_units = [u for u in self.units if u.faction == "PLAYER" and u.is_alive and u.state != UnitState.DONE]
            if not active_units:
                break

            print(f"\n==================== TURN {self.turn_count} (TACTICAL DEPLOYMENT) ====================")
            print("Select a unit to activate:")
            for idx, u in enumerate(active_units):
                status = "STAGGERED" if u.is_staggered else "READY"
                print(f"  [{idx}] {u.name} [{u.id_tag}] ({status}) - ({u.x}, {u.y})")
            print("  [E] End Player Turn Early")

            choice = input(f"Select unit (0-{len(active_units)-1}) or 'E': ").strip().lower()
            if choice == "e":
                break

            if choice.isdigit() and 0 <= int(choice) < len(active_units):
                sel_unit = active_units[int(choice)]
                if sel_unit.is_staggered:
                    print(f"\n{sel_unit.name} is recovering from Stagger this turn.")
                    sel_unit.is_staggered = False
                    sel_unit.poise = sel_unit.max_poise * 0.5
                    sel_unit.state = UnitState.DONE
                    continue
                self._execute_unit_menu(sel_unit)
            else:
                print("[Invalid unit index.]")

            # Check if all enemies are defeated mid-phase
            if not any(e.is_alive for e in self.units if e.faction == "ENEMY"):
                self.render_map()
                print("\nVICTORY! All hostiles cleared from the outpost.")
                sys.exit(0)

        # Enemy Phase
        print(f"\n==================== TURN {self.turn_count} (ENEMY PHASE) ====================")
        self.update_auras()
        for enemy in [e for e in self.units if e.faction == "ENEMY" and e.is_alive]:
            if enemy.is_staggered:
                print(f"{enemy.name} is staggered and loses their turn.")
                enemy.is_staggered = False
                enemy.poise = enemy.max_poise * 0.5
                continue

            living_players = [p for p in self.units if p.faction == "PLAYER" and p.is_alive]
            if not living_players:
                break
            living_players.sort(key=lambda p: abs(p.x - enemy.x) + abs(p.y - enemy.y))
            target = living_players[0]

            step_x = 1 if target.x > enemy.x else (-1 if target.x < enemy.x else 0)
            step_y = 1 if target.y > enemy.y else (-1 if target.y < enemy.y else 0)

            cand_x, cand_y = enemy.x + step_x, enemy.y
            if step_x != 0 and 0 <= cand_x < self.width and not self.get_unit_at(cand_x, enemy.y) and (cand_x, enemy.y) not in self.ruin_tiles:
                if self.check_spear_hedge_reaction(enemy, cand_x, enemy.y):
                    enemy.x = cand_x
            else:
                cand_y = enemy.y + step_y
                if step_y != 0 and 0 <= cand_y < self.height and not self.get_unit_at(enemy.x, cand_y) and (enemy.x, cand_y) not in self.ruin_tiles:
                    if self.check_spear_hedge_reaction(enemy, enemy.x, cand_y):
                        enemy.y = cand_y

            # Re-orient facing towards target
            dx, dy = target.x - enemy.x, target.y - enemy.y
            if abs(dx) > abs(dy):
                enemy.facing = Direction.EAST if dx > 0 else Direction.WEST
            elif dy != 0:
                enemy.facing = Direction.SOUTH if dy > 0 else Direction.NORTH

            dist = abs(enemy.x - target.x) + abs(enemy.y - target.y)
            if dist <= enemy.attack_range and enemy.is_alive and not enemy.is_staggered:
                self.execute_combat(enemy, target)

        # Environmental phase & passive recovery
        self.apply_bloom_hazard()
        for u in self.units:
            if u.is_alive:
                u.fatigue = max(0.0, u.fatigue - 1.0)

        if not any(p.is_alive for p in self.units if p.faction == "PLAYER"):
            self.render_map()
            print("\nDEFEAT: Your mercenary vanguard has perished.")
            sys.exit(0)

        self.turn_count += 1


if __name__ == "__main__":
    game = CrossroadsGame()
    print("Welcome to Ironclad Oath: The Crossroads Outpost (State Machine Build).")
    print("Direct squad movement, protect your unarmored flanks, and watch the Bloom.")
    while True:
        try:
            game.run_turn()
        except KeyboardInterrupt:
            print("\nTactical simulation ended.")
            sys.exit(0)