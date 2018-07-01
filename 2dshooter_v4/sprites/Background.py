import config
import pygame as pg

class Background(pg.sprite.Sprite):
    def __init__(self, game, image_file, location):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)  #call Sprite initializer
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location