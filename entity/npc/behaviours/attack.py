from entity.npc.behaviours.behaviour import Behaviour


class Attack(Behaviour):
    def __init__(self, game, enemy):
        super().__init__(game, enemy)

    def movement(self, destination=None):
        pass

    def update(self):
        self.enemy.last_fire_time += self.game.dt
        if self.enemy.bullet_in_gun <= 0 and not self.enemy.is_reloading:
            self.enemy.is_reloading = True
            self.enemy.reload_time = 0

        if self.enemy.is_reloading and self.enemy.reload_time >= self.enemy.reload_duration:
            self.enemy.reload_time = 0
            self.enemy.is_reloading = False
            self.enemy.bullet_in_gun = self.enemy.bullet_after_reload
            self.enemy.bullet_in_total -= self.enemy.bullet_after_reload
            if self.enemy.bullet_in_total <= 0:
                self.enemy.bullet_in_total = self.enemy.bullet_reset_amount

        if self.enemy.is_reloading:
            self.enemy.reload_time += self.game.dt
            self.enemy.change_state("Idle")
            return
        else:
            if self.enemy.last_fire_time > self.enemy.fire_cooldown:
                self.enemy.change_state("Attack")

        if self.enemy.current_state == "Attack" and self.enemy.animation.completed:
            if self.enemy.bullet_in_gun >= self.enemy.bullet_per_shot:
                for i in range(self.enemy.bullet_per_shot):
                    self.enemy.create_projectile()
                    self.game.sound.play_sfx(self.enemy.sfx_attack, [self.enemy.exact_pos,
                                                                     self.enemy.player.exact_pos])
                if self.enemy.take_damage_on_attack:
                    self.enemy.apply_damage(self.enemy.damage_on_attack)
                self.enemy.last_fire_time = 0
                self.enemy.bullet_in_gun -= self.enemy.bullet_per_shot
