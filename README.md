# Treemap Hierarchical Data Visualization System

An interactive Python application that turns hierarchical data into nested, area-proportional rectangles. Explore disk usage in a directory or the citation distribution of computer science education research papers through a Pygame interface.

The same recursive tree model powers both data sources, demonstrating inheritance, polymorphism, recursive layout algorithms, and event-driven interaction.

## Features

- **File system visualisation:** recursively load files and folders, with rectangle areas based on file sizes in bytes.
- **Research paper visualisation:** load the included CSV and organise papers by year and nested research category, with areas based on citation counts.
- **Interactive exploration:** select nodes, inspect their paths, expand or collapse branches, and focus on a subtree.
- **Editable visual model:** change leaf sizes, move leaves between branches, and remove nodes from the displayed hierarchy.
- **Resizable display:** recalculate the treemap layout when the window size changes.

Edits affect the in-memory tree only. Moving, resizing, or deleting a node does not modify the original files or write changes back to the CSV.

## Getting started

Use Python 3.10 or newer and a desktop environment capable of opening a Pygame window.

```bash
git clone https://github.com/LucasWHJ/Treemap-Hierarchical-Data-Visualization-System.git
cd Treemap-Hierarchical-Data-Visualization-System
python -m pip install pygame
python treemap_visualiser.py
```

By default, the application visualises the current working directory. Click the root rectangle and press **E** to reveal its immediate children, or **A** to expand the full hierarchy.

### Visualise a specific directory

Set `PATH_TO_VISUALISE` at the bottom of `treemap_visualiser.py`:

```python
PATH_TO_VISUALISE = "/path/to/your/folder"
```

Then run `python treemap_visualiser.py` again. Use a valid, readable path. The file system loader skips entries whose names begin with a dot.

You can also launch a visualisation directly from Python:

```python
from tm_trees import FileSystemTree
from treemap_visualiser import Visualiser

Visualiser().run_visualisation(FileSystemTree("/path/to/your/folder"))
```

### Explore research papers

Run this example from the repository root so the loader can find `cs1_papers.csv`:

```python
from papers import PaperTree
from treemap_visualiser import Visualiser

tree = PaperTree("CS1", [], all_papers=True, by_year=True)
Visualiser().run_visualisation(tree)
```

Set `by_year=False` to group directly by category instead of adding a year level. Paper rectangles are weighted by citations, so papers with zero citations have no visible area.

Alternatively, in the script's `__main__` block, comment out `run_treemap_file_system(...)` and uncomment `run_treemap_papers()`.

## Controls

Click a displayed rectangle to select it; click it again to clear the selection. The bottom bar shows the selected node's path and descriptor.

| Input | Action |
| --- | --- |
| **E** | Expand the selected branch one level. |
| **A** | Expand the selected branch and all descendants. |
| **C** | Collapse the selected node's parent. |
| **X** | Collapse the hierarchy rooted at the current view's root. |
| **Q** | Focus the view on the selected subtree. |
| **B** | Return to the previous view saved by Q. |
| **↑ / ↓** | Increase or decrease the selected leaf's size by approximately 1%, with integer rounding. |
| **M** | Move the selected leaf into the branch under the pointer. |
| **Delete** | Remove the selected node from the visual model, provided it has a parent. |
| **Backspace on macOS** | Alternative to Delete. |
| Resize window | Recalculate the treemap dimensions. |

Most keyboard actions require a selection. For **M**, hover over a destination that contains children; empty folders do not qualify as destinations in the current implementation.

## How it works

1. **Build the hierarchy.** `FileSystemTree` loads a directory recursively; `PaperTree` parses the paper CSV into nested categories.
2. **Aggregate sizes.** Internal nodes store the sum of their descendants' leaf sizes.
3. **Partition rectangles.** `TMTree.update_rectangles()` splits the available rectangle along its longer dimension, assigning space in proportion to child sizes. The last child receives the remaining pixels to account for rounding.
4. **Render the displayed tree.** Expanded nodes reveal their children; collapsed branches appear as a single rectangle. Nodes with zero data size are omitted from rendering.
5. **Handle interaction.** The visualiser responds to mouse and keyboard events and updates the tree and layout.

Colours are randomly assigned to nodes. They distinguish regions; they do not encode file type, year, or citation count.

## Data format

`papers.py` reads `cs1_papers.csv` using these columns:

| Column | Use |
| --- | --- |
| `Author` | Paper authors. |
| `Title` | Leaf node name. |
| `Year` | Optional first hierarchy level. |
| `Category` | Nested category path, separated by `:`. |
| `Url` | Paper URL stored in the node's DOI field. |
| `Citations` | Integer leaf weight. |

The source module identifies the included data as adapted from a dataset presented at SIGCSE 2019. See the [dataset reference](https://www.brettbecker.com/sigcse2019/) for its background.

## Project structure

```text
.
├── tm_trees.py            # Recursive tree model and file system subclass
├── papers.py              # CSV parsing and paper tree subclass
├── treemap_visualiser.py  # Pygame rendering, navigation, and event handling
├── cs1_papers.csv         # Included research paper data
├── print_dirs.py          # Directory-printing helper
├── my_tests.py            # Layout and expansion tests
└── sample_test.py         # Original sample tests requiring external fixtures
```

## Tests

Run the self-contained layout tests:

```bash
python -m pip install pytest
python -m pytest my_tests.py -v
```

`sample_test.py` additionally requires `hypothesis` and an `example-directory/workshop` fixture that is not included in this repository. Some sample expectations describe an earlier implementation stage, so this file needs fixture setup and review before use with the interactive tree behaviour.

The optional `python_ta` checks at the bottom of the model modules are for static analysis and are not required to launch the visualiser.
