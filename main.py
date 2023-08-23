'''
class SeaBattle для управления игровым процессом в целом. Игра должна осуществляться между человеком и компьютером.
Выстрелы со стороны компьютера можно реализовать случайным образом в свободные клетки.
'''

from random import randint, choice
from copy import deepcopy


class GamePole:
    def __init__(self, size):
        self._size = size
        self._ships = []

    def init(self):
        self._ships = [Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(4, tp=randint(1, 2))][::-1]
        indx = 0
        while indx < len(self._ships):
            curr = True
            while curr:
                if indx == 0:
                    self._ships[indx].set_start_coords(randint(0, self._size - 1), randint(0, self._size - 1))
                    self._ships[indx].set_coords()
                    self._ships[indx].set_no(self._size)
                    if self._ships[indx].is_out_pole(self._size):
                        continue
                    else:
                        indx += 1
                        curr = False
                else:
                    self._ships[indx].set_start_coords(randint(0, self._size - 1), randint(0, self._size - 1))
                    self._ships[indx].set_coords()
                    self._ships[indx].set_no(self._size)
                    if self._ships[indx].is_out_pole(self._size):
                        continue
                    k = 0
                    for j in range(indx):
                        if self._ships[indx].is_collide(self._ships[j]):
                            k += 1
                    if k == 0:
                        indx += 1
                        curr = False
                    else:
                        continue


    def get_ships(self):
        return self._ships

    def move_ships(self):
        for i in self._ships:
            b = deepcopy(i)
            b.move(1, self._size)
            if b.get_start_coords() == i.get_start_coords():
                b.move(-1)
                k = 0
                for j in self._ships:
                    if i != j:
                        if b.is_collide(j):
                            k += 1
                if k == 0:
                    i.set_start_coords(b._x, b._y)
                    i.set_coords()
                    i.set_no(self._size)
            else:
                k = 0
                for j in self._ships:
                    if i != j:
                        if b.is_collide(j):
                            k += 1
                if k == 0:
                    i.set_start_coords(b._x, b._y)
                    i.set_coords()
                    i.set_no(self._size)

    def show(self):
        res = self.get_pole()
        for i in res:
            for j in i:
                print(j, end=' ')
            print()

    def get_pole(self):
        pole = [[0 for i in range(self._size)] for _ in range(self._size)]
        for ship in self._ships:
            for i in range(len(ship._coords)):
                pole[ship._coords[i][1]][ship._coords[i][0]] = ship._cells[i]
        res = []
        for y in pole:
            res.append(tuple(y))
        return tuple(res)


