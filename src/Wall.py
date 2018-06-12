# packet import section
import pygame as pg
import math

# defined import section
from config import *
from Player import *
from Enemy import *
from Wall import *
from Bullet import *

# definition section
vec = pg.math.Vector2
pg.mixer.pre_init(44100, 16, 2, 4096)


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        self.image = pg.image.load(game.img_folder + "/" + WALL_IMG)
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE