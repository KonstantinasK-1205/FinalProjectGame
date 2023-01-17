from collision import *
from sprites.animation_manager import *
from sprites.sprite import Sprite


class NPC(Sprite):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)

        # Create animation class for each NPC and set default state
        self.animation = Animation()
        self.current_state = "Idle"

        # Ranges for NPC activity
        self.attack_range = 1  # Range on which enemy starts to attack
        self.detect_range = 1  # Range on which enemy can detect player through walls ( if he has ability )
        self.vision_range = 17  # Range on which enemy can see player, and move towards it
        self.update_range = 100  # Range on which enemy starts to receive update

        # Base Stats
        self.alive = True
        self.pain = False
        self.health = 100
        self.speed = 0.002
        self.angle = 0
        self.dx = 0
        self.dy = 0

        # Default size for NPC
        self.size = [0.7, 0.7]

        # Variable which allows to save distance, for reusing
        self.distance_from_player = 0

        # Base Sounds
        self.sfx_attack = "Soldier attack"
        self.sfx_pain = "Soldier pain"
        self.sfx_death = "Soldier death"

    def apply_damage(self, damage):
        self.health -= damage
        if self.health > 0:
            sound = self.sfx_pain
            self.pain = True
            self.change_state("Pain")
        else:
            sound = self.sfx_death
            self.alive = False
            self.game.object_handler.update_npc_list()
        self.game.sound.play_sfx(sound, [self.exact_pos, self.player.exact_pos])

    # Using power of trigonometry check if NPC can see player
    def can_see_player(self, npc_pos, player_pos, angle):
        # Init variables
        step = 0.5

        # Preload map object function
        is_wall = self.game.map.is_wall

        # Calculate NPC sin and cos of angle once and reuse
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        # Workaround, so we won't modify original enemy values
        npc_pos = [npc_pos[0], npc_pos[1], npc_pos[2]]

        # Check if NPC can walk straight line to player, if so NPC can see player
        for i in range(self.vision_range):
            # Increase NPC position by step, stop increasing certain axis, if pos == player axis pos
            if not int(npc_pos[0]) == player_pos[0]:
                npc_pos[0] += cos_angle * step
            if not int(npc_pos[1]) == player_pos[1]:
                npc_pos[1] += sin_angle * step

            # Check if NPC pos == player, or if pos is in wall
            if player_pos[0] == int(npc_pos[0]) and player_pos[1] == int(npc_pos[1]):
                return True
            elif is_wall(int(npc_pos[0]), int(npc_pos[1])):
                break
        return False

    # Change NPC state and animation
    def change_state(self, state):
        if not self.current_state == state or state == "Pain":
            self.current_state = state
            self.animation.change_animation(state)
