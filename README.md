# Travelling Salesperson Problem (TSP) AI Solver

This repository contains my submission for the **COMP2261 Artificial Intelligence** coursework (Academic Year 2025-26) at Durham University. The project focuses on solving the classic Travelling Salesperson Problem (TSP) by implementing and enhancing two distinct AI search algorithms in Python. 

##  Project Overview

The objective of this project was to implement two different search algorithms to find the shortest possible tours across 10 different city datasets. For each algorithm, both a "basic" (vanilla) version and an "enhanced" (optimized) version were developed. The project strictly avoids the use of non-standard Python modules.

### Implemented Algorithms

#### 1. Genetic Algorithm (GA)
* **Basic Implementation:** Follows a standard evolutionary approach to find the optimal tour.
* **Enhanced Implementation (`AlgAenhanced.py`):**
    * **Nearest Neighbour Seeding:** Seeds 10% of the initial population using a nearest neighbour heuristic to provide a strong starting point, while the remaining 90% is randomized to maintain diversity.
    * **2-opt Mutation Operator:** Replaces standard random swaps with a local improvement step. When a child mutates, up to 10 random 2-opt moves are attempted, applying only those that improve the tour.
    * **Inversion Mutation:** 30% of mutations reverse a random segment of the tour, adding structural variation to escape local optima.
    * *Reference:* Goldberg, D.E. (1989) Genetic Algorithms in Search, Optimization, and Machine Learning.

#### 2. Ant Colony Optimization (AC)
* **Basic Implementation:** A probabilistic technique simulating the foraging behavior of ants to construct tours.
* **Enhanced Implementation (`AlgBenhanced.py`):**
    * **Nearest Neighbour Initialisation & Pheromone Scaling:** Uses a nearest neighbour (NN) tour to set the initial pheromone level relative to problem size, and sets the NN tour as the initial best solution.
    * **Limited 2-opt Per Iteration:** Applies up to 5 improving 2-opt moves to the iteration's best tour before updating pheromones, allowing the colony to learn from locally optimized solutions.
    * **Reinforcement Based on Improved Best Tours:** Pheromone updates are strengthened by the locally improved solutions rather than raw ant tours.
    * *Reference:* Dorigo, M. and Stutzle, T. (2004) Ant Colony Optimization.

##  Repository Structure

* `AlgAbasic.py` & `AlgAenhanced.py`: Basic and enhanced implementations of the Genetic Algorithm.
* `AlgBbasic.py` & `AlgBenhanced.py`: Basic and enhanced implementations of the Ant Colony Optimization algorithm.
* `RunParallel.py`: A custom Python script utilizing the `multiprocessing` module to run all algorithm variants continuously across all city files. It automatically tracks, saves, and formats the best (shortest) tours discovered.
* `Skeleton.py`: The foundational university-provided template handling distance matrix generation and secure tour-file formatting.
* `alg_codes_and_tariffs.txt`: Configuration file outlining the approved algorithms and their associated difficulty tariffs.
* `*.txt` (Tour Files): 20 output files detailing the optimal routes discovered by the algorithms for 10 distinct city maps.
* `AISearchProforma.pdf`: A detailed document explaining algorithm enhancements.

##  Execution

**Generate Tours (Parallel Runner)**
To run the algorithms across all city datasets for a specified duration and automatically save the shortest tours, execute:
```bash
python RunParallel.py
