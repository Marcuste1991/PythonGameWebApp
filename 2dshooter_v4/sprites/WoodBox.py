# packet import section
from config import *
import pygame as pg
# defined import section

# definition section
vec = pg.math.Vector2
pg.mixer.pre_init(44100, 16, 2, 4096)


class WoodBox(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.destroyable_objects, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        self.image = pg.image.load(game.img_folder + "/" + WOODEN_BOX_IMG).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.hp = 100

    def break_sound(self):
        sound = pg.mixer.Sound(self.game.sound_folder + "/" + BREAK_SOUND)
        print("BREAK SOUND")
        sound.set_volume(0.5)
        pg.mixer.Channel(3).play(sound)