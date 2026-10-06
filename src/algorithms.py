class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        
        # Computed during scheduling
        self.remaining_time = burst_time
        self.completion_time = 0
        self.start_time = -1 # First time getting CPU
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0

    def reset(self):
        self.remaining_time = self.burst_time
        self.completion_time = 0
        self.start_time = -1
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0


def _calculate_metrics(processes):
    for p in processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        p.response_time = p.start_time - p.arrival_time


def fcfs(processes):
    # First Come First Serve (Non-preemptive)
    for p in processes: p.reset()
    processes.sort(key=lambda x: (x.arrival_time, x.pid))
    
    current_time = 0
    gantt = []
    
    for p in processes:
        if current_time < p.arrival_time:
            # Idle time
            gantt.append(("Idle", current_time, p.arrival_time))
            current_time = p.arrival_time
        
        p.start_time = current_time
        start = current_time
        current_time += p.burst_time
        p.completion_time = current_time
        gantt.append((p.pid, start, current_time))
        
    _calculate_metrics(processes)
    return gantt, processes


def sjf(processes):
    # Shortest Job First (Non-preemptive)
    for p in processes: p.reset()
    
    current_time = 0
    completed = 0
    n = len(processes)
    gantt = []
    
    while completed < n:
        available = [p for p in processes if p.arrival_time <= current_time and p.completion_time == 0]
        
        if not available:
            next_arrival = min(p.arrival_time for p in processes if p.completion_time == 0)
            gantt.append(("Idle", current_time, next_arrival))
            current_time = next_arrival
            continue
            
        # Shortest burst time first
        available.sort(key=lambda x: (x.burst_time, x.arrival_time, x.pid))
        p = available[0]
        
        p.start_time = current_time
        start = current_time
        current_time += p.burst_time
        p.completion_time = current_time
        gantt.append((p.pid, start, current_time))
        completed += 1
        
    _calculate_metrics(processes)
    return gantt, processes


def srtf(processes):
    # Shortest Remaining Time First (Preemptive)
    for p in processes: p.reset()
    
    current_time = 0
    completed = 0
    n = len(processes)
    gantt = []
    current_pid = None
    block_start = 0
    
    while completed < n:
        available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if not available:
            if current_pid is not None:
                gantt.append((current_pid, block_start, current_time))
                current_pid = None
            next_arrival = min(p.arrival_time for p in processes if p.remaining_time > 0)
            if not gantt or gantt[-1][0] != "Idle":
                block_start = current_time
            current_pid = "Idle"
            current_time = next_arrival
            continue
            
        available.sort(key=lambda x: (x.remaining_time, x.arrival_time, x.pid))
        p = available[0]
        
        if current_pid != p.pid:
            if current_pid is not None:
                gantt.append((current_pid, block_start, current_time))
            block_start = current_time
            current_pid = p.pid
            
        if p.start_time == -1:
            p.start_time = current_time
            
        p.remaining_time -= 1
        current_time += 1
        
        if p.remaining_time == 0:
            p.completion_time = current_time
            completed += 1
            
    if current_pid is not None:
        gantt.append((current_pid, block_start, current_time))
        
    # Consolidate Gantt chart blocks
    consolidated_gantt = []
    for pid, start, end in gantt:
        if consolidated_gantt and consolidated_gantt[-1][0] == pid:
            consolidated_gantt[-1] = (pid, consolidated_gantt[-1][1], end)
        else:
            consolidated_gantt.append((pid, start, end))
            
    _calculate_metrics(processes)
    return consolidated_gantt, processes


