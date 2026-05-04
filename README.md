# Simulated Annealing – 8 Puzzle Solver

## 📌 Project Overview

This project implements the Simulated Annealing algorithm to solve the classic 8-puzzle problem. The algorithm is inspired by the annealing process in physics, where a system starts with high randomness and gradually becomes stable to reach the best possible solution .

The 8-puzzle is a 3×3 grid with numbers from 1 to 8 and one empty space. The objective is to arrange the tiles in the correct order by making valid moves.

## 🧠 Algorithm Idea

Simulated Annealing works by exploring different states of the puzzle:

Starts with a random state
Moves to a new state by shifting tiles
Accepts better solutions always
Sometimes accepts worse solutions to avoid local traps
Gradually reduces randomness (cooling process)

This helps the algorithm find a global optimal solution instead of getting stuck.

## ⚙️ Features
🎮 Interactive 8-puzzle game
🤖 Auto-solve using Simulated Annealing
⏱️ Timer and move counter
🎨 Multiple themes (Neon, Ice, Golden)
🔀 Shuffle and reset options
🖥️ Simple GUI using Tkinter

## 🛠️ Technologies Used
Python
Tkinter (for GUI)

## ▶️ How to Run
Install Python
Download or clone this repository
Run the project:
python puzzle.py

## 📊 Performance Analysis

The algorithm was tested on different puzzle difficulties:

Difficulty	Moves	Time
Easy	10–15	~120 ms
Medium	25–40	~350 ms
Hard	50+	~800 ms

As complexity increases, time also increases, but the algorithm consistently finds a solution .

## 📈 Complexity

Best Case: O(1)
Average Case: O(N)
Worst Case: O(k × L)
Space Complexity: O(L)

## 🌍 Real-World Applications

Route planning (delivery systems)
Scheduling problems
Circuit and chip design optimization
Russell & Norvig – Artificial Intelligence: A Modern Approach
Python Tkinter Documentation
👨‍💻 Author
