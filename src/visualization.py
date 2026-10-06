import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def plot_gantt_chart(gantt_data, ax):
    """
    Plots a Gantt chart on the given matplotlib Axes.
    gantt_data: list of tuples (pid, start_time, end_time)
    """
    ax.clear()
    
    if not gantt_data:
        ax.text(0.5, 0.5, "No data to display", ha='center', va='center')
        ax.set_title("Gantt Chart")
        return

    # Assign colors to unique PIDs
    unique_pids = list(set([pid for pid, _, _ in gantt_data if pid != "Idle"]))
    try:
        colors = plt.colormaps.get_cmap("tab10").resampled(len(unique_pids))
    except AttributeError:
        # Fallback for older matplotlib versions
        colors = plt.cm.get_cmap("tab10", len(unique_pids))
    color_map = {pid: colors(i) for i, pid in enumerate(unique_pids)}
    color_map["Idle"] = "#cccccc" # Gray for idle time

    y_pos = 10
    height = 5
    
    max_end_time = 0
    for pid, start, end in gantt_data:
        duration = end - start
        ax.broken_barh([(start, duration)], (y_pos, height), facecolors=color_map[pid], edgecolor="black")
        
        # Add text label in the middle of the block
        ax.text(start + duration/2, y_pos + height/2, str(pid), ha='center', va='center', color='white' if pid != "Idle" else 'black', fontweight='bold', fontsize=9)
        max_end_time = max(max_end_time, end)

    ax.set_ylim(5, 20)
    ax.set_xlim(0, max_end_time + 1)
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title('Gantt Chart')
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)


def plot_metrics(processes, ax):
    """
    Plots a bar chart comparing Waiting Time and Turnaround Time for each process.
    """
    ax.clear()
    
    if not processes:
        ax.text(0.5, 0.5, "No data to display", ha='center', va='center')
        ax.set_title("Performance Metrics")
        return
        
    pids = [p.pid for p in processes]
    wts = [p.waiting_time for p in processes]
    tats = [p.turnaround_time for p in processes]
    
    x = np.arange(len(pids))
    width = 0.35
    
    ax.bar(x - width/2, wts, width, label='Waiting Time', color='#1f77b4')
    ax.bar(x + width/2, tats, width, label='Turnaround Time', color='#ff7f0e')
    
    ax.set_ylabel('Time')
    ax.set_title('Process Metrics')
    ax.set_xticks(x)
    ax.set_xticklabels(pids, rotation=45 if len(pids) > 10 else 0)
    ax.legend()
    
def plot_overall_comparison(results_dict, ax):
    """
    Plots a comparison of average waiting times across different algorithms.
    results_dict: { "Algorithm Name": avg_waiting_time }
    """
    ax.clear()
    if not results_dict:
        return
        
    algos = list(results_dict.keys())
    avg_wts = list(results_dict.values())
    
    bars = ax.bar(algos, avg_wts, color='coral')
    ax.set_ylabel('Average Waiting Time')
    ax.set_title('Algorithm Comparison')
    ax.set_xticklabels(algos, rotation=45, ha='right')
    
    # Add values on top of bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, round(yval, 2), ha='center', va='bottom', fontsize=9)