class Ship(GamePole):
    def __init__(self, length, tp=1, x=None, y=None):
        self._x = x
        self._y = y
        if 1 <= length <= 4:
            self._length = length
        if tp in (1, 2):
            self._tp = tp
        self._is_move = True
        self._cells = [1 for _ in range(self._length)]
        self._coords = []
        if self._x is not None and self._y is not None:
            self.set_coords()
            self.set_no(size=10)


    def set_coords(self):
        self._coords = []
        '''на основе начальных координат, ориентации и длины'''
        self._coords.append((self._x, self._y))
        if self._length != 1:
            if self._tp == 1:
                for i in range(self._length - 1):
                    self._coords.append((self._x + i + 1, self._y))
            else:
                for i in range(self._length - 1):
                    self._coords.append((self._x, self._y + i + 1))

    def set_no(self, size):
        self._no = []
        self._no = self._coords.copy()
        if self._tp == 1:
            if self._y == 0 and self._x == 0:
                for i in range(len(self._coords)):
                    if i != len(self._coords) - 1:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
            elif self._y == 0 and self._coords[-1][0] == size - 1:
                for i in range(len(self._coords)):
                    if i != 0:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
            elif self._y == 0 and self._coords[-1][0] != size - 1 and self._x != 0:
                for i in range(len(self._coords)):
                    if i == 0:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                    elif i == len(self._coords) - 1:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
            elif self._y == size - 1 and self._x == 0:
                for i in range(len(self._coords)):
                    if i != len(self._coords) - 1:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
            elif self._y == size - 1 and self._coords[-1][0] == size - 1:
                for i in range(len(self._coords)):
                    if i != 0:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
            elif self._y == size - 1 and self._coords[-1][0] != size - 1 and self._x != 0:
                for i in range(len(self._coords)):
                    if i == 0:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                    elif i == len(self._coords) - 1:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
            elif self._y != 0 and self._y != size - 1 and self._x == 0:
                for i in range(len(self._coords)):
                    if i != len(self._coords) - 1:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] - 1))
            elif self._y != 0 and self._y != size - 1 and self._coords[-1][0] == size - 1:
                for i in range(len(self._coords)):
                    if i == 0:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] - 1))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
            else:
                for i in range(len(self._coords)):
                    if i == 0:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                    elif i == len(self._coords) - 1:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
        else:
            if self._y == 0 and self._x == 0:
                for i in range(len(self._coords)):
                    if i != len(self._coords) - 1:
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
            elif self._x == 0 and self._coords[-1][1] == size - 1:
                for i in range(len(self._coords)):
                    if i != 0:
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
            elif self._x == 0 and self._coords[-1][1] != size - 1 and self._y != 0:
                for i in range(len(self._coords)):
                    if i == 0:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                    elif i == len(self._coords) - 1:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                    else:
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
            elif self._x == size - 1 and self._y == 0:
                for i in range(len(self._coords)):
                    if i != len(self._coords) - 1:
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
            elif self._x == size - 1 and self._coords[-1][1] == size - 1:
                for i in range(len(self._coords)):
                    if i != 0:
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
            elif self._x == size - 1 and self._coords[-1][1] != size - 1 and self._y != 0:
                for i in range(len(self._coords)):
                    if i == 0:
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                    elif i == len(self._coords) - 1:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                    else:
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
            elif self._x != 0 and self._x != size - 1 and self._y == 0:
                for i in range(len(self._coords)):
                    if i != len(self._coords) - 1:
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                    else:
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] + 1))
            elif self._x != 0 and self._x != size - 1 and self._coords[-1][1] == size - 1:
                for i in range(len(self._coords)):
                    if i == 0:
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                    else:
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
            else:
                for i in range(len(self._coords)):
                    if i == 0:
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0], self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] - 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                    elif i == len(self._coords) - 1:
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0], self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1] + 1))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))
                    else:
                        self._no.append((self._coords[i][0] - 1, self._coords[i][1]))
                        self._no.append((self._coords[i][0] + 1, self._coords[i][1]))

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_start_coords(self):
        return (self._x, self._y)

    def move(self, go, size=10, obj=None):
        if self._is_move:
            if self._tp == 1:
                a = deepcopy(self)
                a.set_start_coords(a._x + go, a._y)
                a.set_coords()
                if not a.is_out_pole(size):
                    if obj is None:
                        self.set_start_coords(a._x, a._y)
                        self.set_coords()
                        self.set_no(size)
                    else:
                        if not a.is_collide(obj):
                            a.set_no(size)
                            self.set_start_coords(a._x, a._y)
                            self.set_coords()
                            self.set_no(size)
            else:
                a = deepcopy(self)
                a.set_start_coords(a._x, a._y + go)
                a.set_coords()
                if not a.is_out_pole(size):
                    if obj is None:
                        self.set_start_coords(a._x, a._y)
                        self.set_coords()
                        self.set_no(size)
                    else:
                        if not a.is_collide(obj):
                            a.set_no(size)
                            self.set_start_coords(a._x, a._y)
                            self.set_coords()
                            self.set_no(size)

    def is_collide(self, ship):
        k = 0
        for i in self._coords:
            if i in ship._no:
                k += 1
                return True
        if k == 0:
            return False

    def is_out_pole(self, size):
        '''возвращает выходит ли за границы поля'''
        if self._tp == 1:
            if self._coords[-1][0] >= size:
                return True
            else:
                return False
        else:
            if self._coords[-1][1] >= size:
                return True
            else:
                return False

    def __getitem__(self, item):
        if 0 <= item < self._length:
            return self._cells[item]

    def __setitem__(self, key, value):
        if 0 <= key < self._length:
            self._cells[key] = value