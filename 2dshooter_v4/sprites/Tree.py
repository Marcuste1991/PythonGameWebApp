import pygame as pg

from config import *

class Tree(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        self.image = pg.image.load(game.img_folder + "/" + TREE_IMG).convert_alpha()
        self.image = pg.transform.scale(self.image, (TILESIZE*4,TILESIZE*4))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE