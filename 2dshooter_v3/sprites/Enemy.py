# packet import section

import random
import time

import pygame as pg
# defined import section
from config import *
from map import collide_hit_rect
from sprites.Bullet import *
from sprites.Player import *

# definition section
vec = pg.math.Vector2
pg.mixer.pre_init(44100, 16, 2, 4096)


def movement():
    while True:
        time.sleep(5)
        move = (random.randint(0, 20000) % 7)
        return move


def make_move(self):
    move = movement()
    return move


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, num):
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_img
        self.rect = self.image.get_rect()
        self.rect_col = self.image.get_rect()
        self.hit_rect = ENEMY_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.rot = ENEMY_ROT_ADJUST
        self.img_rot = 0
        self.hp = ENEMY_HP
        self.player_kills = 0

        # logic behind ai
        self.distance = 0
        self.eff_dist = 0
        self.num = num
        # debugging no real function !!!
        # self.posEnemy = self.pos[0], self.pos[1], self.num

    def hit_by_player(self):
        E_hits = pg.sprite.spritecollide(self, self.game.bullets, False)

        if E_hits:
            if self.hp > 0:
                self.hp -= BULLET_DAMAGE
                # Bullet.collide_with_figure(self.game.enemies)
            else:
                E_killed = pg.mixer.Sound(self.game.sound_folder + "/" + ENEMY_DEATH_SOUND)
                pg.mixer.Channel(1).play(E_killed)
                self.kill()
                # Bullet.collide_with_figure(self.game.enemies)
                self.game.player.enemy_kills += 1
                print("Enemy killed. Total: " + str(self.game.player.enemy_kills))
                # Game Win Sequence
                if (self.CountEnemy() - self.game.player.enemy_kills) == 0:
                    print("All Enemies killed. You win!")
                    self.game.quit()

    def debuggerEnemy(self):
        logicalPos = self.posEnemy
        # print("Enemy :" + str(logicalPos))

    # Enemy Counter for Quit Game at Win #
    global xnum
    global max_num
    max_num = [0]  # needed here otherwise it would be rewrite every time it gets used

    def CountEnemy(self):
        for xnum in range(self.num):
            if max(max_num) < self.num:
                max_num.append(xnum + 1)
            else:
                break
            xnum += 1
        return max(max_num)

    def collide_with_walls(self, dir):
        if dir == 'x':
            E_hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if E_hits:
                if self.vel.x > 0:
                    self.pos.x = E_hits[0].rect.left - self.hit_rect.width / 2.0
                if self.vel.x < 0:
                    self.pos.x = E_hits[0].rect.right + self.hit_rect.width / 2.0
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            E_hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if E_hits:
                if self.vel.y > 0:
                    self.pos.y = E_hits[0].rect.top - self.hit_rect.height / 2.0
                if self.vel.y < 0:
                    self.pos.y = E_hits[0].rect.bottom + self.hit_rect.height / 2.0
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def update(self):
        self.hit_by_player()
        self.walk_through_map()

        self.image = pg.transform.rotate(self.game.enemy_img, self.img_rot + self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.hit_rect.center

        self.distance_to_player()

    def movement_collision(self, dir):
        if dir == 'x':
            E_hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if E_hits:
                if self.vel.x > 0:
                    self.pos.x = E_hits[0].rect.left - self.hit_rect.width / 2.0
                if self.vel.x < 0:
                    self.pos.x = E_hits[0].rect.right + self.hit_rect.width / 2.0
                self.vel.x = 0
                self.rect_col.centerx = self.pos.x
                return True
            else:
                return False
        if dir == 'y':
            E_hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if E_hits:
                if self.vel.y > 0:
                    self.pos.y = E_hits[0].rect.top - self.hit_rect.height / 2.0
                if self.vel.y < 0:
                    self.pos.y = E_hits[0].rect.bottom + self.hit_rect.height / 2.0
                self.vel.y = 0
                self.rect_col.centery = self.pos.y
                return True
            else:
                return False

    def movement_collision_Handler(self):

        if self.movement_collision('x'):
            collision = True
        elif self.movement_collision('y'):
            collision = True
        else:
            collision = False

        return collision

    def walk_through_map(self):
        global moveNum
        global collision
        collision = False
        moveNum = 0
        # enemy should avoid to hit walls and needs to be able to hunt player
        # only possible for actual map atm
        init = vec(0, 0)
        self.vel = init
        EnNum = 1
        maxRange = self.num

        for EnNum in range(maxRange):
            EnNum += 1
            if not collision:
                if moveNum == '':
                    moveNum = make_move(moveNum)
                elif not self.movement_collision(moveNum):
                    moveNum = moveNum
                else:
                    moveNum = make_move(moveNum)

                # 0 -> w, 1 -> a, 2 -> s, 3 -> d
                # 4 -> w + d, 5 -> w + a, 6 -> s + d, 7 -> s + a
                while moveNum == 4:
                    self.vel = vec(ENEMY_SPEED, -ENEMY_SPEED) * 0.773
                    self.rot = 90
                    collision = self.movement_collision_Handler()
                while moveNum == 5:
                    self.vel = vec(-ENEMY_SPEED, -ENEMY_SPEED) * 0.773
                    self.rot = 90
                    collision = self.movement_collision_Handler()
                while moveNum == 6:
                    self.vel = vec(ENEMY_SPEED, ENEMY_SPEED) * 0.773
                    self.rot = -90
                    collision = self.movement_collision_Handler()
                while moveNum == 7:
                    self.vel = vec(-ENEMY_SPEED, ENEMY_SPEED) * 0.773
                    self.rot = -90
                    collision = self.movement_collision_Handler()
                while moveNum == 0:
                    self.vel = vec(0, -ENEMY_SPEED)
                    self.rot = 90
                    collision = self.movement_collision_Handler()
                while moveNum == 1:
                    self.vel = vec(0, ENEMY_SPEED)
                    self.rot = 180
                    collision = self.movement_collision_Handler()
                while moveNum == 2:
                    self.vel = vec(-ENEMY_SPEED, 0)
                    self.rot = 0
                    collision = self.movement_collision_Handler()
                while moveNum == 3:
                    self.vel = vec(ENEMY_SPEED, 0)
                    self.rot = -90
                    collision = self.movement_collision_Handler()
            else:
                moveNum = make_move(moveNum)

    def distance_to_player(self):
        # effective distance with ignoring walls
        # real distance need to include walls for shoot and hunt
        distance = (self.game.player.pos // 80) - (self.game.enemy.pos // 80)
        # print(self.game.player.pos, self.game.enemy.pos) # debug
        coord_distance = distance
        # print(coord_distance)
        pass

    def shoot(self):
        # if distance below 4 and player is visible to enemy -> shoot
        # distance of 4 means 320px
        # self.debuggerEnemy()
        pass
