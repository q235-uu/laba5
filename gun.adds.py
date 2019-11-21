from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, x=20, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.ay = 1.5
        self.xtr = 0
        self.ytr = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        self.xtr = -0.1 * self.vx
        self.ytr = -0.1 * self.vy
        if (self.x - self.r < 0 or self.x + self.r > 800):
            self.vx = -self.vx
            self.ytr = -0.1 * self.vy
            self.vy += self.ay + self.ytr
        elif (self.y - self.r < 0 or self.y + self.r > 600):
            self.vy = -self.vy
            self.vx += self.xtr
            self.vy += self.ay
        else:
            self.vy += self.ay
        self.vy += self.ay
        self.y += self.vy
        self.x += self.vx
        canv.move(self.id, self.vx, self.vy)
        if self.y + self.r > 650:
            self.vy = 0
            self.ay = 0
            self.vx = 0
            self.xtr = 0
            self.ytr = 0
            canv.delete(self.id)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли
        данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели.
            В противном случае возвращает False.
        """
        # FIXME
        if (obj.r + self.r) ** 2 > (self.x - obj.x) ** 2 + (self.y -
                                                            obj.y) ** 2:
            return True
        else:
            return False


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.vy = 5
        self.x = 20
        self.y = 450
        self.id = canv.create_line(self.x, self.y, self.x + 30, self.y - 20,
                                   width=7) #FIXME: don't know how to set it...

    def onclick1(self, event):
        self.y -= 5
        # canv.move(self.id, 0, self.vy)

    def onclick2(self, event):
        self.y += 5

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча
        vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball(g1.x, g1.y)
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, self.x, self.y,
                    self.x + max(self.f2_power, 20) * math.cos(self.an),
                    self.y + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():

    # FIXME: don't work!!! How to call this functions when object is created?
    def __init__(self):
        self.point = 0
        self.live = 1
        self.x = 0
        self.y = 0
        self.r = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])

    def new_target(self, n):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(10, 60)
        self.vy = rnd(1, 10)
        self.vx = rnd(5, 15)
        self.n = n
        if n == 0:
            self.id = canv.create_oval(0, 0, 0, 0)
            canv.coords(self.id, self.x - self.r,
                        self.y - self.r, self.x + self.r, self.y + self.r)
        else:
            dA = math.pi * 2 / n
            A = 0
            size = 2 * self.r * math.sin(math.pi / n)
            self.points = []
            x1 = self.x - size / 2
            y1 = self.y - math.sqrt(self.r ** 2 - (size / 2) ** 2)
            self.points += (x1, y1)
            for i in range(n):
                x1 += size * math.sin(A)
                y1 += size * math.cos(A)
                A += dA
                self.points += (x1, y1)
            self.id = canv.create_polygon(self.points, outline="black")
        canv.itemconfig(self.id, fill=self.color)

    def move(self):
        self.y += self.vy
        self.x += self.vx
        if (self.x - self.r < 0 or self.x + self.r > 800):
            self.vx = -self.vx
        if (self.y - self.r < 0 or self.y + self.r > 600):
            self.vy = -self.vy
        canv.move(self.id, self.vx, self.vy)

    def hit(self, point=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.point += point
        canv.itemconfig(self.id_point, text=self.point)


t1 = target()
t2 = target()
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []


class Game():
    def __init__(self):
        quantity = [0, 3, 4, 5]
        n = choice(quantity)
        t1.new_target(n)
        n = choice(quantity)
        t2.new_target(n)
        self.bullet = bullet
        self.balls = balls
        canv.bind('<Button-1>', g1.fire2_start)
        canv.bind('<ButtonRelease-1>', g1.fire2_end)
        canv.bind('<Motion>', g1.targetting)

        z = 0.03
        t1.live = 1
        t2.live = 1
        while t1.live or t2.live or balls:
            t1.move()
            t2.move()
            for b in balls:
                b.move()
                if b.hittest(t1) and t1.live:
                    t1.live = 0
                    t1.hit()

                if b.hittest(t2) and t2.live:
                    t2.live = 0
                    t2.hit()

                if t1.live == 0 and t2.live == 0:
                    canv.itemconfig(screen1, text='Попыток: ' + str(bullet))
                    canv.bind('<Button-1>', '')
                    canv.bind('<ButtonRelease-1>', '')
            canv.update()
            time.sleep(0.03)
            g1.targetting()
            g1.power_up()
        canv.itemconfig(screen1, text='')
        canv.delete(gun)
        root.after(750, new_game)

new_game = Game()

mainloop()
