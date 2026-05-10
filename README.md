# Swap Puzzle Solver

A Python project developed at ENSAE focused on solving a grid-based swap puzzle using graph search algorithms and artificial intelligence techniques.

The goal of the project is to transform an initial grid into a target configuration by swapping adjacent tiles while minimizing the number of moves. To solve the puzzle efficiently, the project implements the A* (A-star) search algorithm, a classical pathfinding and optimization method widely used in artificial intelligence.

Because apparently humans looked at combinatorial explosion and thought: “this seems like a fun semester project.”


---

Project Objectives

This project aims to:

model a grid-based puzzle as a graph problem;

implement tile swapping mechanics;

design and analyze search algorithms;

solve the puzzle using the A* algorithm;

evaluate heuristic performance and complexity;

apply software engineering best practices.



---

Puzzle Description

The puzzle consists of a grid containing numbered tiles.

A valid move swaps two adjacent cells. The objective is to transform the initial configuration into the target sorted configuration using the minimum number of swaps.

Example

Initial grid:

1 3 2
4 5 6
7 8 9

Target grid:

1 2 3
4 5 6
7 8 9


---

A* Search Algorithm

The main solving strategy relies on the A* search algorithm.

The algorithm combines:

the current path cost;

a heuristic estimating the remaining distance to the goal.


Typical heuristics include:

Manhattan distance;

misplaced tiles count;

custom grid evaluation metrics.


This allows the solver to efficiently explore the search space while avoiding brute-force enumeration of every possible state. Which is fortunate, because entropy already has enough victories.


