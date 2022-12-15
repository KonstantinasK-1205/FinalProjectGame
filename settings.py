import math

# Game Settings
RES = WIDTH, HEIGHT = 1280, 720
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
VSYNC = 1
PRINT_FPS = 0

# On mini map
PLAYER_ANGLE = 1.5
PLAYER_SPEED = 0.003
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100
MARGIN = 20

# MOUSE CONTROL
MOUSE_SENSITIVITY = 0.0002
MOUSE_MAX_REL = 40

# FLOOR COLOR
FLOOR_COLOR = (34, 28, 29)

# RayCasting
FOV = 36
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

# Projectile
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# State input delay
STATE_WAIT_MS = 500

# Player hit flash
HIT_FLASH_COLOR = (102, 0, 0, 128)
HIT_FLASH_MS = 100

# Map change delay
MAP_CHANGE_WAIT_MS = 2000
