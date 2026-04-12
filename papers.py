"""
=== Module Description ===
This module contains a new class, PaperTree, which is used to model data on
publications in a particular area of Computer Science Education research.
This data is adapted from a dataset presented at SIGCSE 2019.
You can find the full dataset here: https://www.brettbecker.com/sigcse2019/
"""
import csv
from tm_trees import TMTree

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    _authors:
        The authors of the paper.
    _doi:
        The doi of the paper.
    These should store information about this paper's <authors> and <doi>.

    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
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
    - All TMTree RIs are inherited.
    """
    _authors: str
    _doi: str

    def __init__(self, name: str, subtrees: list[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        """Initialize a new PaperTree with the given <name> and <subtrees>, 
        <authors> and <doi>, and with <citations> as the size of the data.

        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.

        If <all_papers> is False, Do NOT load new data.

        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """
        self._authors = authors
        self._doi = doi

        if all_papers:
            paper_dict = _load_papers_to_dict(by_year)
            loaded_subtrees = _build_tree_from_dict(paper_dict)
            super().__init__(name, loaded_subtrees)
        else:
            super().__init__(name, subtrees, citations)

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        return ': '

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        if len(self._subtrees) == 0:
            return ' (paper)'
        else:
            return ' (category)'


def _load_papers_to_dict(by_year: bool = True) -> tuple[dict, list]:
    """Return a nested dictionary of the data read from the papers dataset file.

    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """
    with open(DATA_FILE, newline='') as f:
        reader = csv.DictReader(f)
        return _build_nested_dict(reader, by_year)


def _build_nested_dict(reader: csv.DictReader,
                       by_year: bool) -> tuple[dict, list]:
    """Build and return the nested tuple-dictionary structure."""
    root = ({}, [])

    for row in reader:
        curr = root[0]
        categories = [c.strip() for c in row['Category'].split(':')]
        path = [row['Year']] + categories if by_year else categories

        for i in range(len(path)):
            level_name = path[i]
            if level_name not in curr:
                curr[level_name] = ({}, [])
            if i == len(path) - 1:
                curr[level_name][1].append(row)
            else:
                curr = curr[level_name][0]

    return root


def _build_tree_from_dict(nested_dict: dict) -> list[PaperTree]:
    """Return a list of trees from the nested dictionary <nested_dict>.
    """
    subtrees = []
    sub_categories_dict, papers_list = nested_dict

    for row in papers_list:
        paper_leaf = PaperTree(row['Title'], [], row['Author'],
                               row['Url'], int(row['Citations']), False, False)
        subtrees.append(paper_leaf)

    for category_name in sub_categories_dict:
        inner_subtrees = _build_tree_from_dict(
            sub_categories_dict[category_name])

        category_node = PaperTree(category_name, inner_subtrees,
                                  '', '', 0, False, False)
        subtrees.append(category_node)

    return subtrees


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
        'allowed-io': ['_load_papers_to_dict'],
        'max-args': 8
    })
