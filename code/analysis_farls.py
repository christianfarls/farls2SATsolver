"""
2-SAT SOLVER
Theory of Computing
Christian Farls
10/18/24
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the results from the CSV file
try:
    results = pd.read_csv("../output/timing_results_farls.csv")
except FileNotFoundError:
    print("Error: The results file could not be found. Please check the path.")
    exit(1)

# Check that the required columns exist
required_columns = {"Problem Size", "Execution Time (s)", "Result"}
if not required_columns.issubset(results.columns):
    print("Error: Missing required columns in the results file.")
    exit(1)

# Convert columns to appropriate data types if necessary
results["Problem Size"] = pd.to_numeric(results["Problem Size"], errors='coerce')
results["Execution Time (s)"] = pd.to_numeric(results["Execution Time (s)"], errors='coerce')

# Drop rows with invalid data
results = results.dropna()

# Separate the results based on satisfiability
yes_results = results[results["Result"] == "Yes"]
no_results = results[results["Result"] == "No"]

# Plot the results
plt.figure(figsize=(10, 6))
plt.scatter(yes_results["Problem Size"], yes_results["Execution Time (s)"],
            label="Satisfiable (Yes)", marker='o', alpha=0.7, edgecolor='black')
plt.scatter(no_results["Problem Size"], no_results["Execution Time (s)"],
            label="Unsatisfiable (No)", marker='x', alpha=0.7, edgecolor='black')

# Add labels, title, and legend
plt.xlabel("Problem Size (Number of Clauses)", fontsize=12)
plt.ylabel("Execution Time (seconds)", fontsize=12)
plt.title("2-SAT Solver Execution Time vs. Problem Size", fontsize=14)
plt.legend(title="Satisfiability", fontsize=10)

# Display the plot
plt.tight_layout()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
