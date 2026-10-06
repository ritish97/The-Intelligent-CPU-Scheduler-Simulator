import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import copy

from algorithms import Process, fcfs, sjf, srtf, rr, priority_np, priority_p
from visualization import plot_gantt_chart, plot_metrics
from suggest_algorithm import suggest_algorithm
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tests')))
from datagen import generate_sample_data

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SimulatorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Intelligent CPU Scheduler Simulator")
        self.geometry("1100x700")

        self.processes = []
        self.process_counter = 1

        self.setup_ui()

    def setup_ui(self):
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CPU Scheduler", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Inputs
        self.arrival_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Arrival Time")
        self.arrival_entry.grid(row=1, column=0, padx=20, pady=10)
        
        self.burst_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Burst Time")
        self.burst_entry.grid(row=2, column=0, padx=20, pady=10)

        self.priority_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Priority (opt)")
        self.priority_entry.grid(row=3, column=0, padx=20, pady=10)

        self.add_btn = ctk.CTkButton(self.sidebar_frame, text="Add Process", command=self.add_process)
        self.add_btn.grid(row=4, column=0, padx=20, pady=10)

        self.gen_btn = ctk.CTkButton(self.sidebar_frame, text="Generate Random Data", command=self.generate_data, fg_color="gray")
        self.gen_btn.grid(row=5, column=0, padx=20, pady=10)
        
        self.clear_btn = ctk.CTkButton(self.sidebar_frame, text="Clear Processes", command=self.clear_processes, fg_color="#C8504B", hover_color="#8E3531")
        self.clear_btn.grid(row=6, column=0, padx=20, pady=10)

        self.algo_label = ctk.CTkLabel(self.sidebar_frame, text="Select Algorithm:")
        self.algo_label.grid(row=7, column=0, padx=20, pady=(20, 0), sticky="sw")
        
        self.algo_var = ctk.StringVar(value="FCFS")
        self.algo_dropdown = ctk.CTkOptionMenu(self.sidebar_frame, variable=self.algo_var, 
                                               values=["FCFS", "SJF", "SRTF", "Round Robin", "Priority (NP)", "Priority (P)"])
        self.algo_dropdown.grid(row=8, column=0, padx=20, pady=10, sticky="nw")
        
        self.quantum_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Quantum (RR only)")
        self.quantum_entry.grid(row=9, column=0, padx=20, pady=5, sticky="nw")

        self.suggest_btn = ctk.CTkButton(self.sidebar_frame, text="Suggest Algorithm", command=self.suggest_algo, fg_color="#2FA572", hover_color="#106A43")
        self.suggest_btn.grid(row=10, column=0, padx=20, pady=10)

        self.run_btn = ctk.CTkButton(self.sidebar_frame, text="Run Simulation", command=self.run_simulation, height=40, font=ctk.CTkFont(weight="bold"))
        self.run_btn.grid(row=11, column=0, padx=20, pady=20)

        # --- Main Frame (Plots & Text) ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=2)
        self.main_frame.grid_rowconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Matplotlib Setup
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax_gantt = self.fig.add_subplot(211)
        self.ax_metrics = self.fig.add_subplot(212)
        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=0, rowspan=2, column=0, sticky="nsew", padx=10, pady=10)
        
        # Text Output
        self.output_textbox = ctk.CTkTextbox(self.main_frame, height=100)
        self.output_textbox.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.output_textbox.insert("0.0", "Welcome to Intelligent CPU Scheduler Simulator.\nAdd processes to begin.")

    def add_process(self):
        try:
            arr = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            prio = self.priority_entry.get()
            prio = int(prio) if prio else 0
            
            pid = f"P{self.process_counter}"
            self.processes.append(Process(pid, arr, burst, prio))
            self.process_counter += 1
            
            self.log(f"Added {pid}: Arrival={arr}, Burst={burst}, Priority={prio}")
            
            self.arrival_entry.delete(0, 'end')
            self.burst_entry.delete(0, 'end')
            self.priority_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for time.")

    def generate_data(self):
        self.processes = generate_sample_data(num_processes=8)
        self.process_counter = 9
        self.log(f"Generated 8 random processes.")
        for p in self.processes:
            self.log(f"{p.pid}: Arr={p.arrival_time}, Burst={p.burst_time}, Prio={p.priority}")

    def clear_processes(self):
        self.processes.clear()
        self.process_counter = 1
        self.log("Processes cleared.")
        self.ax_gantt.clear()
        self.ax_metrics.clear()
        self.canvas.draw()

    def log(self, message):
        self.output_textbox.insert("end", "\n" + message)
        self.output_textbox.see("end")

    def suggest_algo(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Add processes first.")
            return
            
        suggestion = suggest_algorithm(self.processes)
        self.log(f"[HEURISTIC] Suggested Algorithm based on workload stats: {suggestion}")
        
    def run_simulation(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Add processes first.")
            return
            
        algo = self.algo_var.get()
        
        # Deepcopy processes to preserve originals for re-runs
        sim_procs = copy.deepcopy(self.processes)
        
        gantt = []
        try:
            if algo == "FCFS":
                gantt, sim_procs = fcfs(sim_procs)
            elif algo == "SJF":
                gantt, sim_procs = sjf(sim_procs)
            elif algo == "SRTF":
                gantt, sim_procs = srtf(sim_procs)
            elif algo == "Round Robin":
                q = self.quantum_entry.get()
                q = int(q) if q else 2
                gantt, sim_procs = rr(sim_procs, quantum=q)
            elif algo == "Priority (NP)":
                gantt, sim_procs = priority_np(sim_procs)
            elif algo == "Priority (P)":
                gantt, sim_procs = priority_p(sim_procs)
        except Exception as e:
            self.log(f"Error during simulation: {str(e)}")
            return
            
        # Draw plots
        plot_gantt_chart(gantt, self.ax_gantt)
        plot_metrics(sim_procs, self.ax_metrics)
        self.canvas.draw()
        
        # Calculate overall metrics
        avg_wt = sum(p.waiting_time for p in sim_procs) / len(sim_procs)
        avg_tat = sum(p.turnaround_time for p in sim_procs) / len(sim_procs)
        
        self.log(f"--- Results for {algo} ---")
        self.log(f"Average Waiting Time: {avg_wt:.2f}")
        self.log(f"Average Turnaround Time: {avg_tat:.2f}")

if __name__ == "__main__":
    app = SimulatorGUI()
    app.mainloop()
