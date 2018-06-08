import pygame as pg
from config import *
import math
from os import path
from map import collide_hit_rect
vec = pg.math.Vector2

pg.mixer.pre_init(44100, 16, 2, 4096)

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y,camera):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.camera = camera;
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.img_rot = 0
        #player stats
        self.enemy_kills = 0

    def get_keys(self):
        #self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_w] and keys[pg.K_d]:
            self.vel = vec(PLAYER_SPEED,-PLAYER_SPEED) * 0.773
        elif keys[pg.K_w] and keys[pg.K_a]:
            self.vel = vec(-PLAYER_SPEED,-PLAYER_SPEED) * 0.773
        elif keys[pg.K_s] and keys[pg.K_d]:
            self.vel = vec(PLAYER_SPEED,PLAYER_SPEED) * 0.773
        elif keys[pg.K_s] and keys[pg.K_a]:
            self.vel = vec(-PLAYER_SPEED,PLAYER_SPEED) * 0.773

        elif keys[pg.K_w]:
            self.vel = vec(0,-PLAYER_SPEED)
        elif keys[pg.K_s]:
            self.vel = vec(0 ,PLAYER_SPEED)
        elif keys[pg.K_a]:
            self.vel = vec(-PLAYER_SPEED,0)
        elif keys[pg.K_d]:
            self.vel = vec(PLAYER_SPEED,0)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2.0
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2.0
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2.0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2.0
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    #calc rotation of char with mouse
    def rotate(self):
        self.mousex, self.mousey = pg.mouse.get_pos()
        if self.camera.camera.topleft[0] < 0:
            self.mousex -= self.camera.camera.topleft[0]
        if self.camera.camera.topleft[1] < 0:
            self.mousey -= self.camera.camera.topleft[1]
        run, rise = (self.mousex - self.pos.x, self.mousey - self.pos.y)
        self.img_rot = math.degrees(math.atan2(-rise, run))

    def update(self):
        self.get_keys()
        self.rotate()
        #self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.img_rot + PLAYER_ROT_ADJUST)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.hit_rect.center
        #print("playerpos:" + str(self.pos[0]) + " " + str(self.pos[1]) +"   mousepos:" + str("(" + str(self.mousex) + "," + str(self.mousey) + ")") + "  camerapos: " + str(self.camera.camera.topleft))

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        self.image = pg.image.load(game.img_folder + "/" + WALL_IMG)
        self.image = pg.transform.scale(self.image, (TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, player):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game;
        self.image = pg.Surface((7,3) , pg.SRCALPHA)
        self.image.fill(YELLOW)
        self.velocity = (math.cos(math.radians(player.img_rot)) * BULLET_SPEED,
                    -math.sin(math.radians(player.img_rot)) * BULLET_SPEED)
        self.image = pg.transform.rotate(self.image, (player.img_rot))
        self.rect = self.image.get_rect(center=(player.pos.x,player.pos.y))
        self.pos = list(self.rect.center)
        self.bullet_sound()

    def bullet_sound(self):
        shot = pg.mixer.Sound(self.game.sound_folder + "/" + BULLET_SHOT_SOUND)
        shot.set_volume(0.5)
        pg.mixer.Channel(0).play(shot)

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.center = self.pos
        self.collide_with_walls()

    def collide_with_walls(self):
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.kill()

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.hp = ENEMY_HP

    def update(self):
        self.hit_by_player()
        self.rect.center = self.pos

    def hit_by_player(self):
        hits = pg.sprite.spritecollide(self, self.game.bullets, False)

        if hits:
            if self.hp > 0:
                self.hp -= BULLET_DAMAGE
            else:
                killed = pg.mixer.Sound(self.game.sound_folder + "/" + ENEMY_DEATH_SOUND)
                pg.mixer.Channel(1).play(killed)
                self.kill()
                self.game.player.enemy_kills += 1
                print("Enemy killed. Total: " + str(self.game.player.enemy_kills))