import pygame as pg

from Food import Food
from Creature import Creature

from random import randint as rand
from lib_func import *
from settings import *

count_crt = COUNT_CRT
alive = count_crt
days = 1
brd_info = ""
iterator = 0

pg.init()

window = pg.display.set_mode((SCR_W, SCR_H))
run = 1

all_s = pg.sprite.Group()
fd_gr = pg.sprite.Group()
crt_gr = pg.sprite.Group()
crtb_gr = pg.sprite.Group()
crts_gr = pg.sprite.Group()
deadb_gr = pg.sprite.Group()
deads_gr = pg.sprite.Group()

crt_mas = [Creature(WCR, HCR, SENS) for i in range(count_crt)]
fd_mas = [Food() for i in range(COUNT_FD)]

breed_mas = [count_crt]

for i in range(count_crt):
    crt_gr.add(crt_mas[i].terretory)
    crtb_gr.add(crt_mas[i].body)
    crts_gr.add(crt_mas[i].sens_circ)
    all_s.add(crt_mas[i].terretory)

for i in range(COUNT_FD):
    all_s.add(fd_mas[i].food)
    fd_gr.add(fd_mas[i].food)

f = pg.font.Font(None, 36)
index = [fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crt_gr, deadb_gr, fd_gr) for i in range(count_crt)]

