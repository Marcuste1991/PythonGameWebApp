# packet import section
from config import *
import pygame as pg
# defined import section


class ActionArea(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.action_area
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.surface = pg.Surface((TILESIZE,TILESIZE))
        self.rect = self.surface.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        player_in_area = pg.sprite.spritecollide(self.game.player, self.game.action_area,False)

        keys = pg.key.get_pressed()

        if player_in_area and keys[pg.K_e]:
            print("Gate opened")
            for gate in self.game.gates:
                self.gate_opened_sound()
                gate.kill()

    def gate_opened_sound(self):
        sound = pg.mixer.Sound(self.game.sound_folder + "/" + GATE_OPENED_SOUND)
        sound.set_volume(0.25)
        pg.mixer.Channel(2).play(sound)