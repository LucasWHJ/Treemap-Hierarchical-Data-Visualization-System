"""
Tests for Assignment 2
"""
from tm_trees import TMTree


def test_update_rec_vertical() -> None:
    """Test vertical partition when width > height.
    """
    leaf_a = TMTree("A", [], 25)
    leaf_b = TMTree("B", [], 75)
    root = TMTree("Root", [leaf_a, leaf_b])
    root.update_rectangles((0, 0, 200, 100))
    assert leaf_a.rect == (0, 0, 50, 100)
    assert leaf_b.rect == (50, 0, 150, 100)


def test_update_rec_horizontal() -> None:
    """Test horizontal partition when width <= height.
    """
    leaf_a = TMTree("A", [], 2)
    leaf_b = TMTree("B", [], 8)
    root = TMTree("Root", [leaf_a, leaf_b])
    root.update_rectangles((0, 0, 100, 200))
    assert leaf_a.rect == (0, 0, 100, 40)
    assert leaf_b.rect == (0, 40, 100, 160)


def test_rounding_and_sync() -> None:
    """Test size change rounding and root synchronization.
    """
    leaf = TMTree("leaf", [], 10)
    root = TMTree("root", [leaf])
    leaf.change_size(0.01)
    assert leaf.data_size == 11
    assert root.data_size == 11
    leaf.change_size(-0.99)
    assert leaf.data_size == 1


def test_get_rec_with_exp() -> None:
    """Test get_rectangles logic with node expansion.
    """
    child = TMTree("child", [], 100)
    folder = TMTree("folder", [child])
    root = TMTree("root", [folder])
    root.update_rectangles((0, 0, 100, 100))
    rects = root.get_rectangles()
    assert len(rects) == 1
    assert rects[0][0] == (0, 0, 100, 100)
    root.expand()
    rects = root.get_rectangles()
    assert len(rects) == 1
    root.expand_all()
    rects = root.get_rectangles()
    assert len(rects) == 1
