from settings import *
import pygame as pg
import math

class Player:
	def __init__(self, game):
		self.game = game
		self.angle = PLAYER_ANGLE
		self.fired = False
		self.weapon_attack = 'Standby'
		self.health = PLAYER_MAX_HEALTH
		self.rel = 0
		self.health_recovery_delay = 5000
		self.time_prev = pg.time.get_ticks()

		self.armor = 100
		self.bullet_left = 10

		self.movingForward = False
		self.movingBackward = False
		self.movingLeft = False
		self.movingRight = False

	def handle_events(self, event):
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_w: self.movingForward = True
			if event.key == pg.K_s: self.movingBackward = True
			if event.key == pg.K_a: self.movingLeft = True
			if event.key == pg.K_d: self.movingRight = True

		elif event.type == pg.KEYUP:
			if event.key == pg.K_w: self.movingForward = False
			if event.key == pg.K_s: self.movingBackward = False
			if event.key == pg.K_a: self.movingLeft = False
			if event.key == pg.K_d: self.movingRight = False

		if event.type == pg.MOUSEMOTION:
			self.rel = pg.mouse.get_rel()[0]
			self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
			self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
			pg.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))

		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				if not self.game.weapon.reloading and self.bullet_left > 0:
					self.game.sound.shotgun.play()
					self.bullet_left -= 1
					self.fired = True
					self.weapon_attack = "Fire"
					self.game.global_trigger = True
					self.game.weapon.reloading = True

			if event.button == 3:
				if not self.game.weapon.reloading:
					self.game.sound.melee.play()
					self.fired = True
					self.weapon_attack = "Melee"
					self.game.global_trigger = True
					self.game.weapon.reloading = True

	def update(self):
		self.movement()
		self.recover_health()
		self.game.weapon.update(self.weapon_attack)
		if self.game.object_handler.killed >= self.game.map.enemy_amount:
			self.set_state("win")
		if self.health < 1:
			self.set_state("gameover")

	def recover_health(self):
		if self.health < PLAYER_MAX_HEALTH:
			time_now = pg.time.get_ticks()
			if time_now - self.time_prev > self.health_recovery_delay:
				self.time_prev = time_now
				self.health += 1

	def check_if_last_level(self):
		if len(self.game.map_lists) > 1:
			return False
		return True

	def set_state(self, string):
		if string == "gameover":
			self.game.object_renderer.status_game_over()
		elif string == "win":
			if self.check_if_last_level():
				self.game.object_renderer.status_game_won()
			else:
				self.game.map_lists.pop(0)
				self.game.new_game("resources/levels/" + str(self.game.map_lists[0]) + ".txt")
		pg.display.flip()
		pg.time.delay(1500)
		self.game.new_game()

	def get_hit(self, damage):
		noncompensated_dmg = 0
		if self.armor > 0:
			if self.armor < damage:
				noncompensated_dmg = damage - self.armor
				self.armor = 0
				self.health -= noncompensated_dmg
			else:
				self.armor -= damage
		else:
			self.armor = 0
			self.health -= damage
		self.game.object_renderer.player_hitted()
		self.game.sound.player_pain.play()

	def movement(self):
		dx, dy = 0, 0
		speed = PLAYER_SPEED * self.game.delta_time
		speed_sin = speed * math.sin(self.angle)
		speed_cos = speed * math.cos(self.angle)

		if self.movingForward:
			dx += speed_cos
			dy += speed_sin
		if self.movingBackward:
			dx += -speed_cos
			dy += -speed_sin
		if self.movingLeft:
			dx += speed_sin
			dy += -speed_cos
		if self.movingRight:
			dx += -speed_sin
			dy += speed_cos

		if not (dx == 0 and dy == 0):
			self.check_wall_collision(dx, dy)
			self.angle %= math.tau

	def check_wall_collision(self, dx, dy):
		scale = PLAYER_SIZE_SCALE / self.game.delta_time
		if not self.game.map.isWall(int(self.x + dx * scale), int(self.y)):
			self.x += dx
		if not self.game.map.isWall(int(self.x), int(self.y + dy * scale)):
			self.y += dy

# Getters
	@property
	def get_angle(self):
		return self.angle

	@property
	def get_pos(self):
		return self.x, self.y

	@property
	def get_map_pos(self):
		return int(self.x), int(self.y)

# Setters
	def set_spawn(self, x, y):
		self.x = x
		self.y = y

	def set_health(self, number):
		self.health = number
