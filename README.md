# Sheet-Wappalyzer

A Python toolset to analyze a list of websites from an Excel file, identify their underlying technologies, **and then intelligently prioritize leads based on those technologies**. This expanded toolset is ideal for market research, highly targeted lead generation, and competitive analysis, providing actionable insights directly in your Excel sheet.

This project uses `pandas` for data manipulation, `aiohttp` with `asyncio` for fast, concurrent website analysis, and a fork of `python-Wappalyzer` for technology detection. It now includes multiple scripts working in concert to provide a comprehensive and customizable workflow.

**Disclaimer:** This project was initially built to solve a specific personal problem. While it aims to be robust and functional, it is provided as-is. Feel free to adapt and use it for your own needs.

## Features

-   **Reads from Excel:** Processes `.xlsx` files directly.
-   **Enriches Data In-Place:** Adds "Technologies", "Status", and **"Priority"** columns to your original file.
-   **Fast & Concurrent:** Uses `asyncio` to analyze dozens of sites simultaneously.
-   **Intelligent Lead Prioritization:** Utilizes a customizable, scoring-based algorithm to assign "High", "Medium", or "Low" priority to leads based on detected technologies.
-   **Modular Workflow:** The process is broken down into modular Python scripts, orchestrated by a main pipeline script.
-   **Algorithm Development Tools:** Includes a dedicated script (`develop_algorithm.py`) to help you refine and "train" the prioritization algorithm on your own data.
-   **Robust:** Includes error handling for common issues.

## Installation

1.  **Clone the repository:**
    *(Assuming you have already initialized a Git repository as planned)*
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
    You will also need to clone the Wappalyzer submodule if you didn't clone this project recursively.
    ```bash
    git submodule update --init --recursive
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    The `python-Wappalyzer` from `chokepoint` must be installed from its local directory, followed by the other requirements.
    ```bash
    pip install ./python-Wappalyzer
    pip install -r requirements.txt
    ```

## Usage

This project now features a streamlined pipeline for analyzing websites and prioritizing leads.

### 1. Prepare your Excel File

-   Ensure your Excel file (e.g., `leads.xlsx`) is in the project directory.
-   It must contain a column with website URLs. The script will look for a column named `Website` by default.

### 2. Run the Full Analysis Pipeline

Use the `run_pipeline.py` script to execute all steps automatically: website analysis, technology inspection, and lead prioritization.

```bash
python3 run_pipeline.py [--file "path/to/your/leads.xlsx"] [--url_column "Company Website"] [--concurrency 50]
```

**Command-Line Arguments for `run_pipeline.py` (passed to `analyze_websites.py`):**

-   `--file`: Path to the input Excel file. **Default:** `leads.xlsx`.
-   `--url_column`: Name of the column containing website URLs. **Default:** `Website`.
-   `--concurrency`: Number of concurrent requests to make. **Default:** `25`.

### 3. Develop and Refine Your Prioritization Algorithm (Optional, but Recommended)

The heart of the intelligent lead prioritization is the `should_call_lead` function inside `add_call_lead_column.py`. To "train" and refine this algorithm for your specific needs, use `develop_algorithm.py`.

**Workflow:**

a.  **Generate Technology Data:** First, ensure `leads.xlsx` has the "Technologies" column by running `run_pipeline.py` at least once, or just `analyze_websites.py` if you only need the technology data.
b.  **Analyze and Test:** Run `develop_algorithm.py`. This script will:
    *   Read `leads.xlsx`.
    *   Output a summary of all unique technologies found to `technology.txt`.
    *   Apply the current prioritization algorithm (from its internal `should_call_lead` function).
    *   Print a statistical overview and samples of its decisions (e.g., High, Medium, Low Priority).
    *   **Important: `leads.xlsx` will NOT be modified by this script.** It provides output directly to your console and `technology.txt` for review.
    ```bash
    python3 develop_algorithm.py
    ```
c.  **Refine the Algorithm:** Open `develop_algorithm.py` and **manually edit the `should_call_lead` function** to adjust the scoring logic, add new rules, or change existing ones.
d.  **Repeat:** Go back to step (b) and re-run `develop_algorithm.py` to see the impact of your changes. Iterate until the algorithm provides the desired lead prioritization.

### 4. Update the Production Algorithm

Once you are satisfied with the `should_call_lead` function you developed in `develop_algorithm.py`, you need to transfer it to the production script.

a.  **Copy the Function:** Manually copy the entire `should_call_lead` function from `develop_algorithm.py`.
b.  **Paste into `add_call_lead_column.py`:** Open `add_call_lead_column.py` and replace its `should_call_lead` function with your perfected version.

Your `run_pipeline.py` will now use your refined algorithm for future lead prioritization.

## Core Scripts

-   `analyze_websites.py`: Asynchronously fetches website technologies using `python-Wappalyzer`.
-   `inspect_file.py`: (Primarily used internally by `run_pipeline.py` or for quick manual inspection) Reads `leads.xlsx` and provides a summary of detected technologies.
-   `add_call_lead_column.py`: Applies the intelligent prioritization algorithm to the "Technologies" column and adds a "Priority" column. This is the script whose `should_call_lead` function you will refine.
-   `develop_algorithm.py`: A utility script for iteratively developing and testing the `should_call_lead` algorithm against your `leads.xlsx` data. It also outputs a `technology.txt` summary.
-   `run_pipeline.py`: The main orchestration script that runs `analyze_websites.py`, `inspect_file.py`, and `add_call_lead_column.py` in sequence.

## Attribution

This project utilizes the `python-Wappalyzer` library, which is a fork of the original `Wappalyzer` web application detection utility.

-   **`python-Wappalyzer` (fork):** [chokepoint/python-Wappalyzer](https://github.com/chokepoint/python-Wappalyzer)
-   **Original `Wappalyzer`:** [AliasIO/wappalyzer](https://github.com/AliasIO/wappalyzer)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE](LICENSE)) file for details.
