import math
import pygame
import random

## recycled from Enzymemania
class Drawable(object):
    ID = 0

    def __init__(self, name="",
                 x=0, y=0, xvel=1.0, yvel=1.0,
                 angle= math.pi/2, xsize=10, ysize=10,
                 color=(0, 255, 0), shapeStr="rectangle"):

        Drawable.ID += 1
        self.id = Drawable.ID
        self._name = name
        self._x = x
        self._y = y
        self._xvel = xvel
        self._yvel = yvel
        self._angle = angle
        self._xsize = xsize
        self._ysize = ysize
        self._shape = self.initShape(shapeStr)
        self._shapeStr = shapeStr
        self.xsurface = self.x+self.xsize
        self.ysurface = self.y+self.ysize
        self._color = color
        self.textxOffset = 0
        # create an actual rect, polygon etc; easier for collision handling
#        self.hasCollided = False
    def addText(self, screen, font):
        tmpfont = font.render(self.name, True, (0,255,0))
        rect = tuple(tmpfont.get_rect())
        #print(rect)
        tmpwidth = rect[2]
        tmpheight = rect[3]
        #if self.x-tmpwidth/2+self.textxOffset  < self.x-tmpwidth/2:
        fontx = self.x-tmpwidth/2+math.sin(self.textxOffset)*60
        #else:
        #    fontx = self.x-tmpwidth/2-self.textxOffset
        self.textxOffset += 0.02
        #self.textxOffset%tmpwidth
        screen.blit(tmpfont, (fontx, self.y-tmpheight))
        #pygame.display.update()

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
    def yvel(self):
        return self._yvel

    @yvel.setter
    def yvel(self, val):
        try:
            self._yvel = float(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def xvel(self):
        return self._xvel

    @xvel.setter
    def xvel(self, val):
        try:
            self._xvel = float(val)
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
        if self._shapeStr == "rectangle":
            if isinstance(self._shape, pygame.Rect):
                pygame.draw.rect(display, self._color, self._shape, 0)
        else:
            #TODO
            pass

    def move(self, x=None, y=None, boundx=800, boundy=500):
        if x is None:
            x = self.xvel
        if y is None:
            y = self.yvel

        if not self.x + self.xvel > boundx:
            self.x += self.xvel
        else:
            self.xvel *=-1
        if not (self.y + self.yvel) > boundy:
            self.y += self.yvel
        else:
            self.yvel *= -1

    def checkCollision(self, other):
        try:
            if self.shape.colliderect(other.shape):
                #self._color = (255, 0, 0)
                self.collide()
                other.collide()
        except TypeError as e:
            print(e)

    def checkCollisionList(self, otherList, entityList):
        others = [o.shape for o in otherList]
        try:
            collided = (self.shape.collidelistall(others))
            if len(collided) > 0:
                for i in collided:
                    #otherList[i].collide()
                    otherList[i].bounceOff(self,entityList=entityList)
                    self.bounceOff(otherList[i])
                self._color = (255, 0, 0)
        except TypeError as e:
            print(e)

    def bounceOff(self, other, entityList = None):
        res = self.name+" collided with "+other.name
        #velocity
        vx = self.xvel
        vy = self.yvel
        #print(str(vx)+','+str(vy))
        #coordinates y
        #take colliding sides of each box
        if vy > 0:
            ys = self.y + self.ysize
            yo = other.y
        # take the complementary sides of boxes if collision is in other direction, but inverse for future simplicity
        else:
            ys = self.y * (-1)
            yo = (other.y + other.ysize) * (-1)
        # coordinates x
        if vx > 0:
            xs = self.x + self.xsize
            xo = other.x
        else:
            xs = self.x * (-1)
            xo = (other.x + other.xsize) * (-1)

        #check for last frame pass through y
        test = []
        if (ys >= yo) and ((ys - 2.2*abs(vy)) <= yo):
            self.yvel *= -1
            test.append('y')
        else:
            #print (ys,yo,abs(vy))
            other.yvel *= -1
        #check for last frame pass through x
        if (xs >= xo) and ((xs - 2.2*abs(vx)) <= xo):
            self.xvel *= -1
            test.append('x')
        else:
            other.xvel *= -1
        if len(test) == 0:
            pass

        self.move()
        other.move()

class Tile(Drawable):

    def __init__(self, length, pos_x, pos_y):
        Drawable.__init__(self, yvel=0, xvel=0)
        self._x = pos_x * length
        self._y = pos_y * length
        self._xsize = length
        self._ysize = length
        self.color = (200,200,200)

class Filter(Tile):
    def __init__(self, length, pos_x, pos_y):
        Tile.__init__(self, length, pos_x, pos_y)

    def choose_color(self, col_target):
        # where ranges is a (r,g,b) tuple
        channels = [0,0,0]
        for i in range(3):
            channels[i] = random.choice(range(col_target[i]))
        self.color = tuple(channels)

    def calculate_color(self, col_target, other):
        channels = [0,0,0]
        for i in range(3):
            channels[i] = col_target[i] - other.color[i]
        self.color = tuple(channels)

class Card(Drawable):
    def __init__(self, length, pos_x, pos_y):
        Drawable.__init__(self, xvel=0, yvel=0, x=pos_x * length, y=pos_y * length)
        self.filter_left = Filter(length, pos_x, pos_y)
        self.filter_right = Filter(length, pos_x + 1, pos_y)
