import subprocess
import sys
import os

# Define the file that will be processed.
LEADS_FILE = "leads.xlsx"

def run_step(script_name, *args):
    """Runs a python script as a subprocess and checks for errors."""
    print(f"\n--- Running: {script_name} ---")
    command = [sys.executable, script_name] + list(args)
    
    # The `check=True` argument will raise a CalledProcessError if the script returns a non-zero exit code.
    try:
        # Using capture_output to prevent scripts from printing their own output,
        # making the pipeline's output cleaner. We will print it if an error occurs.
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout) # Print the script's output on success
        print(f"--- Finished: {script_name} ---")
        return True
    except FileNotFoundError:
        print(f"Error: Script '{script_name}' not found.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}.")
        print(f"Return code: {e.returncode}")
        print("\n--- STDOUT ---")
        print(e.stdout)
        print("\n--- STDERR ---")
        print(e.stderr)
        return False

def main():
    """
    Main function to orchestrate the lead processing pipeline.
    """
    print("--- Starting Lead Processing Pipeline ---")

    # Check if the leads file exists before starting.
    if not os.path.exists(LEADS_FILE):
        print(f"\nError: The input file '{LEADS_FILE}' was not found.")
        print("Please make sure your leads are in 'leads.xlsx' before starting the pipeline.")
        return

    # Step 1: Analyze websites and get technologies.
    if not run_step("analyze_websites.py", "--file", LEADS_FILE):
        print("\nPipeline stopped due to an error in the website analysis step.")
        return

    # Step 2: Inspect the technologies found.
    if not run_step("inspect_file.py", "--file", LEADS_FILE):
        print("\nPipeline stopped due to an error in the technology inspection step.")
        return

    # Step 3: Add the 'Call Lead' priority column.
    if not run_step("add_call_lead_column.py", "--file", LEADS_FILE):
        print("\nPipeline stopped due to an error in the priority analysis step.")
        return

    print("\n--- Lead Processing Pipeline Finished Successfully! ---")
    print(f"The file '{LEADS_FILE}' has been fully updated.")

if __name__ == "__main__":
    main()
