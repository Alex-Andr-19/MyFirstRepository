from math import sqrt, sin, asin, cos, pi, fabs

def distance_s(a, b):
    return sqrt((a.rect.x - b.rect.x)**2 + (a.rect.y - b.rect.y)**2)
def distance_c(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
def angle_to(body, cords):
    gip = distance_c(body.rect.x, body.rect.y, cords[0], cords[1])
    kat = fabs(body.rect.y - cords[1])
    sin_a = kat / gip
    a = asin(sin_a)
    if body.rect.x <= cords[0]:
        a += pi / 2
    if body.rect.y >= cords[1]:
        a = -a
    return a

def clamp(a, max=255, min=0):
    if a >= max:
        return max
    if a < min:
        return min
    return a

def fn_nrst_trg(crt, crt_mas, fd_mas, crt_gr, dead_gr, fd_gr, without=[]):
    index = 0
    min_dis = 10000

    if len(crt_gr) - len(dead_gr) > len(fd_gr):
        for i in range(len(fd_mas)):
            if min_dis > distance_s(crt.body, fd_mas[i].food) and fd_mas[i].food in fd_gr:
                min_dis = distance_s(crt.body, fd_mas[i].food)
                index = i
    else:
        for i in range(len(fd_mas)):
            if min_dis > distance_s(crt.body, fd_mas[i].food) and fd_mas[i].food in fd_gr and i not in without:
                min_dis = distance_s(crt.body, fd_mas[i].food)
                index = i

    for i in range(len(crt_mas)):
        if min_dis > distance_s(crt.body, crt_mas[i].body) and crt_mas[i].body in dead_gr:
            min_dis = distance_s(crt.body, crt_mas[i].body)
            index = i + len(fd_mas)

    return index

def circ_on(crt, start_w=0, clock=1):
    if clock:
        angle_tmp = crt.angle + pi / 90 + start_w
    else:
        angle_tmp = pi - (crt.angle + pi / 90) + start_w

    crt.body.rect.x = crt.center[0] + crt.radius * cos(angle_tmp)
    crt.body.rect.y = crt.center[1] - crt.radius * sin(angle_tmp)
    crt.sens_circ.rect.x = crt.body.rect.x - crt.sens + crt.w//2
    crt.sens_circ.rect.y = crt.body.rect.y - crt.sens + crt.h//2
    crt.angle += pi / 90

    if crt.angle >= 2 * pi:
        crt.angle = 0