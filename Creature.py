import pygame as pg
from random import randint as rand
from math import fabs, cos, sin, pi
from lib_func import clamp
from settings import *

class Creature:
    def __init__(self, w, h, sens=70, start_cords=(0, 0), breed=1, color1=(0, 0, 255), color2=(87, 87, 87), fon_c=(0, 0, 0)):
        self.w = w
        self.h = h
        self.sens = sens
        self.color1 = color1
        self.color2 = color2
        self.fon_c = fon_c
        self.breed = breed
        self.days = 1

        self.center = (0, 0)
        self.angle = 0

        self.terretory = pg.sprite.Group()

        self.body = pg.sprite.Sprite()
        self.body.image = pg.Surface([w, h])
        self.body.rect = self.body.image.get_rect()
        if start_cords[0] or start_cords[1]:
            self.body.rect.x = start_cords[0]
            self.body.rect.y = start_cords[1]
        else:
            self.body.rect.x = rand(0, SCR_W - w)
            self.body.rect.y = rand(0, SCR_H - h)
        self.body.image.fill(color1)

        self.sens_circ = pg.sprite.Sprite()
        self.sens_circ.image = pg.Surface([sens*2, sens*2])
        self.sens_circ.rect = self.sens_circ.image.get_rect()
        self.sens_circ.rect.x = self.body.rect.x - sens + w//2
        self.sens_circ.rect.y = self.body.rect.y - sens + h//2
        self.sens_circ.image.fill(fon_c)
        self.sens_circ.image.set_colorkey(fon_c)

        self.terretory.add(self.sens_circ)
        self.terretory.add(self.body)

        pg.draw.circle(self.sens_circ.image,
                       color2,
                       (sens, sens),
                       sens)

        self.energy = 2.5
        self.speed = 1
        self.birth_enr = 5

        self.f = pg.font.Font(None, 15)
        self.brd_info = self.f.render(str(self.breed), 0, (255, 255, 255))
        self.sens_circ.image.blit(self.brd_info, (18, 12))

        self.enrg_info = self.f.render(str(self.energy), 0, (255, 255, 255))
        # self.days_info = self.f.render(str(self.breed), 0, (255, 255, 255))
        # self.speed_info = self.f.render(str(self.speed), 0, (255, 255, 255))
        # self.birth_info = self.f.render(str(self.birth_enr), 0, (255, 255, 255))

    def type(self):
        return "Creature"

    def go_to_targer(self, targ):
        x_t = targ.rect.x
        y_t = targ.rect.y

        for i in range(self.speed):
            if fabs(self.body.rect.x - x_t) > fabs(self.body.rect.y - y_t):
                if self.body.rect.x > x_t:
                    self.body.rect.x -= 1
                    self.sens_circ.rect.x -= 1
                else:
                    self.body.rect.x += 1
                    self.sens_circ.rect.x += 1
            else:
                if self.body.rect.y > y_t:
                    self.body.rect.y -= 1
                    self.sens_circ.rect.y -= 1
                else:
                    self.body.rect.y += 1
                    self.sens_circ.rect.y += 1
            self.energy = clamp(self.energy - 0.005, 10)


        r = clamp(int(self.color1[0] * self.energy))
        if self.energy > 5.5:
            r = clamp(int((self.energy - 5.5) * 255))
        g = clamp(int(self.color1[1] * self.energy))
        if self.energy > 8.5:
            g = clamp(int((self.energy - 8.5) * 255))
        b = clamp(int(self.color1[2] * self.energy / 5.5))
        self.sens_circ.image = pg.Surface([self.sens * 2, self.sens * 2])
        self.sens_circ.image.fill((0, 0, 0))
        self.sens_circ.image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sens_circ.image,
                       self.color2,
                       (self.sens, self.sens),
                       self.sens)
        self.body.image.fill((r, g, b))

        self.sens_circ.image.blit(self.brd_info, (18, 12 + 3 * HCR))

        self.enrg_info = self.f.render(str(self.energy)[:5], 1, (255, 255, 255))
        # self.days_info = self.f.render(str(self.days), 1, (255, 255, 255))
        # self.speed_info = self.f.render(str(self.speed), 1, (255, 255, 255))
        # self.birth_info = self.f.render(str(self.birth_enr), 1, (255, 255, 255))
        self.sens_circ.image.blit(self.enrg_info, (18, 12))
        # self.sens_circ.image.blit(self.days_info, (36, 12 + 3 * HCR))
        # self.sens_circ.image.blit(self.speed_info, (11, 25))
        # self.sens_circ.image.blit(self.birth_info, (11 + 4*WCR, 25))

        if not self.energy:
            return 0
        return 1

    def just_walk(self):
        angle_tmp = self.angle + pi / 90

        self.body.rect.x = self.center[0] + self.sens * cos(angle_tmp)
        self.body.rect.y = self.center[1] - self.sens * sin(angle_tmp)
        self.sens_circ.rect.x = self.body.rect.x - self.sens + self.w // 2
        self.sens_circ.rect.y = self.body.rect.y - self.sens + self.h // 2
        self.angle += pi / 90
