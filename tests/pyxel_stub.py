import math
import random

width = 256
height = 256

KEY_LEFT = 1
KEY_RIGHT = 2
KEY_UP = 3
KEY_DOWN = 4
KEY_SPACE = 5
KEY_RETURN = 6
KEY_E = 7

_btn = set()
_btnp = set()

def btn(key):
    return key in _btn

def btnp(key):
    if key in _btnp:
        _btnp.remove(key)
        return True
    return False

def set_btn(key, value=True):
    if value:
        _btn.add(key)
    else:
        _btn.discard(key)

def set_btnp(key, value=True):
    if value:
        _btnp.add(key)
    else:
        _btnp.discard(key)

def cos(angle):
    return math.cos(math.radians(angle))

def sin(angle):
    return math.sin(math.radians(angle))

def atan2(y, x):
    return math.degrees(math.atan2(y, x))

def rndi(a, b):
    return random.randint(a, b)


def rndf(a, b):
    return random.uniform(a, b)


def stop():
    pass


def quit():
    pass


def play(*a, **k):
    pass


def playm(*a, **k):
    pass


def text(*a, **k):
    pass


def blt(*a, **k):
    pass


def circ(*a, **k):
    pass


def circb(*a, **k):
    pass


def pset(*a, **k):
    pass


def rect(*a, **k):
    pass


def rectb(*a, **k):
    pass


def cls(*a, **k):
    pass


class Image:
    def __init__(self, w=0, h=0):
        self.w = w
        self.h = h

    def load(self, x, y, filename):
        pass

    @staticmethod
    def from_image(filename, incl_colors=False):
        return Image()
images = [Image(256,256), Image(256,256), Image(256,256)]

