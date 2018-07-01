import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 200
TITLE = "Hunting Terrorist"
VERSION = "1.00.022.1702"
BGCOLOR = DARKGREY

TILESIZE = 40
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# evnironment
SOUND_BACKGROUND = "fx_day.wav"
BACKGROUND_IMG = "background_komprimiert.jpg"
BACKGROUND_IMG_SIZE = [700, 700]  # [x,y]

# object settings
WALL_IMG = "block.jpg"
TREE_IMG = "palm 1-25.png"
WOODEN_BOX_IMG = "woodbox.png"
GATE_IMG = "gate.jpg"
CONTROL_BOX = "control_room.png"

BREAK_SOUND = "box_break1.wav"
GATE_OPENED_SOUND = "gate_opened.wav"

# Player settings
PLAYER_SPEED = 1000.0
PLAYER_HP = 100
# PLAYER_ROT_SPEED = 250.0
PLAYER_IMG = "cs2d_terrorist.png"
PLAYER_ROT_ADJUST = -90  # 0 if  rot ok, only take right angles
PLAYER_IMG_SIZE = (39, 50)  # (39,50) for cs2d_terrorist.png
PLAYER_HIT_RECT = pg.Rect(0, 0, 39, 50)

# bullet settings
BULLET_SPEED = 30
BULLET_DAMAGE = 20
BULLET_SHOT_SOUND = "gunshot1.wav"

# enemy settings
ENEMY_IMG = "manblue.png"
ENEMY_SPEED = 250.0
ENEMY_IMG_SIZE = (50, 50)
ENEMY_HIT_RECT = pg.Rect(0, 0, 45, 45)
ENEMY_ROT_ADJUST = -90
ENEMY_DEATH_SOUND = "death2.wav"
ENEMY_HP = 100
