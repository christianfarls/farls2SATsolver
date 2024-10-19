"""
2-SAT SOLVER
Theory of Computing
Christian Farls
10/18/24
"""

import time

def parse_2sat_file(file):
    """Parses the entire 2-SAT input file and splits it into separate test cases."""
    with open(file, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    tests = []
    current_clauses = []
    for line in lines:
        if line.startswith("c"):  # New test case starts
            if current_clauses:
                tests.append(current_clauses)
            current_clauses = []  # Reset for the new test case
        elif not line.startswith("p"):  # Ignore 'p' lines, they only contain metadata
            clause = [int(lit) for lit in line.split(",") if lit.strip() and lit.strip() != "0"]
            if len(clause) == 2:  # Only accept valid 2-literal clauses
                current_clauses.append(clause)

    # Append the last collected clauses as a test
    if current_clauses:
        tests.append(current_clauses)

    return tests


def unit_propagation(clauses, assignment):
    """Perform unit propagation on the given clauses and assignment."""
    while True:
        unit_clause_found = False
        for clause in clauses:
            if len(clause) == 1:
                unit_clause_found = True
                literal = clause[0]
                assignment[abs(literal)] = literal > 0
                clauses = [c for c in clauses if literal not in c]
                clauses = [[l for l in c if l != -literal] for c in clauses]
        if not unit_clause_found:
            break
    return clauses, assignment

def dpll_2sat(clauses):
    """Solve the 2SAT problem using the DPLL algorithm."""
    assignment = {}

    def dpll(clauses, assignment):
        clauses, assignment = unit_propagation(clauses, assignment)

        if not clauses:
            return True, assignment

        if any(not clause for clause in clauses):
            return False, {}

        literal = next(iter(clauses[0]))
        return (dpll(clauses + [[literal]], assignment.copy()) or
                dpll(clauses + [[-literal]], assignment.copy()))

    return dpll(clauses, assignment)

def run_test(file, output_csv_path, output_txt_path):
    """Run the 2-SAT solver on multiple tests and record timings."""
    tests = parse_2sat_file(file)  # Parse all tests from the input file

    # Write headers for the CSV output
    with open(output_csv_path, "w") as f:
        f.write("Test ID,Problem Size,Execution Time (s),Result\n")

    # Prepare txt file for detailed results
    with open(output_txt_path, "w") as f_txt:
        f_txt.write("Results for 2-SAT Tests\n")
        f_txt.write("=" * 40 + "\n")

    for i, clauses in enumerate(tests):
        start_time = time.time()  # Start timing
        is_sat, assignment = dpll_2sat(clauses)
        end_time = time.time()  # End timing

        # Calculate elapsed time
        execution_time = end_time - start_time
        result = "Yes" if is_sat else "No"

        # Log the results in CSV
        with open(output_csv_path, "a") as f_csv:
            f_csv.write(f"{i+1},{len(clauses)},{execution_time},{result}\n")

        # Log detailed results in txt file
        with open(output_txt_path, "a") as f_txt:
            f_txt.write(f"Test {i+1}:\n")
            f_txt.write(f"Clauses ({len(clauses)}):\n")
            for clause in clauses:
                f_txt.write(f"  {clause}\n")
            f_txt.write(f"Execution Time: {execution_time:.6f}s\n")
            f_txt.write(f"Satisfiable: {result}\n")
            if is_sat:
                f_txt.write(f"Assignment: {assignment}\n")
            f_txt.write("-" * 40 + "\n")

        # Print to console
        print(f"Test {i+1}: Clauses: {len(clauses)}, Time: {execution_time:.6f}s, Satisfiable: {result}")

if __name__ == "__main__":
    input_file = "../data/2SAT.cnf.csv"  # Input file
    output_csv = "../output/timing_results_farls.csv"  # CSV output
    output_txt = "../output/output_farls.txt"  # TXT output for detailed results

    # Run the tests and log the results
    run_test(input_file, output_csv, output_txt)