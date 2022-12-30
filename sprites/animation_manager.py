import pygame as pg


class Animation:
    def __init__(self):
        self.currently_playing = None
        self.animation_finished = True
        self.current_state = "Standby"
        self.sprite = None

        self.play_next_frame = None
        self.prev_frame_time = 0
        self.animation_started_time = 0

    def change_animation(self, state, frames):
        self.current_state = state

        # Reset animation variables
        self.animation_started_time = pg.time.get_ticks()
        self.animation_finished = False
        self.currently_playing = True

        self.animate(frames)

    def animate(self, frames):
        if self.animation_finished:
            self.currently_playing = False
            self.current_state = "Standby"
            self.sprite = frames["Sprites"][0]

        if self.play_next_frame:
            frames["Sprites"].rotate(-1)
            self.sprite = frames["Sprites"][0]
            self.play_next_frame = False
        return self.current_state

    def check_animation_time(self, frames):
        current_time = pg.time.get_ticks()

        if current_time - self.prev_frame_time > frames["Speed"] \
                and not self.animation_finished:
            self.prev_frame_time = current_time
            self.play_next_frame = True

        if current_time - self.animation_started_time > len(frames["Sprites"]) * frames["Speed"] \
                and not self.animation_finished:
            self.animation_finished = True
