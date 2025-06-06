import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from firstshot.logic.collision import check_collision

class DummyEntity:
    def __init__(self, x, y, hit_area):
        self.x = x
        self.y = y
        self.hit_area = hit_area

def test_overlapping_rectangles_return_true():
    e1 = DummyEntity(0, 0, (0, 0, 10, 10))
    e2 = DummyEntity(5, 5, (0, 0, 10, 10))
    assert check_collision(e1, e2)

def test_separated_rectangles_return_false():
    e1 = DummyEntity(0, 0, (0, 0, 10, 10))
    e2 = DummyEntity(20, 20, (0, 0, 10, 10))
    assert not check_collision(e1, e2)

def test_edge_touching_rectangles_return_true():
    e1 = DummyEntity(0, 0, (0, 0, 10, 10))
    e2 = DummyEntity(10, 0, (0, 0, 10, 10))
    assert check_collision(e1, e2)
