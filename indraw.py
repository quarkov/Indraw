import pygame as pg
import random


class Vec2d:
    def __init__(self, x=1.0, y=1.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return self.x*other.x + self.y*other.y
        else:
            return Vec2d(self.x*other, self.y*other)

    __rmul__ = __mul__

    def __len__(self):
        return (self.x**2 + self.y**2)**0.5

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    def __init__(self, points=(), speeds=()):
        self.points = [Vec2d(point) for point in points]
        self.speeds = [Vec2d(speed) for speed in speeds]
        self.p_count = len(self.points)

    def add_point(self, new_point):
        self.points.append(Vec2d(x=new_point[0], y=new_point[1]))
        self.p_count += 1

    def add_speed(self):
        new_speed = [random.random()*10, random.random()*10]
        self.speeds.append(Vec2d(x=new_speed[0], y=new_speed[1]))

    def set_points(self):
        for i in range(self.p_count):
            self.points[i] = self.points[i] + self.speeds[i]
            if not 0 <= self.points[i].x <= SCREEN_DIM[0]:
                self.speeds[i].x = -self.speeds[i].x
            if not 0 <= self.points[i].y <= SCREEN_DIM[1]:
                self.speeds[i].y = -self.speeds[i].y

    def draw_lines(self, width=3, color=(255, 255, 255)):
        if self.p_count >= 3:
            for i in range(-1, self.p_count - 1):
                pg.draw.line(gameDisplay, color, self.points[i].int_pair(),
                             self.points[i+1].int_pair(), width)

    def draw_points(self, width=3, color=(255, 255, 255)):
        for point in self.points:
            pg.draw.circle(gameDisplay, color, point.int_pair(), width)


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pg.font.SysFont("courier", 24)
    font2 = pg.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help/Resume"])
    data.append(["P", "Pause/Play"])
    data.append(["R", "Restart"])
    data.append(["↑", "Speed up"])
    data.append(["↓", "Speed down"])

    pg.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30*i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30*i))


if __name__ == "__main__":
    SCREEN_DIM = (800, 600)
    fps = 60
    pg.init()
    gameDisplay = pg.display.set_mode(SCREEN_DIM)
    pg.display.set_caption(f"Indraw, speedrate {int(fps/2)} %")
    gameDisplay.fill((0, 0, 0))

    pol = Polyline()
    working = True
    show_help = True
    pause = False

    hue = 0
    color = pg.Color(0)

    while working:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                working = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    working = False
                if event.key == pg.K_r:
                    gameDisplay.fill((0, 0, 0))
                    pol.points, pol.speeds, pol.p_count = [], [], 0
                if event.key == pg.K_p:
                    pause = not pause
                if event.key == pg.K_F1:
                    gameDisplay.fill((0, 0, 0))
                    show_help = not show_help
                if event.key == pg.K_UP:
                    fps += 20 if fps < 200 else 0
                    pg.display.set_caption(f"Indraw, speedrate {int(fps/2)} %")
                if event.key == pg.K_DOWN:
                    fps -= 20 if fps > 20 else 0
                    pg.display.set_caption(f"Indraw, speedrate {int(fps/2)} %")
            if event.type == pg.MOUSEBUTTONDOWN:
                pol.add_point(event.pos)
                pol.add_speed()

        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        pol.draw_points()
        pol.draw_lines(color=color)

        if not pause:
            pol.set_points()
        if show_help:
            draw_help()

        pg.display.flip()
        pg.time.Clock().tick(fps)
    pg.display.quit()
    pg.quit()
    exit(0)