def rr(processes, quantum=2):
    # Round Robin (Preemptive)
    for p in processes: p.reset()
    
    # Process sorting by arrival for initial queue
    sorted_processes = sorted(processes, key=lambda x: (x.arrival_time, x.pid))
    
    current_time = 0
    completed = 0
    n = len(processes)
    gantt = []
    queue = []
    
    i = 0
    while completed < n:
        # Enqueue newly arrived processes
        while i < n and sorted_processes[i].arrival_time <= current_time:
            queue.append(sorted_processes[i])
            i += 1
            
        if not queue:
            next_arrival = sorted_processes[i].arrival_time
            gantt.append(("Idle", current_time, next_arrival))
            current_time = next_arrival
            continue
            
        p = queue.pop(0)
        
        if p.start_time == -1:
            p.start_time = current_time
            
        execute_time = min(p.remaining_time, quantum)
        start = current_time
        current_time += execute_time
        p.remaining_time -= execute_time
        
        gantt.append((p.pid, start, current_time))
        
        # Enqueue processes that arrived while p was executing
        while i < n and sorted_processes[i].arrival_time <= current_time:
            queue.append(sorted_processes[i])
            i += 1
            
        if p.remaining_time > 0:
            queue.append(p)
        else:
            p.completion_time = current_time
            completed += 1
            
    _calculate_metrics(processes)
    
    # Consolidate Gantt
    consolidated_gantt = []
    for pid, start, end in gantt:
        if consolidated_gantt and consolidated_gantt[-1][0] == pid:
            consolidated_gantt[-1] = (pid, consolidated_gantt[-1][1], end)
        else:
            consolidated_gantt.append((pid, start, end))
            
    return consolidated_gantt, processes


def priority_np(processes):
    # Priority (Non-preemptive) - lower number = higher priority
    for p in processes: p.reset()
    
    current_time = 0
    completed = 0
    n = len(processes)
    gantt = []
    
    while completed < n:
        available = [p for p in processes if p.arrival_time <= current_time and p.completion_time == 0]
        
        if not available:
            next_arrival = min(p.arrival_time for p in processes if p.completion_time == 0)
            gantt.append(("Idle", current_time, next_arrival))
            current_time = next_arrival
            continue
            
        # Lower priority value means higher priority, tie break by arrival time
        available.sort(key=lambda x: (x.priority, x.arrival_time, x.pid))
        p = available[0]
        
        p.start_time = current_time
        start = current_time
        current_time += p.burst_time
        p.completion_time = current_time
        gantt.append((p.pid, start, current_time))
        completed += 1
        
    _calculate_metrics(processes)
    return gantt, processes


def priority_p(processes):
    # Priority (Preemptive) - lower number = higher priority
    for p in processes: p.reset()
    
    current_time = 0
    completed = 0
    n = len(processes)
    gantt = []
    current_pid = None
    block_start = 0
    
    while completed < n:
        available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if not available:
            if current_pid is not None:
                gantt.append((current_pid, block_start, current_time))
                current_pid = None
            next_arrival = min(p.arrival_time for p in processes if p.remaining_time > 0)
            if not gantt or gantt[-1][0] != "Idle":
                block_start = current_time
            current_pid = "Idle"
            current_time = next_arrival
            continue
            
        available.sort(key=lambda x: (x.priority, x.arrival_time, x.pid))
        p = available[0]
        
        if current_pid != p.pid:
            if current_pid is not None:
                gantt.append((current_pid, block_start, current_time))
            block_start = current_time
            current_pid = p.pid
            
        if p.start_time == -1:
            p.start_time = current_time
            
        p.remaining_time -= 1
        current_time += 1
        
        if p.remaining_time == 0:
            p.completion_time = current_time
            completed += 1
            
    if current_pid is not None:
        gantt.append((current_pid, block_start, current_time))
        
    # Consolidate Gantt
    consolidated_gantt = []
    for pid, start, end in gantt:
        if consolidated_gantt and consolidated_gantt[-1][0] == pid:
            consolidated_gantt[-1] = (pid, consolidated_gantt[-1][1], end)
        else:
            consolidated_gantt.append((pid, start, end))
            
    _calculate_metrics(processes)
    return consolidated_gantt, processes
