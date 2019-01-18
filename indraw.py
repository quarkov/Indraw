import pygame as pg
import random


class Vec2d:
    def __init__(self, x=1.0, y=1.0):
        self.x = int(x)
        self.y = int(y)

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
        self.knots_count = 1
        self.knots = []

    def add_point(self, new_point):
        self.points.append(Vec2d(x=new_point[0], y=new_point[1]))
        self.p_count += 1

    def add_speed(self):
        new_speed = [random.random()*10, random.random()*10]
        self.speeds.append(Vec2d(x=new_speed[0], y=new_speed[1]))

    def remove_point(self):
        self.points.pop() if self.points else None
        self.speeds.pop() if self.speeds else None
        self.p_count = len(self.points)

    def set_points(self):
        for i in range(self.p_count):
            self.points[i] = self.points[i] + self.speeds[i]
            if not 0 <= self.points[i].x <= SCREEN_DIM[0]:
                self.speeds[i].x = -self.speeds[i].x
            if not 0 <= self.points[i].y <= SCREEN_DIM[1]:
                self.speeds[i].y = -self.speeds[i].y

    def draw_lines(self, width=3, color=(255, 255, 255)):
        if self.p_count >= 3:
            for i in range(-1, len(self.knots) - 1):
                pg.draw.line(gameDisplay, color, self.knots[i].int_pair(),
                             self.knots[i+1].int_pair(), width)

    def draw_points(self, width=3, color=(255, 255, 255)):
        for point in self.points:
            pg.draw.circle(gameDisplay, color, point.int_pair(), width)


class Knot(Polyline):
    def increase_knots(self):
        self.knots_count += 1 if self.knots_count < 30 else 0

    def decrease_knots(self):
        self.knots_count -= 1 if self.knots_count > 1 else 0

    def get_point(self, base_p, alpha):
        knot = (alpha * base_p[2] +
               (1-alpha) * (alpha * base_p[1] + (1-alpha) * base_p[0]))
        return knot

    def get_points(self, base_p):
        alpha = 1 / self.knots_count
        knots = [self.get_point(base_p, i*alpha) for i in range(self.knots_count)]
        return knots

    def get_knot(self):
        if self.p_count >= 3:
            self.knots.clear()
            for i in range(-2, self.p_count - 2):
                ptn = []
                ptn.append((self.points[i] + self.points[i+1]) * 0.5)
                ptn.append(self.points[i+1])
                ptn.append((self.points[i+1] + self.points[i+2]) * 0.5)
                self.knots.extend(self.get_points(ptn))


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pg.font.SysFont("courier", 24)
    font2 = pg.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help/Resume"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["", ""])
    data.append(["Num+", "More knots"])
    data.append(["Num-", "Less knots"])
    data.append(["↑", "Speed up"])
    data.append(["↓", "Speed down"])
    data.append(["", ""])
    data.append(["C", "Change colors"])
    data.append(["F", "Bad trip/normal"])
    data.append(["Z", "Remove last point"])

    pg.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30*i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30*i))

SCREEN_DIM = (800, 600)

if __name__ == "__main__":
    fps = 60
    pg.init()
    gameDisplay = pg.display.set_mode(SCREEN_DIM)
    pg.display.set_caption(f"Indraw, speedrate - {int(fps/2)} %, knots count - 1")
    gameDisplay.fill((0, 0, 0))

    pol = Knot()
    coloring = True
    filling = True
    working = True
    show_help = True
    pause = True

    hue = 0
    color = pg.Color(0)

    while working:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                working = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    gameDisplay.fill((0, 0, 0))
                    show_help = not show_help
                if event.key == pg.K_ESCAPE:
                    working = False
                if event.key == pg.K_r:
                    pol.points, pol.speeds, pol.p_count = [], [], 0
                if event.key == pg.K_p:
                    pause = not pause
                if event.key == pg.K_KP_PLUS:
                    pol.increase_knots()
                    pg.display.set_caption(f"Indraw, speedrate - {int(fps/2)} %, knots count - {pol.knots_count}")
                if event.key == pg.K_KP_MINUS:
                    pol.decrease_knots()
                    pg.display.set_caption(f"Indraw, speedrate - {int(fps/2)} %, knots count - {pol.knots_count}")
                if event.key == pg.K_UP:
                    fps += 20 if fps < 200 else 0
                    pg.display.set_caption(f"Indraw, speedrate - {int(fps/2)} %, knots count - {pol.knots_count}")
                if event.key == pg.K_DOWN:
                    fps -= 20 if fps > 20 else 0
                    pg.display.set_caption(f"Indraw, speedrate - {int(fps/2)} %, knots count - {pol.knots_count}")
                if event.key == pg.K_c:
                    coloring = not coloring
                if event.key == pg.K_f:
                    filling = not filling
                if event.key == pg.K_z:
                    pol.remove_point()

            if event.type == pg.MOUSEBUTTONDOWN:
                pol.add_point(event.pos)
                pol.add_speed()

        gameDisplay.fill((0, 0, 0)) if filling else None
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        pol.draw_points()
        pol.get_knot()
        pol.draw_lines(color=color) if coloring else pol.draw_lines()

        pol.set_points() if not pause else None
        draw_help() if show_help else None

        pg.display.flip()
        pg.time.Clock().tick(fps)
    pg.display.quit()
    pg.quit()
    exit(0)
