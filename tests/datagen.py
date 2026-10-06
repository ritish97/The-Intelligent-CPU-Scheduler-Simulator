import os
import sys
import random
import pandas as pd

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from algorithms import Process

def generate_sample_data(num_processes=100, arrival_range=(0, 50), burst_range=(1, 20), priority_range=(1, 10), seed=None):
    """
    Generates a list of stochastic Process objects for testing.
    """
    if seed is not None:
        random.seed(seed)
        
    processes = []
    for i in range(1, num_processes + 1):
        pid = f"P{i}"
        
        # Exponential arrival is more realistic for queueing, but uniform is easier to understand.
        # Let's use uniform for simplicity, with some clustering.
        arrival_time = random.randint(arrival_range[0], arrival_range[1])
        
        # Burst time can be a mix of CPU bound (long) and IO bound (short)
        if random.random() < 0.7:
            # 70% IO bound (short burst)
            burst_time = random.randint(burst_range[0], max(1, burst_range[1] // 3))
        else:
            # 30% CPU bound (long burst)
            burst_time = random.randint(max(1, burst_range[1] // 3), burst_range[1])
            
        priority = random.randint(priority_range[0], priority_range[1])
        
        processes.append(Process(pid, arrival_time, burst_time, priority))
        
    return processes

def generate_csv_dataset(filename, num_samples=1000, max_procs_per_sample=10):
    """
    Generates a large dataset of workloads (samples) for potential ML training.
    """
    data = []
    
    for sample_id in range(num_samples):
        num_processes = random.randint(3, max_procs_per_sample)
        procs = generate_sample_data(num_processes)
        
        # We can extract features
        burst_times = [p.burst_time for p in procs]
        arrival_times = [p.arrival_time for p in procs]
        
        # Very simple stats
        data.append({
            "sample_id": sample_id,
            "num_processes": num_processes,
            "avg_burst": sum(burst_times) / num_processes,
            "max_burst": max(burst_times),
            "min_burst": min(burst_times),
            "avg_arrival": sum(arrival_times) / num_processes
        })
        
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Generated dataset with {num_samples} samples at {filename}")

if __name__ == "__main__":
    # Test generation
    procs = generate_sample_data(5)
    print("Sample generated processes:")
    for p in procs:
        print(f"{p.pid}: Arr={p.arrival_time}, Burst={p.burst_time}, Prio={p.priority}")
