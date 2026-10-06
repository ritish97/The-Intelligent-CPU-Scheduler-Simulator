import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from suggest_algorithm import exact_best_algorithm, suggest_algorithm
from datagen import generate_sample_data

def evaluate_heuristic(num_samples=100):
    print(f"Evaluating heuristic accuracy over {num_samples} samples...")
    matches = 0
    results = []

    for i in range(num_samples):
        # Generate random processes (3 to 15 processes)
        import random
        procs = generate_sample_data(num_processes=random.randint(3, 15))
        
        # What does the exact simulation say is best?
        exact_best, _ = exact_best_algorithm(procs)
        
        # What does our statistical heuristic say?
        heuristic_guess = suggest_algorithm(procs, check_priorities=False) 
        
        # Since we use 'SJF (Non-Preemptive)' vs 'SJF (Non-Preemptive)', we need to match strings
        match = exact_best == heuristic_guess
        if match:
            matches += 1
            
        results.append({
            "Sample": i,
            "Exact": exact_best,
            "Heuristic": heuristic_guess,
            "Match": match
        })
        
    accuracy = (matches / num_samples) * 100
    print(f"Heuristic Accuracy: {accuracy:.2f}%")
    return results

if __name__ == "__main__":
    results = evaluate_heuristic(200)
    
    df = pd.DataFrame(results)
    
    # Plot accuracy distribution
    match_counts = df['Match'].value_counts()
    
    plt.figure(figsize=(6,6))
    plt.pie(match_counts, labels=["Matched", "Mismatched"], autopct='%1.1f%%', colors=["#2FA572", "#C8504B"])
    plt.title("Statistical Heuristic Accuracy")
    
    if not os.path.exists("test_reports"):
        os.makedirs("test_reports")
    plt.savefig("test_reports/accuracy_pie.png")
    print("Saved accuracy chart to test_reports/accuracy_pie.png")
    