while run:
    l1 = f.render("Creatures - " + str(len(crt_gr) // 2), 1, (255, 255, 255))
    l2 = f.render("Alive      - " + str(alive), 1, (255, 255, 255))
    l3 = f.render("Food      - " + str(len(fd_gr)), 1, (255, 255, 255))
    l4 = f.render("Days      - " + str(days), 1, (255, 255, 255))
    while iterator != len(breed_mas) and not breed_mas[iterator]:
        brd_info = str(iterator + 1) + "^0: "
        iterator += 1

    for i in range(iterator, len(breed_mas)):
        brd_info += str(breed_mas[i])
        if i != len(breed_mas) - 1:
            brd_info += ", "
    iterator = 0
    l6 = f.render("Breeds      - " + brd_info, 1, (255, 255, 255))

    window.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = 0

    crts_gr.draw(window)
    fd_gr.draw(window)
    crtb_gr.draw(window)

    # видит ли особь еду
    for i in range(count_crt):
        vis_gr = pg.sprite.spritecollide(crt_mas[i].sens_circ, fd_gr, False)
        if len(vis_gr) and index[i] >= 0:
            for j in range(len(vis_gr)):
                vis_gr[j].image.fill((255, 0, 0))

    # передвижение каждой особи
    for i in range(count_crt):
            tmp = 1
            if index[i] < len(fd_mas):
                if (crt_mas[i].body.rect.x != fd_mas[index[i]].food.rect.x or
                    crt_mas[i].body.rect.y != fd_mas[index[i]].food.rect.y) and \
                        index[i] != -1:

                    tmp = crt_mas[i].go_to_targer(fd_mas[index[i]].food)
            else:
                if (crt_mas[i].body.rect.x != crt_mas[clamp(index[i] - len(fd_mas), len(crt_mas) - 1)].body.rect.x or
                    crt_mas[i].body.rect.y != crt_mas[clamp(index[i] - len(fd_mas), len(crt_mas) - 1)].body.rect.y) and \
                        index[i] != -1:
                    tmp = crt_mas[i].go_to_targer(crt_mas[clamp(index[i] - len(fd_mas), len(crt_mas) - 1)].body)
            # регестрация гибели
            if tmp == 0:
                alive -= 1
                index[i] = -1
                deadb_gr.add(crt_mas[i].body)
                deads_gr.add(crt_mas[i].sens_circ)
                breed_mas[crt_mas[i].breed - 1] -= 1
                crt_mas[i].color2 = (60, 60, 60)
            crt_mas[i].center = (crt_mas[i].body.rect.x - crt_mas[i].sens, crt_mas[i].body.rect.y)

    # обработка энергии
    for i in range(count_crt):
        hit_gr = pg.sprite.spritecollide(crt_mas[i].body, fd_gr, True)
        # съела ли особь еду
        if len(hit_gr):
            for j in range(len(hit_gr)):
                crt_mas[i].energy += FD_EN
        # съела ли особь особь
        if index[i] >= 0:
            hit_gr = pg.sprite.spritecollide(crt_mas[i].body, deadb_gr, True)
            if len(hit_gr):
                # for j in range(len(hit_gr)):
                crt_mas[i].energy += 0.5
                hit_gr_dead = pg.sprite.spritecollide(crt_mas[i].body, deads_gr, True)
                hit_gr_dead = pg.sprite.spritecollide(crt_mas[i].body, deadb_gr, True)

        # рождение
        if crt_mas[i].energy > 9.8:
            tmp = crt_mas[i].energy
            while tmp // crt_mas[i].birth_enr:
                # вычисление координат дочерней особи
                cords = (crt_mas[i].body.rect.x + WCR, crt_mas[i].body.rect.y + HCR)

                # факт рождения
                crt_mas.append(Creature(WCR, HCR, SENS, cords, crt_mas[i].breed+1))
                index.append(fn_nrst_trg(crt_mas[-1], crt_mas, fd_mas, crt_gr, deadb_gr, fd_gr, [index[j] for j in range(count_crt) if j != i]))

                crt_mas[-1].energy = crt_mas[i].birth_enr / 1.5
                crt_mas[-1].birth_enr = crt_mas[i].birth_enr
                crt_mas[-1].speed = crt_mas[i].speed
                crt_mas[-1].color2 = crt_mas[i].color2

                crt_gr.add(crt_mas[-1].terretory)
                crtb_gr.add(crt_mas[-1].body)
                crts_gr.add(crt_mas[-1].sens_circ)
                all_s.add(crt_mas[-1].terretory)
                count_crt += 1

                # мутация
                # скорость
                chance = rand(0, 100)
                if 50 <= chance < 75 and crt_mas[-1].speed != clamp(crt_mas[-1].speed - 1, 5, 1):
                    crt_mas[-1].color2 = (clamp(crt_mas[-1].color2[0] - 13),
                                          crt_mas[-1].color2[1],
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].speed = clamp(crt_mas[-1].speed - 1, 5, 1)
                elif chance >= 75 and crt_mas[-1].speed != clamp(crt_mas[-1].speed + 1, 5, 1):
                    crt_mas[-1].color2 = (clamp(crt_mas[-1].color2[0] + 13),
                                          crt_mas[-1].color2[1],
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].speed = clamp(crt_mas[-1].speed + 1, 5, 1)

                # размножение
                chance = rand(0, 100)
                if 50 <= chance < 75 and crt_mas[-1].birth_enr != clamp(crt_mas[-1].birth_enr + 1, 5, 1):
                    crt_mas[-1].color2 = (crt_mas[-1].color2[0],
                                          clamp(crt_mas[-1].color2[1] - 13),
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].birth_enr = clamp(crt_mas[-1].birth_enr + 1, 5, 2)
                elif chance >= 75 and crt_mas[-1].birth_enr != clamp(crt_mas[-1].birth_enr - 1, 5, 1):
                    crt_mas[-1].color2 = (crt_mas[-1].color2[0],
                                          clamp(crt_mas[-1].color2[1] + 13),
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].birth_enr = clamp(crt_mas[-1].birth_enr - 1, 5, 2)

                # статистика
                if len(breed_mas) < crt_mas[-1].breed:
                    breed_mas.append(1)
                else:
                    breed_mas[crt_mas[-1].breed - 1] += 1
                alive += 1

                # затраты на рождение
                tmp -= crt_mas[i].birth_enr
            crt_mas[i].energy -= (6 + (5 - crt_mas[i].birth_enr)*0.4)

    # пересчёт следущей цели-еды
    for i in range(count_crt):
        if index[i] < len(fd_mas):
            if fd_mas[index[i]].food not in fd_gr and index[i] != -1:
               index[i] = fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crt_gr, deadb_gr, fd_gr,
                                      [index[j] for j in range(count_crt) if j != i])
        elif crt_mas[clamp(index[i] - len(fd_mas), len(crt_mas) - 1)].body not in crt_gr:
            index[i] = fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crt_gr, deadb_gr, fd_gr,
                                   [index[j] for j in range(count_crt) if j != i])

    # генерация нового дня
    if len(fd_gr) < COUNT_FD // 10:
        # генерация нового поля еды
        for i in range(COUNT_FD - len(fd_gr)):
            fd_mas[i].food.rect.x = rand(WCR, SCR_W - WCR)
            fd_mas[i].food.rect.y = rand(HCR, SCR_H - HCR)
            fd_mas[i].food.image.fill((0, 255, 0))
            fd_gr.add(fd_mas[i].food)
            all_s.add(fd_mas[i].food)

        # навый подсчет целей-еды для каждой живой особи (чтобы не бежали все в одну сторону)
        for i in range(count_crt):
            if index[i] >= 0:
                index[i] = fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crt_gr, deadb_gr, fd_gr)
            crt_mas[i].days += 1

        # очистка "памяти" от съеденных особей
        index = [index[i] for i in range(count_crt) if crt_mas[i].body in crt_gr]
        crt_mas = [crt_mas[i] for i in range(count_crt) if crt_mas[i].body in crt_gr]
        count_crt = len(crt_mas)

        # обновление дня
        days += 1
        aver_days = 0
        # if days > 5:
            # COUNT_FD = clamp(COUNT_FD - 25, 5000, 500)

    '''keys = pg.key.get_pressed()
    if keys[pg.K_RIGHT] and crt_mas[0].body.rect.x + 20 < 495:
        crt_mas[0].body.rect.x += 2
        crt_mas[0].senc_circ.rect.x += 2
    if keys[pg.K_UP] and crt_mas[0].body.rect.y > 5:
        crt_mas[0].body.rect.y -= 2
        crt_mas[0].senc_circ.rect.y -= 2
    if keys[pg.K_LEFT] and crt_mas[0].body.rect.x > 5:
        crt_mas[0].body.rect.x -= 2
        crt_mas[0].senc_circ.rect.x -= 2
    if keys[pg.K_DOWN] and crt_mas[0].body.rect.y + 20 < 495:
        crt_mas[0].body.rect.y += 2
        crt_mas[0].senc_circ.rect.y += 2
'''
    brd_info = ""
    window.blit(l1, (20, 15))
    window.blit(l2, (40, 40))
    window.blit(l3, (41, 65))
    window.blit(l4, (44, 86))
    window.blit(l6, (20, 110))
    pg.time.delay(10)
    pg.display.update()
