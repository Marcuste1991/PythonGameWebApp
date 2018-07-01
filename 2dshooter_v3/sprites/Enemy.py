# packet import section

import time, datetime
import easygui # easy_install easygui !!! important for Username input !!!!!!
import pygame as pg
# defined import section
from config import *
from map import *
from sprites.Wall import *
from sprites.Bullet import *
from sprites.Player import *
from sprites.ActionArea import *

# definition section
vec = pg.math.Vector2
pg.mixer.pre_init(44100, 16, 2, 4096)

# Enemy Counter for Quit Game at Win #
global xnum
global max_num
max_num = [0]  # needed here otherwise it would be rewrite every time it gets used


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, num):
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_img
        self.rect = self.image.get_rect()
        self.hit_rect = ENEMY_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.rot = ENEMY_ROT_ADJUST
        self.img_rot = 0
        self.hp = ENEMY_HP
        self.player_kills = 0

        # logic behind ai
        self.distance = self.EnemyNum = 0
        self.eff_dist = 0
        self.num = num
        self.exec = False
        # debugging no real function !!!
        # self.posEnemy = self.pos[0], self.pos[1], self.num

    def on_objective_keypressed(self):
        keys = pg.key.get_pressed()

        objective = {}
        height = {}

        if keys[pg.K_o]:
            objective[0] = "Remaining Enemies: " + str(self.CountEnemy() - self.game.player.enemy_kills)
            height[0] = 60
            objective[1] = "Gate opened: " + str(self.game.a_area.Gate_open)
            height[1] = 90

            print(len(objective))

            self.game.a_area.objective_text(objective[0], height[0])
            self.game.a_area.objective_text(objective[1], height[1])


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
                # Game Win Sequence with Scoreboard Writing
                if (self.CountEnemy() - self.game.player.enemy_kills) == 0:
                    Time = datetime.datetime.now()

                    PlayerName = easygui.enterbox(
                        msg="Please enter your Name below: ",
                        title="Nameinput  for Scoreboard!",
                        strip=True, # will remove whitespace around whatever the user types in
                        default="Username")

                    FinalTime = Time - self.game.Time_start
                    with open("score.txt", "w") as f:
                        f.write(str(PlayerName + " : " + str(FinalTime) + " : " +  str(datetime.date.today())))

                    self.exec = True
                    text_1 = 'All Enemies killed!'
                    text_2 = 'You win!'
                    text = text_1 + ".." + text_2
                    self.game.a_area.event_display_text(text)
                    time.sleep(5)
                    self.game.quit()

    def debuggerEnemy(self):
        # logicalPos = self.posEnemy
        # print("Enemy :" + str(logicalPos))
        pass

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
        # self.walk_through_map()
        self.rect.center = self.pos

        self.image = pg.transform.rotate(self.game.enemy_img, self.img_rot + self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # self.pos += self.vel * self.game.dt
        # self.hit_rect.centerx = self.pos.x
        # self.collide_with_walls('x')
        # self.hit_rect.centery = self.pos.y
        # self.collide_with_walls('y')
        # self.rect.center = self.hit_rect.center

        # self.distance_to_player()

    # def movement_collision(self, dir):
    #     if dir == 'x':
    #         E_hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
    #         if E_hits:
    #             if self.vel.x > 0:
    #                 self.pos.x = E_hits[0].rect.left - self.hit_rect.width / 2.0
    #             if self.vel.x < 0:
    #                 self.pos.x = E_hits[0].rect.right + self.hit_rect.width / 2.0
    #             self.vel.x = 0
    #             self.hit_rect.centerx = self.pos.x
    #
    #     if dir == 'y':
    #         E_hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
    #         if E_hits:
    #             if self.vel.y > 0:
    #                 self.pos.y = E_hits[0].rect.top - self.hit_rect.height / 2.0
    #             if self.vel.y < 0:
    #                 self.pos.y = E_hits[0].rect.bottom + self.hit_rect.height / 2.0
    #             self.vel.y = 0
    #             self.hit_rect.centery = self.pos.y
    #
    # def movement_collision_Handler(self):
    #
    #     if self.movement_collision('x'):
    #         self.hit_rect.centery = self.pos.x
    #         collision = True
    #     elif self.movement_collision('y'):
    #         self.hit_rect.centery = self.pos.y
    #         collision = True
    #     else:
    #         collision = False
    #
    #     return collision
    #
    # def movement(self):
    #     while True:
    #         move = (random.randint(0, 20000) % 7)
    #         return move
    #
    # def make_move(self):
    #     move = self.movement()
    #     return move
    #
    # def walk_through_map(self):
    #     global moveNum
    #     global collision
    #     collision = False
    #     moveNum = 0
    #     # enemy should avoid to hit walls and needs to be able to hunt player
    #     # only possible for actual map atm
    #     init = vec(0, 0)
    #     self.vel = init
    #     EnNum = 1
    #     maxRange = self.num
    #
    #     pg.time.delay(10)
    #
    #     for EnNum in range(maxRange):
    #         EnNum += 1
    #         if not collision:
    #             if moveNum == '':
    #                 pass
    #                 # moveNum = self.make_move()
    #             # elif not self.movement_collision(moveNum):
    #             # moveNum = moveNum
    #             else:
    #                 pass
    #                 # moveNum = self.make_move()
    #
    #             # 0 -> w, 1 -> a, 2 -> s, 3 -> d
    #             # 4 -> w + d, 5 -> w + a, 6 -> s + d, 7 -> s + a
    #             if moveNum == 4:
    #                 self.vel = vec(ENEMY_SPEED, -ENEMY_SPEED) * 0.773
    #                 self.rot = 90
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 5:
    #                 self.vel = vec(-ENEMY_SPEED, -ENEMY_SPEED) * 0.773
    #                 self.rot = 90
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 6:
    #                 self.vel = vec(ENEMY_SPEED, ENEMY_SPEED) * 0.773
    #                 self.rot = -90
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 7:
    #                 self.vel = vec(-ENEMY_SPEED, ENEMY_SPEED) * 0.773
    #                 self.rot = -90
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 0:
    #                 self.vel = vec(0, -ENEMY_SPEED)
    #                 self.rot = 90
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 1:
    #                 self.vel = vec(0, ENEMY_SPEED)
    #                 self.rot = 180
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 2:
    #                 self.vel = vec(-ENEMY_SPEED, 0)
    #                 self.rot = 0
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 3:
    #                 self.vel = vec(ENEMY_SPEED, 0)
    #                 self.rot = -90
    #                 collision = self.movement_collision_Handler()
    #         else:
    #             moveNum = self.make_move()

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
