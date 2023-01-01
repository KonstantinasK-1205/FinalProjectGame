import pygame as pg


class Animation:
    def __init__(self):
        self.sprite_info = None
        self.frames = {}
        self.frame_duration = 0
        self.current_frame = 0
        self.elapsed_time = 0
        self.state = "Idle"
        self.completed = False

    def load_sprite_animations(self, info):
        self.sprite_info = info

    def change_animation(self, state):
        self.state = state
        self.current_frame = 0
        self.elapsed_time = 0
        self.frames = self.sprite_info[self.state]["Frames"]
        self.frame_duration = self.sprite_info[self.state]["Speed"]
        self.completed = False

    def animate(self, dt):
        # Increment the elapsed time
        self.elapsed_time += dt

        # If the elapsed time is greater than the frame duration, move to the next frame
        if self.elapsed_time > self.frame_duration:
            self.current_frame += 1
            self.elapsed_time = 0

        # If the current frame is the last frame, set the completed flag to True
        if self.current_frame > len(self.frames) - 1:
            self.current_frame -= 1
            self.completed = True
            return

        # If the animation has completed, reset it to the first frame
        if self.completed:
            self.current_frame = 0
            self.elapsed_time = 0
            # If the state is "Death", keep the animation at the last frame
            if self.state == "Death":
                self.current_frame = len(self.frames) - 1
            else:
                self.state = "Idle"
                self.frames = self.sprite_info[self.state]["Frames"]
            return

    def get_state(self):
        return self.state

    def get_sprite(self):
        return self.frames[self.current_frame]

    def is_playing(self):
        return not self.completed
