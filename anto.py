import os
import sys

import pygame
import requests


def draw():
    global map_file, ch
    map_request = f"http://static-maps.yandex.ru/1.x/?&pt={','.join(map(str, coord))}&z={z}&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen = pygame.display.set_mode((600, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    ch = False


coord = list(map(float, input().split()))
z = int(input())
step_y = 0
step_x = 0
pygame.init()
ch = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove(map_file)
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                z -= 1
                if z < 0:
                    z = 1
                ch = True
            if event.key == pygame.K_PAGEUP:
                z += 1
                if z > 17:
                    z = 17
                ch = True
            if event.key == pygame.K_UP:
                coord[1] += step_y
                ch = True
            if event.key == pygame.K_DOWN:
                coord[1] -= step_y
                ch = True
            if event.key == pygame.K_LEFT:
                coord[0] -= step_x
                ch = True
            if event.key == pygame.K_RIGHT:
                coord[0] += step_x
                ch = True
    if ch:
        draw()
    pygame.display.flip()
