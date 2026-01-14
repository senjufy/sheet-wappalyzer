# Sheet-Wappalyzer

A Python script to analyze a list of websites from an Excel file, identify their underlying technologies, and update the same file with the results. This tool is ideal for market research, lead generation, and competitive analysis.

This script uses `pandas` for data manipulation and `aiohttp` with `asyncio` to perform fast, concurrent analysis of hundreds or thousands of URLs without getting blocked. Technology detection is powered by a fork of the `python-Wappalyzer` library.

**Disclaimer:** This project was initially built to solve a specific personal problem. While it aims to be robust and functional, it is provided as-is. Feel free to adapt and use it for your own needs.

## Features

- **Reads from Excel:** Processes `.xlsx` files directly.
- **Enriches Data In-Place:** Adds "Technologies" and "Status" columns to your original file, overwriting old data if a previous analysis was run.
- **Fast & Concurrent:** Uses `asyncio` to analyze dozens of sites simultaneously, making it much faster than sequential processing.
- **Configurable:** Command-line arguments let you specify the file path, URL column name, and concurrency limit.
- **Robust:** Includes error handling for common issues like connection timeouts, HTTP errors, and missing URLs.

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

1.  **Prepare your Excel file:**
    -   Ensure your Excel file (e.g., `leads.xlsx`) is in the project directory.
    -   It must contain a column with website URLs. The script will look for a column named `Website` by default.

2.  **Run the script from your terminal:**

    **Basic usage (using defaults):**
    ```bash
    python3 analyze_websites.py
    ```

    **Advanced usage (with custom arguments):**
    ```bash
    python3 analyze_websites.py --file "path/to/your/leads.xlsx" --url_column "Company Website" --concurrency 50
    ```

### Command-Line Arguments

-   `--file`: Path to the input Excel file. **Default:** `leads.xlsx`.
-   `--url_column`: Name of the column containing website URLs. **Default:** `Website`.
-   `--concurrency`: Number of concurrent requests to make. **Default:** `25`.

## Attribution

This project utilizes the `python-Wappalyzer` library, which is a fork of the original `Wappalyzer` web application detection utility.

-   **`python-Wappalyzer` (fork):** [chokepoint/python-Wappalyzer](https://github.com/chokepoint/python-Wappalyzer)
-   **Original `Wappalyzer`:** [AliasIO/wappalyzer](https://github.com/AliasIO/wappalyzer)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
