# The Intelligent CPU Scheduler Simulator

A highly polished, advanced CPU scheduling simulation tool built with Python, CustomTkinter, and Matplotlib. It features real-time dynamic visualization with a smart statistical heuristic for predicting optimal algorithms, and includes a large-sample testing module for stochastic performance evaluation.

## Overview
This simulator extends traditional operating system concept demonstrations by introducing a clean, modern UI and a heuristic engine that evaluates workload characteristics to suggest optimal scheduling strategies.

### Implemented Algorithms:
1. **First Come First Serve (FCFS)** - Non-preemptive
2. **Shortest Job First (SJF)** - Non-preemptive
3. **Shortest Remaining Time First (SRTF)** - Preemptive
4. **Round Robin (RR)** - Preemptive
5. **Priority Scheduling (NP)** - Non-preemptive
6. **Priority Scheduling (P)** - Preemptive

## Features
- **Modern Dark-Mode UI**: Built with `customtkinter` for a vastly improved user experience.
- **Advanced Visualizations**: Embeds Matplotlib dynamically to render crisp Gantt charts and performance metrics graphs.
- **Smart Heuristic Engine**: Analyzes variance in burst times, priorities, and arrivals to predict the most efficient algorithm without brute-force simulation.
- **Stochastic Data Generation**: Easily generate thousands of random datasets for large-scale analysis.
- **Performance Metrics**: Computes Waiting Time, Turnaround Time, and Response Time.

## Project Structure
```
The-Intelligent-CPU-Scheduler-Simulator/
├── src/
│   ├── algorithms.py          # Scheduling algorithms (FCFS, SJF, SRTF, RR, Priority)
│   ├── gui.py                 # Modern CustomTkinter implementation
│   ├── visualization.py       # Matplotlib visualization components
│   ├── main.py                # Application Entry Point
│   └── suggest_algorithm.py   # Smart Statistical Heuristics
├── tests/
│   ├── datagen.py             # Stochastic data generator
│   └── LargeSampleGraph.py    # Large Data Evaluator
├── docs/
│   ├── requirements.txt       # Dependencies
│   └── README.md              # This documentation
```

## How to Run

### Prerequisites
- Python 3.8+

### Installation
1. Install dependencies:
   ```bash
   pip install -r docs/requirements.txt
   ```
2. Run the simulator:
   ```bash
   python src/main.py
   ```

### Usage
- Enter Process Details (Arrival, Burst, Priority) and click **Add Process**.
- Alternatively, use **Generate Random Data** for an instant 8-process workload.
- Use **Suggest Algorithm** to test the smart heuristic.
- Select your desired algorithm from the dropdown and hit **Run Simulation**.
- Review the dynamically rendered Gantt chart and metrics comparison bar chart!
