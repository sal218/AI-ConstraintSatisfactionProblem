# Canada Map Coloring CSP Solver

This project implements a **Constraint Satisfaction Problem (CSP)** to solve the map coloring problem for Canada's provinces and territories. The goal is to assign colors to each province/territory such that no two neighboring regions share the same color.

The program uses **Backtracking Search** and **Arc Consistency** to efficiently find a solution and includes a graphical user interface (GUI) built with Tkinter for user interaction.

---

## Features
- **Canada Map Representation**: A graph structure defines adjacency relationships between provinces and territories.
- **Constraint Enforcement**: Ensures neighboring provinces do not share the same color.
- **Backtracking Algorithm**: Uses recursive search with pruning (arc consistency).
- **GUI**: Allows users to input the number of colors and view results dynamically.

---

## How to Run the Program

### Prerequisites
- Python 3.x installed
- Tkinter library 

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/sal218/AI-ConstraintSatisfactionProblem.git

2. Run ```python csp.py```

### Link to my CSP video submission:

https://youtu.be/66LpkT6Dw90