"""
=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: tuple[int, int, int, int]
    data_size: int
    _colour: tuple[int, int, int]
    _name: str
    _subtrees: list[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: list[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.

        >>> tree1 = TMTree("C", [], 123)
        >>> tree1.data_size
        123
        >>> tree2 = TMTree("C", [TMTree("S", [], 99), TMTree("M", [], 1)], 6)
        >>> tree2.data_size
        100
        >>> tree2._subtrees[1]._parent_tree == tree2
        True
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None
        self._expanded = False
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        if len(self._subtrees) == 0:
            self.data_size = data_size
        else:
            self.data_size = 0
            for subtree in self._subtrees:
                self.data_size += subtree.data_size
                subtree._parent_tree = self

        # You will change this in Task 5

        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        # 2. Set this tree as the parent for each of its subtrees.

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    def update_rectangles(self, rect: tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        width, height = rect[2], rect[3]

        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
        elif len(self._subtrees) == 0:
            self.rect = rect
        else:
            self.rect = rect
            if width > height:  # do vertical rectangles
                self._update_rect_vertical(rect)
            else:  # width <= height -> do horizontal rectangles
                self._update_rect_horizontal(rect)
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect

    def _update_rect_vertical(self, rect: tuple[int, int, int, int]) -> None:
        """Helper function to partition the rectangle vertically"""
        x, y, width, height = rect
        curr_width = 0
        for i in range(len(self._subtrees)):
            subtree = self._subtrees[i]
            if i < len(self._subtrees) - 1:
                new_width = math.floor(width * subtree.data_size
                                       / self.data_size)
            else:
                new_width = width - curr_width
            new_rect = (x + curr_width, y, new_width, height)
            subtree.update_rectangles(new_rect)
            curr_width += new_width

    def _update_rect_horizontal(self, rect: tuple[int, int, int, int]) -> None:
        """Helper function to partition the rectangle horizontally"""
        x, y, width, height = rect
        curr_height = 0
        for i in range(len(self._subtrees)):
            subtree = self._subtrees[i]
            if i < len(self._subtrees) - 1:
                new_height = math.floor(height * subtree.data_size
                                        / self.data_size)
            else:
                new_height = height - curr_height
            new_rect = (x, y + curr_height, width, new_height)
            subtree.update_rectangles(new_rect)
            curr_height += new_height

    def get_rectangles(self) -> list[tuple[tuple[int, int, int, int],
                                           tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self.data_size == 0:
            return []
        if not self._expanded or not self._subtrees:
            return [(self.rect, self._colour)]
        result = []
        for subtree in self._subtrees:
            result.extend(subtree.get_rectangles())
        return result

    def get_tree_at_position(self, pos: tuple[int, int]) -> Optional[TMTree]:
        """
        Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.
        """
        x, y, width, height = self.rect
        px, py = pos

        if not (x <= px < x + width and y <= py < y + height):
            return None
        if not self._subtrees or not self._expanded:
            return self
        for subtree in self._subtrees:
            result = subtree.get_tree_at_position(pos)
            if result:
                return result
        return self

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if not self._subtrees:
            return self.data_size
        size = 0
        for subtree in self._subtrees:
            size += subtree.update_data_sizes()
        self.data_size = size
        return self.data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if not self._subtrees and destination._subtrees:
            if self._parent_tree:
                self._parent_tree._subtrees.remove(self)

            destination._subtrees.append(self)
            self._parent_tree = destination
            root = self
            while root._parent_tree:
                root = root._parent_tree
            root.update_data_sizes()

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if not self._subtrees:
            change_amount = math.ceil(self.data_size * abs(factor))

            if factor > 0:
                self.data_size += change_amount
            elif factor < 0:
                self.data_size = max(1, self.data_size - change_amount)

            root = self
            while root._parent_tree is not None:
                root = root._parent_tree
            root.update_data_sizes()

    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful. You should clean up
        any references the current node may still have to its parent.

        Only do this if this node has a parent tree.
        """
        if self._parent_tree is None:
            return False

        parent = self._parent_tree
        if self in parent._subtrees:
            parent._subtrees.remove(self)

        self._parent_tree = None
        curr = parent
        while curr._parent_tree is not None:
            curr = curr._parent_tree
        curr.update_data_sizes()
        return True

    def expand(self) -> None:
        """Set this node to be expanded.
        Does nothing if this node has no subtrees (is a leaf).
        """
        if self._subtrees:
            self._expanded = True

    def expand_all(self) -> None:
        """Recursively expand this node and all of its subtrees.
        """
        if self._subtrees:
            self._expanded = True
            for subtree in self._subtrees:
                subtree.expand_all()

    def collapse(self) -> None:
        """Unexpand this node's parent.
        If this node is the root, do nothing.
        """
        if self._parent_tree:
            self._parent_tree._expanded = False

    def collapse_all(self) -> None:
        """Recursively unexpand this node and all of its subtrees.
        """
        self._expanded = False
        for subtree in self._subtrees:
            subtree.collapse_all()

    # Methods for the string representation
    def get_path_string(self) -> str:
        """
        Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_path_string() + \
                self.get_separator() + self._name

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        name = os.path.basename(path)
        if not os.path.isdir(path):  # if path represents a file
            file_size = os.path.getsize(path)
            super().__init__(name, [], file_size)
        else:
            subtrees = []
            for item in os.listdir(path):  # if path represents a folder
                if not item.startswith('.'):
                    item_path = os.path.join(path, item)
                    subtrees.append(FileSystemTree(item_path))
            super().__init__(name, subtrees)

        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
