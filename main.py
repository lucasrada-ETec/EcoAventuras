import pygame as pg
import random
import os

pg.init()
pg.mixer.init()

script_dir = os.path.dirname(__file__)
assets_dir = os.path.join(script_dir, 'assets')
load_asset = lambda filename: os.path.join(assets_dir, filename)

running = True
game_over = False
score = 0
win_condition = 15
hearts = 3

icono = pg.image.load(load_asset("etec.jpg"))
pg.display.set_icon(icono)

pg.mixer.music.load(load_asset("ecoaventuras.ogg"))
pg.mixer.music.set_volume(100)
pg.mixer.music.play()

yiji = pg.mixer.Sound(load_asset('yiji.ogg'))

width, height = 1366, 720
screen = pg.display.set_mode((width, height), pg.RESIZABLE)
pg.display.set_caption("Juego de los Plasticos")

black = (0, 0, 0)

i = 0
x = 0
y = 0
ancho = 300
alto = 400
fondo = pg.transform.scale(pg.image.load(load_asset('imagen.jpg')), (1280, 720)).convert()
screen.blit(fondo, (0, 0))

clock = pg.time.Clock()

tacho_size = (130, 147)
tacho_image = pg.transform.scale(pg.image.load(load_asset("tacho.png")), tacho_size)
tacho_x = width // 2 - tacho_size[0] / 2
tacho_y = height - tacho_size[1]
tacho_speed = 15

heart_image = pg.transform.scale(pg.image.load(load_asset('heart.png')), (72, 72))
heart_size = (40, 40)

trash_images = [pg.image.load(load_asset(f"botella{i}.png")) for i in range(6)]
fruit_images = [pg.image.load(load_asset(f"fruta{i}.png")) for i in range(3)]
trash_size = (40, 80)
trash_images = [pg.transform.scale(img, trash_size) for img in trash_images]
trash_speed = 5

last_position = random.randint(0, width - trash_size[0] - 40)
new_position = 0

class Trash:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.image = random.choice(trash_images)

    def update(self):
        self.y += trash_speed

    def check_collision(self):
        global hearts, score
        if tacho_x < self.x + 70 < tacho_x + tacho_size[0] and tacho_y < self.y + 100 < tacho_y + 10:
            score += 1
            trash_objects.remove(self)

        elif tacho_x < self.x + 100 < tacho_x + tacho_size[0] + 40 and tacho_y < self.y + 100 and self.x > tacho_x:
            self.x += 15

        elif tacho_x < self.x + 100 < tacho_x + tacho_size[0] + 40 and tacho_y < self.y + 100 and self.x < tacho_x:
            self.x -= 15
            
        elif self.y > height + 30:
            trash_objects.remove(self)
            if hearts > 0:
                hearts -= 1

trash_objects = []

def show_score():
    font = pg.font.Font(None, 36)
    score_text = font.render("Puntuación: " + str(score), True, black)
    screen.blit(score_text, (10, 10))

def show_hearts():
    for i in range(hearts):
        screen.blit(heart_image, (10 + i * 30, 30))

def end(state):
    fontw = pg.font.Font(None, 80)
    msg = "¡Ganaste!"
    if state == 0:
        msg = "Perdiste :("
    win_text = fontw.render(msg, True, (255, 255, 255))
    screen.blit(win_text, win_text.get_rect(center = screen.get_rect().center))

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if not game_over:
        w = x % fondo.get_rect().width

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            tacho_x -= tacho_speed
        if keys[pg.K_RIGHT]:
            tacho_x += tacho_speed

        tacho_x = max(0, min(tacho_x, width - tacho_size[0]))

        i += 1
        new_position = random.randint(0, width - trash_size[0] - 40)
        position_distance = abs(last_position - new_position)
        # print(f"{last_position} - {new_position} = {position_distance}")
        if position_distance > 300 and i > 70:
            last_position = new_position
            i = 0
            trash_objects.append(Trash(last_position))

        for trash_obj in trash_objects:
            trash_obj.update()
            trash_obj.check_collision()

        screen.blit(fondo, (w, 0))
        x += 1
        screen.blit(fondo, (w - fondo.get_rect().width, y))

        screen.blit(tacho_image, (tacho_x, tacho_y))

        for trash_obj in trash_objects:
            if trash_obj.y < 300: trash_obj.image = pg.transform.rotate(trash_obj.image, 1)
            screen.blit(trash_obj.image, (trash_obj.x, trash_obj.y))

        show_score()
        show_hearts()

        if score >= win_condition or hearts <= 0:
            game_over = True

    else:
        screen.fill((0, 0, 0))

        font = pg.font.Font(None, 36)
        restart_text = font.render("  Reiniciar  ", True, (255, 255, 255))
        exit_text = font.render("  Salir  ", True, (255, 255, 255))

        restart_rect = restart_text.get_rect(center = (width // 2, height // 2 - 50))
        exit_rect = exit_text.get_rect(center = (width // 2, height // 2 + 50))

        pg.draw.rect(screen, (0, 128, 0), restart_rect, border_radius = 10)
        pg.draw.rect(screen, (255, 0, 0), exit_rect, border_radius = 10)

        screen.blit(restart_text, restart_rect)
        screen.blit(exit_text, exit_rect)

        if hearts <= 0:
            end(0)

        elif score >= win_condition:
            end(1)

        mouse_pos = pg.mouse.get_pos()
        mouse_click = pg.mouse.get_pressed()

        if restart_rect.collidepoint(mouse_pos) and mouse_click[0]:
            trash_objects = []
            game_over = False
            score = 0
            hearts = 3

        elif exit_rect.collidepoint(mouse_pos) and mouse_click[0]:
            running = False

    pg.display.flip()
    clock.tick(60)

pg.quit()
