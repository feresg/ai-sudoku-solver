Sudoku Solver
=============

### An app that can solve any sudoku puzzle using DFS and Best First Search.

![Screenshot](https://github.com/feresg/ai-sudoku-solver/raw/master/Screenshot.png)

this sudoku solver uses:

* Depth First Search (DFS): Blind method.
* Best First Search (BestFS): Informed method that uses the Minimum Remaining Values (MRV) heuristic

Environment
-----------

This application is built using `Python` and and the `TkInter` library for GUI
development.

*sudoku.py* contains Problem, Node and Solver classes for solving the problem and *sudoku_gui.py* contains the GUI class.

Execution
---------

In your *Terminal*, simply run:

```
$ python3 sudoku_gui.py
```
