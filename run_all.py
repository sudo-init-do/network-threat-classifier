import os
import sys
import subprocess
from datetime import datetime

# Create results folder
os.makedirs('results', exist_ok=True)

print(f"Running CYB 213 Tasks - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def run_task(script_path, output_file, description, timeout=300):
    """Run a script in batch mode with timeout and output redirection."""
    print(f"=== {description} ===")
    try:
        with open(output_file, 'w') as f:
            # Use sys.executable to ensure we use the same python interpreter (venv)
            result = subprocess.run([sys.executable, script_path, '--batch'], stdout=f, stderr=subprocess.STDOUT, cwd=os.getcwd(), timeout=timeout)
        if result.returncode == 0:
            print(f"{description} complete. Output saved to {output_file}")
            # Preview last 5 lines
            with open(output_file, 'r') as f:
                lines = f.readlines()
                print("Preview (last 5 lines):")
                for line in lines[-5:]:
                    print(line.strip())
        else:
            print(f"Warning: {description} exited with code {result.returncode}. Check {output_file}.")
    except subprocess.TimeoutExpired:
        print(f"Timeout: {description} took >{timeout}s.")
    except FileNotFoundError:
        print(f"Error: {script_path} not found.")
    except Exception as e:
        print(f"Error: {e}")
    print()  # Newline

# Task 1
run_task('src/network_threat_classifier.py', 'results/task1_output.txt', 'Task 1: Basic Network Threat Classifier')

# Task 2
run_task('task2/src/firewall_threat_finder.py', 'results/task2_output.txt', 'Task 2: Firewall Log Threat Pattern Finder')

print("All tasks done! Check results/ for outputs. Plots have been displayed and saved as PNGs.")