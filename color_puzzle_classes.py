import math
import pygame
import random

## recycled from Enzymemania
class Drawable(object):
    ID = 0

    def __init__(self, name="",
                 x=0, y=0,
                 angle= math.pi/2, xsize=10, ysize=10,
                 color=(0, 50, 0), shapeStr="rectangle"):

        Drawable.ID += 1
        self.id = Drawable.ID
        self._name = name
        self._x = x
        self._y = y
        self._angle = angle
        self._xsize = xsize
        self._ysize = ysize
        self._shape = self.initShape(shapeStr)
        self._shapeStr = shapeStr
        self.xsurface = self.x+self.xsize
        self.ysurface = self.y+self.ysize
        self._color = color
        # create an actual rect, polygon etc; easier for collision handling
#        self.hasCollided = False


    def __repr__(self):
        s = ""
        s += ",".join([str(i) for i in [self.id, self.x, self.y, self.xsize, self.ysize, self.shape, self.color]])
        return s

    def initShape(self, shapeStr):
        if isinstance(shapeStr, str):
            if shapeStr.lower() == "rectangle":
                return pygame.Rect(self._x, self._y, self._xsize, self._ysize)
            else:
                return None
        else:
            raise Exception("initShape needs str")

    @property
    def x(self):
        return self._shape.x

    @x.setter
    def x(self, val):
        try:
            self._shape.x = float(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def y(self):
        return self._shape.y

    @y.setter
    def y(self, val):
        try:
            self._shape.y = float(val)
            self._y = float(val)
            # print(self._shape.y)
        except TypeError as e:
            print(e, self.id)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        try:
            self._angle = float(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        if isinstance(val, tuple):
            try:
                self._color = val
            except TypeError as e:
                print(e, self.id)
        else:
            raise Exception("Sth wrong with color setter")

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, val):
        try:
            self._color = int(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def xsize(self):
        return self._xsize

    @xsize.setter
    def xsize(self, val):
        try:
            self._shape.width = int(val)
            self._xsize = int(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def ysize(self):
        return self._ysize

    @ysize.setter
    def ysize(self, val):
        try:
            self._ysize = int(val)
            self._shape.height = int(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if isinstance(val, str):
            self._name = val

    def draw(self, display):
#        if self._shapeStr == "rectangle":
#            if isinstance(self._shape, pygame.Rect):
#                pygame.draw.rect(display, self.color, self._shape, 0)
#        else:
#            #TODO
#            pass
        pygame.draw.rect(display, self.color, self._shape, 0)

class Tile(Drawable):

    def __init__(self, length, pos_x, pos_y):
        Drawable.__init__(self, color=(25,25,25), xsize=length, ysize=length,
                          y=pos_y * length)
        self.x = pos_x * length
        self.pos_x = pos_x
        self.pos_y = pos_y



class Filter(Tile):
    def __init__(self, length, pos_x, pos_y):
        Tile.__init__(self, length, pos_x, pos_y)
        self.x = pos_x * length
        self.ori_color = self.color

    def choose_color(self, col_target):
        # where col_target is a (r,g,b) tuple
        channels = [0,0,0]
        for i in range(3):
            channels[i] = random.choice(range(col_target[i]))

        return tuple(channels)

    def calculate_color(self, col_target, other):
        channels = [0,0,0]
        for i in range(3):
            channels[i] = col_target[i] - other.color[i]
        return tuple(channels)

    def overlap_color(self, other):
        new_colors = [0, 0, 0]
        for i in range(3):
            new_colors[i] = self.ori_color[i] + other.ori_color[i]
            while new_colors[i] > 255:
                new_colors[i] -= 255
        return tuple(new_colors)

    def checkCollisionList(self, filterList, ignore=None):
        filterList = [x for x in filterList if x is not ignore]
        others = [o.shape for o in filterList]
        try:
            collided = (self.shape.collidelistall(others))
            if len(collided) > 0:
                for i in collided:
                    self.color = self.overlap_color(filterList[i])
                    print(filterList[i])


            else:
                self.color = self.ori_color
        except TypeError as e:
            print(e)


class Card(Drawable):
    def __init__(self, length, pos_x, pos_y):
        Drawable.__init__(self, x=pos_x * length, y=pos_y * length, xsize=length*2, ysize=length)
        self.filter_left = Filter(length, pos_x, pos_y)
        self.filter_right = Filter(length, pos_x + 1, pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def move_components(self):
        self.filter_left.x = self.x
        self.filter_left.y = self.y
        self.filter_right.x = self.x + self.filter_left.xsize
        self.filter_right.y = self.y

    def draw(self,screen):
       self.filter_left.draw(screen)
       self.filter_right.draw(screen)
