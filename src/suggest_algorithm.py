import numpy as np

def analyze_workload(processes):
    if not processes:
        return {}
        
    burst_times = [p.burst_time for p in processes]
    arrival_times = [p.arrival_time for p in processes]
    priorities = [p.priority for p in processes]
    
    return {
        "burst_mean": np.mean(burst_times),
        "burst_std": np.std(burst_times),
        "arrival_mean": np.mean(arrival_times),
        "arrival_std": np.std(arrival_times),
        "priority_var": np.var(priorities)
    }

def suggest_algorithm(processes, check_priorities=True):
    """
    Recommends a CPU scheduling algorithm based on the statistical 
    characteristics of the process workload.
    """
    if not processes:
        return "None"
        
    stats = analyze_workload(processes)
    
    burst_mean = stats["burst_mean"]
    burst_std = stats["burst_std"]
    arrival_std = stats["arrival_std"]
    priority_var = stats["priority_var"]
    
    # 1. Check if user explicitly provided varied priorities
    if check_priorities and priority_var > 0:
        if arrival_std > 0:
            return "Priority (Preemptive)"
        else:
            return "Priority (Non-Preemptive)"
            
    # 2. Check for Convoy Effect vulnerability
    # High standard deviation in burst times means we have a mix of long and short jobs.
    # FCFS would suffer here if a long job arrives early.
    if burst_std > burst_mean * 0.4: 
        if arrival_std > 0:
            return "SRTF (Preemptive)" # Preempt long jobs for newly arrived short jobs
        else:
            return "SJF (Non-Preemptive)" # All arrive roughly together, just sort by burst
            
    # 3. Check for uniform workload (Time-sharing)
    # If burst times are relatively uniform, Round Robin provides fair responsiveness.
    if burst_std < burst_mean * 0.2:
        return "Round Robin (RR)"
        
    # 4. Default for moderate variance with steady arrivals
    return "FCFS (First Come First Serve)"
    
def exact_best_algorithm(processes):
    """
    Brute-force approach: run all algorithms and find the one 
    with the lowest average waiting time. Useful for verifying the heuristic.
    """
    import copy
    from algorithms import fcfs, sjf, srtf, rr, priority_np, priority_p
    
    # We must deepcopy so we don't pollute the original objects
    results = {}
    
    algos = {
        "FCFS": fcfs,
        "SJF (Non-Preemptive)": sjf,
        "SRTF (Preemptive)": srtf,
        "Round Robin (RR)": lambda p: rr(p, quantum=4),
        "Priority (Non-Preemptive)": priority_np,
        "Priority (Preemptive)": priority_p
    }
    
    for name, func in algos.items():
        # Copy the processes for simulation
        sim_procs = copy.deepcopy(processes)
        _, completed_procs = func(sim_procs)
        avg_wt = sum(p.waiting_time for p in completed_procs) / len(completed_procs)
        results[name] = avg_wt
        
    # Return the one with minimum average waiting time
    best_algo = min(results, key=results.get)
    return best_algo, results
