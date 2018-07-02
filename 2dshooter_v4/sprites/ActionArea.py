# packet import section
from config import *
import pygame as pg
import time


# defined import section


class ActionArea(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.action_area
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.surface = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.surface.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.Gate_open = False

        # text vars

        self.event_text_size = 80
        self.default_size = 50

    def Font_With_Size(self, size):
        self.Arial_font = pg.font.SysFont('Arial', size)

        return self.Arial_font

    def update(self):
        player_in_area = pg.sprite.spritecollide(self.game.player, self.game.action_area, False)

        keys = pg.key.get_pressed()

        if player_in_area and keys[pg.K_e]:
            area_text = "Gate opened!"
            self.Gate_open = True
            for gate in self.game.gates:
                self.gate_opened_sound()
                self.event_display_text(area_text)
                self.Gate_open = True
                gate.kill()

    def gate_opened_sound(self):
        sound = pg.mixer.Sound(self.game.sound_folder + "/" + GATE_OPENED_SOUND)
        sound.set_volume(0.25)
        pg.mixer.Channel(2).play(sound)

    def text_objects(self, text, font):
        grey = (128, 0, 128)
        textSurface = font.render(text, True, grey)
        return textSurface, textSurface.get_rect()

    # display event text
    def event_display_text(self, text):
        text_splitter = text

        if '..' in text:
            text_new = (text_splitter.split('..'))
            splitter = True
        else:
            text_new = text
            splitter = False

        largeText = self.Font_With_Size(self.event_text_size)
        if text_new[0] and splitter:
            TextSurf1, TextRect1 = self.text_objects(text_new[0], largeText)
            TextRect1.center = ((WIDTH / 2), (HEIGHT / 2))
            self.game.screen.blit(TextSurf1, TextRect1)
            print(text_new[0])
        if text_new[1] and splitter:
            TextSurf2, TextRect2 = self.text_objects(text_new[1], largeText)
            TextRect2.center = ((WIDTH / 2), (HEIGHT / 3))
            self.game.screen.blit(TextSurf2, TextRect2)
            print(text_new[1])
        else:
            TextSurf, TextRect = self.text_objects(text_new, largeText)
            TextRect.center = ((WIDTH / 2), (HEIGHT / 2))
            self.game.screen.blit(TextSurf, TextRect)
            print(text_new)

        pg.display.update()
        pg.time.delay(60)

    def objective_text(self, text, height):
        objText = str(text)
        ObjText = self.Font_With_Size(self.default_size - 10)
        ObjSurf, ObjRect = self.text_objects(objText, ObjText)
        ObjRect.center = ((WIDTH / 2), (height))
        self.game.screen.blit(ObjSurf, ObjRect)
        pg.display.update()
        pg.time.delay(240)

    def life_text(self, life):
        lifeText = "Lifepoints: " + str(life)
        LifeText = self.Font_With_Size(self.default_size)
        LifeSurf, LifeRect = self.text_objects(lifeText, LifeText)
        LifeRect.center = ((200), (735))
        self.game.screen.blit(LifeSurf, LifeRect)
        pg.display.update()

    def score_board_data(self, file):
        # read file
        name = []
        time = []
        date = []
        with open(file, 'r+') as f:
            data = f.readlines()
            for line in data:
                words = line.split("|")
                name.append(words[0])
                time.append(words[1])
                date.append(words[2])

        return name, time, date

    def score_board_print(self, table, rowNum):
        self.game.screen.fill((255, 255, 255))  # White
        if rowNum > 10:
            TableTxt = table.get_string(start=0, end=11)
            self.blit_text(TableTxt)
            pg.display.update()
        else:
            TableTxt = table
            self.blit_text(TableTxt)
            pg.display.update()

    def blit_text(self, text):
        pos = ((50), (50))
        words = [word.split('\n') for word in str(text).splitlines()]  # 2D array where each row is a list of words.
        space = self.Arial_font.size(' ')[0]  # width of spaces
        max_width, max_height = self.game.screen.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_font = self.Font_With_Size(self.default_size - 28)
                word_surface, WordRect = self.text_objects(word, word_font)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.game.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
