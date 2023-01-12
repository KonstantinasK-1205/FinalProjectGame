import random

from entity.npc.npc_base import *
from entity.npc.behaviours.attack import Attack
from entity.npc.behaviours.pursuit import Pursuit
from entity.npc.behaviours.wandering import Wandering
from entity.npc.behaviours.rush import Rush
from projectile import Projectile
from sprites.pickup_ammo import *


class Enemy(NPC):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        # Base Attack stats
        self.damage = 0  # How much damage should enemy do to player

        self.fire_cooldown = 300  # Cooldown before enemy can shoot again
        self.last_fire_time = 0  # Reset timer, when enemy fired

        self.bullet_in_gun = 0  # How much enemy has bullet in gun at moment
        self.bullet_in_total = 0  # How much enemy has bullet in total
        self.bullet_per_shot = 0  # How many bullets fired per shot
        self.bullet_after_reload = 0  # How many bullets should add after reload
        self.bullet_reset_amount = 0  # How many bullets should enemy have, after being empty

        self.is_reloading = False  # Set to True, if enemy run out of bullets
        self.reload_time = 0  # How long enemy has been reloading
        self.reload_duration = 3000  # How long should enemy reload

        # Base Projectile stats
        self.projectile_speed = 0.025  # Projectile flying speed
        self.projectile_lifetime = 80  # Projectile lifetime in ticks
        self.projectile_spread = [0.0, 0.0]  # Projectile spread from origin
        self.projectile_size = [0.1, 0.1]  # Projectile sprite size
        self.projectile_sprite = "resources/sprites/projectile/empty.png"

        self.take_damage_on_attack = False  # Makes enemy take damage after attack
        self.damage_on_attack = 0  # How much damage enemy should take after attack

        self.seeing_player = False  # Sets boolean if enemy can see player
        self.seeing_player_time = 0  # Reset timer, when enemy saw player
        self.seeing_player_cooldown = 30  # Cooldown before enemy can check for player again

        ####
        # Pursuit variables
        self.in_pursuit = False
        self.last_known_pos = [0, 0, 0]

        # Wandering variables
        self.is_wandering = False
        self.wandering_time = 0
        self.wandering_cooldown = 60

        # Rush variables
        self.can_rush = False
        self.is_rushing = False
        self.rushing_time = 0
        self.rushing_cooldown = 1500
        self.rushing_stop_after = 2000

        # Special Abilities
        self.can_detect_obstructed = True

        self.ammo_dropped = False
        self.droppable_ammo = "None"
        self.can_drop_ammo_on_death = False

        # Base Animation variables
        self.current_state = "Idle"
        self.current_behaviour = "Wandering"
        self.behaviour_states = {
            "Attack": Attack(game, self),
            "Pursuit": Pursuit(game, self),
            "Wandering": Wandering(game, self),
            "Rush": Rush(game, self)
        }

    def update(self):
        self.animation.animate(self.game.dt)

        self.current_state = self.animation.get_state()
        self.sprite = self.animation.get_sprite()

        # If enemy is dead, stop main logic
        if not self.alive:
            if not self.ammo_dropped:
                if self.droppable_ammo == "Shotgun":
                    self.game.object_handler.add_pickup(ShotgunAmmo(self.game,
                                                                    self.exact_pos,
                                                                    self.bullet_in_total))
                self.ammo_dropped = True
            self.change_state("Death")
            return

        # If NPC hurt, he can't do anything else
        if self.pain:
            if self.current_state == "Pain" and self.animation.completed:
                self.pain = False
            return

        # Check logic and set specific behaviour based on logic
        self.run_logic()
        self.behaviour_states[self.current_behaviour].movement(self.last_known_pos)
        self.behaviour_states[self.current_behaviour].update()

    def draw(self):
        self.game.renderer.draw_sprite(self.pos, self.size, self.sprite)

    def run_logic(self):
        # Limit enemy can_see_player calls, and allow to recheck only after N time has passed
        if self.seeing_player_time >= self.seeing_player_cooldown:
            self.seeing_player = False

        # Calculate distance from player once and reuse it
        self.distance_from_player = self.distance_from(self.player)

        # If player outside update range, quit logic
        if self.distance_from_player > self.update_range:
            return
        elif self.distance_from_player <= self.update_range:
            # If player inside update range, let it wander around
            # Although if enemy was in pursuit mode, let it move toward last known position
            if not self.in_pursuit:
                self.current_behaviour = "Wandering"
            else:
                self.current_behaviour = "Pursuit"

            # Check if player in vision range
            if self.distance_from_player <= self.vision_range:
                # Calculate angle which is always opposing player - used for movement and sight
                angle = math.atan2(self.player.pos[1] - self.pos[1], self.player.pos[0] - self.pos[0])

                # If enemy isn't seeing player, allow him to check
                if not self.seeing_player:
                    self.seeing_player = self.can_see_player(self.exact_pos, self.player.grid_pos, angle)
                    self.seeing_player_time = 0
                else:
                    self.seeing_player_time += self.game.dt

                if self.can_detect_obstructed and self.distance_from_player <= self.detect_range:
                    self.seeing_player = True

                # If player is visible, based on distance move towards it or attack
                if self.seeing_player:
                    self.angle = angle
                    self.last_known_pos = self.player.exact_pos
                    self.is_wandering = False

                    # Based on distance to player, choice Action
                    if self.distance_from_player <= self.attack_range:
                        self.current_behaviour = "Attack"
                    else:
                        self.current_behaviour = "Pursuit"

        # Set action based on logic above
        if self.current_behaviour == "Wandering":
            self.change_state("Walk")
            self.is_wandering = True
        elif self.current_behaviour == "Pursuit":
            if self.seeing_player:
                if self.can_rush:
                    self.current_behaviour = "Rush"
                else:
                    self.in_pursuit = True
            self.change_state("Walk")
        elif self.current_behaviour == "Attack":
            pass

    def create_projectile(self):
        # Calculate projectile spawn position
        position = [self.pos[0], self.pos[1], (self.size[1] / 2)]

        # Calculate spread of projectile, if spread is not equal to zero
        if not self.projectile_spread[0] == 0:
            spread = [random.uniform(-self.projectile_spread[0], self.projectile_spread[0]),
                      random.uniform(-self.projectile_spread[1], self.projectile_spread[1])]
        else:
            spread = [0, 0]

        # Calculate projectile trajectory, using player and enemy position
        angle = [math.atan2((self.player.pos[1] - spread[1]) - self.pos[1],
                            (self.player.pos[0] - spread[0]) - self.pos[0]),
                 math.atan(self.player.pos[2] - self.pos[2])]

        # Set-up projectile data array
        bullet_data = [self.damage,
                       self.projectile_speed,
                       self.projectile_lifetime,
                       "Enemy",
                       self.projectile_size[0],
                       self.projectile_size[1]]

        # Spawn bullet
        self.game.object_handler.add_bullet(Projectile(self.game, position, angle, bullet_data, self.projectile_sprite))
